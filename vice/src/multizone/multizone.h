
#ifndef MULTIZONE_MULTIZONE_H
#define MULTIZONE_MULTIZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Links an individual zone in a multizone object to the proper address of a
 * singlezone struct.
 *
 * Parameters
 * ==========
 * mz: 			A pointer to the multizone object
 * address: 	The address of the singlezone object to link
 * zone_index: 	The zone number this singlezone object should correspond to
 *
 * source: multizone.c
 */
extern void link_zone(MULTIZONE *mz, unsigned long address,
	unsigned int zone_index);

/*
 * Runs the multizone simulation under current user settings.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run
 *
 * Returns
 * =======
 * 0 on success, 1 on zone setup failure, 2 on migration normalization
 * error, 3 on tracer particle file I/O error.
 *
 * source: multizone.c
 */
extern unsigned short multizone_evolve(MULTIZONE *mz);

/*
 * Evolve a multizone model under the current settings but ignore enrichment
 * and return only the relevant quantities for the ISM.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone model to run.
 *
 * Returns
 * =======
 * A 3-D double pointer, indexed as ``results[zone][timestep][idx]`` where
 * ``zone`` refers to the N'th zone and ``timestep`` refers to the N'th
 * timestep. ``idx`` maps to a specific quantity as such:
 *
 * 0: Time since the start of the model in Gyr
 * 1: Accretion rate in Msun/yr
 * 2: Star formation rate in Msun/yr
 * 3: ISM mass in Msun
 * 4: Stellar mass in Msun, accounting for recycled stellar envelopes
 *
 * Notes
 * =====
 * This method of evolving the multizone model does not take into account
 * stellar migration due to the computational overhead with fine timestepping
 * or many stellar populations for timestep. It does, however, take into
 * account gas mixing.
 *
 * source: multizone.c
 */
extern double ***multizone_ismonly(MULTIZONE *mz);

/*
 * Runs the multizone simulation under current user settings with tracer
 * particles not tracked at each individual timestep
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run
 *
 * source: multizone.c
 */
extern void multizone_evolve_simple(MULTIZONE *mz);

/*
 * Runs the multizone simulation under current user settings with tracer
 * particle zones tracked at each individual timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run
 *
 * source: multizone.c
 */
extern void multizone_evolve_full(MULTIZONE *mz);

/*
 * Sets up every zone in a multizone object for simulation
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object itself
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: multizone.c
 */
extern unsigned short multizone_setup(MULTIZONE *mz);

/*
 * Frees up the memory allocated in running a multizone simulation. This does
 * not free up the memory stored by simplying having a multizone object in the
 * python interpreter. That is cleared by calling multizone_free.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to clean
 *
 * source: multizone.c
 */
extern void multizone_clean(MULTIZONE *mz);

/*
 * Undo the pieces of preparation to run a multizone simulation that are
 * called from python. This function is invoked when the user cancels their
 * simulation by answer 'no' to whether or not they'd like to overwrite.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to cancel
 *
 * source: multizone.c
 */
extern void multizone_cancel(MULTIZONE *mz);

/*
 * Determine the stellar mass in each zone in a multizone simulation.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for this simulation
 *
 * Returns
 * =======
 * A pointer to the present-day stellar mass in each zone.
 *
 * source: multizone.c
 */
extern double *multizone_stellar_mass(MULTIZONE mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_MDF_H */

