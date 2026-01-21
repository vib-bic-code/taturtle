import numpy as np
from pathlib import Path

import pytest

from taturtle import thickness_correction


def test_parse_filenames_valid():
    files = [
        Path("img_001_z=10um.tif"),
        Path("img_002_z=-5.5um.tif"),
        Path("img_003_z=0um.tif"),
    ]
    pairs = thickness_correction._parse_filenames(files)
    assert len(pairs) == 3
    assert pairs[0].z == np.float64(10)
    assert pairs[1].z == np.float64(-5.5)
    assert pairs[2].z == np.float64(0)
    assert pairs[0].path == files[0]
    assert pairs[1].path == files[1]
    assert pairs[2].path == files[2]


def test_parse_filenames_invalid_format():
    files = [
        Path("img_001_z=10um.tif"),
        Path("badfile.tif"),
    ]
    with pytest.raises(RuntimeError):
        thickness_correction._parse_filenames(files)


def test_parse_filenames_float_and_int():
    files = [
        Path("img_001_z=1.23um.tif"),
        Path("img_002_z=4um.tif"),
    ]
    pairs = thickness_correction._parse_filenames(files)
    assert pairs[0].z == np.float64(1.23)
    assert pairs[1].z == np.float64(4)


def test_resample_info_attributes():
    ri = thickness_correction._ResampleInfo(
        np.float64(1.5), np.float64(2.5), Path("file.tif")
    )
    assert ri.desired_z == np.float64(1.5)
    assert ri.original_z == np.float64(2.5)
    assert ri.original_filename == Path("file.tif")
