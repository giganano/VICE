
#ifndef MULTIZONE_ISM_H
#define MULTIZONE_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Moves the infall rate, total gas mass, and star formation rate in all zones
 * in a multizone simulation forward one timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * Returns
 * =======
 * 0 on success, 1 on an unrecognized mode
 *
 * source: ism.c
 */
extern unsigned short update_zone_evolution(MULTIZONE *mz);

/*
 * Determine the mass outflow rate of each element in each zone of a multizone
 * simulation due solely to entrainment.
 *
 * Parameters
 * ==========
 * mz: 			The multizone object for the current simulation
 *
 * Returns
 * =======
 * mass: A 2D-pointer indexable via [zone][element] containing the mass
 * outflow rate of the given element in Msun / Gyr
 *
 * source: ism.c
 */
extern double **multizone_unretained(MULTIZONE mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_ISM_H */


