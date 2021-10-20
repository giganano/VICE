/*
 * This file implements testing of the core functionality of the callback
 * objects.
 */

#include <stdlib.h>
#include <math.h>
#include "../callback.h"
#include "../objects.h"
#include "../objects/tests.h"

/*
 * Test the callback_1arg_evaluate function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback.h
 */
extern unsigned short test_callback_1arg_evaluate(void) {

	CALLBACK_1ARG *test = callback_1arg_test_instance();

	unsigned short result = 1;
	double x = 0;
	do {
		/* user_func is NULL, should return the assumed_constant */
		if (callback_1arg_evaluate(*test, x) != (*test).assumed_constant) {
			result = 0;
			break;
		} else {}

		test -> user_func = (void *) test;
		/* user_func is not NULL, should return the value of the function */
		if (callback_1arg_evaluate(*test, x) !=
			callback_1arg_test_function(x, NULL)) {
			result = 0;
			break;
		} else {}

		test -> user_func = NULL;
		x += 0.1;
	} while (result && x <= 100);

	callback_1arg_free(test);
	return result;

}


/*
 * Test the callback_2arg evaluate function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: callback.h
 */
extern unsigned short test_callback_2arg_evaluate(void) {

	CALLBACK_2ARG *test = callback_2arg_test_instance();

	unsigned short result = 1;
	double x = 0;
	do {

		double y = 0;
		do {
			/* user_func is NULL, should return the assumed_constant */
			if (callback_2arg_evaluate(*test, x, y) !=
				(*test).assumed_constant) {
				result = 0;
				break;
			} else{}

			test -> user_func = (void *) test;
			/* user_func is not NULL, should return the value of the function */
			if (callback_2arg_evaluate(*test, x, y) !=
				callback_2arg_test_function(x, y, NULL)) {
				result = 0;
				break;
			} else {}

			test -> user_func = NULL;
			y += 0.1;

		} while (result && y <= 100);

		x += 0.1;

	} while (result && x <= 100);

	callback_2arg_free(test);
	return result;

}

