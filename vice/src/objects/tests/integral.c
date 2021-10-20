/*
 * This file implements testing of the integral object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "integral.h"


/*
 * Test the function which constructs an integral object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_integral_initialize(void) {

	INTEGRAL *test = integral_initialize();
	unsigned short result = test != NULL;
	integral_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by an integral object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_integral_free(void) {

	/* The destructor function should not modify the address */
	INTEGRAL *test = integral_initialize();
	void *initial_address = (void *) test;
	integral_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

