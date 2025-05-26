#import numpy as np
import os
import skimage.io as iio
import time
from template_matching import *
from thickness_correction import *
from autocrop import AutoCropper
#from pathlib import Path
#import sys
#sys.path.append(r"C:\GBW_MyDownloads\taturtle")
from utils import *
from tests import *

def main():
    # Argument parsing
    x_a, y_a, search_window, alpha, crop, thick_corr, slice_thickness_nm, cpu, image_ref = arguments_parser() 
    input_path = Path(image_ref).parent
    print(thick_corr)
    # Output Paths
    os.makedirs(os.path.join(Path(input_path).parent, 'output'), exist_ok=True)
    os.makedirs(os.path.join(Path(input_path).parent, 'thickness_corr'), exist_ok=True)
    os.makedirs(os.path.join(Path(input_path).parent, 'cropped'), exist_ok=True)
    precision = np.float64

    #  first template matching
    start = time.time()
    if crop =="False" or crop=="false":
        print("autocrop skipped")
    else:
        x_shift, y_shift=AutoCropper.run_autocrop(input_path, image_ref,'cropped')
        x_a = [x - x_shift for x in x_a]; y_a = [y - y_shift for y in y_a]
        input_path = os.path.join(Path(input_path).parent, 'cropped')
        image_ref = os.path.join(Path(input_path).parent, 'cropped', Path(image_ref).name)

    if thick_corr=="False" or thick_corr=="false":
        init_x, init_y, prev_x, prev_y, patch_ref, patch_prev, patch_list, tiff_files=init_templatematching(input_path, image_ref, x_a, y_a, precision, 1)
        patch_prev, prev_x, prev_y, patch_list=unpack_result_template_step1(run_template_matching(input_path,tiff_files, patch_ref, patch_prev, alpha, search_window, prev_x, prev_y, precision,cpu),patch_ref, tiff_files)
        patch_ref_new, patch_prev = np.median(patch_list, axis=2).astype(precision), patch_ref
        search_window = search_window // 4
        results2=run_template_matching(input_path,tiff_files, patch_ref_new, patch_prev, alpha, search_window, prev_x, prev_y, precision,cpu)
        for i, (pos_x2, pos_y2, patch_temp2) in enumerate(results2):
            shift_x, shift_y=save_shift_image(input_path, 'output', tiff_files[i], init_x, init_y, pos_x2, pos_y2)
            print(f'Registration displacement ({i+1}/{len(tiff_files)}): {shift_x} - {shift_y}')
        print("The time of execution of the template matching without thickness correction is :",(time.time()-start) , "s using", cpu, "CPU")
    elif thick_corr=="True" or thick_corr=="true":
        len_input_files,len_slices =run_thickness_correction(input_path,slice_thickness_nm)
        print("Before", len_input_files, "After", len_slices, "Thickness correction passed")
        init_x, init_y, prev_x, prev_y, patch_ref, patch_prev, patch_list,file_list_thickness=init_templatematching(input_path, image_ref, x_a, y_a, precision, 2)
        patch_prev, prev_x, prev_y, patch_list=unpack_result_template_step1(run_template_matching(input_path,file_list_thickness, patch_ref, patch_prev, alpha, search_window, prev_x, prev_y, precision,cpu), patch_ref,file_list_thickness)
        patch_ref_new, search_window  = np.median(patch_list, axis=2).astype(precision), search_window // 4
        patch_prev = patch_ref
        results2=run_template_matching(input_path,file_list_thickness, patch_ref_new, patch_prev, alpha, search_window, prev_x, prev_y, precision,cpu)
        for i, (pos_x2, pos_y2, patch_temp2) in enumerate(results2):
            shift_x2, shift_y2=save_shift_image(input_path, 'output', file_list_thickness[i], init_x, init_y, pos_x2, pos_y2)
            print(f'Registration displacement ({i+1}/{len(file_list_thickness)}): {shift_x2} - {shift_y2}')
        print("The time of execution of the template matching with thickness correction is :",(time.time()-start) , "s using", cpu, "CPU")
if __name__ == "__main__":
    main()
