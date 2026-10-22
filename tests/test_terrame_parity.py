"""
Parity with the TerraME ``sysdyn`` package.

Each ``ref_*`` function below transcribes, step by step, the update rule of a
model in https://github.com/TerraME/sysdyn (``lua/<Model>.lua``, commit
9e671cb, 2020-08-20), with the TerraME default parameters and ``finalTime``.
A TerraME ``Timer`` runs t = 1, ..., finalTime, so the DisSModel model runs in
``Environment(start_time=1, end_time=finalTime)``.

The test compares the full trajectory, not only the final value. The reference
is a transcription, not output of TerraME itself: it checks that the Python
models follow the Lua equations and the TerraME clock.

Not covered: ``RandomWalk`` (different random generators); the SIR
``maximum`` event and the PredatorPrey ``period`` option (not ported, and
inactive with the default values).

``test_goldens.py`` compares the models with the output of TerraME itself.
"""
from __future__ import annotations

import numpy as np
import pytest

import dissmodel_sysdyn.models as sd
from dissmodel.core import Environment

RTOL = 1e-9
ATOL = 1e-9


def run_dissmodel(cls, final_time, attrs, **params):
    """Run ``cls`` for t = 1..final_time and return the state after each step."""
    env = Environment(start_time=1, end_time=final_time)
    model = cls(**params)  # noqa: F841  (connects to env on creation)
    trace = []
    original = cls.execute

    def recording(self):
        original(self)
        trace.append([getattr(self, a) for a in attrs])

    # record the state after each execute(), for this run only
    try:
        cls.execute = recording
        env.run()
    finally:
        cls.execute = original
    return np.array(trace, dtype=float)


# ---------------------------------------------------------------------------
# Transcriptions of terrame/sysdyn lua/*.lua
# ---------------------------------------------------------------------------

def ref_coffee(final_time=20):
    temperature, room, out = 80.0, 20.0, []
    for _ in range(final_time):
        temperature = temperature - (temperature - room) * 0.1
        out.append([temperature])
    return out


def ref_chaotic_growth(final_time=300):
    pop, rate, out = 0.10, 4.0, []
    for _ in range(final_time):
        pop = rate * pop * (1 - pop)
        out.append([pop])
    return out


def ref_homeostasis(final_time=30):
    stock, gain, rate, out = 0.0, 2.0, -0.4, []
    for _ in range(final_time):
        stock = stock + gain + rate * stock
        out.append([stock])
    return out


def ref_limited_growth(final_time=100):
    pop, rate, capacity, out = 300.0, 0.105, 20000.0, []
    for _ in range(final_time):
        pop = pop + pop * rate * (1 - pop / capacity)
        out.append([pop])
    return out


def ref_lorenz(final_time=10000):
    x = y = z = 1.0
    delta, rho, sigma, beta = 0.01, 28.0, 10.0, 8.0 / 3.0
    out = []
    for _ in range(final_time):
        nx = sigma * (y - x)
        ny = x * (rho - z) - y
        nz = x * y - beta * z
        x, y, z = x + delta * nx, y + delta * ny, z + delta * nz
        out.append([x, y, z])
    return out


def ref_population_growth(final_time=7):
    population, growth, growth_change, out = 60.0, 0.5, 1.0, []
    for _ in range(final_time):
        population = population * (1 + growth)
        growth = growth * growth_change
        out.append([population])
    return out


def ref_predator_prey(final_time=500):
    predator, prey, out = 40.0, 1000.0, []
    for _ in range(final_time):
        prey = prey + 0.08 * prey - 0.001 * prey * predator
        predator = predator - 0.02 * predator + 0.00002 * prey * predator  # uses the new prey
        out.append([prey, predator])
    return out


def ref_room_temperature(final_time=24):
    temp_set, inside, out = 20.0, 15.0, []
    for t in range(1, final_time + 1):
        outside = 15 - 0.1 * (t - 12) ** 2
        inflow = 0.33 * (temp_set - inside)
        outflow = 0.30 * (inside - outside)
        inside = inside + inflow - outflow
        out.append([inside, outside])
    return out


def ref_sir(final_time=30):
    s, i, r = 9998.0, 2.0, 0.0
    duration, contacts, probability = 2, 6, 0.25
    out = []
    for _ in range(final_time):
        proportion = s / (s + i + r)
        new_infected = i * contacts * probability * proportion
        new_recovered = i / duration
        s = s - new_infected
        r = r + new_recovered
        i = i + new_infected - new_recovered
        out.append([s, i, r])
    return out


def ref_tub(final_time=8, in_flow=0.0):
    water, out_flow, out = 40.0, 5.0, []
    for t in range(1, final_time + 1):
        water = water - out_flow
        if water < 0:
            water = 0.0
        if t >= 10 and t % 10 == 0:        # Event{start = 10, period = 10}
            water = water + in_flow
        out.append([water])
    return out


def ref_yeast(final_time=9):
    cells, capacity, rate, out = 9.6, 665.0, 1.1, []
    for _ in range(final_time):
        cells = cells + cells * rate * (1 - cells / capacity)
        if cells > capacity:
            cells = capacity
        out.append([cells])
    return out


_SIGMA, _SOLAR_FLUX, _HEAT = 5.67e-08, 3668.0, 2.06e09


def _daisy_growth(temp_k):
    temp = temp_k - 273
    return 1 - 0.003265 * (22.5 - temp) ** 2 if 5.0 < temp < 40.0 else 0.0


def ref_daisyworld(final_time=100):
    lum, white, black, empty = 0.7, 0.40, 0.273, 0.327

    def albedo():
        return white * 0.75 + black * 0.25 + empty * 0.50

    out = []
    for _ in range(final_time):
        ave = (lum * _SOLAR_FLUX * (1 - albedo()) / (4 * _SIGMA)) ** 0.25
        t_white = (_HEAT * (albedo() - 0.75) + ave ** 4) ** 0.25
        white = white + white * (_daisy_growth(t_white) * empty - 0.3)
        t_black = (_HEAT * (albedo() - 0.25) + ave ** 4) ** 0.25   # albedo with the new white area
        black = black + black * (_daisy_growth(t_black) * empty - 0.3)
        empty = 1.0 - (black + white)
        out.append([white, black, empty])
    return out


def _terrame_spline(xs, ys, steps=1000):
    """TerraME sci.Spline (commit 42b0b3e): sampled Catmull-Rom + linear interpolation."""
    pts = list(zip(xs, ys))
    count = len(pts) - 1
    values = []
    for i in range(1, count + 1):
        if i == 1:
            p0, p1, p2, p3 = pts[0], pts[0], pts[1], pts[2]
        elif i == count:
            p0, p1, p2, p3 = pts[-3], pts[-2], pts[-1], pts[-1]
        else:
            p0, p1, p2, p3 = pts[i - 2], pts[i - 1], pts[i], pts[i + 1]
        t = 0.0
        while t <= 1:
            def cr(a, b, c, d):
                return 0.5 * (2 * b + (c - a) * t + (2 * a - 5 * b + 4 * c - d) * t * t
                              + (3 * b - a - 3 * c + d) * t ** 3)
            x = cr(p0[0], p1[0], p2[0], p3[0])
            y = cr(p0[1], p1[1], p2[1], p3[1])
            if not values or (values[-1][0] != x and values[-1][1] != y):
                values.append((x, y))
            t += 1 / steps
    vx, vy = (np.array(v) for v in zip(*values))
    return lambda v: float(np.interp(v, vx, vy))


def ref_mono_lake(final_time=50):
    volume = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    surface = _terrame_spline(volume, [0, 24.7, 35.3, 48.6, 54.3, 57.2, 61.6, 66.0, 69.9])
    elevation = _terrame_spline(volume, [6224, 6335, 6369, 6392, 6412, 6430, 6447, 6463, 6477])
    water, out = 2228.0, []
    for _ in range(final_time):
        area = surface(water)
        inflow = area * 0.67 + 150 + 47.6
        outflow = 3.75 * area + 100 + 33.6
        water = water + inflow - outflow
        out.append([water, elevation(water)])
    return out


# ---------------------------------------------------------------------------

CASES = [
    # name, class, finalTime, attributes, reference, parameters
    ("Coffee", sd.Coffee, 20, ["temperature"], ref_coffee, {}),
    ("ChaoticGrowth", sd.ChaoticGrowth, 300, ["pop"], ref_chaotic_growth, {}),
    ("Homeostasis", sd.Homeostasis, 30, ["stock"], ref_homeostasis, {}),
    ("LimitedGrowth", sd.LimitedGrowth, 100, ["pop"], ref_limited_growth, {}),
    ("Lorenz", sd.Lorenz, 10000, ["x", "y", "z"], ref_lorenz, {}),
    ("PopulationGrowth", sd.PopulationGrowth, 7, ["population"], ref_population_growth, {}),
    ("PredatorPrey", sd.PredatorPrey, 500, ["prey", "predator"], ref_predator_prey, {}),
    ("RoomTemperature", sd.RoomTemperature, 24, ["inside", "outside"], ref_room_temperature, {}),
    ("SIR", sd.SIR, 30, ["susceptible", "infected", "recovered"], ref_sir, {}),
    ("Tub", sd.Tub, 8, ["water"], ref_tub, {}),
    ("Yeast", sd.Yeast, 9, ["cells"], ref_yeast, {}),
    ("Daisyworld", sd.Daisyworld, 100, ["white_area", "black_area", "empty_area"],
     ref_daisyworld, {}),
    ("MonoLake", sd.MonoLake, 50, ["water_in_lake", "level"], ref_mono_lake, {}),
]


def _param(case):
    return pytest.param(*case, id=case[0])


@pytest.mark.parametrize("name, cls, final_time, attrs, reference, params",
                         [_param(c) for c in CASES])
def test_trajectory_matches_terrame(name, cls, final_time, attrs, reference, params):
    got = run_dissmodel(cls, final_time, attrs, **params)
    expected = np.array(reference(final_time), dtype=float)
    assert got.shape == expected.shape
    np.testing.assert_allclose(got, expected, rtol=RTOL, atol=ATOL)


def test_tub_periodic_inflow():
    """Exercises the TerraME Event{start = 10, period = 10} (inactive by default)."""
    got = run_dissmodel(sd.Tub, 30, ["water"], in_flow=20.0)
    np.testing.assert_allclose(got, np.array(ref_tub(30, in_flow=20.0)), rtol=RTOL, atol=ATOL)
