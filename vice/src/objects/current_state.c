/*
 * This file implements memory management for the CURRENT_STATE object.
 */

#include <stdlib.h>
#include "current_state.h"
#include "objects.h"


/*
 * Allocate memory for and return a pointer to a CURRENT_STATE object.
 * Automatically sets the abundance by mass for each element to 0.0.
 *
 * Parameters
 * ==========
 * n_elements: The number of elements tracked by the model.
 *
 * header: current_state.h
 */
extern CURRENT_STATE *current_state_initialize(unsigned short n_elements) {

	CURRENT_STATE *cs = (CURRENT_STATE *) malloc (sizeof(CURRENT_STATE));
	cs -> n_elements = n_elements;
	cs -> symbols = (char **) malloc (n_elements * sizeof(char *));
	cs -> Z = (double *) malloc (n_elements * sizeof(double));
	for (unsigned short i = 0u; i < n_elements; i++) {
		cs -> symbols[i] = (char *) malloc (5u * sizeof(char));
		cs -> Z[i] = 0.0;
	}
	return cs;

}


/*
 * Free up the memory stored by a CURRENT_STATE object.
 *
 * header: current_state.h
 */
extern void current_state_free(CURRENT_STATE *cs) {

	if (cs != NULL) {

		if ((*cs).symbols != NULL) {
			for (unsigned short i = 0u; i < (*cs).n_elements; i++) {
				if ((*cs).symbols[i] != NULL) {
					free(cs -> symbols[i]);
					cs -> symbols[i] = NULL;
				} else {}
			}
			free(cs -> symbols);
			cs -> symbols = NULL;
		} else {}

		if ((*cs).Z != NULL) {
			free(cs -> Z);
			cs -> Z = NULL;
		} else {}

		free(cs);
		cs = NULL;

	} else {}

}

