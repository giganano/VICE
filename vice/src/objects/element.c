/*
 * This file implements the memory management for the ELEMENT object.
 */

#include <stdlib.h>
#include "../element.h"
#include "objects.h"
#include "element.h"


/*
 * Allocate memory for an return a pointer to an ELEMENT struct. This also
 * allocates memory for the AGB_YIELD_GRID, CCSNE_YIELD_SPECS, and
 * SNEIA_YIELD_SPECS stored in the ELEMENT struct. Allocates memory for a
 * 5-element string for each element's symbol.
 *
 * header: element.h
 */
extern ELEMENT *element_initialize(void) {

	ELEMENT *e = (ELEMENT *) malloc (sizeof(ELEMENT));
	e -> symbol = (char *) malloc (5 * sizeof(char));
	e -> agb_grid = agb_yield_grid_initialize();
	e -> ccsne_yields = ccsne_yield_initialize();
	e -> sneia_yields = sneia_yield_initialize();
	e -> channels = NULL;
	e -> n_channels = 0u;
	return e;

}


/*
 * Free up the memory stored in an ELEMENT struct
 *
 * header: element.h
 */
extern void element_free(ELEMENT *e) {

	if (e != NULL) {

		agb_yield_grid_free(e -> agb_grid);
		ccsne_yield_free(e -> ccsne_yields);
		sneia_yield_free(e -> sneia_yields);

		if ((*e).symbol != NULL) {
			free(e -> symbol);
			e -> symbol = NULL;
		} else {}

		if ((*e).channels != NULL) {
			unsigned short i;
			for (i = 0lu; i < (*e).n_channels; i++) {
				channel_free(e -> channels[i]);
			}
			free(e -> channels);
			e -> channels = NULL;
		} else {}

		free(e);
		e = NULL;

	} else {}

}

