# taturtle

- WPI: preparation for the pip plugin
- https://packaging.python.org/en/latest/


## README

### Installation
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
- the test data and the roi are in "/GBW-0004_CMEVIB_OMERO/0001_LIMONE/Tatiana/test_clem/"
- general usage (in an active conda or venv environment):
 ```bash
usage: __main__.py [-h] [--x_a X_A X_A] [--y_a Y_A Y_A] [--search-window SEARCH_WINDOW] [--alpha ALPHA] [--crop | --no-crop] [--thick-corr | --no-thick-corr]
                   [--slice-thickness-nm SLICE_THICKNESS_NM] [--cpu CPU] [--img-ref IMG_REF]
 ```
- to run a template matching with autocrop and thickness correction
```bash
python  __main__.py  --x_a 6 71 --y_a 1140 1392 --search-window  100 --alpha 1.0  --crop --thick-corr --slice-thickness-nm 5.0  --img-ref "pathway\slice_00100_z=0.6358um.tif" --cpu 8
```

### Contact

- tatiana.woller@kuleuven.be

