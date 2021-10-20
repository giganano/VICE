
#ifndef SINGLEZONE_ELEMENT_H
#define SINGLEZONE_ELEMENT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Allocates memory for bookkeeping each elements previous ISM metallicity
 * and sets each element to zero.
 *
 * Parameters
 * ==========
 * e: 				A pointer to the element to setup the Z array for
 * n_timesteps: 	The number of elements in this array (i.e. the total
 * 					number of timesteps in the simulation)
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: element.c
 */
extern unsigned short malloc_Z(ELEMENT *e, unsigned long n_timesteps);

/*
 * Updates the mass of a single element at the current timestep.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object currently being simulated
 * e: 		A pointer to the element to update
 *
 * source: element.c
 */
extern void update_element_mass(SINGLEZONE sz, ELEMENT *e);

/*
 * Performs a sanity check on a given element immediately after it's mass
 * was updated for the next timestep.
 *
 * Parameters
 * ==========
 * e: 		A pointer to the element to sanity check
 *
 * source: element.c
 */
extern void update_element_mass_sanitycheck(ELEMENT *e);

/*
 * Determine the [X/H] value for a given element in a zone.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object to pull the ISM mass from
 * e: 		The element to find the [X/H] value for
 *
 * Returns
 * =======
 * [X/H] = log10( mass(element) / mass(ISM) / solar )
 *
 * source: element.c
 */
extern double onH(SINGLEZONE sz, ELEMENT e);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_ELEMENT_H */

