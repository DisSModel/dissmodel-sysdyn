# Reference Guide

This reference guide provides a detailed technical description of each model available in the `dissmodel-sysdyn` package. Each entry explains the theoretical background, the underlying equations, and the Python implementation.

---

## Chaotic Growth (Logistic Map)

### Description
The Chaotic Growth model simulates a single-species population using the discrete logistic map (quadratic map). It demonstrates how simple, deterministic rules can lead to complex, chaotic behavior. For growth rates near 4, trajectories become extremely sensitive to initial conditions.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `pop`: Normalized population in the interval (0, 1).
*   **Parameters:**
    *   `rate`: Growth rate parameter (r). Influences the system's stability and chaos.

### Model Logic
The update rule follows the standard logistic map:
P(t+1) = r * P(t) * (1 - P(t))

```python
def execute(self) -> None:
    self.pop = self.rate * self.pop * (1.0 - self.pop)
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import ChaoticGrowth

env = Environment(end_time=100)
model = ChaoticGrowth(pop=0.1, rate=3.9)
env.run()
```

---

## Coffee Cooling (Newton's Law of Cooling)

### Description
This model simulates the cooling of a hot beverage towards ambient temperature. It is a classic example of first-order negative feedback, where the rate of change is proportional to the difference between the stock and its target.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `temperature`: Current temperature of the beverage.
*   **Parameters:**
    *   `room_temperature`: The ambient temperature (target).
    *   `cooling_rate`: Proportionality constant (k).

### Model Logic
The temperature update at each step follows Newton's Law:
T(t+1) = T(t) - k * (T(t) - T(room))

```python
def execute(self) -> None:
    self.temperature -= self.cooling_rate * (self.temperature - self.room_temperature)
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Coffee

env = Environment(end_time=30)
coffee = Coffee(temperature=90, room_temperature=22, cooling_rate=0.15)
env.run()
```

---

## Daisyworld (Gaia Hypothesis)

### Description
Based on the famous model by Watson and Lovelock, Daisyworld demonstrates how life can regulate a planet's environment. White and black daisies interact with solar luminosity through albedo feedback to buffer the planetary temperature.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `white_area`: Area covered by white daisies (high albedo).
    *   `black_area`: Area covered by black daisies (low albedo).
    *   `empty_area`: Bare soil.
*   **Parameters:**
    *   `sun_luminosity`: Fractional solar luminosity.
    *   `white_albedo`, `black_albedo`, `soil_albedo`: Reflectivity values.
    *   `decay_rate`: Mortality rate of daisies.

### Model Logic
The model calculates a global average temperature (Tave) based on the planet's aggregate albedo. Local temperatures for each daisy type then determine their growth rates.
Planet_Albedo = Sum(Area_i * Albedo_i)
Area(t+1) = Area(t) + Area(t) * (Growth - Decay)

```python
def execute(self) -> None:
    pa = self._planet_albedo()
    self.ave_temp = _planet_temp(self.sun_luminosity, pa)

    temp_white = _local_temp(self.ave_temp, pa, self.white_albedo)
    white_growth = _daisy_growth_rate(temp_white) * self.empty_area
    self.white_area += self.white_area * (white_growth - self.decay_rate)
    # ... same for black area
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Daisyworld

env = Environment(end_time=200)
model = Daisyworld(sun_luminosity=1.0)
env.run()
```

---

## Homeostasis

### Description
The Homeostasis model illustrates a system reaching a stable equilibrium through a constant inflow and a rate-proportional negative feedback. It is a fundamental building block for self-regulating systems.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `stock`: The accumulated value.
*   **Parameters:**
    *   `gain`: Fixed increment added each step (Inflow).
    *   `rate`: Proportional feedback coefficient (Outflow regulator).

### Model Logic
S(t+1) = S(t) + g + r * S(t)
Where g is the gain and r is the negative rate.

```python
def execute(self) -> None:
    self.stock += self.gain + self.rate * self.stock
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Homeostasis

env = Environment(end_time=50)
model = Homeostasis(stock=10, gain=5, rate=-0.2)
env.run()
```

---

## Limited Growth (Logistic Growth)

### Description
This model extends simple exponential growth by adding a carrying capacity. As the population grows, the available resources decrease, slowing down the growth rate until the system reaches a stable limit.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `pop`: Population size.
*   **Parameters:**
    *   `rate`: Intrinsic growth rate (r).
    *   `capacity`: Environmental carrying capacity (K).

### Model Logic
The update equation is the discrete logistic growth model:
P(t+1) = P(t) + P(t) * r * (1 - P(t)/K)

```python
def execute(self) -> None:
    self.pop += self.pop * self.rate * (1.0 - self.pop / self.capacity)
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import LimitedGrowth

env = Environment(end_time=100)
model = LimitedGrowth(pop=10, rate=0.2, capacity=1000)
env.run()
```

---

## Lorenz Attractor

### Description
A system of three coupled ordinary differential equations originally derived from atmospheric convection. It is a classic example of deterministic chaos and the "Butterfly Effect".

### Stocks, Flows & Parameters
*   **Stocks:** x, y, z (State variables).
*   **Parameters:**
    *   sigma, rho, beta: System coefficients.
    *   delta: Integration time step (dt).

### Model Logic
The system uses Forward Euler integration:
dx/dt = sigma * (y - x)
dy/dt = x * (rho - z) - y
dz/dt = x * y - beta * z

```python
def execute(self) -> None:
    dx = self.sigma * (self.y - self.x)
    dy = self.x * (self.rho - self.z) - self.y
    dz = self.x * self.y - self.beta * self.z

    self.x += self.delta * dx
    self.y += self.delta * dy
    self.z += self.delta * dz
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Lorenz

env = Environment(end_time=5000)
model = Lorenz()
env.run()
```

---

## Mono Lake

### Description
A water-balance model for Mono Lake, based on Ford's Modelling the Environment. It accounts for precipitation, runoff, evaporation, and human export to track lake volume and elevation.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `water_in_lake`: Lake volume in KAF.
*   **Converters:**
    *   `level`: Lake elevation (derived from volume).
*   **Parameters:**
    *   `prec_rate`, `evap_rate`, `runoff`, `export`.

### Model Logic
Change_V = (Precipitation + Runoff + In) - (Evaporation + Export + Out)

```python
def execute(self) -> None:
    self.water_in_lake += self._total_input() - self._total_output()
    self.level = float(_water_elevation(self.water_in_lake))
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import MonoLake

env = Environment(end_time=50)
model = MonoLake(export=150)
env.run()
```

---

## Population Growth

### Description
Simple exponential growth model with a variable growth rate. It can simulate accelerating or decelerating growth.

### Stocks, Flows & Parameters
*   **Stocks:**
    *   `population`: Number of individuals.
    *   `growth`: Current growth rate.
*   **Parameters:**
    *   `growth_change`: Multiplier for the growth rate.

### Model Logic
P(t+1) = P(t) * (1 + r(t))
r(t+1) = r(t) * c

```python
def execute(self) -> None:
    self.population *= (1 + self.growth)
    self.growth *= self.growth_change
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import PopulationGrowth

env = Environment(end_time=20)
model = PopulationGrowth(population=100, growth=0.05, growth_change=1.1)
env.run()
```

---

## Predator-Prey (Lotka-Volterra)

### Description
Models the interaction between a prey population and a predator population. The system exhibits cyclic oscillations where predators lag behind prey peaks.

### Stocks, Flows & Parameters
*   **Stocks:** prey, predator.
*   **Parameters:**
    *   prey_growth, prey_death_pred, pred_death, pred_growth_kills.

### Model Logic
P(t+1) = P(t) + rP * P(t) - dPP * P(t) * Q(t)
Q(t+1) = Q(t) - dQ * Q(t) + gQ * P(t) * Q(t)

```python
def execute(self) -> None:
    self.prey += (self.prey_growth * self.prey - self.prey_death_pred * self.prey * self.predator)
    self.predator += (-self.pred_death * self.predator + self.pred_growth_kills * self.prey * self.predator)
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import PredatorPrey

env = Environment(end_time=200)
model = PredatorPrey()
env.run()
```

---

## Random Walk

### Description
A stochastic model where a value moves up or down with a specific probability. Demonstrates drift and diffusion.

### Stocks, Flows & Parameters
*   **Stocks:** value.
*   **Parameters:**
    *   prob: Probability of an upward step.
    *   seed: Random number generator seed.

### Model Logic
V(t+1) = V(t) + noise
Where noise is +1 with probability p and -1 with probability 1-p.

```python
def execute(self) -> None:
    rng = object.__getattribute__(self, "_rng")
    if rng.random() <= self.prob:
        self.value += 1.0
    else:
        self.value -= 1.0
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import RandomWalk

env = Environment(end_time=100)
model = RandomWalk(prob=0.55, seed=42)
env.run()
```

---

## Room Temperature (Thermostat)

### Description
Simulates indoor temperature regulation against a time-varying outdoor climate. Uses a thermostat logic (inertia) and thermal loss to the environment.

### Stocks, Flows & Parameters
*   **Stocks:** inside.
*   **Converters:** outside (Time-varying).
*   **Parameters:** temp_set, thermal_inertia, loss_to_outside.

### Model Logic
Delta_in = Theta * (Tset - Tin)
Delta_out = Lambda * (Tin - Tout)
Tin(t+1) = Tin + Delta_in - Delta_out

```python
def execute(self) -> None:
    t = self.env.now()
    self.outside = self._climate(t)
    inflow = self.thermal_inertia * (self.temp_set - self.inside)
    outflow = self.loss_to_outside * (self.inside - self.outside)
    self.inside += inflow - outflow
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import RoomTemperature

env = Environment(end_time=24)
model = RoomTemperature()
env.run()
```

---

## SIR (Epidemiological Model)

### Description
Tracks the spread of a disease through Susceptible, Infected, and Recovered compartments. It is the foundation of modern mathematical epidemiology.

### Stocks, Flows & Parameters
*   **Stocks:** susceptible, infected, recovered.
*   **Parameters:** contacts, probability, duration.

### Model Logic
Delta_I = I * (contacts * probability) * (S/N)
Delta_R = I / duration

```python
def execute(self) -> None:
    total = self.susceptible + self.infected + self.recovered
    alpha = self.contacts * self.probability
    new_infected = self.infected * alpha * (self.susceptible / total)
    new_recovered = self.infected / self.duration

    self.susceptible -= new_infected
    self.infected += new_infected - new_recovered
    self.recovered += new_recovered
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import SIR

env = Environment(end_time=60)
sir = SIR(infected=5, probability=0.3)
env.run()
```

---

## Tub (Water in Tub)

### Description
A fundamental stock-and-flow model representing water levels in a tub with constant drainage and periodic inflow.

### Stocks, Flows & Parameters
*   **Stocks:** water.
*   **Parameters:** out_flow, in_flow, in_period.

### Model Logic
Water level is updated every step and clamped at zero.
W(t+1) = max(0, W(t) - Outflow + Inflow_periodic)

```python
def execute(self) -> None:
    self._step += 1
    self.water -= self.out_flow
    if self.water < 0.0: self.water = 0.0
    if self._step % self.in_period == 0:
        self.water += self.in_flow
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Tub

env = Environment(end_time=50)
tub = Tub(water=100, out_flow=2, in_flow=50, in_period=20)
env.run()
```

---

## Yeast Growth

### Description
Models yeast proliferation in a closed culture using a logistic equation with an explicit hard cap at the carrying capacity.

### Stocks, Flows & Parameters
*   **Stocks:** cells.
*   **Parameters:** capacity, rate.

### Model Logic
C(t+1) = C(t) + C(t) * r * (1 - C(t)/K)
The result is explicitly clamped to K.

```python
def execute(self) -> None:
    self.cells += self.cells * self.rate * (1.0 - self.cells / self.capacity)
    if self.cells > self.capacity:
        self.cells = self.capacity
```

### Full Usage Example
```python
from dissmodel.core import Environment
from dissmodel_sysdyn.models import Yeast

env = Environment(end_time=15)
yeast = Yeast()
env.run()
```
