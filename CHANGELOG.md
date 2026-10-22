# Changelog

## [Unreleased]

- **Fix:** `Daisyworld` now follows TerraME: after updating the white area,
  it computes the planet albedo again for the black daisies. The trajectory
  changes (up to 0.61 in area); the equilibrium is the same. New attributes
  `temp_near_white` and `temp_near_black`, as in TerraME.
- **Fix:** `MonoLake` reads the lake surface and elevation with TerraME's
  `sci.Spline` (a Catmull-Rom curve sampled at 1000 points per segment and
  read linearly; new `dissmodel_sysdyn.models._spline.Spline`) instead of
  scipy's `CubicSpline`, which differed by up to 26 KAF in 50 steps. As in
  TerraME, a volume outside the curve raises an error instead of
  extrapolating. scipy, which was used without being a declared
  dependency, is no longer needed.
- `PredatorPrey`, `RoomTemperature`, `SIR` and `MonoLake` do their
  arithmetic in TerraME's order, so that the results are the same doubles.
- `tests/test_goldens.py` (marker `golden`): every model against TerraME
  2.0.1 runs from `terrame-goldens` v0.1.0. All 16 deterministic cases
  (13 models, some with two parameter sets) give **the same doubles as
  TerraME at every step**; RandomWalk is compared by distribution.
  `tests/goldens/` holds the goldens, their SHA-256 provenance and the
  script that copies them. The strict `xfail`s of `Daisyworld` and
  `MonoLake` in `test_terrame_parity.py` are removed.

- **Fix:** `Tub` kept its counter in `_step`, the attribute where dissmodel's
  `Model` stores the interval between ticks, so the interval grew at every
  execution (a run from t=1 to 30 executed 8 times). The counter is now
  `_tick`; a test checks that every model executes once per tick.
- Examples, notebooks, demo and docs use `Environment(start_time=1, end_time=N)`,
  which runs N steps at t = 1..N like a TerraME `Timer` with `finalTime = N`.
  The default `start_time=0` runs one step more and shifts the clock by one hour
  in `RoomTemperature`. A note in the docs explains the convention.
- `tests/test_terrame_parity.py` compares the full trajectory of each model
  with a step-by-step transcription of the TerraME `sysdyn` package
  (`terrame/sysdyn`, commit 9e671cb). Eleven models match within 1e-9.
  Two known differences are kept as strict `xfail`: `MonoLake` (TerraME's
  sampled Catmull-Rom spline vs scipy `CubicSpline`) and `Daisyworld`
  (TerraME recomputes the planet albedo after updating the white area; same
  equilibrium, different trajectory). `RandomWalk` is not compared.

## [0.1.1] — 2026-10-08

First citable release. The `v0.1.0` tag was created before the release
branch was merged and points to the previous code (no license, citation
metadata or tests); use 0.1.1.

- Models compatible with dissmodel 0.5.0 or later (tested with 0.5.0, 0.6.0 and 0.6.6).
- `tests/test_models_smoke.py` runs every exported model for a few steps, headless,
  and checks that its state stays numeric; a GitHub Actions workflow runs it.
- `streamlit` is no longer a required dependency: no module of the package uses
  it, only the Streamlit examples (`pip install "dissmodel-sysdyn[examples]"`).
- `demo/`: self-contained Streamlit app (Dockerfile, pinned requirements,
  Hugging Face Space header) that can be deployed on its own; before, the
  Dockerfile copied `src/` and `pyproject.toml` from the repository root.
- MIT license and `CITATION.cff`.
