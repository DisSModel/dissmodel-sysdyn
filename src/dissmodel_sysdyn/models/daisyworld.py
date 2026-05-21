from __future__ import annotations

from dissmodel.core import Model
from dissmodel.visualization import track_plot

_SIGMA      = 5.67e-8
_SOLAR_FLUX = 3668.0
_Q          = 2.06e9


def _daisy_growth_rate(temp_k: float) -> float:
    temp_c = temp_k - 273.0
    if 5.0 < temp_c < 40.0:
        return max(0.0, 1.0 - 0.003265 * (22.5 - temp_c) ** 2)
    return 0.0


def _planet_temp(luminosity: float, albedo: float) -> float:
    return (_SOLAR_FLUX * luminosity * (1.0 - albedo) / (4.0 * _SIGMA)) ** 0.25


def _local_temp(planet_temp: float, planet_albedo: float, daisy_albedo: float) -> float:
    return (_Q * (planet_albedo - daisy_albedo) + planet_temp ** 4) ** 0.25


@track_plot("white_area", "white")
@track_plot("black_area", "black")
@track_plot("empty_area", "gray")
@track_plot("ave_temp", "red")
class Daisyworld(Model):
    """
    Daisyworld model — Gaia hypothesis demonstration.

    Two species of daisies (white and black) regulate planetary
    temperature through albedo feedback. White daisies cool the
    planet; black daisies warm it. Their relative abundance shifts
    with solar luminosity, buffering the planet temperature over a
    wide luminosity range.

    Based on: Watson & Lovelock (1983) and Wood et al. (2008).

    Parameters
    ----------
    sun_luminosity : float, optional
        Fractional solar luminosity relative to the Watson & Lovelock
        baseline. Values in (0.70, 1.60) support life. By default 0.70.
    planet_area : float, optional
        Total normalised planetary area. The sum of ``white_area``,
        ``black_area``, and ``empty_area`` must equal this value.
        By default 1.0.
    white_area : float, optional
        Initial fractional area covered by white daisies, by default 0.40.
    black_area : float, optional
        Initial fractional area covered by black daisies, by default 0.273.
    empty_area : float, optional
        Initial bare-soil fractional area, by default 0.327.
    white_albedo : float, optional
        Reflectivity of white daisies, by default 0.75.
    black_albedo : float, optional
        Reflectivity of black daisies, by default 0.25.
    soil_albedo : float, optional
        Reflectivity of bare soil, by default 0.50.
    decay_rate : float, optional
        Per-step mortality rate for both daisy species, by default 0.3.

    Notes
    -----
    The ``@track_plot`` decorators register ``white_area``,
    ``black_area``, ``empty_area``, and ``ave_temp`` for automatic
    live plotting.

    Examples
    --------
    >>> from dissmodel.core import Environment
    >>> env = Environment(end_time=100)
    >>> model = Daisyworld(sun_luminosity=1.0)
    >>> env.run()
    """

    #: Fractional area covered by white daisies.
    white_area: float

    #: Fractional area covered by black daisies.
    black_area: float

    #: Bare-soil fractional area.
    empty_area: float

    #: Current average planet temperature (K).
    ave_temp: float

    #: Solar luminosity (fractional).
    sun_luminosity: float

    #: Total planet area.
    planet_area: float

    #: White daisy albedo.
    white_albedo: float

    #: Black daisy albedo.
    black_albedo: float

    #: Bare-soil albedo.
    soil_albedo: float

    #: Per-step daisy mortality rate.
    decay_rate: float

    def setup(
        self,
        sun_luminosity: float = 0.70,
        planet_area: float = 1.0,
        white_area: float = 0.40,
        black_area: float = 0.273,
        empty_area: float = 0.327,
        white_albedo: float = 0.75,
        black_albedo: float = 0.25,
        soil_albedo: float = 0.50,
        decay_rate: float = 0.30,
    ) -> None:
        self.sun_luminosity = sun_luminosity
        self.planet_area    = planet_area
        self.white_area     = white_area
        self.black_area     = black_area
        self.empty_area     = empty_area
        self.white_albedo   = white_albedo
        self.black_albedo   = black_albedo
        self.soil_albedo    = soil_albedo
        self.decay_rate     = decay_rate
        self.ave_temp       = _planet_temp(self.sun_luminosity, self._planet_albedo())

    def _planet_albedo(self) -> float:
        return (
            self.white_area * self.white_albedo
            + self.black_area * self.black_albedo
            + self.empty_area * self.soil_albedo
        )

    def execute(self) -> None:
        pa = self._planet_albedo()
        self.ave_temp = _planet_temp(self.sun_luminosity, pa)

        temp_white     = _local_temp(self.ave_temp, pa, self.white_albedo)
        white_growth   = _daisy_growth_rate(temp_white) * self.empty_area
        self.white_area += self.white_area * (white_growth - self.decay_rate)

        temp_black     = _local_temp(self.ave_temp, pa, self.black_albedo)
        black_growth   = _daisy_growth_rate(temp_black) * self.empty_area
        self.black_area += self.black_area * (black_growth - self.decay_rate)

        self.empty_area = self.planet_area - (self.white_area + self.black_area)


__all__ = ["Daisyworld"]
