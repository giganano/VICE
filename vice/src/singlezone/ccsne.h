
#ifndef SINGLEZONE_CCSNE_H
#define SINGLEZONE_CCSNE_H

#ifdef __cpluslpus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: ccsne.c
 */
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e);

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
 * source: ccsne.c
 */
extern double get_cc_yield(ELEMENT e, double Z);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_CCSNE_H */

