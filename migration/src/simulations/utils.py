
import math as m 
import numbers 


class exponential: 

	def __init__(self, norm = 1, timescale = 1): 
		self.norm = norm 
		self.timescale = timescale 

	def __call__(self, time): 
		return self.norm * m.exp(-time / self.timescale) 

	@property 
	def norm(self): 
		r""" 
		Type : real number 

		The normalization of the exponential. 
		""" 
		return self._norm 

	@norm.setter 
	def norm(self, value): 
		if isinstance(value, numbers.Number): 
			self._norm = float(value) 
		else: 
			raise TypeError("Normalization must be a real number. Got: %s" % (
				type(value))) 

	@property 
	def timescale(self): 
		r""" 
		Type : real number 

		The e-folding timescale of the exponential. If positive, this object 
		describes exponential decay. If negative, it describes exponential 
		growth. 
		""" 
		return self._timescale 

	@timescale.setter 
	def timescale(self, value): 
		if isinstance(value, numbers.Number): 
			if value: 
				self._timescale = value 
			else: 
				raise ValueError("Timescale must be nonzero.") 
		else: 
			raise TypeError("Timescale must be a real number. Got: %s" % (
				type(value))) 

class linear_exponential(exponential): 

	def __call__(self, time): 
		return time * super().__call__(time) 

