r"""
This file implements the normalization calculation in Appendix A of
Johnson et al. (2021).
"""

from ..._globals import MAX_SF_RADIUS, END_TIME, M_STAR_MW
import math as m


def normalize(time_dependence, radial_gradient, radius, dt = 0.01, dr = 0.5,
	recycling = 0.4):
	r"""
	Determine the prefactor on the surface density of star formation as a
	function of time as described in Appendix A of Johnson et al. (2021).

	Parameters
	----------
	time_dependence : <function>
		A function accepting time in Gyr and galactocentric radius in kpc, in
		that order, specifying the time-dependence of the star formation
		history at that radius. Return value assumed to be unitless and
		unnormalized.
	radial_gradient : <function>
		A function accepting galactocentric radius in kpc specifying the
		desired stellar radial surface density gradient at the present day.
		Return value assumed to be unitless and unnormalized.
	radius : real number
		The galactocentric radius to evaluate the normalization at.
	dt : real number [default : 0.01]
		The timestep size in Gyr.
	dr : real number [default : 0.5]
		The width of each annulus in kpc.
	recycling : real number [default : 0.4]
		The instantaneous recycling mass fraction for a single stellar
		population. Default is calculated for the Kroupa IMF [1]_.

	Returns
	-------
	A : real number
		The prefactor on the surface density of star formation at that radius
		such that when used in simulation, the correct total stellar mass with
		the specified radial gradient is produced.

	Notes
	-----
	This function automatically adopts the desired maximum radius of star
	formation, end time of the model, and total stellar mass declared in
	``src/_globals.py``.

	.. [1] Kroupa (2001), MNRAS, 322, 231
	"""

	time_integral = 0
	for i in range(int(END_TIME / dt)):
		time_integral += time_dependence(i * dt) * dt * 1.e9 # yr to Gyr

	radial_integral = 0
	for i in range(int(MAX_SF_RADIUS / dr)):
		radial_integral += radial_gradient(dr * (i + 0.5)) * m.pi * (
			(dr * (i + 1))**2 - (dr * i)**2
		)

	return M_STAR_MW / ((1 - recycling) * radial_integral * time_integral)

