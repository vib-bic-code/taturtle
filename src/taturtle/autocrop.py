"""Image cropping."""

from pathlib import Path

import numpy as np
import tifffile

from taturtle.region import Region
from taturtle.utils import get_file_list

_Image = np.ndarray[tuple[int, ...], np.dtype[np.unsignedinteger]]


def _get_nonblack_region(
    image: _Image,
) -> Region:
    """Return the bounding box of the non-black region in the image."""
    image_height, image_width, *_ = image.shape
    top_black_margin = _get_num_black_rows(image, 0, image_height - 1, +1)
    bottom_black_margin = _get_num_black_rows(image, image_height - 1, 0, -1)

    left_black_margin = _get_num_black_columns(image, 0, image_width - 1, +1)
    right_black_margin = _get_num_black_columns(image, image_width - 1, 0, -1)

    x, y = left_black_margin, top_black_margin
    width = image_width - left_black_margin - right_black_margin
    height = image_height - top_black_margin - bottom_black_margin

    if width > 0 and height > 0:
        return Region(x1=x, y1=y, x2=x + width, y2=y + height)
    return Region(0, 0, 0, 0)


def _get_num_black_rows(
    image: _Image,
    start_row: int,
    end_row: int,
    row_increment: int,
) -> int:
    """Count the number of consecutive fully black rows starting from start_row."""
    num_black_rows = 0
    for row in range(start_row, end_row, row_increment):
        if np.all(image[row, :] == 0):
            num_black_rows += 1
        else:
            return num_black_rows
    return num_black_rows


def _get_num_black_columns(
    image: _Image,
    start_col: int,
    end_col: int,
    col_increment: int,
) -> int:
    """Count the number of consecutive fully black columns starting from start_col."""
    num_black_columns = 0
    for col in range(start_col, end_col, col_increment):
        if np.all(image[:, col] == 0):
            num_black_columns += 1
        else:
            return num_black_columns
    return num_black_columns


def _get_crop_im_ref(image: _Image) -> tuple[_Image, Region]:
    """Return the cropped image excluding all fully black rows and columns."""
    nonblack_region = _get_nonblack_region(image)
    cropped_image = image[
        nonblack_region.y1 : nonblack_region.y2,
        nonblack_region.x1 : nonblack_region.x2,
    ]
    return cropped_image, nonblack_region


def _get_crop(image: _Image, nonblack_region: Region) -> _Image:
    """Return the cropped image excluding all fully black rows and columns."""
    return image[
        nonblack_region.y1 : nonblack_region.y2,
        nonblack_region.x1 : nonblack_region.x2,
    ]


def _shift_xy(image: _Image) -> tuple[int, int]:
    """Return the shift in x and y (top and left black margins)."""
    image_height, image_width = image.shape
    top_black_margin = _get_num_black_rows(image, 0, image_height - 1, +1)
    left_black_margin = _get_num_black_columns(image, 0, image_width - 1, +1)
    return top_black_margin, left_black_margin

def reference_shift(image: np.ndarray[tuple[int, ...], np.dtype[np.float64]]) -> tuple[int, int]:
    """Find where the black r"""
    cropped_image, nonblack_region = _get_crop_im_ref(image)
    return _shift_xy(image)

def run_autocrop(input_path: Path, im_ref: Path, outdir: Path) -> tuple[int, int]:
    """Run the autocropper on all images in the input folder."""
    image = tifffile.imread(im_ref)
    cropped_image, nonblack_region = _get_crop_im_ref(image)
    x_shift, y_shift = _shift_xy(image)
    tifffile.imwrite(input_path.parent / outdir / f"{im_ref.stem}.tif", cropped_image)
    file_list = [path for path in get_file_list(input_path) if path != im_ref]
    for f in file_list:
        image = tifffile.imread(f)
        cropped_image = _get_crop(image, nonblack_region)
        tifffile.imwrite(input_path.parent / outdir / f"{f.stem}.tif", cropped_image)

    return x_shift, y_shift
