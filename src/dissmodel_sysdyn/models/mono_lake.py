from __future__ import annotations

from scipy.interpolate import CubicSpline
import numpy as np

from dissmodel.core import Model
from dissmodel.visualization import track_plot

_VOLUME_KAF  = np.array([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000], dtype=float)
_SURFACE_KM2 = np.array([0, 24.7, 35.3, 48.6, 54.3, 57.2, 61.6, 66.0, 69.9], dtype=float)
_ELEV_FT     = np.array([6224, 6335, 6369, 6392, 6412, 6430, 6447, 6463, 6477], dtype=float)

_water_surface   = CubicSpline(_VOLUME_KAF, _SURFACE_KM2, extrapolate=True)
_water_elevation = CubicSpline(_VOLUME_KAF, _ELEV_FT,     extrapolate=True)


@track_plot("level", "blue")
@track_plot("water_in_lake", "cyan")
class MonoLake(Model):
    """
    Mono Lake water-balance model.

    Reproduces the first Mono Lake model from Ford's *Modelling the
    Environment*. The lake gains water through precipitation and runoff
    and loses it through evaporation and human export.

    Parameters
    ----------
    water_in_lake : float, optional
        Initial lake volume in kilo-acre-feet (KAF), by default 2228.0.
    level : float, optional
        Initial lake elevation in feet, by default 6375.0.
    prec_rate : float, optional
        Precipitation rate in feet/year, by default 0.67.
    runoff : float, optional
        Annual runoff into the lake in KAF/year, by default 150.0.
    other_in : float, optional
        Other annual inputs in KAF/year, by default 47.6.
    evap_rate : float, optional
        Evaporation rate in feet/year, by default 3.75.
    other_out : float, optional
        Other annual outputs in KAF/year, by default 33.6.
    export : float, optional
        Annual water exported in KAF/year, by default 100.0.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=50)
    >>> model = MonoLake(export=100)
    >>> env.run()
    """

    #: Current lake volume (KAF).
    water_in_lake: float

    #: Current lake elevation (feet).
    level: float

    #: Precipitation rate (feet/year).
    prec_rate: float

    #: Annual runoff (KAF/year).
    runoff: float

    #: Other annual inputs (KAF/year).
    other_in: float

    #: Evaporation rate (feet/year).
    evap_rate: float

    #: Other annual outputs (KAF/year).
    other_out: float

    #: Annual water exported (KAF/year).
    export: float

    def setup(
        self,
        water_in_lake: float = 2228.0,
        level: float = 6375.0,
        prec_rate: float = 0.67,
        runoff: float = 150.0,
        other_in: float = 47.6,
        evap_rate: float = 3.75,
        other_out: float = 33.6,
        export: float = 100.0,
    ) -> None:
        self.water_in_lake = water_in_lake
        self.level         = level
        self.prec_rate     = prec_rate
        self.runoff        = runoff
        self.other_in      = other_in
        self.evap_rate     = evap_rate
        self.other_out     = other_out
        self.export        = export

    def _surface(self) -> float:
        return float(_water_surface(self.water_in_lake))

    def _total_input(self) -> float:
        return self._surface() * self.prec_rate + self.runoff + self.other_in

    def _total_output(self) -> float:
        return self._surface() * self.evap_rate + self.export + self.other_out

    def execute(self) -> None:
        self.water_in_lake += self._total_input() - self._total_output()
        self.level = float(_water_elevation(self.water_in_lake))


__all__ = ["MonoLake"]
