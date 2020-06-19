/* 
 * This file implements the core routines of the repfunc object. 
 */ 

#include <math.h> 
#include "repfunc.h" 
#include "../utils.h" 


/* 
 * Evaluate a repfunc object at some value of the x-coordinate. 
 * 
 * Parameters 
 * ==========
 * repfunc: 	The repfunc object 
 * x: 			The value of the x-coordinate to evaluate the function at 
 * 
 * Returns 
 * ======= 
 * repfunc(x), the value of the original function f(x) approximated via 
 * linear interpolation off the known values of the function 
 * 
 * header: repfunc.h 
 */ 
extern double repfunc_evaluate(REPFUNC rpf, double x) {

	long bin = get_bin_number(rpf.xcoords, rpf.n_points - 1ul, x); 
	if (bin == -1l) {
		if (x < rpf.xcoords[0]) {
			bin = 0l; 
		} else if (x > rpf.xcoords[rpf.n_points - 1l]) {
			bin = (long) rpf.n_points - 2l; 
		} else {
			/* error handling for manylinux1 distribution */ 
			#ifdef NAN 
				return NAN; 
			#else 
				return 0; 
			#endif 
		} 
	} 

	return interpolate(rpf.xcoords[bin], rpf.xcoords[bin + 1l], 
		rpf.ycoords[bin], rpf.ycoords[bin + 1l], x); 

}

