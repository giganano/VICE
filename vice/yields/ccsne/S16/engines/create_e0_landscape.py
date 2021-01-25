r"""
Constructs an explodability landscape using the mu4 and M4 pre-SN values
from S16 with the formalism from Griffith et al. (2021)
"""
import scipy.interpolate 
import numpy as np


def e0_landscape(e0, M):
	r"""
	Reads in the pre-SN stellar values and returns the explodability landscape 
	assiciated the the specified e0.

	Parameters
	----------
	e0 : float
		The value of e0 to set the threshold of explodability
	M : float
		The ZAMS stellar mass whose explodability you want to evaluate


	Returns
	-------
	Explodability : float
		A value of 0 if the specified stellar mass explodes
		A value of 1 if the specified stellar mass collapses to a BH

	Raises
	------
	- error if e0 is not a float?
	"""


	data = np.genfromtxt('pre_sn.dat', 
						skip_header=1, names=True)
	M_ZAMS = data['M_ZAMSM_sun']
	M4s = data['M_s4M_sun']
	mu4s = data['mu_4']

	interp_mu4 = scipy.interpolate.interp1d(M_ZAMS, mu4s)
	interp_M4 = scipy.interpolate.interp1d(M_ZAMS, M4s)

	mu4 = interp_mu4(M)
	M4 = interp_M4(M)

	e = 0.28*M4*mu4 - mu4 + e0

	if e<=0: return 0
	elif e>0: return 1



