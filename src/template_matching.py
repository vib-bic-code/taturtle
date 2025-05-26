import numpy as np
from src.utils import *
import scipy.ndimage as ndi
import tifffile
import multiprocessing as mp

def init_templatematching(input_path:str, image_ref:str, x_a:list, y_a:list, precision:float, tm_number:int)-> tuple:
    ''' initializing parameters for template matching'''
    if tm_number==1:
        tiff_files_list = get_file_list(input_path)
        im=np.array(tifffile.imread(image_ref))
    elif tm_number==2:
        tiff_files_list=get_file_list(Path(input_path).parent / "thickness_corr" )
        for f in tiff_files_list:
            if Path(image_ref).stem in Path(f).stem:
                im =np.array(tifffile.imread(image_ref))
    patch_ref = im[x_a[0]:x_a[1], y_a[0]:y_a[1]].astype(precision)
    init_x, init_y = x_a[0], y_a[0]
    prev_x, prev_y = init_x, init_y
    patch_prev = patch_ref
    patch_list = np.zeros((patch_ref.shape[0], patch_ref.shape[1], len(tiff_files_list)))
    return init_x, init_y, prev_x, prev_y, patch_ref, patch_prev, patch_list, tiff_files_list

def calculate_mad(patch:np.ndarray, patch_ref:np.ndarray, patch_prev:np.ndarray, alpha:int)->int:
    ''' calculates the mean absolute difference between two patches'''
    diff1 = patch - patch_ref
    diff2 = patch - patch_prev
    return alpha * np.sum(np.abs(diff1)) + (1 - alpha) * np.sum(np.abs(diff2))

def process_image(i:int, input_path:str, file_array:np.ndarray,patch_r:np.ndarray, patch_p:np.ndarray, alpha:int, search_window:int, prev_x:int, prev_y:int, precision:float) -> tuple:
    ''' returns the new position in x/y and the new patch'''
    im=tifffile.imread(os.path.join(input_path,file_array[i]))
    mad_max = 255 * (patch_r.size)
    min_x, min_y = max(prev_x - search_window, 0), max(prev_y - search_window, 0)
    pos_x, pos_y = min_x, min_y
    for x in range(min_x, min_x + 2 * search_window + 2):
        for y in range(min_y, min_y + 2 * search_window + 2):
            patch = im[x:(x + patch_r.shape[0]), y:(y + patch_r.shape[1])].astype(precision)
            mad = calculate_mad(patch, patch_r, patch_p, alpha)
            if mad < mad_max:
                mad_max = mad
                pos_x, pos_y = x, y
                patch_temp = patch
    return pos_x, pos_y, patch_temp

def save_shift_image(input_path:str, outdir:str, file:np.ndarray, x_0:int, y_0:int, posx:int, posy:int )-> tuple:
    ''' shift, save the aligned images and returns the shift in x/y'''
    im = ndi.shift(tifffile.imread(os.path.join(input_path,file)), (x_0 - posx, y_0 - posy))
    iio.imsave(os.path.join(Path(input_path).parent, outdir, f"{Path(file).stem}.tif"), im)
    shift_x, shift_y=x_0 - posx, y_0 - posy
    return shift_x, shift_y

def run_template_matching(input_path:str,tiff_files:np.ndarray, patch_ref:np.ndarray, patch_prev:np.ndarray, alpha:int, search_window:int, prev_x:int, prev_y:int, precision:float,cpu:int)->tuple:
    ''' runs the template matching'''
    with mp.Pool(processes=cpu) as pool:
        results = pool.starmap(process_image, [(i, input_path,tiff_files, patch_ref, patch_prev, alpha, search_window, prev_x, prev_y, precision) for i in range(len(tiff_files))])
    return results

def unpack_result_template_step1(results:tuple, patch_ref:np.ndarray, tiff_files_list:np.ndarray)->tuple:
    ''' unpack results of the first step of the template matching'''
    patch_list = np.zeros((patch_ref.shape[0], patch_ref.shape[1], len(tiff_files_list)))
    for i, (pos_x, pos_y, patch_temp) in enumerate(results):
        patch_prev = patch_temp
        prev_x, prev_y = pos_x, pos_y
        patch_list[:, :, i] = patch_temp
    return patch_prev, prev_x, prev_y, patch_list