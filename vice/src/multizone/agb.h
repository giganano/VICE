
#ifndef MULTIZONE_AGB_H
#define MULTIZONE_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the mass of a given element produced by AGB stars in each
 * zone.
 *
 * Parameters
 * ==========
 * mz: 			The multizone object for the current simulation
 * index: 		The index of the element to determine the mass production for
 *
 * Returns
 * =======
 * The mass of the given element produced in each zone in the next timestep by
 * AGB stars.
 *
 * source: agb.c
 */
extern double *m_AGB_from_tracers(MULTIZONE mz, unsigned short index);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_AGB_H */
