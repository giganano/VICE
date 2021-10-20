/*
 * This file implements testing of the element object's memory management
 */

#include <stdlib.h>
#include <string.h>
#include "../../objects.h"
#include "element.h"
#include "ccsne.h"
#include "sneia.h"
#include "agb.h"


/*
 * Test the function which constructs an element object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short test_element_initialize(void) {

	ELEMENT *test = element_initialize();
	unsigned short result = (test != NULL &&
		(*test).symbol != NULL &&
		(*test).agb_grid != NULL &&
		(*test).ccsne_yields != NULL &&
		(*test).sneia_yields != NULL &&
		(*test).channels == NULL &&
		(*test).n_channels == 0u
	);
	element_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored by an element object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short test_element_free(void) {

	/* The destructor function should not modify the address */
	ELEMENT *test = element_initialize();
	void *initial_address = (void *) test;
	element_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}


/*
 * Obtain a pointer to a test instance of the ELEMENT object.
 *
 * header: element.h
 */
extern ELEMENT *element_test_instance(void) {

	ELEMENT *test = element_initialize();

	agb_yield_grid_free(test -> agb_grid);
	test -> agb_grid = agb_yield_grid_test_instance();
	ccsne_yield_free(test -> ccsne_yields);
	test -> ccsne_yields = ccsne_yield_test_instance();
	sneia_yield_free(test -> sneia_yields);
	test -> sneia_yields = sneia_yield_test_instance();
	strcpy(test -> symbol, "test");
	test -> primordial = 0.01;
	test -> solar = 0.01;

	return test;

}


