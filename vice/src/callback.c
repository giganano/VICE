/* 
 * This file implements the functionality of the callback object 
 */ 

#include "callback.h" 


/* 
 * Evaluate a callback function at a given value x 
 * 
 * Parameters 
 * ========== 
 * cb1: 		The callback object 
 * x: 			The value to evaluate the function at 
 * 
 * Returns 
 * ======= 
 * f(x), where f is the function passed from python 
 * 
 * header: callback.h 
 */ 
extern double callback_1arg_evaluate(CALLBACK_1ARG cb1, double x) { 

	if (cb1.user_func != NULL) { 
		return cb1.callback(x, cb1.user_func); 
	} else { 
		return 0; 
	} 

} 


