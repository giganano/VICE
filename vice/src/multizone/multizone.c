/*
 * This file implements the time evolution of multizone simulations in VICE.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "../tracer.h"
#include "../utils.h"
#include "../io.h"
#include "multizone.h"
#include "tracer.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static unsigned short multizone_timestepper(MULTIZONE *mz);
static void verbosity(MULTIZONE mz);


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
 * header: multizone.h
 */
extern void link_zone(MULTIZONE *mz, unsigned long address,
	unsigned int zone_index) {

	mz -> zones[zone_index] = (SINGLEZONE *) address;

}


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
 * header: multizone.h
 */
extern unsigned short multizone_evolve(MULTIZONE *mz) {

	/*
	 * x differentiates between failed setup and migration matrix failing
	 * the sanity check.
	 */
	unsigned short x = multizone_setup(mz);
	if (x) return x;

	/*
	 * Run either the simple or full evolution depending on the user's
	 * specification at runtime.
	 */
	if ((*mz).simple) {
		multizone_evolve_simple(mz);
	} else {
		multizone_evolve_full(mz);
	}

	/*
	 * Before writing out the tracer particle information, chop off the ones
	 * that were formed in the previous timestep. These stars formed one
	 * timestep after the user's specified ending time, and will mess up
	 * age calculations from the output.
	 */
	tracers_MDF(mz);
	write_multizone_mdf(*mz);

	/* Write the tracer particle data */
	if (!multizone_open_tracer_file(mz)) {
		write_tracers_header(*mz);
		write_tracers_output(*mz);
		multizone_close_tracer_file(mz);
	} else {
		x = 3;
	}

	multizone_clean(mz);
	if ((*mz).verbose) printf("Finished.\n");
	return x;

}


/*
 * Runs the multizone simulation under current user settings with tracer
 * particles not tracked at each individual timestep
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run
 *
 * header: multizone.h
 */
extern void multizone_evolve_simple(MULTIZONE *mz) {

	/*
	 * Allocate memory for the progressbar regardless of verbosity to avoid it
	 * being used uninitialized as a failsafe.
	 */
	PROGRESSBAR *pb = progressbar_initialize((*(*mz).mig).n_zones);
	if ((*mz).verbose) printf("Evolving zones....\n");

	unsigned int i;
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		singlezone_evolve_no_setup_no_clean(mz -> zones[i]);
		if ((*mz).verbose) progressbar_update(pb, i + 1u);
	}
	if ((*mz).verbose) progressbar_finish(pb);
	progressbar_free(pb);

	/*
	 * Set the tracer count to the proper value for computing the MDF
	 *
	 * Note: +1l accounts for time = 0 or final timestep populations,
	 * depending on which one is viewed as the "extra" set.
	 */
	mz -> mig -> tracer_count = (
		(n_timesteps(*(*mz).zones[0]) - BUFFER + 1l) *
		(*(*mz).mig).n_zones *
		(*(*mz).mig).n_tracers
	);
	compute_tracer_masses(mz);

}


/*
 * Runs the multizone simulation under current user settings with tracer
 * particle zones tracked at each individual timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run
 *
 * header: multizone.h
 */
extern void multizone_evolve_full(MULTIZONE *mz) {

	/*
	 * Use the variable n to keep track of the number of outputs. Pull a
	 * local copy of the first zone just for convenience. Lastly, tracer
	 * particles are injected at the end of each timestep, so inject them at
	 * the start of the simulation to account for the first timestep.
	 */
	long n = 0l;
	SINGLEZONE *sz = mz -> zones[0];
	inject_tracers(mz);
	while ((*sz).current_time <= (*sz).output_times[(*sz).n_outputs - 1l]) {
		/*
		 * Run the simulation until the time reaches the final output time
		 * specified by the user. Write to each zone's history.out file
		 * whenever an output time is reached, or if the current timestep is
		 * closer to the next output time than the subsequent timestep.
		 */
		if ((*sz).current_time >= (*sz).output_times[n] ||
			2 * (*sz).output_times[n] < 2 * (*sz).current_time + (*sz).dt) {
			write_multizone_history(*mz);
			n++;
		} else {}
		if (multizone_timestepper(mz)) break;
		verbosity(*mz);
	}
	verbosity(*mz);
	inject_tracers(mz);
	write_multizone_history(*mz);

}


/*
 * Advances all quantities in a multizone object forward one timestep
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to move forward
 *
 * Returns
 * =======
 * 0 while the simulation is running, 1 if the simulation is over
 */
static unsigned short multizone_timestepper(MULTIZONE *mz) {

	update_zone_evolution(mz);
	update_elements(mz);

	/*
	 * Now each element and the ISM in each zone are at the next timestep.
	 * bookkeep the new metallicity and update the MDF in each zone.
	 */
	unsigned int i, j;

	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		SINGLEZONE *sz = mz -> zones[i];
		for (j = 0; j < (*sz).n_elements; j++) {
			sz -> elements[j] -> Z[(*sz).timestep + 1l] = (
				(*(*sz).elements[j]).mass / (*(*sz).ism).mass
			);
		}
		update_MDF(sz);
	}

	/*
	 * Migrating gas and stars before injecting tracers ensures that stars
	 * will never migrate the timestep they're born.
	 */
	migrate(mz);
	inject_tracers(mz);
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> current_time += (*(*mz).zones[i]).dt;
		mz -> zones[i] -> timestep++;
	}

	return ((*(*mz).zones[0]).current_time >
		(*(*mz).zones[0]).output_times[(*(*mz).zones[0]).n_outputs - 1l]);

}


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
 * header: multizone.h
 */
extern unsigned short multizone_setup(MULTIZONE *mz) {

	unsigned int i;
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		if (singlezone_setup(mz -> zones[i])) return 1;
	}

	if (migration_matrix_sanitycheck((*(*mz).mig).gas_migration,
		n_timesteps((*(*mz).zones[0])), (*(*mz).mig).n_zones)) {
		return 2;
	} else {
		mz -> mig -> tracer_count = 0l;
		return 0;
	}

}


/*
 * Frees up the memory allocated in running a multizone simulation. This does
 * not free up the memory stored by simplying having a multizone object in the
 * python interpreter. That is cleared by calling multizone_free.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to clean
 *
 * header: multizone.h
 */
extern void multizone_clean(MULTIZONE *mz) {

	/* clean each singlezone object */
	unsigned int i;
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		singlezone_close_files(mz -> zones[i]);
		singlezone_clean(mz -> zones[i]);
	}

	/* free up each tracer and set the pointer to NULL again */
	unsigned long j;
	for (j = 0l; j < (*(*mz).mig).tracer_count; j++) {
		tracer_free(mz -> mig -> tracers[j]);
	}
	free(mz -> mig -> tracers);
	mz -> mig -> tracers = NULL;

	/* free up the migration matrix */
	free(mz -> mig -> gas_migration);
	mz -> mig -> gas_migration = NULL;

}


/*
 * Undo the pieces of preparation to run a multizone simulation that are
 * called from python. This function is invoked when the user cancels their
 * simulation by answer 'no' to whether or not they'd like to overwrite.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to cancel
 *
 * header: multizone.h
 */
extern void multizone_cancel(MULTIZONE *mz) {

	unsigned int i;
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		singlezone_cancel(mz -> zones[i]);
	}
	free(mz -> mig -> gas_migration);
	mz -> mig -> gas_migration = NULL;

}


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
 * header: multizone.h
 */
extern double *multizone_stellar_mass(MULTIZONE mz) {

	unsigned long i;
	double *mstar = (double *) malloc ((*mz.mig).n_zones * sizeof(double));
	for (i = 0ul; i < (*mz.mig).n_zones; i++) {
		mstar[i] = 0;
	}
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		TRACER t = *(*mz.mig).tracers[i];
		unsigned long timestep = (*mz.zones[0]).timestep;
		
		mstar[t.zone_current] += t.mass * (1 -
			(*(*mz.zones[t.zone_origin]).ssp).crf[
				timestep - t.timestep_origin + 1l
			]);
	}
	return mstar;

}


/*
 * Prints the current time on the same line on the console if the user has
 * specified verbosity.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 */
static void verbosity(MULTIZONE mz) {

	if (mz.verbose) {
		if (!(*mz.zones[0]).verbose) mz.zones[0] -> verbose = 1u;
		singlezone_verbosity(*mz.zones[0]);
	} else {}

}

