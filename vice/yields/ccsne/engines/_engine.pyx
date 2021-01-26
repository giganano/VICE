# cython: language_level = 3, boundscheck = False 
r""" 
This file implements the explodability engine base class 
""" 

from __future__ import absolute_import 
from .read_engine import read 
import numbers 
from libc.stdlib cimport malloc, free 
from . cimport _engine 


cdef class engine: 

	r""" 
	Explodability as a function of mass. 

	Parameters 
	----------
	filename : str 
		The path to the file to read the explodability table from. 

	This class can be indexed or called with a stellar mass in :math:`M_\odot` 
	and it will interpolate between grid elements to estimate the fraction of 
	stars of that mass which explode as a core collapse supernova. 
	""" 

	# no __cinit__ because this will be subclassed in pure python with a 
	# different call signature -> __cinit__ causes an error to be raised. 

	def __init__(self, filename): 
		# read in the file and copy it into C double pointers 
		masses, freq = read(filename) 
		assert len(masses) == len(freq), "Internal Error" 
		self._n_masses = <unsigned long> len(masses) 
		self._masses = <double *> malloc (self._n_masses * sizeof(double)) 
		self._frequencies = <double *> malloc (self._n_masses * sizeof(double)) 
		for i in range(self._n_masses): 
			self._masses[i] = masses[i] 
			self._frequencies[i] = freq[i] 

	def __dealloc__(self): 
		free(self._masses) 
		free(self._frequencies) 
		self._n_masses = 0l 

	def __call__(self, mass): 
		# Simple interpolation scheme with bin number finder  
		if isinstance(mass, numbers.Number): 
			if mass < _engine.CC_MIN_STELLAR_MASS: return 0. 
			bin_ = _engine.get_bin_number(self._masses, self._n_masses, 
				<double> mass) 
			if bin_ == -1: 
				if mass < self._masses[0]: 
					bin_ = 0 
				elif mass > self._masses[self._n_masses - 1l]: 
					bin_ = self._n_masses - 2l 
				else: 
					raise SystemError("Internal Error") 
			else: 
				pass 
			# be careful not to return a value <0 or >1.  
			result = _engine.interpolate(
				self._masses[bin_], 
				self._masses[bin_ + 1l], 
				self._frequencies[bin_], 
				self._frequencies[bin_ + 1l], 
				<double> mass
			) 
			if result < 0: 
				return 0. 
			elif result > 1: 
				return 1. 
			else: 
				return result 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(mass))) 

	def __getitem__(self, mass): 
		# Allow indexing with the same functionality as calling 
		return self.__call__(mass) 

	@property 
	def masses(self): 
		r""" 
		Type : list 

		The stellar  masses in :math:`M_\odot` on which the explosion engine 
		is sampled. 
		""" 
		return [float(self._masses[i]) for i in range(self._n_masses)] 

	@property 
	def frequencies(self): 
		r""" 
		Type : list 

		The frequencies with which stars whose masses are given by the 
		attribute 'masses' explode as a core collapse supernova. 
		""" 
		return [float(self._frequencies[i]) for i in range(self._n_masses)] 

