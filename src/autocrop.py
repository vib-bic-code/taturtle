import numpy as np
from src.utils import *
from pathlib import Path
import skimage.io as iio

class AutoCropper:
    def get_nonblack_region(image):
        """Return the bounding box of the non-black region in the image."""
        if image is None:
            return None

        image_height, image_width = image.shape
        top_black_margin = AutoCropper.get_num_black_rows(image, 0, image_height-1, +1)
        bottom_black_margin = AutoCropper.get_num_black_rows(image, image_height-1, 0, -1)

        left_black_margin = AutoCropper.get_num_black_columns(image, 0, image_width-1, +1)
        right_black_margin = AutoCropper.get_num_black_columns(image, image_width-1, 0, -1)

        x, y = left_black_margin, top_black_margin
        width = image_width - left_black_margin - right_black_margin
        height = image_height - top_black_margin - bottom_black_margin

        if width > 0 and height > 0:
            return (x, y, width, height)
        else:
            return (0, 0, 0, 0)  

    def get_num_black_rows(image, start_row, end_row, row_increment):
        """Count the number of consecutive fully black rows starting from start_row."""
        num_black_rows = 0
        for row in range(start_row, end_row, row_increment):
            if np.all(image[row, :] == 0):
                num_black_rows += 1
            else:
                return num_black_rows
        return num_black_rows

    def get_num_black_columns(image, start_col, end_col, col_increment):
        """Count the number of consecutive fully black columns starting from start_col."""
        num_black_columns = 0
        for col in range(start_col, end_col, col_increment):
            if np.all(image[:, col] == 0):
                num_black_columns += 1
            else:
                return num_black_columns
        return num_black_columns

    def get_crop_im_ref(image: np.array)-> tuple:
        """Return the cropped image excluding all fully black rows and columns."""
        nonblack_region = AutoCropper.get_nonblack_region(image)
        cropped_image = image[nonblack_region[1]:nonblack_region[1] + nonblack_region[3],nonblack_region[0]:nonblack_region[0] + nonblack_region[2]]
        return cropped_image,nonblack_region
    
    def get_crop(image: np.array, nonblack_region:tuple)-> np.array:
        """Return the cropped image excluding all fully black rows and columns."""
        cropped_image = image[nonblack_region[1]:nonblack_region[1] + nonblack_region[3],nonblack_region[0]:nonblack_region[0] + nonblack_region[2]]
        return cropped_image

    def shift_xy(image: np.array) -> tuple:
        """Return the shift in x and y (top and left black margins)."""
        image_height, image_width = image.shape
        top_black_margin = AutoCropper.get_num_black_rows(image, 0, image_height-1, +1)
        left_black_margin = AutoCropper.get_num_black_columns(image, 0, image_width-1, +1)
        return top_black_margin,left_black_margin
    
    def run_autocrop(input_path:str, im_ref:str, outdir:str)->tuple:
        """Run the autocropper on all images in the input folder."""
        file_list=get_file_list(input_path)
        for f in file_list:
            image = tifffile.imread(f)
            if f == im_ref:
                cropped_image, nonblack_region = AutoCropper.get_crop_im_ref(image)
                x_shift, y_shift = AutoCropper.shift_xy(image)
                tifffile.imwrite(os.path.join(Path(input_path).parent, outdir, f"{Path(f).stem}.tif"), cropped_image)
            else:
                cropped_image = AutoCropper.get_crop(image,nonblack_region)
                tifffile.imwrite(os.path.join(Path(input_path).parent, outdir, f"{Path(f).stem}.tif"), cropped_image)
        return x_shift, y_shift