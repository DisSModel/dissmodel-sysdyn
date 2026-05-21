from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Pop", "green")
class LimitedGrowth(Model):
    """
    Logistic population growth with a carrying capacity.

    Extends simple exponential growth with a density-dependent
    brake: as the population approaches ``capacity`` the effective
    growth rate falls towards zero, producing the characteristic
    S-shaped (sigmoidal) curve.

    Parameters
    ----------
    pop : float, optional
        Initial population size, by default 300.
    rate : float, optional
        Intrinsic (maximum) growth rate per step, by default 0.105.
    capacity : float, optional
        Environmental carrying capacity (maximum sustainable
        population), by default 20 000.

    Notes
    -----
    The ``@track_plot`` decorator registers ``pop`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    The update equation is the discrete logistic growth model:

    .. math::

        P_{t+1} = P_t + P_t \\cdot r \\cdot \\left(1 - \\frac{P_t}{K}\\right)

    Where :math:`r` is :attr:`rate` and :math:`K` is :attr:`capacity`.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=100)
    >>> model = LimitedGrowth()
    >>> env.run()
    """

    #: Current population size.
    pop: float

    #: Intrinsic growth rate.
    rate: float

    #: Environmental carrying capacity.
    capacity: float

    def setup(
        self,
        pop: float = 300.0,
        rate: float = 0.105,
        capacity: float = 20_000.0,
    ) -> None:
        self.pop      = pop
        self.rate     = rate
        self.capacity = capacity

    def execute(self) -> None:
        self.pop += self.pop * self.rate * (1.0 - self.pop / self.capacity)


__all__ = ["LimitedGrowth"]
