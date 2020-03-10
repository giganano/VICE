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
A decorator which wraps the __call__ function of the callback1 object and 
all subclasses to suppress TypeErrors by not allowing non-numerical values 
to be returned. 
""" 
def numerical_1arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x): 
		y = function(obj, x) 
		if isinstance(y, numbers.Number): 
			return float(y) 
		else: 
			warnings.warn("""\
Function %s evaluated to non-numerical value at %s. Suppressing TypeError by \
returning 0. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(x)), ScienceWarning) 
			return 0 
	return wrapper 


""" 
A decorator which wraps the __call__ function of the callback2 object and 
all subclasses to suppress TypeErrors by not allowing non-numerical values 
to be returned. 
""" 
def numerical_2arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x, y): 
		z = function(obj, x, y) 
		if isinstance(z, numbers.Number): 
			return float(z) 
		else: 
			warnings.warn("""\
Function %s evaluated to non-numerical value at %s. Suppressing TypeError by \
return 0. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(x)), ScienceWarning) 
			return 0 
	return wrapper 


""" 
A decorator which wraps the __call__ function of the callback1 object to 
suppress ArithmeticErrors by not allowing NaN from user functions 
""" 
def no_nan_1arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x): 
		y = function(obj, x) 
		if m.isnan(y): 
			warnings.warn("""\
Function %s evaluated to NaN at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(x)), ScienceWarning) 
			return 0 
		else: 
			return y 
	return wrapper 


""" 
A decorator which wraps the __call__ function of the callback2 object to 
suppress ArithmeticErrors by not allowing NaNs from user functions. 
""" 
def no_nan_2arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x, y): 
		z = function(obj, x, y) 
		if m.isnan(z): 
			warnings.warn("""\
Function %s evaluated to NaN at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(x)), ScienceWarning) 
			return 0 
		else: 
			return z 
	return wrapper 


""" 
A decorator which subsequently wraps the numerical_1arg decorator on the 
callback1 __call__ function. This ensures that infinite values are not 
allowed. 
""" 
def no_inf_1arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x): 
		y = function(obj, x) 
		if m.isinf(y): 
			warnings.warn("""\
Function %s evaluated to inf at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(x)), ScienceWarning) 
			return 0 
		else: 
			return y 
	return wrapper 


""" 
A decorator which subsequently wraps the numerical_2arg decorator on the 
callback2 __call__ function. This ensures that infinite values are not 
allowed. 
""" 
def no_inf_2arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x, y): 
		z = function(obj, x, y) 
		if m.isinf(z): 
			warnings.warn("""\
Function %s evaluated to inf at %s. Suppressing ArithmeticError by returning \
0. Checking simulation output for numerical consistency is advised.""" % (
				str(function), str(x)), ScienceWarning) 
			return 0 
		else: 
			return z 
	return wrapper 


""" 
A decorator which subsequently wraps the numerical_1arg decorator on the 
callback1 __call__ function. This ensures that the returned value is 
positive definite. 
""" 
def positive_1arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x): 
		y = function(obj, x) 
		if y <= 0: 
			warnings.warn("""\
Function %s evaluated to non-positive value at %s. Suppressing ArithmeticError \
by returning 1e-12. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(x)), ScienceWarning) 
			return 1e-12 
		else: 
			return y 
	return wrapper 


""" 
A decorator which subsequently wraps the numerical_2arg decorator on the 
callback2 __call__ function. This ensures that infinite values are not 
allowed. 
""" 
def positive_2arg(function): 
	@functools.wraps(function) 
	def wrapper(obj, x, y): 
		z = function(obj, x, y) 
		if z <= 0: 
			warnings.warn("""\
Function %s evaluted to non-positive value at %s. Suppressing ArithmeticError \
by return 1e-12. Checking simulation output for numerical consistency is \
advised.""" % (str(function), str(x)), ScienceWarning) 
			return 1e-12 
		else: 
			return z 
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

	@numerical_1arg 
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

	@no_nan_1arg 
	@numerical_1arg 
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

	@no_inf_1arg 
	@no_nan_1arg 
	@numerical_1arg 
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

	@positive_1arg 
	@no_nan_1arg 
	@numerical_1arg 
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

	@positive_1arg 
	@no_inf_1arg 
	@no_nan_1arg 
	@numerical_1arg 
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

	@numerical_2arg 
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

	@no_nan_2arg 
	@numerical_2arg 
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

	@no_inf_2arg 
	@no_nan_2arg 
	@numerical_2arg 
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

	@positive_2arg 
	@no_inf_2arg 
	@no_nan_2arg 
	@numerical_2arg 
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

	@positive_2arg 
	@no_nan_2arg 
	@numerical_2arg 
	def __call__(self, x, y): 
		return self._function(x, y) 

