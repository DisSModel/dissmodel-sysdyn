from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Water", "blue")
class Tub(Model):
    """
    Simple water-in-tub stock-and-flow model.

    A tub loses water each time step through a constant outflow.
    Optionally, water is added at a fixed periodic interval.
    Water level is clamped at zero — the tub never goes negative.

    Parameters
    ----------
    water : float, optional
        Initial volume of water in the tub (gallons), by default 40.
    out_flow : float, optional
        Volume drained per time step (gallons/step), by default 5.
    in_flow : float, optional
        Volume added every ``in_period`` steps (gallons), by default 0.
    in_period : int, optional
        Number of steps between each inflow event, by default 10.

    Notes
    -----
    The ``@track_plot`` decorator registers ``water`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    This model is the DisSModel equivalent of the TerraME ``Tub`` example,
    which uses two ``Event`` objects with different periods. Here the same
    behaviour is achieved by tracking the step counter internally and
    applying the inflow only when ``step % in_period == 0``.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=8)
    >>> tub = Tub(water=40, out_flow=5, in_flow=20, in_period=10)
    >>> env.run()
    """

    #: Current volume of water in the tub.
    water: float

    #: Volume drained per time step.
    out_flow: float

    #: Volume added every ``in_period`` steps.
    in_flow: float

    #: Number of steps between each inflow event.
    in_period: int

    def setup(
        self,
        water: float = 40.0,
        out_flow: float = 5.0,
        in_flow: float = 0.0,
        in_period: int = 10,
    ) -> None:
        """
        Configure the model parameters.

        Parameters
        ----------
        water : float, optional
            Initial volume of water in the tub, by default 40.0.
        out_flow : float, optional
            Volume drained per time step, by default 5.0.
        in_flow : float, optional
            Volume added every ``in_period`` steps, by default 0.0.
        in_period : int, optional
            Number of steps between each inflow event, by default 10.
        """
        self.water     = water
        self.out_flow  = out_flow
        self.in_flow   = in_flow
        self.in_period = in_period
        self._step     = 0

    def execute(self) -> None:
        """
        Advance the model by one time step.

        Applies the outflow every step and the inflow every
        ``in_period`` steps. Water is clamped to zero from below.
        """
        self._step += 1

        self.water -= self.out_flow
        if self.water < 0.0:
            self.water = 0.0

        if self._step % self.in_period == 0:
            self.water += self.in_flow


__all__ = ["Tub"]
