
#ifndef TESTS_OBJECTS_CALLBACK_2ARG_H
#define TESTS_OBJECTS_CALLBACK_2ARG_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a callback_2arg object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: callback_2arg.c
 */
extern unsigned short test_callback_2arg_initialize(void);

/*
 * Test the function which frees the memory stored by a callback_2arg object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: callback_2arg.c
 */
extern unsigned short test_callback_2arg_free(void);

/*
 * Obtain a pointer to a test instance of the callback_2arg object
 *
 * source: callback_2arg.c
 */
extern CALLBACK_2ARG *callback_2arg_test_instance(void);

/*
 * A dummy mathematical function intended purely for testing the callback_2arg
 * object.
 *
 * Accepts a void* as a third parameter because the callback function is
 * implemented such that this will correspond to the PyObject holding the
 * user's function
 *
 * source: callback_2arg.c
 */
extern double callback_2arg_test_function(double x, double y, void *dummy);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_CALLBACK_2ARG_H */
