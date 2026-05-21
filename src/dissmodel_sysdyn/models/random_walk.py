from __future__ import annotations

import random as _random

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Value", "gray")
class RandomWalk(Model):
    """
    Simple random walk model.

    At each step the tracked value moves up by one with probability
    ``prob`` or down by one with probability ``1 - prob``. Setting
    ``prob = 0.5`` produces a symmetric (unbiased) random walk;
    values above or below 0.5 introduce a drift.

    Parameters
    ----------
    value : float, optional
        Initial value of the walk, by default 0.0.
    prob : float, optional
        Probability of stepping up (+1) at each time step.
        Must be in ``[0, 1]``. By default 0.5.
    seed : int or None, optional
        Seed for the random number generator. Pass an integer for
        reproducible runs; ``None`` (default) uses the system entropy.

    Notes
    -----
    The ``@track_plot`` decorator registers ``value`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    The update rule at each step is:

    .. math::

        V_{t+1} = V_t + \\begin{cases} +1 & \\text{with prob } p \\\\ -1 & \\text{with prob } 1-p \\end{cases}

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=100)
    >>> model = RandomWalk(seed=42)
    >>> env.run()
    """

    #: Current value of the walk.
    value: float

    #: Probability of stepping up (+1).
    prob: float

    #: RNG seed — stored as a serialisable int so the model state
    #: survives pydantic round-trips. The RNG instance is reconstructed
    #: lazily on first use inside ``execute``.
    seed: int | None

    def setup(
        self,
        value: float = 0.0,
        prob: float = 0.5,
        seed: int | None = None,
    ) -> None:
        """
        Configure the model parameters.

        Parameters
        ----------
        value : float, optional
            Initial value of the walk, by default 0.0.
        prob : float, optional
            Probability of stepping up (+1) each step, by default 0.5.
        seed : int or None, optional
            RNG seed for reproducibility, by default None.
        """
        self.value = value
        self.prob  = prob
        self.seed  = seed
        # Initialise the RNG instance directly — not stored as a model
        # attribute to avoid pydantic serialisation issues with non-primitive
        # types. The instance lives on the object's __dict__ only.
        object.__setattr__(self, "_rng", _random.Random(seed))

    def execute(self) -> None:
        """
        Advance the model by one time step.

        Steps the value up or down by one according to :attr:`prob`.
        """
        rng: _random.Random = object.__getattribute__(self, "_rng")
        if rng.random() <= self.prob:
            self.value += 1.0
        else:
            self.value -= 1.0


__all__ = ["RandomWalk"]
