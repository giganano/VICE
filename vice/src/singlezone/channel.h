
#ifndef SINGLEZONE_CHANNEL_H
#define SINGLEZONE_CHANNEL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the rate of mass enrichment of a given element at the current
 * timestep from all arbitrary enrichment channels.
 *
 * Parameters
 * ==========
 * sz: 		The SINGLEZONE object for the current simulation
 * e: 		The element to find the rate of mass enrichment for
 *
 * Returns
 * =======
 * The time-derivative of the arbitrary enrichment channels mass enrichment
 * term
 *
 * source: channel.c
 */
extern double mdot(SINGLEZONE sz, ELEMENT e);

/*
 * Obtain the IMF-integrated fractional mass yield of a given element from
 * its internal yield table.
 *
 * Parameters
 * ==========
 * e: 		The element to find the yield for
 * Z: 		The metallicity to look up on the grid
 *
 * Returns
 * =======
 * The interpolated yield off of the stored yield grid within the CHANNEL
 * struct.
 *
 * source: channel.c
 */
extern double get_yield(CHANNEL ch, double Z);

/*
 * Normalize the rate once it is set according to an arbitrary normalization
 * by the user in python.
 *
 * Parameters
 * ==========
 * e: 			The ELEMENT struct to normalize the rate for.
 * length: 		The length of the e -> channels[i] -> rate array
 *
 * source: channel.c
 */
extern void normalize_rates(ELEMENT *e, unsigned long length);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_CHANNEL_H */

