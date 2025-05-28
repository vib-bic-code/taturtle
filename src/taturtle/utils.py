import argparse
from pathlib import Path



# TODO: None handling can be avoided by returning an empty list?
def get_file_list(folder_path: Path) -> list[Path] | None:
    """returns the list of tiff files in the folder"""
    if folder_path.exists():
        return [
            folder_path / f
            for f in folder_path.iterdir()
            if f.suffix in (".tif", ".tiff")
        ]

    return None


def create_filename_output(input_path: Path, f: Path, output_folder: Path) -> Path:
    """creates the output filename"""
    filename = f.stem
    output_path = input_path.parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}.tif"


def create_filename_output_thickness(
    input_path: Path, f: Path, output_folder: Path, index: int
) -> Path:
    """creates the out filename after thickness correction"""
    filename = f.stem
    output_path = input_path.parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}_{index}.tif"


def arguments_parser():
    """collects arguments to run the template matching and thickness correction"""
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument("--x_a", nargs=2, type=int, help="x_a values")
    parser.add_argument("--y_a", nargs=2, type=int, help="y_a values")
    parser.add_argument("--search-window", type=int, help="search window")
    parser.add_argument("--alpha", type=float, default=1.0, help="alpha value")
    parser.add_argument("--to-crop", type=str, help="set to True to crop images")
    parser.add_argument(
        "--thick-corr",
        action=argparse.BooleanOptionalAction,
        help="Do thickness correction",
    )
    parser.add_argument(
        "--slice-thickness-nm", type=float, help="slice thickness in nm"
    )
    parser.add_argument("--cpu", type=int, help="number of cpus to use")
    parser.add_argument(
        "--img-ref", type=str, help="reference image associated to the ROI"
    )
    args = parser.parse_args()
    return (
        args.x_a,
        args.y_a,
        args.search_window,
        args.alpha,
        args.to_crop,
        args.thick_corr,
        args.slice_thickness_nm,
        args.cpu,
        args.img_ref,
    )
