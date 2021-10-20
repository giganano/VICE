/*
 * This file implements memory management for the MDF object.
 */

#include <stdlib.h>
#include "../mdf.h"
#include "objects.h"
#include "mdf.h"


/*
 * Allocate memory for and return a pointer to an MDF struct. Initializes all
 * fields to NULL.
 *
 * header: mdf.h
 */
extern MDF *mdf_initialize(void) {

	MDF *mdf = (MDF *) malloc (sizeof(MDF));
	mdf -> abundance_distributions = NULL;
	mdf -> ratio_distributions = NULL;
	mdf -> bins = NULL;
	return mdf;

}


/*
 * Free up the memory stored in an MDF struct.
 *
 * header: mdf.h
 */
extern void mdf_free(MDF *mdf) {

	if (mdf != NULL) {

		if ((*mdf).abundance_distributions != NULL) {
			free(mdf -> abundance_distributions);
			mdf -> abundance_distributions = NULL;
		} else {}

		if ((*mdf).ratio_distributions != NULL) {
			free(mdf -> ratio_distributions);
			mdf -> ratio_distributions = NULL;
		} else {}

		if ((*mdf).bins != NULL) {
			free(mdf -> bins);
			mdf -> bins = NULL;
		} else {}

		free(mdf);
		mdf = NULL;

	} else {}

}

