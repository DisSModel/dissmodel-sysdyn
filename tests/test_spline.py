"""The ``sci.Spline`` of TerraME used by MonoLake."""
from __future__ import annotations

import pytest

from dissmodel_sysdyn.models._spline import Spline

XS = [0, 1000, 2000, 3000]
YS = [0, 24.7, 35.3, 48.6]


def test_passes_through_the_points():
    s = Spline(XS, YS, steps=1000)
    for x, y in zip(XS[:-1], YS[:-1], strict=True):
        assert s.value(x) == pytest.approx(y, abs=1e-12)


def test_last_sample_falls_short_of_the_last_point_as_in_lua():
    # Lua's ``for t = 0, 1, 1 / steps`` adds 1/1000 a thousand times and ends
    # just below 1, so the curve stops before the last point; TerraME then
    # refuses x beyond the last sample
    s = Spline(XS, YS, steps=1000)
    assert 2999 < s.xs[-1] < 3000
    with pytest.raises(ValueError):
        s.value(3000)
    assert Spline(XS, YS, steps=10).xs[-1] == 3000


def test_linear_between_samples():
    s = Spline(XS, YS, steps=10)
    (x0, y0), (x1, y1) = s.values[3], s.values[4]
    mid = (x0 + x1) / 2
    assert s.value(mid) == pytest.approx((y0 + y1) / 2)


def test_outside_the_range_raises_as_in_terrame():
    s = Spline(XS, YS)
    with pytest.raises(ValueError):
        s.value(-1)
    with pytest.raises(ValueError):
        s.value(3000.5)


def test_two_points_are_kept_as_given():
    s = Spline([0, 10], [1, 3])
    assert s.value(5) == 2
