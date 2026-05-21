from __future__ import annotations

from typing import Callable

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("inside", "orange")
@track_plot("outside", "blue")
@track_plot("temp_set", "red")
class RoomTemperature(Model):
    """
    Thermostat model with a time-varying outdoor climate.

    Parameters
    ----------
    temp_set : float, optional
        Thermostat set-point temperature (°C), by default 20.0.
    inside : float, optional
        Initial indoor temperature (°C), by default 15.0.
    outside : float, optional
        Initial outdoor temperature (°C), by default 1.0.
    thermal_inertia : float, optional
        Fraction of the heating gap added per step, by default 0.33.
    loss_to_outside : float, optional
        Fraction of the indoor-outdoor gap lost per step, by default 0.30.
    climate : callable or None, optional
        Function ``f(t) -> float`` for outdoor temperature.
        Defaults to a parabolic midday-peak curve (1–15 °C).

    Notes
    -----
    The update equations at each step are:

    .. math::

        T_{out} = f(t)

        \\Delta_{in}  = \\theta \\cdot (T_{set} - T_{in})

        \\Delta_{out} = \\lambda \\cdot (T_{in} - T_{out})

        T_{in,t+1}   = T_{in} + \\Delta_{in} - \\Delta_{out}

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=24)
    >>> model = RoomTemperature()
    >>> env.run()
    """

    #: Thermostat set-point temperature.
    temp_set: float

    #: Current indoor temperature.
    inside: float

    #: Current outdoor temperature.
    outside: float

    #: Fraction of heating gap added per step.
    thermal_inertia: float

    #: Fraction of indoor-outdoor gap lost per step.
    loss_to_outside: float

    def setup(
        self,
        temp_set: float = 20.0,
        inside: float = 15.0,
        outside: float = 1.0,
        thermal_inertia: float = 0.33,
        loss_to_outside: float = 0.30,
        climate: Callable[[float], float] | None = None,
    ) -> None:
        self.temp_set        = temp_set
        self.inside          = inside
        self.outside         = outside
        self.thermal_inertia = thermal_inertia
        self.loss_to_outside = loss_to_outside
        object.__setattr__(
            self, "_climate",
            climate if climate is not None
            else lambda t: 15.0 - 0.1 * (t - 12.0) ** 2
        )

    def execute(self) -> None:
        t = self.env.now()
        climate = object.__getattribute__(self, "_climate")
        self.outside = climate(t)
        inflow  = self.thermal_inertia * (self.temp_set - self.inside)
        outflow = self.loss_to_outside  * (self.inside   - self.outside)
        self.inside += inflow - outflow


__all__ = ["RoomTemperature"]
