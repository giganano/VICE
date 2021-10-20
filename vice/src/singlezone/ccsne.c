/*
 * This file implements the enrichment of arbitrary elements from core
 * collapse supernovae (CCNSe) in VICE's singlezone simulations.
 */

#include <stdlib.h>
#include "../singlezone.h"
#include "../callback.h"
#include "../ccsne.h"
#include "../utils.h"
#include "ccsne.h"

/*
 * Determine the rate of mass enrichment of an element X from core-collapse
 * supernovae at the current timestep. This is implemented acording to the
 * following formulation (see section 4.2 of VICE's science documentation):
 *
 * Mdot_x_CC = y_x_CC * SFR
 *
 * Parameters
 * ==========
 * sz: 			The SINGLEZONE object for the current integration
 * e: 			The ELEMENT struct corresponding to the element to find the
 * 				mass enrichment rate for
 *
 * Returns
 * =======
 * The rate of mass enrichment in Msun/Gyr.
 *
 * header: ccsne.h
 */
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e) {
	
	/* Entrainment is handled in vice/src/singlezone/element.c */
	return (get_cc_yield(e, scale_metallicity(sz, sz.timestep)) *
		(*sz.ism).star_formation_rate);

}


/*
 * Obtain the IMF-integrated fractional mass yield of a given element from its
 * internal yield table.
 *
 * Parameters
 * ==========
 * e: 				The element to find the yield for
 * Z: 				The metallicity to look up on the grid
 *
 * Returns
 * =======
 * The interpolated yield off of the stored yield grid within the ELEMENT
 * struct.
 *
 * header: ccsne.h
 */
extern double get_cc_yield(ELEMENT e, double Z) {

	return callback_1arg_evaluate(*(*e.ccsne_yields).yield_, Z);

}

