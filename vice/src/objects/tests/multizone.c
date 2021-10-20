/*
 * This file implements testing of the multizone object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "multizone.h"


/*
 * Test the function which constructs a multizone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: multizone.h
 */
extern unsigned short test_multizone_initialize(void) {

	MULTIZONE *test = multizone_initialize(TESTS_N_ZONES);
	unsigned short result = (test != NULL &&
		(*test).zones != NULL &&
		(*test).name != NULL &&
		(*test).mig != NULL &&
		(*(*test).mig).n_zones == TESTS_N_ZONES &&
		(*test).verbose == 0
	);
	multizone_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a multizone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: multizone.h
 */
extern unsigned short test_multizone_free(void) {

	/* The destructor function should not modify the address */
	MULTIZONE *test = multizone_initialize(TESTS_N_ZONES);
	void *initial_address = (void *) test;
	multizone_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

