
from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from ._output import c_output
from . import _output_utils
import zipfile
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

class output:

	r"""
	Reads in the output from singlezone simulations and allows the
	user to access it easily via dataframes.

	**Signature**: vice.output(name)

	Parameters
	----------
	name : ``str``
		The full or relative path to the output directory. The '.vice'
		extension is not required.

	.. note:: If ``name`` corresponds to output from the ``multizone`` class,
		a ``multioutput`` object is created instead.

	Attributes
	----------
	name : ``str``
		The name of the .vice directory containing the simulation output.
	elements : ``tuple``
		The symbols of the elements whose enrichment was tracked by the
		simulation, as they appear on the periodic table.
	history : ``dataframe``
		The dataframe read in via vice.history.
	mdf : ``dataframe``
		The dataframe read in via vice.mdf.
	agb_yields : ``dataframe``
		The asymptotic giant branch star yields employed in the simulation.
	ccsne_yields : ``dataframe``
		The core-collapse supernova yields employed in the simulation.
	sneia_yields : ``dataframe``
		The type Ia supernova yields employed in the simulation.

	.. note:: Reinstancing functional yields and simulation parameters
		requires dill_, an extension to ``pickle`` in the python standard
		library. It is recommand that VICE users install dill_ >= 0.2.0.

		.. _dill: https://pypi.org/project/dill/

	.. tip:: VICE outputs are stored in directories with a '.vice' extension
		following the name of the simulation. This allows users to run
		<command> \*.vice in a terminal to run commands on all VICE outputs
		in a given directory.

	Functions
	---------
	- show (requires matplotlib_ >= 2.0.0)

	.. _matplotlib: https://matplotlib.org/

	.. seealso::
		- vice.history
		- vice.mdf
		- vice.multioutput

	Example Code
	------------
	>>> import vice
	>>> out = vice.output("example")
	>>> out.history[100]
		vice.dataframe{
			time -----------> 1.0
			mgas -----------> 5795119000.0
			mstar ----------> 2001106000.0
			sfr ------------> 2.897559
			ifr ------------> 9.1
			ofr ------------> 7.243899
			eta_0 ----------> 2.5
			r_eff ----------> 0.3534769
			z_in(fe) -------> 0.0
			z_in(sr) -------> 0.0
			z_in(o) --------> 0.0
			z_out(fe) ------> 0.0002769056
			z_out(sr) ------> 3.700754e-09
			z_out(o) -------> 0.001404602
			mass(fe) -------> 1604701.0
			mass(sr) -------> 21.44631
			mass(o) --------> 8139837.0
			z(fe) ----------> 0.0002769056166059748
			z(sr) ----------> 3.700754031107903e-09
			z(o) -----------> 0.0014046022178319376
			[fe/h] ---------> -0.6682579454664828
			[sr/h] ---------> -1.1074881208001155
			[o/h] ----------> -0.6098426789720387
			[sr/fe] --------> -0.43923017533363273
			[o/fe] ---------> 0.05841526649444406
			[o/sr] ---------> 0.4976454418280768
			z --------------> 0.0033582028978416337
			[m/h] ----------> -0.6200211036287412
			lookback -------> 9.0
		}
	>>> out.mdf[60]
		vice.dataframe{
			bin_edge_left --> 0.0
			bin_edge_right -> 0.05
			dn/d[fe/h] -----> 0.0
			dn/d[sr/h] -----> 0.0
			dn/d[o/h] ------> 0.0
			dn/d[sr/fe] ----> 0.06001488
			dn/d[o/fe] -----> 0.4337209
			dn/d[o/sr] -----> 0.0
		}
	"""

	def __new__(cls, name):
		name = _output_utils._get_name(name)
		if _output_utils._is_multizone(name):
			from .multioutput import multioutput
			return multioutput(name)
		else:
			return super(output, cls).__new__(cls)

	def __init__(self, name):
		self.__c_version = c_output(name)

	def __repr__(self):
		"""
		Prints the name of the simulation
		"""
		return "<VICE output from singlezone: %s>" % (self.name)

	def __str__(self):
		"""
		Returns self.__repr__()
		"""
		return self.__repr__()

	def __eq__(self, other):
		"""
		Returns True if the outputs came from the same directory
		"""
		if isinstance(other, output):
			return os.path.abspath(self.name) == os.path.abspath(other.name)
		else:
			return False

	def __ne__(self, other):
		"""
		Returns not self.__eq__(other)
		"""
		return not self.__eq__(other)

	def __enter__(self):
		"""
		Opens a with statement
		"""
		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		"""
		Raises all exceptions inside with statements
		"""
		return exc_value is None

	@property
	def name(self):
		r"""
		Type : ``str``

		The name of the simulation; this corresponds to the name of the '.vice'
		directory containing the output.

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.name
			'example'
		"""
		return self.__c_version.name

	@property
	def elements(self):
		r"""
		Type : ``tuple`` of strings

		The symbols of the elements whose enrichment was modeled to produce
		the output file, as they appear on the periodic table.

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.elements
			('fe', 'sr', 'o')
		"""
		return self.__c_version.elements

	@property
	def history(self):
		r"""
		Type : ``dataframe``

		The dataframe read in via vice.history with the same name as this
		output.

		.. seealso:: vice.history

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.history["time"][100]
			1.0
		>>> example.history
			vice.dataframe{
				time -----------> 1.0
				mgas -----------> 5795119000.0
				mstar ----------> 2001106000.0
				sfr ------------> 2.897559
				ifr ------------> 9.1
				ofr ------------> 7.243899
				eta_0 ----------> 2.5
				r_eff ----------> 0.3534769
				z_in(fe) -------> 0.0
				z_in(sr) -------> 0.0
				z_in(o) --------> 0.0
				z_out(fe) ------> 0.0002769056
				z_out(sr) ------> 3.700754e-09
				z_out(o) -------> 0.001404602
				mass(fe) -------> 1604701.0
				mass(sr) -------> 21.44631
				mass(o) --------> 8139837.0
				z(fe) ----------> 0.0002769056166059748
				z(sr) ----------> 3.700754031107903e-09
				z(o) -----------> 0.0014046022178319376
				[fe/h] ---------> -0.6682579454664828
				[sr/h] ---------> -1.1074881208001155
				[o/h] ----------> -0.6098426789720387
				[sr/fe] --------> -0.43923017533363273
				[o/fe] ---------> 0.05841526649444406
				[o/sr] ---------> 0.4976454418280768
				z --------------> 0.0033582028978416337
				[m/h] ----------> -0.6200211036287412
				lookback -------> 9.0
			}
		"""
		return self.__c_version.history

	@property
	def mdf(self):
		r"""
		Type : ``dataframe``

		The dataframe read in via vice.mdf with the same name as this output.

		.. seealso:: vice.mdf

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.mdf["bin_edge_left"][:10]
			[-3.0, -2.95, -2.9, -2.85, -2.8, -2.75, -2.7, -2.65, -2.6, -2.55]
		>>> example.mdf[60]
			vice.dataframe{
				bin_edge_left --> 0.0
				bin_edge_right -> 0.05
				dn/d[fe/h] -----> 0.0
				dn/d[sr/h] -----> 0.0
				dn/d[o/h] ------> 0.0
				dn/d[sr/fe] ----> 0.06001488
				dn/d[o/fe] -----> 0.4337209
				dn/d[o/sr] -----> 0.0
			}
		"""
		return self.__c_version.mdf

	@property
	def agb_yields(self):
		r"""
		Type : ``dataframe``

		The asymptotic giant branch star yields employed in the simulation.

		.. versionadded:: 1.2.0
			Prior to version 1.2.0, the ``singlezone`` object required an
			attribute ``agb_model``, denoting which table of yields to adopt.

		.. note:: This dataframe is not customizable.

		.. seealso:: vice.yields.agb.settings

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.agb_yields
			vice.dataframe{
				fe -------------> cristallo11
				o --------------> cristallo11
				sr -------------> cristallo11
			}
		"""
		return self.__c_version.agb_yields

	@property
	def ccsne_yields(self):
		r"""
		Type : ``dataframe``

		The core-collapse supernova yields employed in the simulation.

		.. note:: This dataframe is not customizable

		.. seealso:: vice.yields.ccsne.settings

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.ccsne_yields
			vice.dataframe{
				fe -------------> 0.000246
				o --------------> 0.00564
				sr -------------> 1.34e-08
			}
		"""
		return self.__c_version.ccsne_yields

	@property
	def sneia_yields(self):
		r"""
		Type : ``dataframe``

		The type Ia supernova yields employed in the simulation.

		.. note:: This dataframe is not customizable.

		.. seealso:: vice.yields.sneia.settings

		Example Code
		------------
		>>> import vice
		>>> example = vice.output("example")
		>>> example.sneia_yields
			vice.dataframe{
				fe -------------> 0.00258
				o --------------> 5.79e-05
				sr -------------> 0
			}
		"""
		return self.__c_version.sneia_yields

	def show(self, key, xlim = None, ylim = None):
		r"""
		Show a plot of the given quantity referenced by a keyword argument.

		**Signature**: x.show(key, xlim = None, ylim = None)

		Parameters
		----------
		x : ``output``
			An instance of this class.
		key : ``str`` [case-insensitive]
			The keyword argument. If this is a quantity stored in the history
			attribute, it will be plotted against time by defult. Conversely,
			if it is stored in the mdf attribute, the corresponding stellar
			metallicity distribution function will be plotted.

			Users can also specify an argument of the format "key1-key2"
			where key1 and key2 are elements of the history output. This will
			then plot key1 against key2.
		xlim : array-like (contains real numbers) [default : None]
			The x-limits to impose on the shown plot, if any.
		ylim : array-like (contains real numbers) [default : None]
			The y-limits to impose on the shown plot, if any.

		Raises
		------
		* KeyError
			-	Key is not found in either history or mdf attributes
		* ModuleNotFoundError
			- 	Matplotlib version >= 2.0.x is not found in the user's system.

				.. note:: In python 3.5.x, this will be an ``ImportError``.

		Other errors may be raised by matplotlib.pyplot.show.

		Notes
		-----
		This function is **NOT** intended to generate publication quality
		plots for users. It is included purely as a convenience function to
		allow "quick and dirty" data visualization and inspection of simulation
		outputs immediately with only one line of code.

		Example Code
		------------
		>>> import vice
		>>> out = vice.output("example")
		>>> out.show("dn/d[o/fe]")
		>>> out.show("sfr")
		>>> out.show("[o/fe]-[fe/h]")
		"""
		self.__c_version.show(key, xlim = xlim, ylim = ylim)


	@staticmethod
	def zip(name):
		r"""
		Compress a VICE output into a zipfile.

		**Signature**: vice.output.zip(name)

		.. versionadded:: 1.1.0

		Parameters
		----------
		name : ``str`` or output
			The full or relative path to an output, or the output object
			itself. The '.vice' extension is not required.

		Raises
		------
		* IOError
			- Output is not found
			- Directory could not be interpreted as a VICE output.

		Example Code
		------------
		>>> import numpy as np
		>>> import vice
		>>> vice.singlezone(name = "example").run(np.linspace(0, 10, 1001))
		>>> vice.output.zip("example")
		"""
		if isinstance(name, output):
			output.zip(name.name)
		elif isinstance(name, strcomp):
			name = _output_utils._get_name(name)
			if os.path.exists(name):
				try:
					test = output(name)
				except:
					raise IOError("Could not read VICE output: %s" % (name))
				zipf = zipfile.ZipFile("%s.zip" % (name), 'w',
					zipfile.ZIP_DEFLATED)
				for root, dirs, files in os.walk(name):
					for file in files:
						zipf.write(os.path.join(root, file))
				zipf.close()
			else:
				raise IOError("Output not found: %s" % (name))
		else:
			raise TypeError("Must be of type str. Got: %s" % (type(name)))


	@staticmethod
	def unzip(name):
		r"""
		Decompress a VICE output from a zipfile.

		**Signature**: vice.output.unzip(name)

		.. versionadded:: 1.1.0

		Parameters
		----------
		name : ``str``
			The full or relative path to a compressed VICE output file.
			The '.vice.zip' extension is not required.

		Raises
		------
		* IOError
			- Zipped file is not found.

		Example Code
		------------
		>>> import vice
		>>> vice.output.unzip("example.vice.zip")
		>>> out = vice.output("example")
		"""
		if isinstance(name, strcomp):
			if not name.endswith(".vice.zip"): name += ".vice.zip"
			if os.path.exists(name):
				with zipfile.ZipFile(name, 'r') as zipf:
					zipf.extractall('.')
			else:
				raise IOError("Zipped file not found: %s" % (name))
		else:
			raise TypeError("Must be of type str. Got: %s" % (type(name)))

