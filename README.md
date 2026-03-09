# taturtle

- WPI: preparation for the pip plugin
- https://packaging.python.org/en/latest/
- python version of [EM_reg](https://github.com/vibbits/EMRegistration)

## README

### Installation

#### To use, with conda
```bash
git clone https://github.com/vib-bic-code/taturtle.git
cd taturtle
conda create -n taturtle-env -c conda-forge python=3.11
conda activate taturtle-env
python -m pip install -e .
```

#### To edit

```bash
git clone https://github.com/vib-bic-code/taturtle.git
cd taturtle
python -m venv .venv
pip install numpy scikit-image scipy tifffile
pip install pytest
pip install --editable .
```

### How to run tests after installation
 ```bash pytest```
 - what you should see:
```bash
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.13.3, pytest-8.3.5, pluggy-1.6.0
rootdir: C:\GBW_MyDownloads\taturtle
configfile: pyproject.toml
collected 14 items

tests\test_autocrop.py ......                                                                                                                                                [ 42%] 
tests\test_thickness_corr.py ....                                                                                                                                            [ 71%] 
tests\test_utils.py ....                                                                                                                                                     [100%] 

=============================================================================== 14 passed in 4.89s ================================================================================
```

### Usage and tutorial
- example data1: `C:\GBW_MyDownloads\data_HR\debug100\slice_00100_z=0.6358um.tif`
- test data and the roi are in `/GBW-0004_CMEVIB_OMERO/0001_LIMONE/Tatiana/test_clem/debug50` or `L:\GBW-0004_CMEVIB_OMERO\0001_LIMONE\Tatiana\test_clem\debug_50_d2`
- general usage (in an active conda or venv environment):
 ```bash
usage: taturtle [-h] [--rows row1 row2] [--cols col1 col2] [--region row1 row2 col1 col2]
                [--search_window SEARCH_WINDOW] [--alpha ALPHA] [--crop | --no_crop] [--thick_corr]
                [--slice_thickness_nm SLICE_THICKNESS_NM] [--cpu CPU] [--img_ref IMG_REF] [--output OUTPUT]
 ```
- to run a template matching with autocrop and thickness correction (example 1)
```bash
taturtle --rows 6 182 --cols 2073 2278 --search_window 100 --alpha 1.0 --crop --thick_corr --slice_thickness_nm 5.0 --cpu 8 --img_ref "/path/to/img_ref.tif"
```

- example2 using --region (row1 row2 col1 col2):
```bash
taturtle --region 6 71 1140 1392 --search_window 100 --alpha 1.0 --crop --thick_corr --slice_thickness_nm 5.0 --img_ref "pathway\slice_00100_z=0.6358um.tif" --cpu 8
```
  
### Contact

- tatiana.woller@vib.be

