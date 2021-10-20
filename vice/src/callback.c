/*
 * This file implements the functionality of the callback objects
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
		return cb1.assumed_constant;
	}

}


/*
 * Evaluate a callback function at a given value (x, y)
 *
 * Parameters
 * ==========
 * cb2: 		The callback object
 * x: 			The value of the first numerical argument
 * y: 			The value of the second numerical argument
 *
 * Returns
 * =======
 * f(x, y), where f is the function passed from python
 *
 * header: callback.h
 */
extern double callback_2arg_evaluate(CALLBACK_2ARG cb2, double x, double y) {

	if (cb2.user_func != NULL) {
		return cb2.callback(x, y, cb2.user_func);
	} else {
		return cb2.assumed_constant;
	}

}

