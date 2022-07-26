
#ifndef MULTIZONE_RECYCLING_H
#define MULTIZONE_RECYCLING_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Compute the mass of the index'th element added back to the ISM by recycled
 * stellar envelopes. Zones with instantaneous recycling will behave as such,
 * but zones that produce tracer particles will re-enrich their current zone,
 * even if their current has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to re-enrich
 * index: 	The element's index in each of mz's singlezone objects.
 *
 * Returns
 * =======
 * A pointer containing an entry for each of the zones in the multizone model.
 * Each element contains the mass in solar masses of the index'th element
 * re-enriched to the ISM by recycled stellar envelopes.
 *
 * source: recycling.c
 */
extern double *recycled_mass(MULTIZONE mz, unsigned int index);

/*
 * Determine the amount of ISM gas recycled from stars in each zone in a
 * multizone simulation. Just as is the case with re-enrichment of metals,
 * zones with instantaneous recycling will behave as such, but zones with
 * continuous recycling will produce tracer particles that re-enrich their
 * current zone, even if that zone has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for this simulation
 *
 * Returns
 * =======
 * An array of doubles, each element is the mass in Msun of ISM gas returned
 * to each zone at the current timestep.
 *
 * source: recycling.c
 */
extern double *gas_recycled_in_zones(MULTIZONE mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_RECYCLING_H */

