# dissmodel-sysdyn

System Dynamics models for [dissmodel](https://github.com/LambdaGeo/dissmodel).

This library provides a collection of System Dynamics models implemented using the `dissmodel` core.

## Installation

```bash
pip install dissmodel-sysdyn
```

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

Or to run a specific model (e.g., SIR):

```bash
streamlit run examples/streamlit/sysdyn_sir.py
```

### Notebooks

Interactive Jupyter notebooks are available in the `examples/notebooks/` directory.
