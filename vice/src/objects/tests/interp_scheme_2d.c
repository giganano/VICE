/*
 * This file implements testing of the
 */

#include "../interp_scheme_2d.h"
#include "interp_scheme_2d.h"


/*
 * Tests the memory allocation routine for the interp_scheme_2d object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: interp_scheme_2d.h
 */
extern unsigned short test_interp_scheme_2d_initialize(void) {

	INTERP_SCHEME_2D *test = interp_scheme_2d_initialize();
	unsigned short status = test != NULL;
	if (status) {
		status &= (*test).n_x_values == 0ul;
		status &= (*test).n_y_values == 0ul;
		status &= (*test).xcoords == NULL;
		status &= (*test).ycoords == NULL;
		status &= (*test).zcoords == NULL;
		interp_scheme_2d_free(test);
		return status;
	} else {
		return 0u;
	}


}


/*
 * Test the function which frees the memory stored by an interp_scheme_2d
 * object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure.
 *
 * header: interp_scheme_2d.h
 */
extern unsigned short test_interp_scheme_2d_free(void) {

	/* The destructor function should not modify the address */
	INTERP_SCHEME_2D *test = interp_scheme_2d_initialize();
	void *initial_address = (void *) test;
	interp_scheme_2d_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

