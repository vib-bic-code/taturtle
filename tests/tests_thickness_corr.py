import unittest
import numpy as np
from pathlib import Path
import sys
sys.path.append("../src")
from src.thickness_correction import SliceThicknessCorrection
from tests.tests_thickness_corr import *

class DummyPair:
    def __init__(self, path, z):
        self.path = path
        self.z = z


class TestThicknessCorr(unittest.TestCase):
    def test_parse_filenames_valid(self):
        files = [
            Path("img_001_z=10um.tif"),
            Path("img_002_z=-5.5um.tif"),
            Path("img_003_z=0um.tif"),
        ]
        pairs =SliceThicknessCorrection.parse_filenames(files)
        self.assertEqual(len(pairs), 3)
        self.assertEqual(pairs[0].z, np.float64(10))
        self.assertEqual(pairs[1].z, np.float64(-5.5))
        self.assertEqual(pairs[2].z, np.float64(0))
        self.assertEqual(pairs[0].path, files[0])
        self.assertEqual(pairs[1].path, files[1])
        self.assertEqual(pairs[2].path, files[2])

    def test_parse_filenames_invalid_format(self):
        files = [
            Path("img_001_z=10um.tif"),
            Path("badfile.tif"),
        ]
        with self.assertRaises(RuntimeError):
                SliceThicknessCorrection.parse_filenames(files)

    def test_parse_filenames_float_and_int(self):
        files = [
             Path("img_001_z=1.23um.tif"),
             Path("img_002_z=4um.tif"),
         ]
        pairs = SliceThicknessCorrection.parse_filenames(files)
        self.assertEqual(pairs[0].z, np.float64(1.23))
        self.assertEqual(pairs[1].z, np.float64(4))

    def test_sort_by_monotonically_increasing_z(self):
        pairs = [
             DummyPair("a", 5.0),
             DummyPair("b", -2.0),
             DummyPair("c", 0.0),
         ]
        sorted_pairs = SliceThicknessCorrection.sort_by_monotonically_increasing_z(pairs)
        zs = [p.z for p in sorted_pairs]
        self.assertEqual(zs, [-2.0, 0.0, 5.0])

    def test_sort_by_monotonically_increasing_z_with_duplicates(self):
        pairs = [
             DummyPair("a", 1.0),
             DummyPair("b", 1.0),
             DummyPair("c", 2.0),
         ]
        sorted_pairs = SliceThicknessCorrection.sort_by_monotonically_increasing_z(pairs)
        zs = [p.z for p in sorted_pairs]
        self.assertEqual(zs, [1.0, 1.0, 2.0])

    def test_resample_info_attributes(self):
        ri = SliceThicknessCorrection.ResampleInfo(np.float64(1.5), np.float64(2.5), Path("file.tif"))
        self.assertEqual(ri.desired_z, np.float64(1.5))
        self.assertEqual(ri.original_z, np.float64(2.5))
        self.assertEqual(ri.original_filename, Path("file.tif"))

if __name__ == "__main__":
    unittest.main()
