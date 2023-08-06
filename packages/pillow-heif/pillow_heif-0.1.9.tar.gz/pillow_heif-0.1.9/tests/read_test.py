import os
import builtins

from gc import collect
from io import BytesIO
from pathlib import Path
from json import load

import pytest

from PIL import Image, ImageCms
from pillow_heif import (
    check_heif,
    is_supported,
    open_heif,
    read_heif,
    libheif_version,
    HeifFile,
    UndecodedHeifFile,
    HeifFiletype,
    HeifError,
    HeifErrorCode,
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with builtins.open("images_info.json", "rb") as _:
    all_images = load(_)
invalid_images = [e for e in all_images if not e["valid"]]
heif_images = [e for e in all_images if e["valid"]]

heic_images = [e for e in heif_images if e["name"].endswith(".heic")]
hif_images = [e for e in heif_images if e["name"].endswith(".hif")]
avif_images = [e for e in heif_images if e["name"].endswith(".avif")]


@pytest.mark.parametrize("img_info", heif_images)
def test_open_and_load(img_info):
    heif_file = open_heif(img_info["file"])
    assert heif_file.size[0] > 0
    assert heif_file.size[1] > 0
    assert heif_file.has_alpha is not None
    assert heif_file.mode is not None
    assert heif_file.bit_depth is not None

    assert heif_file.data is None
    assert heif_file.stride is None

    if img_info["color_profile"]:
        assert len(heif_file.info["color_profile"])
    else:
        assert not len(heif_file.info["color_profile"])

    assert len(heif_file.info["metadata"]) == len(img_info["metadata"])

    assert heif_file.data is None
    if img_info.get("icc_profile", None) is None:
        assert "icc_profile" not in heif_file.info
    else:
        assert len(heif_file.info["icc_profile"]) == img_info["icc_profile"]
        if len(heif_file.info["icc_profile"]):
            ImageCms.getOpenProfile(BytesIO(heif_file.info["icc_profile"]))
    if img_info.get("nclx_profile", None):
        assert len(heif_file.info["nclx_profile"]) == img_info["nclx_profile"]
    else:
        assert "nclx_profile" not in heif_file.info

    assert heif_file.load() is heif_file
    assert heif_file.data is not None
    assert heif_file.stride is not None
    assert len(heif_file.data) >= heif_file.stride * heif_file.size[1]
    assert type(heif_file.data[:100]) == bytes
    assert isinstance(heif_file, HeifFile)
    pillow_img = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    heif_file.close()
    pillow_img.close()


@pytest.mark.parametrize("img_info", heic_images[:1] + hif_images[:1] + avif_images[:1])
def test_read_bytes(img_info):
    with open(Path(img_info["file"]), "rb") as f:
        d = f.read()
        for heif_file in (read_heif(d), read_heif(bytearray(d)), read_heif(BytesIO(d))):
            width, height = heif_file.size
            assert width > 0
            assert height > 0
            assert heif_file.info
            assert len(heif_file.data) > 0


@pytest.mark.parametrize("img_info", hif_images)
def test_10bit(img_info):
    heif_file = open_heif(Path(img_info["file"]), convert_hdr_to_8bit=False)
    assert not heif_file.convert_hdr_to_8bit
    heif_file.load()


@pytest.mark.parametrize("img_info", heic_images[:1] + hif_images[:1] + avif_images[:1])
def test_heif_open_load_close(img_info):
    heif_file = open_heif(Path(img_info["file"]))
    assert isinstance(heif_file, UndecodedHeifFile)
    assert heif_file.data is None
    heif_file.load()
    assert isinstance(heif_file, HeifFile)
    assert heif_file.data is not None
    heif_file.close()  # free decoded data.
    assert heif_file.data is None


@pytest.mark.parametrize("img_info", heic_images[:2] + hif_images[:2] + avif_images[:2])
def test_load_after_fp_close(img_info):
    f = builtins.open(Path(img_info["file"]), "rb")
    heif_file = open_heif(f)
    f.close()
    heif_file.load()


@pytest.mark.parametrize("img_info", heic_images[:2] + hif_images[:2] + avif_images[:2])
def test_load_after_data_free(img_info):
    data = Path(img_info["file"]).read_bytes()
    heif_file = open_heif(data)
    data = None
    collect()
    heif_file.load()


@pytest.mark.parametrize("img_info", heic_images[:1] + hif_images[:1] + avif_images[:1])
def test_with_file_handle(img_info):
    with builtins.open(Path(img_info["file"]), "rb") as fh:
        assert is_supported(fh)
        assert check_heif(fh) != HeifFiletype.NO
        heif_file_1 = open_heif(fh)
        heif_file_2 = open_heif(fh)
        heif_file_1.load()
        heif_file_2.load()
        assert repr(heif_file_1) == repr(heif_file_2)
        heif_file_1.close()
        assert repr(heif_file_1) != repr(heif_file_2)
        heif_file_2.close()
        assert repr(heif_file_1) == repr(heif_file_2)
        assert fh.tell() == 0


@pytest.mark.parametrize("img_info", heic_images[:1] + hif_images[:1] + avif_images[:1])
def test_multiply_load(img_info):
    heif_file = open_heif(Path(img_info["file"]))
    for i in range(4):
        res = heif_file.load()
        assert heif_file is res
        assert heif_file.data is not None
        assert heif_file.stride is not None
    heif_file.close()


@pytest.mark.parametrize("img_info", invalid_images)
def test_invalid_file(img_info):
    with pytest.raises(HeifError):
        read_heif(Path(img_info["file"]).as_posix())
    with pytest.raises(HeifError):
        read_heif(Path(img_info["file"]))
    with pytest.raises(HeifError):
        with builtins.open(Path(img_info["file"]), "rb") as f:
            read_heif(BytesIO(f.read()))
    with pytest.raises(HeifError):
        with builtins.open(Path(img_info["file"]), "rb") as f:
            read_heif(f)


@pytest.mark.parametrize("img_info", invalid_images)
def test_heif_error(img_info):
    try:
        read_heif(Path(img_info["file"]))
        assert False
    except HeifError as exception:
        assert exception.code == HeifErrorCode.INVALID_INPUT
        assert repr(exception).find("HeifErrorCode.INVALID_INPUT") != -1
        assert str(exception).find("Invalid input") != -1


def test_lib_version():
    assert libheif_version() == "1.12.0"
