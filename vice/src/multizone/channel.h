
#ifndef MULTIZONE_CHANNEL_H
#define MULTIZONE_CHANNEL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the total mass of a given element produced through custom
 * enrichment channels in each zone.
 *
 * Parameters
 * ==========
 * mz:		The multizone object for the current simulation.
 * index: 	The index of the element to calculate the yield information for
 *
 * Returns
 * =======
 * The total mass production of the given element in each zone.
 *
 * Notes
 * =====
 * This function also adds the unretained mass from each additional enrichment
 * channel to the outflow, following the built-in AGB star, CCSN, and SN Ia
 * enrichment channels.
 *
 * source: channel.c
 */
extern double *m_channels_from_tracers(MULTIZONE *mz, unsigned short index);

#if 0
/*
 * Enrichh all elements in a multizone simulation from all custom enrichment
 * channels from all tracer particles in the simulation.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 *
 * source: channel.c
 */
extern void channels_from_tracers(MULTIZONE *mz);
#endif

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_CHANNEL_H */


