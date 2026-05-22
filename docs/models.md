# Step-by-Step Tutorials

This guide provides practical, laboratory-style tutorials for the two most iconic models in System Dynamics: the SIR epidemiological model and the Lotka-Volterra Predator-Prey model.

---

## Tutorial 1: Mapping an Epidemic (SIR Model)

In this laboratory, we will simulate the spread of a contagious disease through a population of 10,000 individuals.

### Step 1: Environment Setup
We define the time horizon for our simulation. Epidemiological events often unfold over weeks or months. Here, we set a 60-step duration.

```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import SIR
import matplotlib.pyplot as plt

# Create the simulation environment
env = Environment(end_time=60)
```

### Step 2: Model Configuration
We instantiate the SIR model. We start with a nearly susceptible population and a small number of "Patient Zeros".

```python
# Initialize the model with specific parameters
model = SIR(
    susceptible=9995, 
    infected=5, 
    recovered=0,
    contacts=10,      # High contact rate
    probability=0.1,   # 10% chance of transmission
    duration=5         # Disease lasts 5 steps
)
```

### Step 3: Run the Simulation
Execute the environment loop. The framework will call the model's `execute()` method at each step.

```python
# Run the simulation
env.run()
```

### Step 4: Visualization
A System Dynamics model is best understood through Time Series. We will plot the evolution of all three compartments.

```python
# Accessing history
plt.figure(figsize=(10, 6))
# Plot Susceptible (Green), Infected (Red), Recovered (Blue)
plt.plot(model.history["susceptible"], color='green', label='Susceptible')
plt.plot(model.history["infected"], color='red', label='Infected')
plt.plot(model.history["recovered"], color='blue', label='Recovered')

plt.title("SIR Model: Epidemic Evolution")
plt.xlabel("Time Steps")
plt.ylabel("Number of Individuals")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
```

---

## Tutorial 2: The Dance of Life and Death (Predator-Prey)

Learn how to simulate the oscillatory relationship between wolves (predators) and moose (prey).

### Step 1: Initialize the Space
Set a longer time horizon to observe at least two full cycles of oscillation.

```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import PredatorPrey
import matplotlib.pyplot as plt

env = Environment(end_time=200)
```

### Step 2: Define Biological Parameters
The stability of the cycle depends on the balance between growth and death rates.

```python
model = PredatorPrey(
    prey=1000, 
    predator=40,
    prey_growth=0.1,         # Fast prey reproduction
    prey_death_pred=0.002,   # Predation efficiency
    pred_death=0.1,          # Predator mortality
    pred_growth_kills=0.0001 # Conversion of prey to predator offspring
)
```

### Step 3: Execute the Cycle
Observe how the populations interact. As prey becomes abundant, predators thrive; then, over-predation leads to a prey crash, followed by a predator famine.

```python
env.run()
```

### Step 4: Multi-Axis Visualization
Because prey and predator populations often have different orders of magnitude, we use contrasting colors and clear legends.

```python
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Prey on primary axis (Green)
ax1.set_xlabel('Time Steps')
ax1.set_ylabel('Prey Population', color='green')
ax1.plot(model.history["prey"], color='green', label='Prey (Moose)')
ax1.tick_params(axis='y', labelcolor='green')

# Plot Predators on secondary axis (Red)
ax2 = ax1.twinx()
ax2.set_ylabel('Predator Population', color='red')
ax2.plot(model.history["predator"], color='red', label='Predator (Wolves)')
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Lotka-Volterra: Predator-Prey Oscillations")
fig.tight_layout()
plt.grid(True, axis='x', linestyle=':', alpha=0.5)
plt.show()
```

!!! info "Observation"
    Notice the phase shift: the predator population peaks shortly after the prey population reaches its maximum. This "lag" is a classic signature of negative feedback with delay.
