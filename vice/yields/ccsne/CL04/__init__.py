r"""
Chieffi & Limongi (2014), ApJ, 608, 405 core collapse supernova (CCSN) yields

**Signature**: from vice.yields.ccsne import CL04

Importing this module will automatically set the CCSN yield settings for all
elements to the IMF-averaged yields calculated with the Chieffi & Limongi
(2004) yield table for [M/H] = 0.15 stars. This will adopt an upper mass limit
of 35 :math:`M_\odot`.

We provide core collapse supernova yields for non-rotating progenitors as
reported by Chieffi & Limongi (2004) at metallicities relative to solar of
:math:`\log_{10}(Z / Z_\odot)` =

	- -inf
	- -4
	- -2
	- -1
	- -0.37
	- 0.15

assuming :math:`Z_\odot` = 0.014 according to Asplund et al. (2009) [1]_.

.. tip:: By importing this module, the user does not sacrifice the ability to
	specify their yield settings directly.

.. note:: This module is not imported with a simple ``import vice`` statement.

.. note:: When this module is imported, the yields will be updated with a
	maximum of 10^5 bins in quadrature to decrease computational overhead. For
	some elements, the yield calculation may not converge. To rerun the yield
	calculation with higher numerical precision, simply call ``set_params``
	with a new value for the keyword ``Nmax`` (see below).

Contents
--------
set_params : <function>
	Update the parameters with which the yields are calculated.

.. [1] Asplund et al. (2009), ARA&A, 47, 481
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False
try:
	__VICE_DOCS__
except NameError:
	__VICE_DOCS__ = False

if not __VICE_SETUP__:

	__all__ = ["set_params", "test"]
	from ...._globals import _RECOGNIZED_ELEMENTS_
	from .. import fractional as __fractional
	from .. import settings as __settings
	from .tests import test

	def set_params(**kwargs):
		r"""
		Update the parameter with which the yields are calculated from the
		Chieffi & limongi (2004) [1]_ data.

		**Signature**: vice.yields.ccsne.CL04.set_params(\*\*kwargs)

		Parameters
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.ccsne.fractional.

		Raises
		------
		* TypeError
			 - 	Received a keyword argument "study". This will always be "CL04"
				when called from this module.

		Other exceptions are raised by vice.yields.ccsne.fractional.

		Notes
		-----
		We provide core collapse supernova yields for non-rotating progenitors
		as reported by Chieffi & Limongi (2004) at metallicities relative to
		solar of :math:`\log_{10}(Z / Z_\odot)` =

			- -inf
			- -4
			- -2
			- -1
			- -0.37
			- 0.15

		assuming :math:`Z_\odot` = 0.014 according to Asplund et al.
		(2009) [2]_.

		Example Code
		------------
		>>> import vice
		>>> from vice.yields.ccsne import CL04
		>>> # negative yields simply imply a net loss
		>>> vice.yields.ccsne.settings['o']
		-0.07258767478609592
		>>> CL04.set_params(MoverH = -4)
		>>> vice.yields.ccsne.settings['o']
		0.01835902419240956
		>>> CL04.set_params(IMF = "salpeter")
		>>> vice.yields.ccsne.settings['o']
		-0.056090913652505486
		>>> CL04.set_params(IMF = "salpeter", m_upper = 60)
		>>> vice.yields.ccsne.settings['o']
		-0.0512909951164916
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> from vice.yields.ccsne.engines import E16
		>>> # Sukhbold et al. (2016) W18 black hole landscape with CL04 yields
		... CL04.set_params(explodability = W18)
		>>> vice.yields.ccsne.settings['o']
		-0.049690600129938464
		>>> # Ertl et al. (2016) black hole landscape with CL04 yields
		... CL04.set_params(explodability = E16, MoverH = -4)
		>>> vice.yields.ccsne.settings['o']
		0.001936110535019444

		.. seealso:: 
			- vice.yields.ccsne.fractional
			- vice.yields.ccsne.table

		.. [1] Chieffi & Limongi (2004), ApJ, 608, 405
		.. [2] Asplund et al. (2009), ARA&A, 47, 481
		"""
		if "study" in kwargs.keys():
			raise TypeError("Got an unexpected keyword argument: 'study'")
		else:
			if "MoverH" not in kwargs.keys():
				# fractional will default to 0, override this
				kwargs["MoverH"] = 0.15
			else:
				pass
			for i in _RECOGNIZED_ELEMENTS_:
				__settings[i] = __fractional(i, study = "CL04", **kwargs)[0]

	if not __VICE_DOCS__: set_params(MoverH = 0.15, m_upper = 35, Nmax = 1e5)

else:
	pass

