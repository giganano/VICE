/*
 * This file implements the functionality of stellar population tracer
 * particles in VICE's multizone simulations.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "../tracer.h"
#include "../utils.h"
#include "tracer.h"

/*
 * Injects tracer particles into a multizone object for the current timestep
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * Notes
 * =====
 * This function updates the tracer count only if the new tracer particles
 * formed before the final output time. This'll ensure that superfluous tracer
 * particles are left out of the output and distribution function calculations.
 *
 * header: tracer.h
 */
extern void inject_tracers(MULTIZONE *mz) {

	if ((*(*mz).zones[0]).current_time <=
		(*(*mz).zones[0]).output_times[(*(*mz).zones[0]).n_outputs - 1l]) {

		unsigned long i, timestep = (*(*mz).zones[0]).timestep;
		MIGRATION *mig = mz -> mig;
		for (i = (*mig).tracer_count;
			i < (*mig).tracer_count + (*mig).n_tracers * (*mig).n_zones;
			i++) {

			SINGLEZONE sz = *(*mz).zones[(*(*mig).tracers[i]).zone_origin];
			TRACER *t = mz -> mig -> tracers[i];
			t -> mass = (*sz.ism).star_formation_rate * sz.dt / (*mig).n_tracers;
			t -> zone_current = (unsigned) (
				(*(*mig).tracers[i]).zone_history[timestep + 1l]);
		}

		mig -> tracer_count += (*mig).n_tracers * (*mig).n_zones;

	} else {}

}

/*
 * Compute the masses of each tracer particle after a multizone simulation in
 * simple mode.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object
 *
 * header: tracer.h
 */
extern void compute_tracer_masses(MULTIZONE *mz) {

	unsigned long i;
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) {
		TRACER *t = (*(*mz).mig).tracers[i];
		SINGLEZONE origin = *(*mz).zones[(*t).zone_origin];

		t -> mass = (
			(*origin.ism).star_formation_history[(*t).timestep_origin] *
			origin.dt / (*(*mz).mig).n_tracers
		);
	}

}

/*
 * Determine the metallicity of a tracer particle.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 * t: 		The tracer particle to determine the metallicity of
 *
 * Returns
 * =======
 * The scaled metallicity of the tracer particle
 *
 * header: tracer.h
 */
extern double tracer_metallicity(MULTIZONE mz, TRACER t) {

	return scale_metallicity(
		(*mz.zones[t.zone_origin]),
		t.timestep_origin
	);

}

/*
 * Allocate memory for the stellar tracer particles
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * header: tracer.h
 */
extern void malloc_tracers(MULTIZONE *mz) {

	unsigned long i, n = (
		(*(*mz).mig).n_zones * (*(*mz).mig).n_tracers *
		n_timesteps(*(*mz).zones[0])
	);
	mz -> mig -> tracers = (TRACER **) malloc (n * sizeof(TRACER *));
	for (i = 0l; i < n; i++) {
		mz -> mig -> tracers[i] = tracer_initialize();
	}

}

