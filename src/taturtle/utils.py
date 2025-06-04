"""Utility functions."""

import argparse
from pathlib import Path


def get_file_list(folder_path: Path) -> list[Path]:
    """Return the list of tiff files in the folder."""
    if folder_path.exists():
        return [f for f in folder_path.iterdir() if f.suffix in (".tif", ".tiff")]

    return []


def create_filename_output(input_path: Path, f: Path, output_folder: Path) -> Path:
    """Create the output filename."""
    filename = f.stem
    output_path = input_path.parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}.tif"


def create_filename_output_thickness(
    input_path: Path,
    f: Path,
    output_folder: Path,
    index: int,
) -> Path:
    """Create the out filename after thickness correction."""
    filename = f.stem
    output_path = input_path.parent / output_folder
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{filename}_{index}.tif"


def arguments_parser() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Alignment of FIB-SEM images using template matching and "
            "thickness correction."
        ),
    )
    parser.add_argument("--xa", nargs=2, type=int, help="x_a values")
    parser.add_argument("--ya", nargs=2, type=int, help="y_a values")
    parser.add_argument("--search-window", type=int, help="search window")
    parser.add_argument("--alpha", type=float, default=1.0, help="alpha value")
    parser.add_argument(
        "--crop",
        action=argparse.BooleanOptionalAction,
        help="set to True to crop images",
    )
    parser.add_argument(
        "--thick-corr",
        action=argparse.BooleanOptionalAction,
        help="Do thickness correction",
    )
    parser.add_argument(
        "--slice-thickness-nm",
        type=float,
        help="slice thickness in nm",
    )
    parser.add_argument("--cpu", type=int, help="number of cpus to use")
    parser.add_argument(
        "--img-ref",
        type=Path,
        help="reference image associated to the ROI",
    )
    return parser.parse_args()
