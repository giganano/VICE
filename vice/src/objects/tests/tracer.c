/*
 * This file implements testing of the tracer object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "tracer.h"


/*
 * Test the function which constructs a tracer object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: tracer.h
 */
extern unsigned short test_tracer_initialize(void) {

	TRACER *test = tracer_initialize();
	unsigned short result = (test != NULL &&
		(*test).mass == 0 &&
		(*test).zone_history == NULL
	);
	tracer_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored in a tracer object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: tracer.h
 */
extern unsigned short test_tracer_free(void) {

	/* The destructor function should not modify the address */
	TRACER *test = tracer_initialize();
	void *initial_address = (void *) test;
	tracer_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

