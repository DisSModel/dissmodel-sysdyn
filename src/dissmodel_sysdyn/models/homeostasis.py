from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Stock", "orange")
class Homeostasis(Model):
    """
    Homeostasis model — stock with fixed inflow and proportional outflow.

    Demonstrates how a system reaches a stable equilibrium (homeostasis)
    through the interplay of a constant additive gain and a rate-proportional
    negative feedback. Regardless of the initial stock value the system
    converges to the same steady state ``gain / |rate|``.

    Parameters
    ----------
    stock : float, optional
        Initial stock value, by default 0.0.
    gain : float, optional
        Fixed increment added to the stock each step, by default 2.0.
    rate : float, optional
        Proportional feedback coefficient. Negative values produce
        stabilising feedback (homeostasis). By default -0.4.

    Notes
    -----
    The ``@track_plot`` decorator registers ``stock`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    The update equation at each step is:

    .. math::

        S_{t+1} = S_t + g + r \\cdot S_t

    Where :math:`g` is :attr:`gain` and :math:`r` is :attr:`rate`.
    The steady-state is :math:`S^* = -g / r`.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=30)
    >>> model = Homeostasis()
    >>> env.run()
    """

    #: Current stock value.
    stock: float

    #: Fixed increment added each step.
    gain: float

    #: Proportional feedback coefficient.
    rate: float

    def setup(
        self,
        stock: float = 0.0,
        gain: float = 2.0,
        rate: float = -0.4,
    ) -> None:
        """
        Configure the model parameters.

        Parameters
        ----------
        stock : float, optional
            Initial stock value, by default 0.0.
        gain : float, optional
            Fixed increment added each step, by default 2.0.
        rate : float, optional
            Proportional feedback coefficient, by default -0.4.
        """
        self.stock = stock
        self.gain  = gain
        self.rate  = rate

    def execute(self) -> None:
        """
        Advance the model by one time step.

        Adds the fixed gain and the proportional feedback to the stock.
        """
        self.stock += self.gain + self.rate * self.stock


__all__ = ["Homeostasis"]
