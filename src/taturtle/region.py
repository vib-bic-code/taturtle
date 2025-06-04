"""A 2D region."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """A 2D spatial region."""

    x1: int
    x2: int
    y1: int
    y2: int

    def __post_init__(self) -> None:
        """Validate parameters."""
        if self.x1 > self.x2 or self.y1 > self.y2:
            raise ValueError("Invalid region: x1 > x2 or y1 > y2")

        if self.x1 < 0 or self.x2 < 0 or self.y1 < 0 or self.y2 < 0:
            raise ValueError("Invalid region: cannot be negative")

    def xs(self, x1: int, x2: int) -> Region:
        """Make a new Region with updated x values."""
        return Region(x1, x2, self.y1, self.y2)

    def ys(self, y1: int, y2: int) -> Region:
        """Make a new Region with updated y values."""
        return Region(self.x1, self.x2, y1, y2)
