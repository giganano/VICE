/*
 * This file implements memory management for the SSP object.
 */

#include <stdlib.h>
#include "../ssp.h"
#include "objects.h"
#include "ssp.h"


/*
 * Allocate memory for and return a pointer to an SSP struct. Automatically
 * sets both crf and msmf to NULL. Allocates memory for a 100-element char *
 * IMF specifier.
 *
 * header: ssp.h
 */
extern SSP *ssp_initialize(void) {

	/*
	 * The imf object is initialized with the default lower and upper mass
	 * limits. They will be modified by the python wrapper in VICE anyway.
	 * This keeps the implementation simpler in that now singlezone_initialize
	 * does not need to take arguments for the mass limits.
	 */

	SSP *ssp = (SSP *) malloc (sizeof(SSP));
	ssp -> imf = imf_initialize(
		SSP_IMF_DEFAULT_M_LOWER, SSP_IMF_DEFAULT_M_UPPER
	);
	ssp -> crf = NULL;
	ssp -> msmf = NULL;
	return ssp;

}


/*
 * Free up the memory stored in an SSP struct.
 *
 * header: ssp.h
 */
extern void ssp_free(SSP *ssp) {

	if (ssp != NULL) {

		if ((*ssp).crf != NULL) {
			free(ssp -> crf);
			ssp -> crf = NULL;
		} else {}

		if ((*ssp).msmf != NULL) {
			free(ssp -> msmf);
			ssp -> msmf = NULL;
		} else {}

		if ((*ssp).imf != NULL) {
			imf_free(ssp -> imf);
			ssp -> imf = NULL;
		} else {}

		free(ssp);
		ssp = NULL;

	} else {}

}

