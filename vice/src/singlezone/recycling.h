
#ifndef SINGLEZONE_RECYCLING_H
#define SINGLEZONE_RECYCLING_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the mass recycled from all previous generations of stars for
 * either a given element or the gas supply. For details, see section 3.3 of
 * VICE's science documentation.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 * e: 		A pointer to the element to find the recycled mass. NULL to find
 * 			it for the total ISM gas.
 *
 * Returns
 * =======
 * The recycled mass in Msun
 *
 * source: recycling.c
 */
extern double mass_recycled(SINGLEZONE sz, ELEMENT *e);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_RECYCLING_H */
