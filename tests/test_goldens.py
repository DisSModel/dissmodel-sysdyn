"""
The models against TerraME itself.

``goldens/`` holds the ``sysdyn`` suite of ``terrame-goldens`` (see
``goldens/README.md``): what TerraME 2.0.1 computed running the models of the
``sysdyn`` package, written with 17 significant digits so that every double
is recovered exactly. Each model runs with the same parameters and must give
**the same doubles** as TerraME at every step (bit for bit), for every
variable TerraME records.

The exception is Daisyworld, whose temperatures take a fourth root
(``x ** 0.25`` in Python, ``x ^ 0.25`` in Lua). Both languages call the C
library's ``pow``, and its last bit depends on the library: the goldens come
from the ``terrame-docker`` image (glibc 2.27), and the same TerraME binary
on glibc 2.39 differs from the 16th significant digit on (see the README of
``terrame-goldens``). Python on any recent system behaves like the latter, so
Daisyworld is compared with a relative tolerance of ``POW_RTOL``.

RandomWalk draws random numbers, so it is compared by distribution with the
50 TerraME runs.
"""
from __future__ import annotations

import csv
import gzip
import re
from pathlib import Path

import numpy as np
import pytest
from dissmodel.core import Environment, Model

import dissmodel_sysdyn.models as sd

pytestmark = pytest.mark.golden

GOLDENS = Path(__file__).resolve().parent / "goldens"

#: Cases that use the C library's pow, and their relative tolerance (see above).
POW_RTOL = {"daisyworld": 1e-13}

with open(GOLDENS / "cases.csv", newline="") as _f:
    CASES = [c for c in csv.DictReader(_f) if not c["seeds"]]


def snake(name: str) -> str:
    """TerraME's camelCase attribute name in DisSModel's snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def parse_arguments(text: str) -> dict[str, float]:
    return {snake(k): float(v) for k, v in (a.split("=") for a in text.split(";") if a)}


def load(case: str) -> tuple[list[str], dict[int, list[float]]]:
    with gzip.open(GOLDENS / f"{case}.csv.gz", "rt", newline="") as f:
        rows = list(csv.reader(f))
    nan = float("nan")
    return rows[0][1:], {int(r[0]): [float(v) if v else nan for v in r[1:]] for r in rows[1:]}


class _Recorder(Model):
    """Reads the model after each step (created after the model, so it runs after it)."""

    def setup(self, model: Model, attrs: list[str]) -> None:  # type: ignore[override]
        self.model, self.attrs, self.rows = model, attrs, {}
        self.rows[0] = self.read()

    def read(self) -> list[float]:
        return [float(getattr(self.model, a, float("nan"))) for a in self.attrs]

    def execute(self) -> None:
        self.rows[int(self.env.now())] = self.read()


@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_trajectory_matches_terrame(case: dict[str, str]) -> None:
    variables, ref = load(case["case"])
    attrs = [snake(v) for v in variables]
    env = Environment(start_time=1, end_time=int(case["final_time"]))
    model = getattr(sd, case["model"])(**parse_arguments(case["arguments"]))
    rec = _Recorder(model=model, attrs=attrs)
    env.run()
    for t, expected in ref.items():
        got = rec.rows[t]
        for var, e, g in zip(variables, expected, got, strict=True):
            if np.isnan(e):  # not defined yet in TerraME (Daisyworld at step 0)
                continue
            rtol = POW_RTOL.get(case["case"])
            if rtol is None:
                assert g == e, f"{case['case']}.{var} at step {t}: {g!r} != TerraME {e!r}"
            else:
                assert abs(g - e) <= rtol * abs(e), (
                    f"{case['case']}.{var} at step {t}: {g!r} vs TerraME {e!r}")


def test_random_walk_matches_terrame_distribution() -> None:
    with gzip.open(GOLDENS / "random_walk.csv.gz", "rt", newline="") as f:
        rows = list(csv.DictReader(f))
    final_tm = np.array([int(r["value"]) for r in rows if r["step"] == "100"])
    ours = []
    for seed in range(1, 201):
        env = Environment(start_time=1, end_time=100)
        model = sd.RandomWalk(seed=seed)
        env.run()
        ours.append(model.value)
    ours_a = np.array(ours)
    # a walk of 100 steps of +-1: mean 0, standard deviation 10
    se = np.sqrt(final_tm.var(ddof=1) / len(final_tm) + ours_a.var(ddof=1) / len(ours_a))
    assert abs(ours_a.mean() - final_tm.mean()) < 4 * se
    assert 7 < ours_a.std() < 13 and 7 < final_tm.std() < 13
    assert set(np.unique(ours_a % 2)) == {0}  # even after an even number of steps
