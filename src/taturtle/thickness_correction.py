"""Do whatever thickness correction does."""

from __future__ import annotations

from dataclasses import dataclass
import logging
import re
from pathlib import Path

import numpy as np
import skimage.io as iio
import tifffile

from taturtle import isotonic_regression
from taturtle.utils import get_file_list, create_filename_output_thickness


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _PathPair:
    path: Path
    z: np.float64


@dataclass(frozen=True)
class _ResampleInfo:
    desired_z: np.float64
    original_z: np.float64
    original_filename: Path


def _nearest_neighbor_resample(
    input_files: list[Path], slice_thickness_nm: float
) -> list[_ResampleInfo]:
    slices = _parse_filenames(input_files)
    if not _slice_positions_monotonically_increasing(slices):
        logger.debug(
            "Z-position of slices is *not* monotonically increasing! Performing isotonic regression."
        )
        zs = np.array([s.z for s in slices], dtype=np.float64)
        isotonic = isotonic_regression.fit(zs)
        _make_strictly_monotonic(isotonic)
        slices = [_PathPair(slices[i].path, z) for i, z in enumerate(isotonic)]

    return _do_nearest_neighbor_resampling(slices, slice_thickness_nm)


def _get_resampled_files(
    resample_info: list[_ResampleInfo],
) -> list[Path]:
    return [info.original_filename for info in resample_info]


def _do_nearest_neighbor_resampling(
    slices: list[_PathPair], slice_thickness_nm: float
) -> list[_ResampleInfo]:
    dz = slice_thickness_nm / 1000.0
    zfirst = slices[0].z
    zlast = slices[-1].z
    num_resampled_slices = int((zlast - zfirst) / dz + dz / 2.0)
    num_original_slices = len(slices)

    index_nearest_z = 0
    resample_info = []

    for i in range(num_resampled_slices):
        desired_z = zfirst + i * dz
        while index_nearest_z < num_original_slices - 1 and abs(
            slices[index_nearest_z].z - desired_z
        ) >= abs(slices[index_nearest_z + 1].z - desired_z):
            index_nearest_z += 1

        nearest_original_z = slices[index_nearest_z].z
        nearest_original_path = slices[index_nearest_z].path
        resample_info.append(
            _ResampleInfo(desired_z, nearest_original_z, nearest_original_path)
        )

    return resample_info


def _parse_filenames(
    input_files: list[Path],
) -> list[_PathPair]:
    regex = re.compile(r".*_(\d+)_z=(-?\d*\.?\d*)um?\.tif")
    slices = []

    for path in input_files:
        match = regex.match(str(path))
        if not match:
            raise RuntimeError(
                f"The file {path} does not match our expected filename format string."
            )
        slice_z = match.group(2)
        z = np.float64(slice_z)
        slices.append(_PathPair(path, z))

    return slices


def _slice_positions_monotonically_increasing(
    slices: list[_PathPair],
) -> bool:
    zprev = -1e9
    for p in slices:
        if zprev >= p.z:
            return False
        zprev = p.z
    return True


def _make_strictly_monotonic(zs: np.ndarray) -> None:
    if len(zs) == 0:
        return

    interval_z = zs[0]
    interval_begin = 0
    interval_end = 0

    for i in range(1, len(zs)):
        if zs[i] == interval_z:
            interval_end = i
            if interval_end == len(zs) - 1:
                _make_strictly_monotonic_interval(zs, interval_begin, interval_end)
        else:
            if interval_end != interval_begin:
                _make_strictly_monotonic_interval(zs, interval_begin, interval_end)
            interval_begin = i
            interval_end = i
            interval_z = zs[i]


def _make_strictly_monotonic_interval(zs: np.ndarray, i1: int, i2: int) -> None:
    assert i2 < len(zs)
    assert i1 < i2

    ideal_eps = 0.1 / 1000.0
    n = i2 - i1

    max_dz_left = zs[i1] - zs[i1 - 1] if i1 > 0 else np.inf
    max_dz_right = zs[i2 + 1] - zs[i2] if i2 < len(zs) - 1 else np.inf

    max_dz = min(max_dz_left, max_dz_right)
    max_eps = 2.0 * max_dz / n

    eps = 0.95 * min(ideal_eps, max_eps)

    i_mid = (i1 + i2) / 2.0

    for i in range(i1, i2 + 1):
        dz = (i - i_mid) * eps
        zs[i] += dz


def run_thickness_correction(
    input_path: Path, slice_thickness: float, outdir: Path
) -> tuple:
    """runs thickness correction and returns change in numbers of slices"""
    input_files = sorted(get_file_list(input_path))
    slices = _get_resampled_files(
        _nearest_neighbor_resample(input_files, slice_thickness)
    )
    for idx, slice_path in enumerate(slices):
        iio.imsave(
            create_filename_output_thickness(slice_path, outdir, idx),
            tifffile.imread(slice_path),
        )
    return len(input_files), len(slices)
