"""
System Dynamics Explorer — Streamlit
=====================================
Interactive interface to explore system dynamics models from the 
``dissmodel-sysdyn`` library.

This application dynamically discovers all available models and generates 
the corresponding UI for parameters and live plotting.
"""
from __future__ import annotations

import inspect

import streamlit as st

import dissmodel_sysdyn.models as sysdyn_models
from dissmodel.core import Environment, Model
from dissmodel.visualization import Chart, display_inputs

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="SysDyn Explorer", layout="centered", page_icon="📈")
st.title("System Dynamics Explorer (dissmodel)")

# ---------------------------------------------------------------------------
# Discover models — only concrete Model subclasses
# ---------------------------------------------------------------------------
model_classes: dict[str, type] = {
    name: cls
    for name, cls in inspect.getmembers(sysdyn_models, inspect.isclass)
    if issubclass(cls, Model)
    and cls is not Model
    and not inspect.isabstract(cls)
}

# ---------------------------------------------------------------------------
# Sidebar & Configuration
# ---------------------------------------------------------------------------
st.sidebar.title("Simulation Control")

model_name = st.sidebar.selectbox("Select Model", list(model_classes.keys()))
steps      = st.sidebar.slider("Simulation steps", min_value=1, max_value=1000, value=30)
run        = st.button("🚀 Run Simulation")

# Get selected class
ModelClass = model_classes[model_name]

# Display Model Description
if ModelClass.__doc__:
    with st.expander("📖 About this model", expanded=True):
        st.markdown(ModelClass.__doc__)

# ---------------------------------------------------------------------------
# Setup & Model Instantiation
# ---------------------------------------------------------------------------

# 1. Environment
env = Environment(start_time=0, end_time=steps)

# 2. Model
model = ModelClass()

# 3. Sidebar widgets — model-specific parameters
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{model_name} Parameters**")
display_inputs(model, st.sidebar)

# 4. Chart
Chart(
    show_legend=True,
    show_grid=True,
    title=f"Results: {model_name}",
    plot_area=st.empty(),
)

# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------
if run:
    env.reset()
    env.run()
    st.success("Simulation completed!")
