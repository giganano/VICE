r"""
Built-in stellar radial migration schema for disk galaxies inspired by
hydrodynamical simulations.

.. versionadded:: 1.2.0

Contents
--------
hydrodiskstars : ``object``
	A stellar migration scheme informed by the ``h277`` simulation, a zoom-in
	hydrodynamic simulation of a Milky Way like galaxy ran from cosmological
	initial conditions (a part of the ``g14`` simulation suite, Christensen et
	al 2012 [1]_). Stellar migrations can migrate according to a handful of
	assumptions about the time dependence of their orbital radius between
	birth and the end of the simulation. For discussion, see section 2 of
	Johnson et al. (2021) [2]_.
data : ``module``
	Manages VICE's supplementary data containing the ``h277`` star particle
	subsamples. Executes a download upon first creation of a ``hydrodiskstars``
	object.

.. [1] Christensen et al. (2012), MNRAS, 425, 3058
.. [2] Johnson et al. (2021), arxiv:2103.09838
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["data", "hydrodiskstars", "test"]
	from .hydrodiskstars import hydrodiskstars
	from . import data
	from .tests import test

else:
	pass

