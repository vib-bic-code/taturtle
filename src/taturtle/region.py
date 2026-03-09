"""A 2D region."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """A 2D spatial region."""

    col1: int
    col2: int
    row1: int
    row2: int

    def __post_init__(self) -> None:
        """Validate parameters."""
        if self.col1 > self.col2 or self.row1 > self.row2:
            raise ValueError("Invalid region: col1 > col2 or row1 > row2")

        if self.col1 < 0 or self.col2 < 0 or self.row1 < 0 or self.row2 < 0:
            raise ValueError("Invalid region: cannot be negative")

    def cols(self, col1: int, col2: int) -> Region:
        """Make a new Region with updated column values."""
        return Region(col1, col2, self.row1, self.row2)

    def rows(self, row1: int, row2: int) -> Region:
        """Make a new Region with updated row values."""
        return Region(self.col1, self.col2, row1, row2)
