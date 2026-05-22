# System Dynamics with DisSModel

Welcome to the official documentation for the **dissmodel-sysdyn** package. This library is a specialized toolkit for building, simulating, and visualizing **System Dynamics (SD)** models using the Python programming language.

!!! tip "Try it Now: Interactive Demo"
    You can explore all the models in this package right in your browser! Visit our live demo on Hugging Face Spaces:
    [**dissmodel-sysdyn-demo**](https://huggingface.co/spaces/profsergiocosta/dissmodel-sysdyn-demo)

## What is System Dynamics?

System Dynamics is a methodology and mathematical modeling technique used to understand, conceptualize, and analyze the behavior of complex systems over time. Originally developed by Professor Jay Forrester at MIT in the 1950s, it focuses on the internal structure of a system—how elements interact through feedback loops and delays—to explain nonlinear behavior.

### The Core Pillars

To model any system dynamic, we rely on three fundamental concepts:

1.  **Stocks (Accumulators)**: These represent the state of the system at any given moment. They are the "bathtubs" of the system, accumulating flows over time (e.g., population, wealth, amount of water).
2.  **Flows (Rates)**: These represent the activities that change the stocks. Flows are the "faucets" and "drains" (e.g., birth rate, interest accumulation, evaporation).
3.  **Feedback Loops**: The circular chain of cause and effect. 
    *   **Reinforcing (+)**: Leads to exponential growth or collapse (e.g., interest on savings).
    *   **Balancing (-)**: Leads to stability and goal-seeking behavior (e.g., a thermostat).

## Why use dissmodel-sysdyn?

While many System Dynamics tools are purely visual (like Vensim or Stella), `dissmodel-sysdyn` brings the power of **Computational Modeling** to the Python ecosystem:

*   **Pedagogical Clarity**: Designed for students and researchers to see exactly how equations translate into code.
*   **Scientific Rigor**: Leverages established numerical integration methods (Euler) and scientific libraries (SciPy, NumPy).
*   **Automatic Visualization**: Integrated with the DisSModel core to provide real-time tracking and plotting of simulation variables.
*   **Interoperability**: Easily integrate your models with Jupyter Notebooks, Streamlit apps, or data science pipelines.

## Getting Started

If you are new to the package, we recommend the following path:

1.  Read the **Architecture Overview** to understand how we translate Forrester diagrams into Python classes.
2.  Explore the **Tutorials** for a hands-on laboratory experience with the SIR and Predator-Prey models.
3.  Use the **Models Reference** as a technical encyclopedia for the 14 pre-built models included in this library.

---
!!! note "Theoretical Foundation"
    "The behavior of a system is determined by its structure." — This is the central tenet of System Dynamics. By modeling the structure of feedback loops, we can predict—and influence—the behavior of the world around us.
