/*
 * This file implements testing of the callback_1arg object's memory management.
 */

#include <stdlib.h>
#include <math.h>
#include "../../objects.h"
#include "callback_1arg.h"


/*
 * Test the function which constructs a callback_1arg object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback_1arg.h
 */
extern unsigned short test_callback_1arg_initialize(void) {

	CALLBACK_1ARG *test = callback_1arg_initialize();
	unsigned short result = (test != NULL &&
		(*test).assumed_constant == 0 &&
		(*test).user_func == NULL
	);
	callback_1arg_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a callback_1arg object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback_1arg.h
 */
extern unsigned short test_callback_1arg_free(void) {

	/* The destructor function should not modify the address */
	CALLBACK_1ARG *test = callback_1arg_initialize();
	void *initial_address = (void *) test;
	callback_1arg_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the callback_1arg object
 *
 * header: callback_1arg.h
 */
extern CALLBACK_1ARG *callback_1arg_test_instance(void) {

	CALLBACK_1ARG *test = callback_1arg_initialize();
	test -> callback = &callback_1arg_test_function;
	test -> assumed_constant = 1;
	return test;

}


/*
 * A dummy mathematical function intended purely for testing the callback_1arg
 * object.
 *
 * Accepts a void* as a second parameter because the callback function is
 * implemented such that this will correspond to the PyObject holding the
 * user's function
 *
 * header: callback_1arg.h
 */
extern double callback_1arg_test_function(double x, void *dummy) {

	return pow(x, 2) * exp(-x);

}

