/*
 * This file implements testing of the migration object's memory management
 */

#include <stdlib.h>
#include "../../objects.h"
#include "migration.h"
#include "multizone.h"


/*
 * Test the function which constructs a migration object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: migration.h
 */
extern unsigned short test_migration_initialize(void) {

	MIGRATION *test = migration_initialize(TESTS_N_ZONES);
	unsigned short result = (test != NULL &&
		(*test).n_zones == TESTS_N_ZONES &&
		(*test).n_tracers == 0u &&
		(*test).tracer_count == 0ul &&
		(*test).gas_migration == NULL &&
		(*test).tracers == NULL &&
		(*test).tracers_output == NULL
	);
	migration_free(test);
	return result;

}


/*
 * Test the function which frees the memory stored in a migration object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: migration.h
 */
extern unsigned short test_migration_free(void) {

	/* The destructor function should not modify the address */
	MIGRATION *test = migration_initialize(TESTS_N_ZONES);
	void *initial_address = (void *) test;
	migration_free(test);
	void *final_address = (void *) test;
	return initial_address == final_address;

}

