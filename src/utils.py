import os
import tifffile
import numpy as np
import skimage.io as iio
from pathlib import Path
import argparse

def get_file_list(folder_path:str)->np.ndarray:
    ''' returns the list of tiff files in the folder'''
    if os.path.exists(folder_path):
        tiff_files = np.array([os.path.join(folder_path,f) for f in os.listdir(folder_path) if f.endswith(('.tif','.tiff'))])
    else:
        print('The folder does not exist')
    return tiff_files

def create_filename_output(input_path:str,f:str, output_folder:str)->str:
    ''' creates the output filename'''
    filename = Path(f).stem
    output_path = Path(input_path).parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    new_filename = output_path / f"{filename}.tif"
    return new_filename

def create_filename_output_thickness(input_path:str, f:str, output_folder:str, index:int)->str:
    ''' creates the out filename after thickness correction'''
    filename = Path(f).stem
    output_path = Path(input_path).parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    new_filename = output_path / f"{filename}_{index}.tif"
    return new_filename

def arguments_parser():
    ''' collects arguments to run the template matching and thickness correction'''
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--x_a', nargs=2, type=int, help='x_a values')
    parser.add_argument('--y_a', nargs=2, type=int, help='y_a values')
    parser.add_argument('--search_window', type=int, help='search window')
    parser.add_argument('--alpha', type=float, default=1.0,help='alpha value')
    parser.add_argument('--to_crop', type=str, help='set to True to crop images')
    parser.add_argument('--thick_corr', type=str, help='set to True for thickness correction')
    parser.add_argument('--slice_thickness_nm', type=float, help='slice thickness in nm')
    parser.add_argument('--cpu', type=int, help='amount of cpus')
    parser.add_argument('--img_ref', type=str, help='reference image associated to the ROI')
    args=parser.parse_args()
    return args.x_a,args.y_a, args.search_window, args.alpha, args.to_crop, args.thick_corr, args.slice_thickness_nm,args.cpu, args.img_ref

def read_image(file_path:str)->np.ndarray:
    ''' reads the image as tiff file'''
    if isinstance(file_path, str):
        return tifffile.imread(file_path)
    else:
        print('The file is not a standard tiff file')
