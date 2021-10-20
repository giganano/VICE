
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

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* CALLBACK_H */

