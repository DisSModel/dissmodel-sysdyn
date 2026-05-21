from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Pop", "red")
class ChaoticGrowth(Model):
    """
    Chaotic population growth via the logistic map.

    A single-species population model where the update rule is the
    discrete logistic (quadratic) map. For growth rates near 4 the
    system exhibits deterministic chaos: trajectories are exquisitely
    sensitive to initial conditions despite the rule being entirely
    deterministic.

    Parameters
    ----------
    pop : float, optional
        Initial population, normalised to the interval (0, 1),
        by default 0.1.
    rate : float, optional
        Growth rate parameter ``r``. Values in (0, 1] lead to a
        stable fixed point; (1, 3] to stable oscillations; (3, 4]
        to period-doubling and eventually chaos. By default 4.0.

    Notes
    -----
    The ``@track_plot`` decorator registers ``pop`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    The update equation is the standard logistic map:

    .. math::

        P_{t+1} = r \\cdot P_t \\cdot (1 - P_t)

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=300)
    >>> model = ChaoticGrowth()
    >>> env.run()
    """

    #: Current normalised population.
    pop: float

    #: Growth rate parameter.
    rate: float

    def setup(
        self,
        pop: float = 0.1,
        rate: float = 4.0,
    ) -> None:
        """
        Configure the model parameters.

        Parameters
        ----------
        pop : float, optional
            Initial normalised population, by default 0.1.
        rate : float, optional
            Logistic map growth rate, by default 4.0.
        """
        self.pop  = pop
        self.rate = rate

    def execute(self) -> None:
        """
        Advance the model by one time step.

        Applies the logistic map update rule.
        """
        self.pop = self.rate * self.pop * (1.0 - self.pop)


__all__ = ["ChaoticGrowth"]
