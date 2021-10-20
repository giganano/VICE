"""
This file implements the mirror function, which takes in output objects or
relative paths to outputs and returns simulations with the same parameters
that ran them.
"""

from __future__ import absolute_import
from .._globals import VisibleDeprecationWarning
from .singlezone import singlezone
import warnings


def mirror(arg):
	r"""
	**[DEPRECATED]**

	Obtain an instance of either vice.singlezone or vice.multizone class
	given only an instance of the vice.output class or the path to the output.
	The returned object will have the same parameters as that which produced
	the output, allowing re-simulation with whatever modifications the user
	desires.

	**Signature**: vice.mirror(arg)

	.. deprecated:: 1.1.0
		Users should instead call vice.singlezone.from_output or
		vice.multizone.from_output to achieve this functionality.

	Parameters
	----------
	arg : ``str`` or ``output``
		Either the path to the output (type ``str``) or the output object
		itself.

	Returns
	-------
	obj : ``singlezone`` or ``multizone``
		If arg is of type ``output``, then the ``singlezone`` object which
		produced the output is returned. If arg is of type ``str``, then obj
		is either of type vice.singlezone or vice.multizone, depending on
		which type of simulation produced the output. If arg is of type
		``multioutput``, then the corresponding ``multizone`` object is
		returned.

	Raises
	------
	* ImportError
		- 	The output has encoded functional attributes and the user does not
			have dill_ installed.
	* UserWarning
		- 	The output was produced with functional attributes, but was ran on
			a system without dill_, and they have thus been lost.

	.. note:: Saving and reinstancing functional simulation parameters from
		VICE outputs requires dill_, an extenstion to ``pickle`` in the
		python standard library. It is recommended that VICE users install
		dill_ >= 0.2.0.

	.. _dill: https://pypi.org/dill/

	Example Code
	------------
	>>> out = vice.output("example")
	>>> new = vice.mirror(out)
	>>> new
	vice.singlezone{
		name -----------> onezonemodel
		func -----------> <function _DEFAULT_FUNC_ at 0x1085a6ae8>
		mode -----------> ifr
		verbose --------> False
		elements -------> ('fe', 'sr', 'o')
		IMF ------------> kroupa
		eta ------------> 2.5
		enhancement ----> 1.0
		Zin ------------> 0.0
		recycling ------> continuous
		delay ----------> 0.15
		RIa ------------> plaw
		Mg0 ------------> 6000000000.0
		smoothing ------> 0.0
		tau_ia ---------> 1.5
		tau_star -------> 2.0
		schmidt --------> False
		schmidt_index --> 0.5
		MgSchmidt ------> 6000000000.0
		dt -------------> 0.01
		m_upper --------> 100.0
		m_lower --------> 0.08
		Z_solar --------> 0.014
		bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
	}
	>>> import numpy as np
	>>> new.run(np.linspace(0, 10, 1001))
	"""
	warnings.warn("""\
The vice.mirror function is deprecated in versions >= 1.1.0 and will be \
removed in a future relase of VICE. Users should instead call \
vice.singlezone.from_output to achieve the same functionality.""",
		VisibleDeprecationWarning)
	return singlezone.singlezone.from_output(arg)

