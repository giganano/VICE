r""" 
This file implements the repfunc class. 
""" 

from __future__ import absolute_import 
from ..._globals import ScienceWarning 
from ...core._pyutils import copy_array_like_object, numeric_check 
from ._repfunc import c_repfunc 


class repfunc: 

	r""" 
	A repaired function. This takes in x-coordinates and y-coordinates of the 
	same length and constructs an interpolation scheme to approximate the 
	value of the function which generated the points. This object can also be 
	used to implement an interpolation scheme. 

	.. versionadded:: 1.X.0 

	.. note:: This object is not imported with a simple ``import vice`` 
		statement. It can be accessed via the following line: 
		``from vice.toolkit.repair_function import repfunc`` 

	Attributes 
	----------
	xcoords : list [elements are real numbers] 
		The x-coordinates of the points on which the function was sampled. 
	ycoords : list [elements are real numbers] 
		The y-coordinates of the points on which the function was sampled. 
	n_points : int 
		The number of points on which 

	Parameters 
	----------
	xcoords : array-like 
		The attribute 'xcoords' - see above 
	ycoords : array-like 
		The attribute 'ycoords' - see above 

	.. note:: It is assumed, though not enforced, that the xcoords and ycoords 
		arrays are sorted in order of increasing x-coordinates. 

	Raises 
	------
	* ScienceWarning 
		- The xcoords attribute is not sorted from least to greatest 

	Calling 
	-------
	Call this object with a given x-coordinate, and it will automatically 
	use linear interpolation to extrapolate the value of the function at that 
	value of x. 

	Indexing 
	--------
	Index this object as you would a list, and it will return the (x, y) 
	coordinates of the sampled points from the attributes 'xcoords' and 
	'ycoords'. 

	Example Code 
	------------
	>>> from vice.toolkit.repair_function import repfunc 
	>>> example = repfunc([1, 2, 3], [2, 4, 6]) 
	>>> example(0) 
	0.0 
	>>> example(5) 
	10.0 
	>>> example(4) 
	8.0 
	>>> example[:] 
	[[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]] 
	>>> example.xcoords 
	[1.0, 2.0, 3.0] 
	>>> example.ycoords 
	[2.0, 4.0, 6.0] 
	>>> example.n_points 
	3  
	""" 

	def __init__(self, xcoords, ycoords): 
		xcoords = copy_array_like_object(xcoords) 
		ycoords = copy_array_like_object(ycoords) 
		numeric_check(xcoords, TypeError, 
			"Non-numerical value detected in x-coordinates.") 
		numeric_check(ycoords, TypeError, 
			"Non-numerical value detected in y-coordinates.") 
		if xcoords != sorted(xcoords): warnings.warn("""\
x-coordinates not sorted from least to greatest. This is assumed to be so by \
this object, and will likely cause numerical artifacts.""", ScienceWarning) 
		self.__c_version = c_repfunc(xcoords, ycoords) 

	def __call__(self, x): 
		return self.__c_version.__call__(x) 

	def __getitem__(self, idx): 
		return self.__c_version.__getitem__(idx) 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		return exc_value is None 

	@property 
	def xcoords(self): 
		r""" 
		Type : list 

		The x-coordinates on which the function was sampled. 
		""" 
		return self.__c_version.xcoords 

	@property 
	def ycoords(self): 
		r""" 
		Type : list 

		The y-coordinates on which the function was sampled. 
		""" 
		return self.__c_version.ycoords 

	@property 
	def n_points(self): 
		r""" 
		Type : int 

		The number of points on which the function was sampled. 
		""" 
		return self.__c_version.n_points 


