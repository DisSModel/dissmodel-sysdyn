# dissmodel-sysdyn

System Dynamics models for [dissmodel](https://github.com/LambdaGeo/dissmodel).

This library provides a collection of System Dynamics models implemented using the `dissmodel` core.

## Installation

```bash
pip install dissmodel-sysdyn
```

## Models

The library includes a wide range of System Dynamics models:

*   **Epidemiology**: SIR Model.
*   **Ecology & Biology**: Predator-Prey (Lotka-Volterra), Yeast Growth, Daisyworld, Population Growth, Limited Growth, Chaotic Growth.
*   **Physics & Thermodynamics**: Coffee Cooling, Room Temperature, Tub (Stock/Flow).
*   **Complex Systems**: Lorenz Attractor, Homeostasis.
*   **Environment**: Mono Lake Water Balance.
*   **Stochasticity**: Random Walk.

## Examples

The project includes several examples demonstrating how to run the models via CLI, Streamlit, or Jupyter Notebooks.

### CLI

To run a simple SIR model in the terminal:

```bash
python examples/cli/sysdyn_sir.py
```

### Streamlit

To explore all available models using an interactive web interface:

```bash
streamlit run examples/streamlit/sysdyn_all.py
```

### Notebooks (Educational)

We have developed a comprehensive suite of **14 educational notebooks** designed for students and researchers. Each notebook functions as a self-contained tutorial, including scientific context, mathematical formulations, and guided experiments.

Located in `examples/notebooks/`:

*   `sysdyn_sir.ipynb` - Epidemiological dynamics.
*   `sysdyn_predator_prey.ipynb` - Predator-prey interactions.
*   `sysdyn_daisyworld.ipynb` - Gaia hypothesis and albedo feedback.
*   `sysdyn_lorenz.ipynb` - Deterministic chaos and strange attractors.
*   `sysdyn_chaotic_growth.ipynb` - Logistic map and population chaos.
*   `sysdyn_yeast.ipynb` - Logistic growth with carrying capacity.
*   `sysdyn_coffee.ipynb` - Newton's Law of Cooling.
*   `sysdyn_mono_lake.ipynb` - Ecological water balance.
*   `sysdyn_homeostasis.ipynb` - Biological self-regulation.
*   `sysdyn_tub.ipynb` - Fundamental stock and flow concepts.
*   ... and more for every model in the library.

To run the notebooks:

```bash
jupyter notebook examples/notebooks/
```
