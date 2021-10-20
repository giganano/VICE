# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = ["ccsn_yield_table"]
import numbers
from . cimport _ccsn_yield_table
from ._base cimport base


cdef class ccsn_yield_table(base):

	r"""
	The VICE dataframe: derived class (inherits from base)

	Stores the data from a core collapse supernova (CCSN) mass yield table
	published in a nucleosynthesis study.

	.. note:: This dataframe is not customizable. Its values cannot be altered.

	Attributes
	----------
	masses : ``tuple``
		The initial CCSN progenitor masses in :math:`M_\odot`.
	isotopes : ``tuple``
		The stable isotopes of the element with reported yields in
		:math:`M_\odot`. ``None`` if created with a call to
		vice.yields.ccsne.table with the keyword argument ``isotopic = False``.

	Indexing
	--------
	- real number : progenitor stellar mass
		The initial mass of the CCSN progenitor in :math:`M_\odot`.

	- ``str`` : isotope
		The isotope of the element. Only allowed when the dataframe is
		initialized with the keyword argument ``isotopic = True``.

	Functions
	---------
	- keys
	- todict

	Example Code
	------------
	>>> import vice
	>>> example = vice.yields.ccsne.table('o')
	>>> example
		vice.dataframe{
			13.0 -----------> 0.247071034
			15.0 -----------> 0.585730308
			20.0 -----------> 1.256452301
			25.0 -----------> 2.4764558329999997
			30.0 -----------> 0.073968147
			40.0 -----------> 0.087475695
			60.0 -----------> 0.149385561
			80.0 -----------> 0.24224373600000002
			120.0 ----------> 0.368598602
		}
	>>> example = vice.yields.ccsne.table('c', isotopic = True)
	>>> example
		vice.dataframe{
			13 -------------> {'c12': 0.11404, 'c13': 0.0006918}
			15 -------------> {'c12': 0.22096, 'c13': 0.00077869}
			20 -------------> {'c12': 0.40941, 'c13': 0.0010411}
			25 -------------> {'c12': 0.61944, 'c13': 0.0012839}
			30 -------------> {'c12': 0.025054, 'c13': 0.0014423}
			40 -------------> {'c12': 0.031933, 'c13': 0.0018031}
			60 -------------> {'c12': 0.39826, 'c13': 0.0017254}
			80 -------------> {'c12': 1.1226, 'c13': 0.0017021}
			120 ------------> {'c12': 2.0178, 'c13': 0.0023899}
		}

	**Signature**: vice.core.dataframe.ccsn_yield_table(masses, yields,
	isotopes = None)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe. To obtain instances of this class, use the
		lookup function vice.yields.ccsne.table.

	Parameters
	----------
	masses : ``tuple``
		The progenitor masses on which the grid is sampled in :math:`M_\odot`.
	yields : ``tuple``
		The yields at each mass. A 2-D ``tuple`` is interpreted as an isotopic
		breakdown.
	isotopes : ``tuple`` [default : ``None``]
		The isotopes of the element. ``None`` if created with a call to
		vice.yields.ccsne.table with the keyword argument ``isotopic = False``.
	"""

	def __init__(self, masses, yields, isotopes = None):
		# Store the masses, yields and isotopes as attributes
		super().__init__({})
		if all(map(lambda x: isinstance(x, numbers.Number), masses)):
			self._masses = tuple(masses[:])
		else:
			raise SystemError("Internal Error 1")
		if isotopes is not None:
			self._isotopes = tuple(isotopes[:])
			if all(map(lambda x: isinstance(x, tuple), yields)):
				for i in yields:
					if not all(map(lambda x: isinstance(x, numbers.Number),
						i)):
						raise SystemError("Internal Error 2")
					else:
						continue
				self._yields = tuple(yields[:])
			else:
				raise SystemError("Internal Error 3")
		else:
			if all(map(lambda x: isinstance(x, numbers.Number), yields)):
				self._yields = tuple(yields[:])
			else:
				raise SystemError("Internal Error 4")


	def __repr__(self):
		rep = "vice.dataframe{\n"
		if self._isotopes is not None:
			for i in range(len(self._masses)):
				rep += "    %g " % (self._masses[i])
				for j in range(15 - len("%g" % (self._masses[i]))):
					rep += "-"
				rep += "> %s\n" % (str(dict(zip(
					self._isotopes,
					[j[i] for j in self._yields]
				))))
		else:
			for i in self._masses:
				rep += "    %s " % (str(i))
				for j in range(15 - len(str(i))):
					rep += "-"
				rep += "> %s\n" % (str(self.__getitem__(i)))
		rep += "}"
		return rep


	def __subget__str(self, key):
		"""
		Override the base __getitem__ functionality for isotope lookup
		"""
		if self._isotopes is not None:
			if key.lower() in self._isotopes:
				yields = self._yields[self._isotopes.index(key.lower())]
				return ccsn_yield_table(self._masses, yields, isotopes = None)
			else:
				raise IndexError("Unrecognized isotope: %s" % (key))
		else:
			raise TypeError("This yields dataframe is not isotopic.")


	def __subget__number(self, key):
		"""
		Override the base __getitem__ functionality for stellar mass lookup
		"""
		if key in self._masses:
			if self._isotopes is not None:
				idx = self._masses.index(key)
				yields = [i[idx] for i in self._yields]
				return base(dict(zip(self._isotopes, yields)))
			else:
				return self._yields[self._masses.index(key)]
		else:
			raise IndexError("Mass not on grid: %g" % (key))

	def __setitem__(self, key, value):
		raise TypeError("This dataframe is not customizable")


	@property
	def masses(self):
		r"""
		Type : ``tuple``

		The initial masses of CCSN progenitors in :math:`M_\odot` reported by
		the nucleosynthesis study.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.ccsne.table("o")
		>>> example.masses
			(13.0, 15.0, 20.0, 25.0, 30.0, 40.0, 60.0, 80.0, 120.0)
		"""
		return self._masses


	@property
	def isotopes(self):
		r"""
		Type : ``tuple``

		The stable isotopes whose yields are reported by the nucleosynthesis
		study. If this table was generated with a call to
		vice.yields.ccsne.table with the keyword argument ``isotopic = False``,
		this attribute will be ``None``.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.ccsne.table("c", isotopic = True)
		>>> example.isotopes
			('c12', 'c13')
		"""
		return self._isotopes


	def keys(self):
		r"""
		Returns the keys to the dataframe in their lower-case format

		**Signature**: x.keys()

		Parameters
		----------
		x : ``dataframe``
			An instance of this class

		Returns
		-------
		keys : ``list``
			A list of lower-case strings which can be used to access the
			values stored in this dataframe.

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.keys()
		['a', 'b', 'c']
		"""
		if self._isotopes is not None:
			return list(self._isotopes)
		else:
			return list(self._masses)


	def todict(self):
		r"""
		Returns the dataframe as a standard python dictionary

		**Signature**: x.todict()

		Parameters
		----------
		x : ``dataframe``
			An instance of this class

		Returns
		-------
		copy : ``dict``
			A dictionary copy of the dataframe.

		.. note:: Python dictionaries are case-sensitive, and are thus less
			flexible than this class.

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.todict()
		{'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
		"""
		if self._isotopes is not None:
			return dict(zip(
				self.keys(),
				[self.__getitem__(i).todict() for i in self.keys()]
			))
		else:
			return dict(zip(
				self.keys(),
				[self.__getitem__(i) for i in self.keys()]
			))

