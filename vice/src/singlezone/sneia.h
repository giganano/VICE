
#ifndef SINGLEZONE_SNEIA_H
#define SINGLEZONE_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the rate of mass enrichment of a given element at the current
 * timestep from SNe Ia. See section 4.3 of VICE's science documentation for
 * further details.
 *
 * Parameters
 * ==========
 * sz: 		The SINGLEZONE object for the current simulation
 * e: 		The element to find the rate of mass enrichment for
 *
 * Returns
 * =======
 * The time-derivative of the type Ia supernovae mass enrichment term
 *
 * source: sneia.c
 */
extern double mdot_sneia(SINGLEZONE sz, ELEMENT e);

/*
 * Obtain the IMF-integrated fractional mass yield of a given element from its
 * internal yield table.
 *
 * Parameters
 * ==========
 * e: 			The element to find the yield for
 * Z: 			The metallicity to look up on the grid
 *
 * Returns
 * =======
 * The interpolated yield off of the stored yield grid within the ELEMENT
 * struct.
 *
 * source: sneia.c
 */
extern double get_ia_yield(ELEMENT e, double Z);

/*
 * Setup the SNe Ia rate in preparation for a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object that is about to be ran
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: sneia.c
 */
extern unsigned short setup_RIa(SINGLEZONE *sz);

/*
 * Normalize the SNe Ia delay-time distribution once it is set according to
 * an arbitrary normalization.
 *
 * Parameters
 * ==========
 * e: 			The ELEMENT struct to normalize the DTD for
 * length: 		The length of the e -> sneia_yields -> RIa array
 *
 * source: sneia.c
 */
extern void normalize_RIa(ELEMENT *e, unsigned long length);

#ifdef __cpluslpus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_SNEIA_H */
