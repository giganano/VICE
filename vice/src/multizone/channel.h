
#ifndef MULTIZONE_CHANNEL_H
#define MULTIZONE_CHANNEL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
extern void from_tracers(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_CHANNEL_H */


