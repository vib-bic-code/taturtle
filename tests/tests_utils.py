import unittest
import shutil
import os
from pathlib import Path
import numpy as np
from src.utils import get_file_list, create_filename_output, create_filename_output_thickness

class TestUtilsFunctions(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_folder"
        os.makedirs(self.test_dir, exist_ok=True)
        self.tiff_files = [
            "image1.tif",
            "image2.tiff",
            "image3.TIFF",  # Should not be matched (case-sensitive)
            "not_image.txt"
        ]
        for fname in self.tiff_files:
            with open(os.path.join(self.test_dir, fname), "w") as f:
                f.write("test")
        self.input_path = os.path.join(self.test_dir, "image1.tif")
        self.output_folder = "output_folder"

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if os.path.exists(os.path.join(self.test_dir, self.output_folder)):
            shutil.rmtree(os.path.join(self.test_dir, self.output_folder))

    def test_get_file_list_returns_tiff_files(self):
        result = get_file_list(self.test_dir)
        expected = np.array([
            os.path.join(self.test_dir, "image1.tif"),
            os.path.join(self.test_dir, "image2.tiff")
        ])
        self.assertCountEqual(result, expected)

    def test_get_file_list_nonexistent_folder(self):
        result = get_file_list("nonexistent_folder")
        self.assertIsNone(result)

    def test_create_filename_output(self):
        f = "image1.tif"
        output_path = create_filename_output(self.input_path, f, self.output_folder)
        expected_path = Path(self.test_dir) / self.output_folder / "image1.tif"
        self.assertEqual(Path(output_path), expected_path)
        self.assertTrue((Path(self.test_dir) / self.output_folder).exists())

    def test_create_filename_output_thickness(self):
        f = "image2.tiff"
        index = 5
        output_path = create_filename_output_thickness(self.input_path, f, self.output_folder, index)
        expected_path = Path(self.test_dir) / self.output_folder / "image2_5.tif"
        self.assertEqual(Path(output_path), expected_path)
        self.assertTrue((Path(self.test_dir) / self.output_folder).exists())

if __name__ == "__main__":
    unittest.main()






