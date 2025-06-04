from pathlib import Path

from taturtle.utils import (
    create_filename_output,
    create_filename_output_thickness,
    get_file_list,
)


def test_get_file_list_returns_tiff_files():
    result = set(get_file_list(Path("tests") / Path("data")))
    expected = {
        Path("tests") / Path("data") / Path("image1.tif"),
        Path("tests") / Path("data") / Path("image2.tiff"),
    }

    assert result == expected


def test_get_file_list_nonexistent_folder():
    result = get_file_list(Path("nonexistent_folder"))
    assert result == []


def test_create_filename_output():
    f = Path("image1.tif")
    output_path = create_filename_output(
        Path("tests") / Path("data") / Path("image1.tif"),
        f,
        Path("test_output"),
    )
    expected_path = Path("tests") / Path("data") / Path("test_output") / "image1.tif"
    assert output_path == expected_path
    assert (Path("tests") / Path("data") / Path("test_output")).exists()


def test_create_filename_output_thickness():
    f = Path("image2.tiff")
    index = 5
    input_path = Path("tests") / Path("data") / Path("image1.tif")
    output_folder = Path("test_output")
    output_path = create_filename_output_thickness(input_path, f, output_folder, index)
    expected_path = Path("tests") / Path("data") / Path("test_output") / "image2_5.tif"
    assert output_path == expected_path
    assert (Path("tests") / Path("data") / Path("test_output")).exists()
