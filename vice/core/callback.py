""" 
This file implements the python side of the callback object - this includes 
raising warnings letting the user know when errors have been suppressed in 
running their simulations. 
""" 

from __future__ import absolute_import 
from .._globals import ScienceWarning 
from . import _pyutils 
import functools 
import math as m 
import warnings 
import numbers 


""" 
Notes 
===== 
The callback1 and callback2 are object are implemented separately from one 
another. This is motivated by the fact that there is a C library expecting a 
very specific number of functions for each attribute. To mirror this level 
of strictness, the number of arguments the callback1 and callback2 objects 
accept is defined explicitly. This has the positive side effect of user's 
being notified via a TypeError that their functions do not accept the correct 
number of arguments prior to simulation as opposed to seeing a long string of 
suppression messages. 
""" 


def numerical(function): 
	""" 
	A decorator which wraps the __call__ function of the callback objects and 
	all subclasses to suppress TypeErrors by not allowing non-numerical values 
	to be returned. 
	""" 
	@functools.wraps(function) 
	def wrapper(*args): 
		y = function(*args) 
		if isinstance(y, numbers.Number): 
			return float(y) 
		else: 
			warnings.warn("""\
Function %s evaluated to non-numerical value at %s. Suppressing TypeError by \
returning 0. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(args[1:])), ScienceWarning) 
			return 0 
	return wrapper 


def no_nan(function): 
	""" 
	A decorator which wrapps the __call__ function of the callback objecs to 
	suppress ArithmeticErrors by not allowing NaN from user functions. 
	""" 
	@functools.wraps(function) 
	def wrapper(*args): 
		y = function(*args) 
		if m.isnan(y): 
			warnings.warn("""\
Function %s evaluated to NaN at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(args[:1])), ScienceWarning) 
			return 0 
		else: 
			return y 
	return wrapper 


def no_inf(function): 
	""" 
	A decorator which wraps the __call__ function of the callback objects to 
	suppress ArithmeticErrors by not allowing inf to be returned from user 
	functions. 
	""" 
	@functools.wraps(function) 
	def wrapper(*args): 
		y = function(*args) 
		if m.isinf(y): 
			warnings.warn("""\
Function %s evaluated to inf at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(args[1:])), ScienceWarning) 
			return 0 
		else: 
			return y 
	return wrapper 


def positive(function): 
	""" 
	A decorator which wraps the __call__ function of the callback objects to 
	suppress ArithmeticErrors by not allowing non-positive numbers to be 
	returned from user functions. 
	""" 
	@functools.wraps(function) 
	def wrapper(*args): 
		y = function(*args) 
		if y <= 0: 
			warnings.warn("""\
Function %s evaluated to non-positive value at %s. Suppressing ArithmeticError \
by returning 1e-12. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(x)), ScienceWarning) 
			return 1e-12 
		else: 
			return y 
	return wrapper 


class callback1: 

	""" 
	The callback object for python functions being called from C accepting one 
	numerical positional parameter. These functions are wrapped in a number 
	type and value checking decorators to ensure the simulation runs 
	smoothly. 
	""" 

	def __init__(self, function): 
		self.function = function 

	@numerical 
	def __call__(self, x): 
		return self._function(x) 

	@property 
	def function(self): 
		""" 
		Type :: <function> 

		The function to call, passed from the user. 
		""" 
		return self._function 

	@function.setter 
	def function(self, value): 
		if callable(value): 
			if _pyutils.arg_count(value) == 1: 
				self._function = value 
			else: 
				raise TypeError("""Attribute 'function' must accept exactly \
one positional argument.""") 
		else: 
			raise TypeError("""Attribute 'function' must be a callable \
object. Got: %s""" % (type(value))) 


class callback1_nan(callback1): 

	""" 
	The callback object for python functions being called from C accepting one 
	numerical positional parameter, and suppressing ArithmeticErrors from 
	NaNs. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@no_nan 
	@numerical 
	def __call__(self, x): 
		return self._function(x) 


class callback1_nan_inf(callback1): 

	""" 
	The callback object for python functions being called from C accepting one 
	numerical positional parameter, and suppressing ArithmeticErrors from both 
	infs and NaNs. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@no_inf 
	@no_nan 
	@numerical 
	def __call__(self, x): 
		return self._function(x) 


class callback1_nan_positive(callback1): 

	""" 
	The callback object for python functions being called from C accepting one 
	numerical positional parameter, and suppressing ArithmeticErrors from both 
	of NaNs and non-positive values. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@positive 
	@no_nan 
	@numerical 
	def __call__(self, x): 
		return self._function(x) 


class callback1_nan_inf_positive(callback1): 

	""" 
	The callback object for python functions being called from C accepting one 
	numerical positional parameter, and suppressing ArithmeticErrors from all 
	of infs, NaNs, and non-positive values. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@positive 
	@no_inf 
	@no_nan 
	@numerical 
	def __call__(self, x): 
		return self._function(x) 


class callback2: 

	""" 
	The callback object for python functions being called from C accepting 
	two numerical positional parameters. These functions are wrapped in a 
	number of type and value checking decorators to ensure the simulation runs 
	smoothly. 
	""" 
	
	def __init__(self, function): 
		self.function = function 

	@numerical 
	def __call__(self, x, y): 
		return self._function(x, y) 

	@property 
	def function(self): 
		""" 
		Type :: <function> 

		The function to call, passed from the user. 
		""" 
		return self._function 

	@function.setter 
	def function(self, value): 
		if callable(value): 
			if _pyutils.arg_count(value) == 2: 
				self._function = value 
			else: 
				raise TypeError("""Attribute 'function' must accept exactly \
two positional arguments.""") 
		else: 
			raise TypeError("""Attribute 'function' must be a callable \
object. Got: %s""" % (type(value))) 


class callback2_nan(callback2): 

	""" 
	The callback object for python functions being called from C accepting 
	two numerical positional paramters, and suppressing ArithmeticErrors from 
	NaNs. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@no_nan 
	@numerical 
	def __call__(self, x, y): 
		return self._function(x, y) 


class callback2_nan_inf(callback2): 

	""" 
	The callback object for python functions being called from C accepting 
	two numerical positional parameters, and suppressing ArithmeticErrors from 
	both infs and NaNs. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@no_inf 
	@no_nan 
	@numerical 
	def __call__(self, x, y): 
		return self._function(x, y) 


class callback2_nan_inf_positive(callback2): 

	""" 
	The callback object for python functions being called from C accepting 
	two numerical positional parameters, and suppressing ArithmeticErrors from 
	all of infs, NaNs, and non-positive values. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@positive 
	@no_inf 
	@no_nan 
	@numerical 
	def __call__(self, x, y): 
		return self._function(x, y) 


class callback2_nan_positive(callback2): 

	""" 
	The callback object for python functions being called from C accepting 
	two numerical positional parameters, and suppressing ArithmeticErrors from 
	both of NaNs and non-positive values. 
	""" 

	def __init__(self, function): 
		super().__init__(function) 

	@positive 
	@no_nan 
	@numerical 
	def __call__(self, x, y): 
		return self._function(x, y) 

