import numpy as np
import re
from pathlib import Path
from typing import List
#import sys
#sys.path.append(r"C:\GBW_MyDownloads\taturtle")
from src.utils import *


class SliceThicknessCorrection:

    class IsotonicRegression:

        @staticmethod
        def fit(a: np.ndarray) -> np.ndarray:
            n = len(a)
            w = np.ones(n, dtype=np.float64)
            return SliceThicknessCorrection.IsotonicRegression.fit_with_weights(a, w)

        @staticmethod
        def fit_with_weights(a: np.ndarray, w: np.ndarray) -> np.ndarray:
            n = len(a)
            assert len(w) == n

            aprime = np.zeros(n, dtype=np.float64)
            wprime = np.zeros(n, dtype=np.float64)
            S = np.zeros(n + 1, dtype=int)

            aprime[0],wprime[0]  = a[0], w[0]
            S[0], S[1] = 0, 1
            j = 0

            for i in range(1, n):
                j += 1
                aprime[j] = a[i]
                wprime[j] = w[i]

                while j > 0 and aprime[j] < aprime[j - 1]:
                    aprime[j - 1] = (wprime[j] * aprime[j] + wprime[j - 1] * aprime[j - 1]) / (wprime[j] + wprime[j - 1])
                    wprime[j - 1] += wprime[j]
                    j -= 1

                S[j + 1] = i + 1

            y = np.zeros(n, dtype=np.float64)
            for k in range(j + 1):
                for L in range(S[k], S[k + 1]):
                    y[L] = aprime[k]

            return y
    class Pair:
        def __init__(self, path: Path, z: np.float64):
            self.path = path
            self.z = z

    class ResampleInfo:
        def __init__(self, desired_z: np.float64, original_z: np.float64, original_filename: Path):
            self.desired_z = desired_z
            self.original_z = original_z
            self.original_filename = original_filename

    @staticmethod
    def nearest_neighbor_resample(input_files: List[Path], slice_thickness_nm: float, preserve_slice_order: bool) -> List['SliceThicknessCorrection.ResampleInfo']:
        slices = SliceThicknessCorrection.parse_filenames(input_files)
        monotonic = SliceThicknessCorrection.slice_positions_monotonically_increasing(slices)
        if not monotonic:
            if preserve_slice_order:
                print("Z-position of slices is *not* monotonically increasing! Performing isotonic regression.")
                zs = np.array([s.z for s in slices], dtype=np.float64)
                isotonic = SliceThicknessCorrection.IsotonicRegression.fit(zs)
                SliceThicknessCorrection.make_strictly_monotonic(isotonic)
                for i, z in enumerate(isotonic):
                    slices[i].z = z
            else:
                print("Z-position of slices is *not* monotonically increasing! Re-ordering them.")
                slices = SliceThicknessCorrection.sort_by_monotonically_increasing_z(slices)

        return SliceThicknessCorrection.do_nearest_neighbor_resampling(slices, slice_thickness_nm)

    @staticmethod
    def get_resampled_files(resample_info: List['SliceThicknessCorrection.ResampleInfo']) -> List[Path]:
        return [info.original_filename for info in resample_info]

    @staticmethod
    def print_resample_info(resample_info: List['SliceThicknessCorrection.ResampleInfo']):
        for info in resample_info:
            print(f"{info.desired_z} -> {info.original_z} -> {info.original_filename}")

    @staticmethod
    def do_nearest_neighbor_resampling(slices: List['SliceThicknessCorrection.Pair'], slice_thickness_nm: float) -> List['SliceThicknessCorrection.ResampleInfo']:
        dz = slice_thickness_nm / 1000.0
        zfirst = slices[0].z
        zlast = slices[-1].z
        num_resampled_slices = int((zlast - zfirst) / dz + dz / 2.0)
        num_original_slices = len(slices)

        index_nearest_z = 0
        resample_info = []

        for i in range(num_resampled_slices):
            desired_z = zfirst + i * dz
            while (index_nearest_z < num_original_slices - 1 and
                   abs(slices[index_nearest_z].z - desired_z) >= abs(slices[index_nearest_z + 1].z - desired_z)):
                index_nearest_z += 1

            nearest_original_z = slices[index_nearest_z].z
            nearest_original_path = slices[index_nearest_z].path
            resample_info.append(SliceThicknessCorrection.ResampleInfo(desired_z, nearest_original_z, nearest_original_path))

        return resample_info
    @staticmethod
    def parse_filenames(input_files: List[Path]) -> List['SliceThicknessCorrection.Pair']:
        regex = re.compile(r".*_(\d+)_z=(-?\d*\.?\d*)um?\.tif")
        slices = []

        for path in input_files:
            match = regex.match(str(path))
            if not match:
                raise RuntimeError(f"The file {path} does not match our expected filename format string.")
            slice_z = match.group(2)
            z = np.float64(slice_z)
            slices.append(SliceThicknessCorrection.Pair(path, z))

        return slices

    @staticmethod
    def slice_positions_monotonically_increasing(slices: List['SliceThicknessCorrection.Pair']) -> bool:
        zprev = -1e9
        for p in slices:
            if zprev >= p.z:
                return False
            zprev = p.z
        return True

    @staticmethod
    def sort_by_monotonically_increasing_z(slices: List['SliceThicknessCorrection.Pair']) -> List['SliceThicknessCorrection.Pair']:
        return sorted(slices, key=lambda p: p.z)

    @staticmethod
    def make_strictly_monotonic(zs: np.ndarray):
        if len(zs) == 0:
            return

        interval_z = zs[0]
        interval_begin = 0
        interval_end = 0

        for i in range(1, len(zs)):
            if zs[i] == interval_z:
                interval_end = i
                if interval_end == len(zs) - 1:
                    SliceThicknessCorrection.make_strictly_monotonic_interval(zs, interval_begin, interval_end)
            else:
                if interval_end != interval_begin:
                    SliceThicknessCorrection.make_strictly_monotonic_interval(zs, interval_begin, interval_end)
                interval_begin = i
                interval_end = i
                interval_z = zs[i]
    @staticmethod
    def make_strictly_monotonic_interval(zs: np.ndarray, i1: int, i2: int):
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

def run_thickness_correction(input_path:str,slice_thickness:int)->tuple:
    ''' runs thickness correction and returns change in numbers of slices'''
    input_files = sorted(get_file_list(input_path))
    slices = SliceThicknessCorrection.get_resampled_files(SliceThicknessCorrection.nearest_neighbor_resample(input_files, slice_thickness, preserve_slice_order = True))
    for idx, slice_path in enumerate(slices):
        iio.imsave(create_filename_output_thickness(input_path, slice_path, "thickness_corr", idx), read_image(slice_path))
    return len(input_files),len(slices)
