/*
 * This file implements testing of the singlezone object's memory management
 */

#include <stdlib.h>
#include <string.h>
#include "../../objects.h"
#include "singlezone.h"
#include "element.h"
#include "ism.h"
#include "mdf.h"
#include "ssp.h"


/*
 * Test the function which constructs a singlezone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: singlezone.h
 */
extern unsigned short test_singlezone_initialize(void) {

	SINGLEZONE *test = singlezone_initialize();
	unsigned short result = (test != NULL &&
		(*test).name != NULL &&
		(*test).history_writer == NULL &&
		(*test).mdf_writer == NULL &&
		(*test).output_times == NULL &&
		(*test).elements == NULL &&
		(*test).ism != NULL &&
		(*test).mdf != NULL &&
		(*test).ssp != NULL
	);
	singlezone_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a singlezone object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: singlezone.h
 */
extern unsigned short test_singlezone_free(void) {

	/* The destructor function should not modify the address */
	SINGLEZONE *test = singlezone_initialize();
	void *initial_address = (void *) test;
	singlezone_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the SINGLEZONE object.
 *
 * header: singlezone.h
 */
extern SINGLEZONE *singlezone_test_instance(void) {

	SINGLEZONE *test = singlezone_initialize();

	strcpy(test -> name, "test.vice");
	test -> n_elements = 1u;
	test -> dt = TEST_SINGLEZONE_TIMESTEP_SIZE;
	test -> current_time = 0;
	test -> n_outputs = 101ul;
	test -> output_times = (double *) malloc (
		(*test).n_outputs * sizeof(double));
	unsigned short i;
	for (i = 0u; i < (*test).n_outputs; i++) {
		test -> output_times[i] = (*test).dt * i;
	}
	test -> Z_solar = 0.014;
	test -> elements = (ELEMENT **) malloc (sizeof(ELEMENT *));
	test -> elements[0] = element_test_instance();
	ism_free(test -> ism);
	test -> ism = ism_test_instance();
	mdf_free(test -> mdf);
	test -> mdf = mdf_test_instance();
	ssp_free(test -> ssp);
	test -> ssp = ssp_test_instance();
	return test;

}

