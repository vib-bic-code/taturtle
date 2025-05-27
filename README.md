# taturtle

- WPI: preparation for the pip plugin
- https://packaging.python.org/en/latest/
- Issues: pytest or unittest and make them work

## README

### Installation
- windows and linux compatible
- a faire

### Usage and tutorial
- the test data and the roi are in "/GBW-0004_CMEVIB_OMERO/0001_LIMONE/Tatiana/test_clem/"
```bash
python main.py  --x_a 6 182 --y_a 2073 2278 --search_window  100 --alpha 1.0 --to_crop True --thick_corr True --slice_thickness_nm 5.0 --cpu 16 --img_ref "pathway_dataset/dataset/ref_image.tif"
```

### How to run tests
 ``` python -m unittest tests/tests_utils.py```
  ``` python -m unittest tests/tests_thickness_corr.py```
   ``` python -m unittest tests/tests_autocrop.py```
### Contact

- tatiana.woller@kuleuven.be

