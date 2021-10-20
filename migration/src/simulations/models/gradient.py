r"""
This file declares the radial dependence of the stellar surface density at
late times in the Johnson et al. (2021) models.
"""

import math as m

_THIN_DISK_SCALE_RADIUS_ = 2.5 # kpc
_THICK_DISK_SCALE_RADIUS_ = 2.0 # kpc
_THICK_TO_THIN_RATIO_ = 0.27 # at r = 0


def gradient(radius):
	r"""
	The gradient in stellar surface density defined in Bland-Hawthorn &
	Gerhard (2016) [1]_.

	Parameters
	----------
	radius : real number
		Galactocentric radius in kpc.

	Returns
	-------
	sigma : real number
		The radial surface density at that radius defined by the following
		double-exponential profile:

		.. math:: \Sigma_\star(r) = e^{-r/r_t} + Ae^{-r/r_T}

		where :math:`r_t` = 2.5 kpc is the scale radius of the thin disk,
		:math:`r_T` = 2.0 kpc is the scale radius of the thick disk, and
		:math:`A = \Sigma_T / \Sigma_t \approx` 0.27 is the ratio of thick to
		thin disks at :math:`r = 0`.

		.. note:: This gradient is un-normalized.

	.. [1] Bland-Hawthorn & Gerhard (2016), ARA&A, 54, 529
	"""
	return (
		m.exp(-radius / _THIN_DISK_SCALE_RADIUS_) +
		_THICK_TO_THIN_RATIO_ * m.exp(-radius / _THICK_DISK_SCALE_RADIUS_)
	)

