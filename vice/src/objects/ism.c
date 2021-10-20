/*
 * This file implements memory management for the ISM object.
 */

#include <stdlib.h>
#include "../ism.h"
#include "callback_2arg.h"
#include "objects.h"
#include "ism.h"

/*
 * Allocate memory for and return a pointer to an ISM struct. Automatically
 * initializes all fields to NULL. Allocates memory for a 5-element char *
 * mode specifier.
 *
 * header: ism.h
 */
extern ISM *ism_initialize(void) {

	ISM *ism = (ISM *) malloc (sizeof(ISM));
	ism -> mode = (char *) malloc (5 * sizeof(char));
	ism -> specified = NULL;
	ism -> star_formation_history = NULL;
	ism -> eta = NULL;
	ism -> enh = NULL;
	ism -> tau_star = NULL;
	ism -> functional_tau_star = callback_2arg_initialize();
	return ism;

}


/*
 * Free up the memory stored in an ISM struct.
 *
 * header: ism.h
 */
extern void ism_free(ISM *ism) {

	if (ism != NULL) {

		if ((*ism).specified != NULL) {
			free(ism -> specified);
			ism -> specified = NULL;
		} else {}

		if ((*ism).star_formation_history != NULL) {
			free(ism -> star_formation_history);
			ism -> star_formation_history = NULL;
		} else {}

		if ((*ism).eta != NULL) {
			free(ism -> eta);
			ism -> eta = NULL;
		} else {}

		if ((*ism).enh != NULL) {
			free(ism -> enh);
			ism -> enh = NULL;
		} else {}

		if ((*ism).tau_star != NULL) {
			free(ism -> tau_star);
			ism -> tau_star = NULL;
		} else {}

		if ((*ism).mode != NULL) {
			free(ism -> mode);
			ism -> mode = NULL;
		} else {}

		free(ism);
		ism = NULL;

	} else {}

}



