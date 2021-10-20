/*
 * This file implements testing of the ssp object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "ssp.h"
#include "imf.h"


/*
 * Test the function which constructs an ssp object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ssp.h
 */
extern unsigned short test_ssp_initialize(void) {

	SSP *test = ssp_initialize();
	unsigned short result = (test != NULL &&
		(*test).imf != NULL &&
		(*test).crf == NULL &&
		(*test).msmf == NULL
	);
	ssp_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored in an ssp object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ssp.h
 */
extern unsigned short test_ssp_free(void) {

	/* The destructor function should not modify the address */
	SSP *test = ssp_initialize();
	void *initial_address = (void *) test;
	ssp_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the SSP object.
 *
 * header: ssp.h
 */
extern SSP *ssp_test_instance(void) {

	SSP *test = ssp_initialize();

	imf_free(test -> imf);
	test -> imf = imf_test_instance();
	test -> postMS = 0.1;
	test -> R0 = 0.2;
	test -> continuous = 0;
	return test;

}

