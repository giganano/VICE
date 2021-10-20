/*
 * This file implements testing of the memory management of the hydrodiskstars
 * object in the parent directory.
 */

#include "hydrodiskstars.h"


/*
 * Tests the constructor function for the hydrodiskstars object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: hydrodiskstars.h
 */
extern unsigned short test_hydrodiskstars_initialize(void) {

	HYDRODISKSTARS *test = hydrodiskstars_initialize();
	unsigned short status = test != NULL;
	status &= (*test).n_stars == 0ul;
	status &= (*test).ids == NULL;
	status &= (*test).birth_times == NULL;
	status &= (*test).birth_radii == NULL;
	status &= (*test).final_radii == NULL;
	status &= (*test).zfinal == NULL;
	status &= (*test).v_rad == NULL;
	status &= (*test).v_phi == NULL;
	status &= (*test).v_z == NULL;
	status &= (*test).rad_bins == NULL;
	status &= (*test).decomp == NULL;
	status &= (*test).n_rad_bins == 0u;
	hydrodiskstars_free(test);
	return status;

}


/*
 * Tests the destructor function for the hydrodiskstars object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: hydrodiskstars.h
 */
extern unsigned short test_hydrodiskstars_free(void) {

	/* Destructor shouldn't change the address of the object */
	HYDRODISKSTARS *test = hydrodiskstars_initialize();
	void *initial_address = (void *) test;
	hydrodiskstars_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

