/*
 * This file implements the memory management for the AGB_YIELD_GRID
 * object.
 */

#include <stdlib.h>
#include "../agb.h"
#include "callback_2arg.h"
#include "interp_scheme_2d.h"
#include "objects.h"
#include "agb.h"


/*
 * Allocate memory for and return a pointer to an AGB_YIELD_GRID struct and
 * initialize all fields to NULL.
 *
 * header: agb.h
 */
extern AGB_YIELD_GRID *agb_yield_grid_initialize(void) {

	AGB_YIELD_GRID *agb_grid = (AGB_YIELD_GRID *) malloc (sizeof(
		AGB_YIELD_GRID));

	agb_grid -> custom_yield = callback_2arg_initialize();
	agb_grid -> interpolator = interp_scheme_2d_initialize();
	agb_grid -> entrainment = 1;

	return agb_grid;

}


/*
 * Free up the memory stored in an AGB_YIELD_GRID struct
 *
 * header: agb.h
 */
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) {

	if (agb_grid != NULL) {

		if ((*agb_grid).custom_yield != NULL) {
			callback_2arg_free(agb_grid -> custom_yield);
			agb_grid -> custom_yield = NULL;
		} else {}

		if ((*agb_grid).interpolator != NULL) {
			interp_scheme_2d_free(agb_grid -> interpolator);
			agb_grid -> interpolator = NULL;
		} else {}

		free(agb_grid);
		agb_grid = NULL;

	} else {}

}


