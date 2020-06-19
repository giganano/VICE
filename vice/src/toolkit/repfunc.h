
#ifndef TOOLKIT_REPFUNC_H 
#define TOOLKIT_REPFUNC_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../objects.h" 

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
 * source: repfunc.c 
 */ 
extern double repfunc_evaluate(REPFUNC rpf, double x); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TOOLKIT_REPFUNC_H */ 
