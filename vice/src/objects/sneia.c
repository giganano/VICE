/*
 * This file implements memory management for the SNEIA_YIELD_SPECS object.
 */

#include <stdlib.h>
#include "../sneia.h"
#include "objects.h"
#include "sneia.h"


/*
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct.
 * Automatically initializes RIa and yield_ to NULL. Allocates memory for a
 * 100-character dtd char * specifier.
 *
 * header: sneia.h
 */
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void) {

	SNEIA_YIELD_SPECS *sneia_yields = (SNEIA_YIELD_SPECS *) malloc (sizeof(
		SNEIA_YIELD_SPECS));

	/* some defaults to prevent errors */
	sneia_yields -> yield_ = callback_1arg_initialize();
	sneia_yields -> RIa = NULL;
	sneia_yields -> dtd = (char *) malloc (100 * sizeof(char));
	sneia_yields -> tau_ia = 1.5;
	sneia_yields -> t_d = 0.15;
	sneia_yields -> entrainment = 1;

	return sneia_yields;

}


/*
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct.
 *
 * header: sneia.h
 */
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields) {

	if (sneia_yields != NULL) {

		if ((*sneia_yields).yield_ != NULL) {
			callback_1arg_free(sneia_yields -> yield_);
			sneia_yields -> yield_ = NULL;
		} else {}

		if ((*sneia_yields).RIa != NULL) {
			free(sneia_yields -> RIa);
			sneia_yields -> RIa = NULL;
		} else {}

		if ((*sneia_yields).dtd != NULL) {
			free(sneia_yields -> dtd);
			sneia_yields -> dtd = NULL;
		} else {}

		free(sneia_yields);
		sneia_yields = NULL;

	} else {}

}

