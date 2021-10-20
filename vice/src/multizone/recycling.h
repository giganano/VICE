
#ifndef MULTIZONE_RECYCLING_H
#define MULTIZONE_RECYCLING_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Re-enriches each zone in a multizone simulation. Zones with instantaneous
 * recycling will behave as such, but zones with continuous recycling will
 * produce tracer particles that re-enrich their current zone, even if that
 * zone has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to re-enrich
 *
 * source: recycling.c
 */
extern void recycle_metals_from_tracers(MULTIZONE *mz, unsigned int index);

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

