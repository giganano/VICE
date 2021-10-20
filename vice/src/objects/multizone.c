/*
 * This file implements memory management for the multizone object.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../io.h"
#include "objects.h"
#include "multizone.h"
#include "migration.h"


/*
 * Allocates memory for and returns a pointer to a multizone object
 *
 * Parameters
 * ==========
 * n: 		The number of zones in the simulation
 *
 * header: multizone.h
 */
extern MULTIZONE *multizone_initialize(unsigned int n) {

	/*
	 * Memory is allocated for n singlezone objects, but they are not
	 * initialized ere. When a multizone object is created through the python
	 * interpreter, it creates an array of singlezone objects, then calls
	 * link_zone to point each zone here to the proper memory addresses.
	 */
	MULTIZONE *mz = (MULTIZONE *) malloc (sizeof(MULTIZONE));
	mz -> zones = (SINGLEZONE **) malloc (n * sizeof(SINGLEZONE *));
	mz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char));
	mz -> mig = migration_initialize(n);
	mz -> verbose = 0;
	return mz;

}


/*
 * Frees the memory stored in a multizone object
 *
 * header: multizone.h
 */
extern void multizone_free(MULTIZONE *mz) {

	if (mz != NULL) {

		/*
		 * Since the singlezone object's __dealloc__ function calls
		 * singlezone_free, the memory for each individual zone should not
		 * be freed here. Doing so will cause a memory error upon system exit.
		 */

		if ((*mz).name != NULL) {
			free(mz -> name);
			mz -> name = NULL;
		} else {}

		if ((*mz).mig != NULL) {
			migration_free(mz -> mig);
			mz -> mig = NULL;
		}

		free(mz);
		mz = NULL;

	}

}

