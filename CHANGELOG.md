# Changelog

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
