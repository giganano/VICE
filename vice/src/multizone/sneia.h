
#ifndef MULTIZONE_SNEIA_H
#define MULTIZONE_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the total mass production of a given element produced by SNe Ia
 * in each zone.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 * index: 	The index of the element to calculate the yield information for
 *
 * Returns
 * =======
 * The total mass production of the given element in each zone
 *
 * source: sneia.c
 */
extern double *m_sneia_from_tracers(MULTIZONE mz, unsigned short index);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_SNEIA_H */

