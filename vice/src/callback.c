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

	// trace_print(); // significant slowdown
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

	// trace_print(); // significant slowdown
	if (cb2.user_func != NULL) {
		return cb2.callback(x, y, cb2.user_func);
	} else {
		return cb2.assumed_constant;
	}

}


/*
 * Evaluate a callback function based on the current state of the ISM.
 *
 * Parameters
 * ==========
 * cbcs: 		The callback object
 * cs: 			The CURRENT_STATE object storing the relevant information
 * 				on the ISM at the current timestep.
 *
 * Returns
 * =======
 * f(cs), where ``f`` is the function passed from python and ``cs`` is the
 * CURRENT_STATE object.
 *
 * header: callback.h
 */
extern double callback_current_state_evaluate(CALLBACK_CURRENT_STATE cbcs,
	CURRENT_STATE cs) {

	if (cbcs.user_func != NULL) {
		return cbcs.callback(cs, cbcs.user_func);
	} else {
		return 0;
	}

}

