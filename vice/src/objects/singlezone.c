/*
 * This file implements memory management for the singlezone object.
 */

#include <stdlib.h>
#include "../singlezone.h"
#include "../io.h"
#include "objects.h"
#include "singlezone.h"
#include "ssp.h"


/*
 * Allocate memory for and return a pointer to a SINGLEZONE struct.
 * Automatically initializes all fields to NULL.
 *
 * header: singlezone.h
 */
extern SINGLEZONE *singlezone_initialize(void) {

	SINGLEZONE *sz = (SINGLEZONE *) malloc (sizeof(SINGLEZONE));
	sz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char));
	sz -> history_writer = NULL;
	sz -> mdf_writer = NULL;
	sz -> output_times = NULL;
	sz -> elements = NULL; 		/* set by python */
	sz -> ism = ism_initialize();
	sz -> mdf = mdf_initialize();
	sz -> ssp = ssp_initialize();
	return sz;

}


/*
 * Free up the memory associated with a singlezone object.
 *
 * header: singlezone.h
 */
extern void singlezone_free(SINGLEZONE *sz) {

	if (sz != NULL) {

		singlezone_close_files(sz);

		if ((*sz).elements != NULL) {
			unsigned int i;
			for (i = 0; i < (*sz).n_elements; i++) {
				element_free(sz -> elements[i]);
			}
			free(sz -> elements);
			sz -> elements = NULL;
		} else {}

		ism_free(sz -> ism);
		mdf_free(sz -> mdf);
		ssp_free(sz -> ssp);

		if ((*sz).name != NULL) {
			free(sz -> name);
			sz -> name = NULL;
		} else {}

		free(sz);
		sz = NULL;

	}

}

