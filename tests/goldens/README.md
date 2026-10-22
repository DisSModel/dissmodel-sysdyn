# TerraME reference values for the sysdyn models

The `sysdyn` suite of
[`terrame-goldens`](https://github.com/LambdaGeo/terrame-goldens) v0.1.0:
what TerraME 2.0.1 computed running the models of the
[`sysdyn`](https://github.com/TerraME/sysdyn) package (commit `9e671cb`; `sci`
commit `42b0b3e` for MonoLake's spline).

- `<case>.csv.gz`: a column `step` and one column per variable, from step 0
  (the state after `init`) to `finalTime`, written with 17 significant digits,
  so every double is recovered exactly. A variable that does not exist yet
  at step 0 is empty. Lorenz keeps steps 0 to 100 and then every 100th step.
- `random_walk.csv.gz`: `seed, step, value` for seeds 1 to 50.
- `cases.csv`: model, arguments, final time and variables of each case.
- `reference.json`: the source version, the package commits and the SHA-256
  of each source file.

To copy them again from a copy of `terrame-goldens`:

```bash
python tests/goldens/make_reference.py /path/to/terrame-goldens
```

The values are the output of TerraME and of the `sysdyn` and `sci` packages
(INPE and TerraLAB/UFOP); they are offered here under CC-BY-4.0, as the
goldens they come from.
