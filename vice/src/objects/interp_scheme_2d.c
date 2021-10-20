/*
 * This file implements memory management for the interp_scheme_2d object.
 */

#include <stdlib.h>
#include "interp_scheme_2d.h"


/*
 * Allocate memory for and return a pointer to an interp_scheme_2d object. The
 * number of x and y coordinates is automatically set to 0 and the coordinates
 * to NULL.
 *
 * header: interp_scheme_2d.h
 */
extern INTERP_SCHEME_2D *interp_scheme_2d_initialize(void) {

	INTERP_SCHEME_2D *is2d = (INTERP_SCHEME_2D *) malloc (
		sizeof(INTERP_SCHEME_2D));
	is2d -> n_x_values = 0ul;
	is2d -> n_y_values = 0ul;
	is2d -> xcoords = NULL;
	is2d -> ycoords = NULL;
	is2d -> zcoords = NULL;
	return is2d;

}


/*
 * Free up the memory stored in an interp_scheme_2d object.
 *
 * header: interp_scheme_2d.h
 */
extern void interp_scheme_2d_free(INTERP_SCHEME_2D *is2d) {

	if (is2d != NULL) {

		if ((*is2d).xcoords != NULL) {
			free(is2d -> xcoords);
			is2d -> xcoords = NULL;
			is2d -> n_x_values = 0ul;
		} else {}

		if ((*is2d).ycoords != NULL) {
			free(is2d -> ycoords);
			is2d -> ycoords = NULL;
			is2d -> n_y_values = 0ul;
		} else {}

		if ((*is2d).zcoords != NULL) {
			free(is2d -> zcoords);
			is2d -> zcoords = NULL;
		} else {}

		free(is2d);
		is2d = NULL;

	} else {}

}

