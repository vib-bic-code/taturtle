"""Utility functions."""

import argparse
from pathlib import Path
from typing import Any

from taturtle.region import Region


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


class RegionAction(argparse.Action):
    """Make a region either by specifying 4 params or xs and ys."""

    def __call__(
        self,
        _parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,  # noqa: ANN401
        _option_string: str | None = None,
    ) -> None:
        """Run the action."""
        if namespace.region is None:
            namespace.region = Region(0, 0, 0, 0)

        if self.dest == "x":
            namespace.region = namespace.region.xs(*values)
        elif self.dest == "y":
            namespace.region = namespace.region.ys(*values)
        else:
            namespace.region = Region(*values)


def arguments_parser() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Alignment of FIB-SEM images using template matching and "
            "thickness correction."
        ),
    )
    parser.add_argument(
        "--region",
        type=int,
        nargs=4,
        action=RegionAction,
        metavar=("x1", "x2", "y1", "y2"),
        help="Specify a region as four integers: x1 x2 y1 y2",
    )
    parser.add_argument(
        "--x",
        nargs=2,
        action=RegionAction,
        type=int,
        metavar=("x1", "x2"),
        help="Specify the x-boundaries of a region.",
    )
    parser.add_argument(
        "--y",
        nargs=2,
        action=RegionAction,
        type=int,
        metavar=("y1", "y2"),
        help="Specify the y-boundaries of a region.",
    )
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
    args = parser.parse_args()

    if not isinstance(args.region, Region):
        parser.error("A region must be specified with --region or --x/--y.")
    delattr(args, "x")
    delattr(args, "y")

    return args
