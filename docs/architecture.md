# Architecture Overview

The `dissmodel-sysdyn` package provides a high-level framework for System Dynamics (SysDyn) modeling in Python. Inspired by the philosophy of TerraME, it allows researchers and students to translate Forrester diagrams directly into executable code using clear abstractions for Stocks, Flows, and Converters.

## Core Abstractions

In `dissmodel-sysdyn`, the fundamental components of System Dynamics are mapped to Python's object-oriented primitives:

### 1. Stocks (Accumulators)
Stocks represent the state of the system at any given time. In our framework, Stocks are defined as **instance attributes** of a model class. They are initialized in the `setup()` method and updated in the `execute()` method.

!!! info "Example"
    In a population model, `self.population` is a Stock that accumulates individuals over time.

### 2. Flows (Rates of Change)
Flows represent the rate at which Stocks change during a time step. Unlike some visual tools where Flows are explicit objects, `dissmodel-sysdyn` expresses Flows as **intermediate variables or logic** within the `execute()` method.

!!! note "Mathematical Mapping"
    A flow is equivalent to the derivative dS/dt or the difference ΔS.

### 3. Converters and Parameters
Converters (or auxiliary variables) and Parameters influence the rates of Flows. These are implemented as **model attributes** that are typically set during the `setup()` phase and remain constant or change according to their own internal logic.

---

## Numerical Integration and Time Discretization

System Dynamics models are naturally described by Ordinary Differential Equations (ODEs). To solve these on a computer, we must discretize time.

### The Integration Loop
The `Environment` class manages the simulation clock. At each time step (t -> t + dt), it calls the `execute()` method of all active models.

### Euler Method
Most models in this package employ the **Forward Euler Method**. The new value of a Stock is calculated by adding the net flow (Inflows - Outflows) multiplied by the time step to the current value:

S(t + dt) = S(t) + (Inflow - Outflow) * dt

In many discrete models within the package, dt is implicitly assumed to be 1, simplifying the update to:
```python
self.stock += inflow - outflow
```

---

## Framework Comparison: Radioactive Decay

To illustrate the framework overhead versus the business logic, consider a simple radioactive decay model.

### Pure Python (Procedural)
```python
amount = 100.0
decay_rate = 0.1
for t in range(50):
    decay = amount * decay_rate
    amount -= decay
    print(f"Time {t}: {amount}")
```

### `dissmodel-sysdyn` Framework
Using the framework adds structure, automatic plotting, and environment management.

```python
from dissmodel.core import Model, Environment
from dissmodel.visualization import track_plot

@track_plot("Substance", "blue")
class Decay(Model):
    def setup(self, amount=100.0, rate=0.1):
        self.amount = amount  # Stock
        self.rate = rate      # Parameter

    def execute(self):
        # Flow logic
        decay = self.amount * self.rate 
        # Update rule (Euler)
        self.amount -= decay

# Running the simulation
env = Environment(end_time=50)
model = Decay()
env.run()
```

The framework allows you to focus on the **Differential Equations** and **Model Logic** while providing tools for complex orchestrations and visualizations.
