/*
 * This file implements testing of the imf_ object's memory management
 */

#include <stdlib.h>
#include <string.h>
#include "../../objects.h"
#include "callback_1arg.h"
#include "imf.h"


/*
 * Test the function which constructs an IMF object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: imf.h
 */
extern unsigned short test_imf_initialize(void) {

	IMF_ *test = imf_initialize(TEST_IMF_M_LOWER, TEST_IMF_M_UPPER);
	unsigned short result = (test != NULL &&
		(*test).spec != NULL &&
		(*test).m_lower == TEST_IMF_M_LOWER &&
		(*test).m_upper == TEST_IMF_M_UPPER
	);
	imf_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by an IMF object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: imf.h
 */
extern unsigned short test_imf_free(void) {

	/* The destructor function should not modify the address */
	IMF_ *test = imf_initialize(TEST_IMF_M_LOWER, TEST_IMF_M_UPPER);
	void *initial_address = (void *) test;
	imf_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the IMF_ object
 *
 * header: imf.h
 */
extern IMF_ *imf_test_instance(void) {

	IMF_ *test = imf_initialize(TEST_IMF_M_LOWER, TEST_IMF_M_UPPER);
	strcpy(test -> spec, "salpeter");
	callback_1arg_free(test -> custom_imf);
	test -> custom_imf = callback_1arg_test_instance();
	return test;

}

