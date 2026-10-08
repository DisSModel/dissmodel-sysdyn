"""
Smoke test: every system dynamics model exported by dissmodel_sysdyn.models
is instantiated with its default parameters and run for a few steps.

It checks that the models work with the installed dissmodel and that the
numeric state stays finite; it does not check the dynamics of each model.
"""
from __future__ import annotations

import inspect
import math

import numpy as np
import pytest

import dissmodel_sysdyn.models as sd_models
from dissmodel.core import Environment, Model

STEPS = 20

MODELS = sorted(
    (name, cls)
    for name, cls in inspect.getmembers(sd_models, inspect.isclass)
    if issubclass(cls, Model) and cls is not Model and not inspect.isabstract(cls)
)


def test_every_exported_model_is_covered():
    assert {n for n, _ in MODELS} == set(sd_models.__all__)


@pytest.mark.parametrize("name, cls", MODELS, ids=[n for n, _ in MODELS])
def test_model_runs(name, cls):
    np.random.seed(0)
    env = Environment(start_time=0, end_time=STEPS)
    model = cls()
    env.run()
    framework = {"start_time", "end_time", "name"}   # Model bookkeeping, not model state
    numeric = {
        k: v for k, v in vars(model).items()
        if not k.startswith("_") and k not in framework
        and isinstance(v, (int, float)) and not isinstance(v, bool)
    }
    assert numeric, f"{name} exposes no numeric state"
    for key, value in numeric.items():
        assert math.isfinite(value), f"{name}.{key} = {value}"
