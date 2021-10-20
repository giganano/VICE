/*
 * This file implements memory management for the interp_scheme_1d object.
 */

#include <stdlib.h>
#include "interp_scheme_1d.h"


/*
 * Allocate memory for and return a pointer to an interp_scheme_1d object. The
 * number of points is automatically set to 0 and the coordinates to NULL.
 *
 * header: interp_scheme_1d.h
 */
extern INTERP_SCHEME_1D *interp_scheme_1d_initialize(void) {

	INTERP_SCHEME_1D *is1d = (INTERP_SCHEME_1D *) malloc (
		sizeof(INTERP_SCHEME_1D));
	is1d -> n_points = 0ul;
	is1d -> xcoords = NULL;
	is1d -> ycoords = NULL;
	return is1d;

}


/*
 * Free up the memory stored in an interp_scheme_1d object.
 *
 * header: interp_scheme_1d.h
 */
extern void interp_scheme_1d_free(INTERP_SCHEME_1D *is1d) {

	if (is1d != NULL) {

		if ((*is1d).xcoords != NULL) {
			free(is1d -> xcoords);
			is1d -> xcoords = NULL;
		} else {}

		if ((*is1d).ycoords != NULL) {
			free(is1d -> ycoords);
			is1d -> ycoords = NULL;
		} else {}

		is1d -> n_points = 0ul;
		free(is1d);
		is1d = NULL;

	} else {}

}

