import argparse
from pathlib import Path


def get_file_list(folder_path: Path) -> list[Path]:
    """returns the list of tiff files in the folder"""
    if folder_path.exists():
        return [f for f in folder_path.iterdir() if f.suffix in (".tif", ".tiff")]

    return []


def create_filename_output(f: Path, output_path: Path) -> Path:
    """creates the output filename"""
    filename = f.stem
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}.tif"


def create_filename_output_thickness(
    f: Path, output_path: Path, index: int
) -> Path:
    """creates the out filename after thickness correction"""
    filename = f.stem
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}_{index}.tif"


def arguments_parser():
    """collects arguments to run the template matching and thickness correction"""
    parser = argparse.ArgumentParser(
        description="Alignment of FIB-SEM images using template matching and thickness correction."
    )
    parser.add_argument("--rows", nargs=2, type=int, help="row range (y values)")
    parser.add_argument("--cols", nargs=2, type=int, help="column range (x values)")
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        help="region coordinates: row1 row2 col1 col2 (y1 y2 x1 x2)",
    )
    parser.add_argument("--search_window", type=int, help="search window")
    parser.add_argument("--alpha", type=float, default=1.0, help="alpha value")
    parser.add_argument(
        "--crop",
        action=argparse.BooleanOptionalAction,
        help="set to True to crop images",
    )
    parser.add_argument(
        "--thick_corr",
        action=argparse.BooleanOptionalAction,
        help="Do thickness correction",
    )
    parser.add_argument(
        "--slice_thickness_nm", type=float, help="slice thickness in nm"
    )
    parser.add_argument("--cpu", type=int, help="number of cpus to use")
    parser.add_argument(
        "--img_ref", type=Path, help="reference image associated to the ROI"
    )
    parser.add_argument(
        "--output", type=Path, help="base output directory for all results"
    )
    return parser.parse_args()
