/*
 * This file implements the interaction between the hydrodiskstars object and
 * and the multizone object, specifically the fast-tracked star particle setup.
 */


#include <stdlib.h>
#include "hydrodiskstars.h"
#include "../toolkit/hydrodiskstars.h"
#include "../utils.h"
#include "../singlezone.h"

/* The hydrodiskstars object that drives this module */
static HYDRODISKSTARS *HDS;


/*
 * Set the hydrodiskstars object globally.
 *
 * Parameters
 * ==========
 * address: The address of the hydrodiskstars object
 *
 * Notes
 * =====
 * This is necessary to avoid issues with the Cython compiler. Since the
 * multizone and hydrodiskstars objects are separate, the _hds attribute of
 * the c_hydrodiskstars object cannot be accessed by the multizone object.
 *
 * header: hydrodiskstars.h
 */
extern void set_hydrodiskstars_object(unsigned long address) {

	HDS = (HYDRODISKSTARS *) ((void *) address);

}


/*
 * Setup the zone history for a single tracer object born in a given zone and
 * at a given timestep.
 *
 * Parameters
 * ==========
 * mz: 				The multizone object
 * hds: 			The hydrodiskstars object
 * t: 				A pointer to the tracer object being set up
 * birth_zone: 		The zone of birth
 * birth_timestep: 	The timestep of birth
 * analog_index: 	The index of the analog star particle in the hds data
 *
 * Returns
 * =======
 * 0 on success, 1 on failure.
 *
 * header: hydrodiskstars.h
 */
extern unsigned short setup_hydrodisk_tracer(MULTIZONE mz, TRACER *t,
	unsigned int birth_zone, unsigned long birth_timestep, long analog_index) {

	/* The timestep size plus time and radius at which the star is born */
	double dt = (*mz.zones[0]).dt;
	double birth_time = birth_timestep * dt;
	double birth_radius = (
		((*HDS).rad_bins[birth_zone] + (*HDS).rad_bins[birth_zone + 1u]) / 2
	);

	/* In case of sudden migration, this can't be done in the for-loop */
	double migration_time = rand_range(birth_time, HYDRODISK_END_TIME);

	/*
	 * The analog star particle will already be assigned by calling the
	 * hydrodiskstars object in python, retaining the user's ability to write
	 * additional output when subclassing the hydrodiskstars object.
	 */
	unsigned long i, N = n_timesteps(*mz.zones[0]);
	t -> zone_history = (int *) malloc (N * sizeof(int));

	for (i = 0ul; i < N; i++) {

		if (i < birth_timestep) {
			/* Zone number is always -1 until it is born */
			t -> zone_history[i] = -1;

		} else if (i == birth_timestep || birth_timestep >= N - BUFFER) {
			/*
			 * This is either the timestep of birth, or the star forms in the
			 * buffer timesteps. In either case, the zone number must be the
			 * birth zone.
			 */
			t -> zone_history[i] = (signed) birth_zone;

		} else if (i >= N - BUFFER) {
			/*
			 * If this timestep is in the buffer, assign it to value from
			 * just outside the buffer.
			 */
			t -> zone_history[i] = (*t).zone_history[N - BUFFER - 1ul];

		} else if (mz.simple && i != N - BUFFER - 1ul) {
			/*
			 * If running in simple mode, the zone history should always be
			 * the birth zone right up until the buffer, at which point it
			 * switches. The second condition in the if statement allows this
			 * algorithm to naturally proceed to the case-switch block in
			 * below in the else-condition for exactly one iteration of the
			 * for-loop to achieve this.
			 */
			t -> zone_history[i] = (signed) birth_zone;

		} else {
			/*
			 * At this intermediate time, use the calczone_* functions that
			 * the hydrodiskstars object employs anyway to determine the zone
			 * number.
			 */

			switch(checksum((*HDS).mode)) {

				case LINEAR_MIGRATION:
					t -> zone_history[i] = (int) calczone_linear(*HDS,
						birth_time, birth_radius, HYDRODISK_END_TIME,
						analog_index, i * dt);
					break;

				case SUDDEN_MIGRATION:
					t -> zone_history[i] = (int) calczone_sudden(*HDS,
						migration_time, birth_radius, analog_index, i * dt);
					break;

				case DIFFUSION_MIGRATION:
					t -> zone_history[i] = (int) calczone_diffusive(*HDS,
						birth_time, birth_radius, HYDRODISK_END_TIME,
						analog_index, i * dt);
					break;

				default:
					return 1u; /* error handling */

			}

		}

	}

	t -> timestep_origin = birth_timestep;
	t -> zone_origin = birth_zone;
	if (mz.simple) {
		t -> zone_current = (unsigned) t -> zone_history[N - BUFFER];
	} else {
		t -> zone_current = birth_zone;
	}
	return 0u;

}

