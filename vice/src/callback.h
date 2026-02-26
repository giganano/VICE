
#ifndef CALLBACK_H
#define CALLBACK_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

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
 * source: callback.c
 */
extern double callback_1arg_evaluate(CALLBACK_1ARG cb1, double x);

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
 * source: callback.c
 */
extern double callback_2arg_evaluate(CALLBACK_2ARG cb2, double x, double y);

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
 * source: callback.c
 */
extern double callback_current_state_evaluate(CALLBACK_CURRENT_STATE cbcs,
	CURRENT_STATE cs);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* CALLBACK_H */

