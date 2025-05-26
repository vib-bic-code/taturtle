import unittest
import numpy as np
from src.autocrop import DummyAutoCropper  # Update this import path to the actual location of DummyAutoCropper

class TestDummyAutoCropper(unittest.TestCase):
    def test_get_num_black_rows_all_black(self):
        img = np.zeros((5, 3), dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_rows(img, 0, 4, 1), 5)
        self.assertEqual(DummyAutoCropper.get_num_black_rows(img, 4, 0, -1), 5)

    def test_get_num_black_rows_partial_black(self):
        img = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ], dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_rows(img, 0, 4, 1), 2)
        self.assertEqual(DummyAutoCropper.get_num_black_rows(img, 4, 0, -1), 2)

    def test_get_num_black_rows_none_black(self):
        img = np.ones((3, 3), dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_rows(img, 0, 2, 1), 0)

    def test_get_num_black_columns_all_black(self):
        img = np.zeros((3, 4), dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_columns(img, 0, 3, 1), 4)
        self.assertEqual(DummyAutoCropper.get_num_black_columns(img, 3, 0, -1), 4)

    def test_get_num_black_columns_partial_black(self):
        img = np.array([
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ], dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_columns(img, 0, 3, 1), 2)
        self.assertEqual(DummyAutoCropper.get_num_black_columns(img, 3, 0, -1), 1)

    def test_get_num_black_columns_none_black(self):
        img = np.ones((2, 2), dtype=np.uint8)
        self.assertEqual(DummyAutoCropper.get_num_black_columns(img, 0, 1, 1), 0)

if __name__ == "__main__":
    unittest.main()
