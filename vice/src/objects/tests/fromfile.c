/*
 * This file implements testing of the fromfile object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "fromfile.h"


/*
 * Test the function which constructs a fromfile object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: fromfile.h
 */
extern unsigned short test_fromfile_initialize(void) {

	FROMFILE *test = fromfile_initialize();
	unsigned short result = (test != NULL &&
		(*test).name != NULL &&
		(*test).n_rows == 0ul &&
		(*test).n_cols == 0u &&
		(*test).labels == NULL &&
		(*test).data == NULL
	);
	fromfile_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by a fromfile object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: fromfile.h
 */
extern unsigned short test_fromfile_free(void) {

	/* The destructor function should not modify the address */
	FROMFILE *test = fromfile_initialize();
	void *initial_address = (void *) test;
	fromfile_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

