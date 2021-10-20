/*
 * This file implements testing of the callback_2arg object's memory management.
 */

#include <stdlib.h>
#include "../../objects.h"
#include "callback_2arg.h"
#include "callback_1arg.h"


/*
 * Test the function which constructs a callback_2arg object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback_2arg.h
 */
extern unsigned short test_callback_2arg_initialize(void) {

	CALLBACK_2ARG *test = callback_2arg_initialize();
	unsigned short result = (test != NULL &&
		(*test).assumed_constant == 0 &&
		(*test).user_func == NULL
	);
	callback_2arg_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a callback_2arg object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback_2arg.h
 */
extern unsigned short test_callback_2arg_free(void) {

	/* The destructor should not modify the address */
	CALLBACK_2ARG *test = callback_2arg_initialize();
	void *initial_address = (void *) test;
	callback_2arg_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the callback_2arg object
 *
 * header: callback_2arg.h
 */
extern CALLBACK_2ARG *callback_2arg_test_instance(void) {

	CALLBACK_2ARG *test = callback_2arg_initialize();
	test -> callback = &callback_2arg_test_function;
	test -> assumed_constant = 1;
	return test;

}


/*
 * A dummy mathematical function intended purely for testing the callback_2arg
 * object.
 *
 * Accepts a void* as a third parameter because the callback function is
 * implemented such that this will correspond to the PyObject holding the
 * user's function
 *
 * header: callback_2arg.h
 */
extern double callback_2arg_test_function(double x, double y, void *dummy) {

	return (
		callback_1arg_test_function(x, dummy) +
		callback_1arg_test_function(y, dummy)
	);

}

