"""
The ``Spline`` of TerraME's ``sci`` package (commit 42b0b3e, ``lua/Spline.lua``).

``sci.Spline`` is not a cubic spline through the points: it samples a
Catmull-Rom curve at ``steps`` points per segment (the first and last points
repeated as end controls) and reads it by linear interpolation between the
samples. :class:`Spline` reproduces both steps, with the same floating-point
operations, so that a model that uses it matches TerraME to the last bit.

One consequence of following Lua: the loop over ``t`` adds ``1 / steps``
to ``t`` and, for some ``steps`` (1000 among them), the sum ends just below
1, so the last sample stops short of the last point (at 7999.5 instead of
8000 in MonoLake) and a larger ``x`` raises an error, in TerraME as here.
"""
from __future__ import annotations

from bisect import bisect_left
from collections.abc import Sequence


class Spline:
    """
    TerraME ``sci.Spline``: a sampled Catmull-Rom curve read linearly.

    Parameters
    ----------
    xs, ys : sequence of float
        Control points, with increasing ``xs``.
    steps : int, optional
        Samples per segment, by default 10 (as in ``sci``).

    Raises
    ------
    ValueError
        From :meth:`value`, for an ``x`` outside the range of the points, as
        TerraME does.
    """

    def __init__(self, xs: Sequence[float], ys: Sequence[float], steps: int = 10) -> None:
        points = list(zip((float(x) for x in xs), (float(y) for y in ys), strict=True))
        self.values = self._build(points, steps)
        self.xs = [p[0] for p in self.values]

    @staticmethod
    def _build(points: list[tuple[float, float]], steps: int) -> list[tuple[float, float]]:
        if len(points) < 3:
            return points
        count = len(points) - 1
        values: list[tuple[float, float]] = []
        for i in range(1, count + 1):  # 1-based, as in Lua
            if i == 1:
                p0, p1, p2, p3 = points[0], points[0], points[1], points[2]
            elif i == count:
                p0, p1, p2, p3 = points[-3], points[-2], points[-1], points[-1]
            else:
                p0, p1, p2, p3 = points[i - 2], points[i - 1], points[i], points[i + 1]
            # Lua's ``for t = 0, 1, 1 / steps`` adds the step to t each time
            t = 0.0
            dt = 1 / steps
            while t <= 1:
                x = 0.5 * ((2 * p1[0]) + (p2[0] - p0[0]) * t
                           + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t * t
                           + (3 * p1[0] - p0[0] - 3 * p2[0] + p3[0]) * t * t * t)
                y = 0.5 * ((2 * p1[1]) + (p2[1] - p0[1]) * t
                           + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t * t
                           + (3 * p1[1] - p0[1] - 3 * p2[1] + p3[1]) * t * t * t)
                if not values or (values[-1][0] != x and values[-1][1] != y):
                    values.append((x, y))
                t += dt
        return values

    def value(self, x: float) -> float:
        """Linear interpolation between the two samples around ``x``."""
        xs = self.xs
        if not xs[0] <= x <= xs[-1]:
            raise ValueError(f"Spline: {x} is outside the range [{xs[0]}, {xs[-1]}].")
        i = bisect_left(xs, x)
        if xs[i] == x:
            return self.values[i][1]
        (x0, y0), (x1, y1) = self.values[i - 1], self.values[i]
        w = (x - x0) / (x1 - x0)
        return (1 - w) * y0 + w * y1

    __call__ = value


__all__ = ["Spline"]
