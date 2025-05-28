from dataclasses import dataclass
import multiprocessing as mp
from pathlib import Path

import numpy as np
import skimage.io as iio
import scipy.ndimage as ndi
import tifffile

from taturtle.utils import get_file_list


@dataclass(frozen=True)
class TemplateMatching:
    init_x: int
    init_y: int
    prev_x: int
    prev_y: int
    patch_ref: np.ndarray[tuple[int, ...], np.dtype[np.float64]]
    patch_prev: np.ndarray[tuple[int, ...], np.dtype[np.float64]]
    patch_list: np.ndarray[tuple[int, int, int], np.dtype[np.float64]]
    tiff_files: list[Path]


def init_templatematching(
    input_path: Path,
    image_ref: Path,
    x_a: list[int],
    y_a: list[int],
) -> TemplateMatching:
    """initializing parameters for template matching"""
    tiff_files_list = get_file_list(input_path)
    im = np.array(tifffile.imread(image_ref))
    patch_ref = im[x_a[0] : x_a[1], y_a[0] : y_a[1]].astype(np.float64)
    init_x, init_y = x_a[0], y_a[0]
    prev_x, prev_y = init_x, init_y
    patch_prev = patch_ref
    patch_list = np.zeros(
        (patch_ref.shape[0], patch_ref.shape[1], len(tiff_files_list))
    )
    return TemplateMatching(
        init_x,
        init_y,
        prev_x,
        prev_y,
        patch_ref,
        patch_prev,
        patch_list,
        tiff_files_list,
    )


def _calculate_mad(
    patch: np.ndarray, patch_ref: np.ndarray, patch_prev: np.ndarray, alpha: int
) -> int:
    """calculates the mean absolute difference between two patches"""
    diff1 = patch - patch_ref
    diff2 = patch - patch_prev
    return alpha * np.sum(np.abs(diff1)) + (1 - alpha) * np.sum(np.abs(diff2))


def _process_image(
    i: int,
    input_path: Path,
    files: list[Path],
    patch_r: np.ndarray,
    patch_p: np.ndarray,
    alpha: int,
    search_window: int,
    prev_x: int,
    prev_y: int,
) -> tuple[int, int, np.ndarray]:
    """returns the new position in x/y and the new patch"""
    im = tifffile.imread(input_path / files[i])
    mad_max = 255 * (patch_r.size)
    min_x, min_y = max(prev_x - search_window, 0), max(prev_y - search_window, 0)
    pos_x, pos_y = min_x, min_y
    for x in range(min_x, min_x + 2 * search_window + 2):
        for y in range(min_y, min_y + 2 * search_window + 2):
            patch = im[x : (x + patch_r.shape[0]), y : (y + patch_r.shape[1])].astype(
                np.float64
            )
            mad = _calculate_mad(patch, patch_r, patch_p, alpha)
            if mad < mad_max:
                mad_max = mad
                pos_x, pos_y = x, y
                patch_temp = patch
    return pos_x, pos_y, patch_temp


def save_shift_image(
    input_path: Path,
    outdir: Path,
    tiff_file: Path,
    x_0: int,
    y_0: int,
    posx: int,
    posy: int,
) -> tuple[int, int]:
    """shift, save the aligned images and returns the shift in x/y"""
    shift = (x_0 - posx, y_0 - posy)
    im = ndi.shift(tifffile.imread(input_path / tiff_file), shift)
    iio.imsave(input_path.parent / outdir / f"{tiff_file.stem}.tif", im)

    return shift


def run_template_matching(
    input_path: str,
    template: TemplateMatching,
    alpha: int,
    search_window: int,
    cpu: int,
) -> list[tuple[int, int, np.ndarray]]:
    """runs the template matching"""
    with mp.Pool(processes=cpu) as pool:
        results = pool.starmap(
            _process_image,
            [
                (
                    i,
                    input_path,
                    template.tiff_files,
                    template.patch_ref,
                    template.patch_prev,
                    alpha,
                    search_window,
                    template.prev_x,
                    template.prev_y,
                )
                for i in range(len(template.tiff_files))
            ],
        )
    return results


def unpack_result_template_step1(
    results: tuple, patch_ref: np.ndarray, number_of_files: int
) -> tuple:
    """unpack results of the first step of the template matching"""
    patch_list = np.zeros((patch_ref.shape[0], patch_ref.shape[1], number_of_files))
    for i, (pos_x, pos_y, patch_temp) in enumerate(results):
        patch_prev = patch_temp
        prev_x, prev_y = pos_x, pos_y
        patch_list[:, :, i] = patch_temp
    return patch_prev, prev_x, prev_y, patch_list


def template_median(template: TemplateMatching, patch_list) -> TemplateMatching:
    return TemplateMatching(
        init_x=template.init_x,
        init_y=template.init_y,
        prev_x=template.prev_x,
        prev_y=template.prev_y,
        patch_ref=np.median(patch_list, axis=2).astype(np.float64),
        patch_prev=template.patch_ref,
        patch_list=template.patch_list,
        tiff_files=template.tiff_files,
    )
