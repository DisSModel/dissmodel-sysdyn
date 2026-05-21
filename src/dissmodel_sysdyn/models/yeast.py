from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot


@track_plot("Cells", "purple")
class Yeast(Model):
    """
    Yeast population growth model.

    Models yeast cell proliferation in a closed culture vessel using
    the discrete logistic equation. Growth is capped at the environment's
    carrying capacity — cells cannot exceed the resource limit.

    Parameters
    ----------
    cells : float, optional
        Initial number of cells, by default 9.6.
    capacity : float, optional
        Maximum cell count the environment can sustain, by default 665.0.
    rate : float, optional
        Per-capita growth rate per step, by default 1.1.

    Notes
    -----
    The ``@track_plot`` decorator registers ``cells`` for automatic
    live plotting. Any :class:`~dissmodel.visualization.Chart` connected
    to the same environment will plot it at every step without any extra
    configuration.

    The update equation is the discrete logistic model with an explicit
    capacity cap:

    .. math::

        C_{t+1} = C_t + C_t \\cdot r \\cdot \\left(1 - \\frac{C_t}{K}\\right)

        C_{t+1} = \\min(C_{t+1},\\, K)

    Where :math:`r` is :attr:`rate` and :math:`K` is :attr:`capacity`.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=9)
    >>> model = Yeast()
    >>> env.run()
    """

    #: Current number of cells.
    cells: float

    #: Maximum cell count the environment can sustain.
    capacity: float

    #: Per-capita growth rate per step.
    rate: float

    def setup(
        self,
        cells: float = 9.6,
        capacity: float = 665.0,
        rate: float = 1.1,
    ) -> None:
        """
        Configure the model parameters.

        Parameters
        ----------
        cells : float, optional
            Initial number of cells, by default 9.6.
        capacity : float, optional
            Carrying capacity of the environment, by default 665.0.
        rate : float, optional
            Per-capita growth rate per step, by default 1.1.
        """
        self.cells    = cells
        self.capacity = capacity
        self.rate     = rate

    def execute(self) -> None:
        """
        Advance the model by one time step.

        Applies the logistic growth equation and clamps the result
        to the carrying capacity.
        """
        self.cells += self.cells * self.rate * (1.0 - self.cells / self.capacity)
        if self.cells > self.capacity:
            self.cells = self.capacity


__all__ = ["Yeast"]
