
#ifndef SINGLEZONE_AGB_H
#define SINGLEZONE_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the mass of a given element produced by AGB stars at the current
 * timestep of a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 			The SINGLEZONE struct associated with the current simulation
 * e: 			The ELEMENT struct to find the total mass yield for
 *
 * Returns
 * =======
 * The mass of the given element in solar masses produced by AGB stars in one
 * timestep from all previous generations of stars.
 *
 * source: agb.c
 */
extern double m_AGB(SINGLEZONE sz, ELEMENT e);

/*
 * Determine the fractional yield of a given element from AGB stars at a
 * given mass and metallicity.
 *
 * Parameters
 * ==========
 * e: 				The element struct containing AGB yield information
 * Z_stars: 		The metallicity by mass Z of the AGB stars
 * turnoff_mass:	The mass of the AGB stars
 *
 * Returns
 * =======
 * The fraction of each AGB star's mass that is converted into the element e
 * under the current yield settings.
 *
 * source: agb.c
 */
extern double get_AGB_yield(ELEMENT e, double Z_stars, double turnoff_mass);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_AGB_H */

