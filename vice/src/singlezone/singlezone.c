/*
 * This file implements the time evolution of a singlezone simulation using
 * VICE's singlezone object.
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "../singlezone.h"
#include "../ssp.h"
#include "../io.h"
#include "singlezone.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static unsigned short singlezone_timestepper(SINGLEZONE *sz);

/* A progressbar that will run for the singlezone object */
static PROGRESSBAR *PB = NULL;


/*
 * Obtain the memory address of a singlezone object as a long.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object to obtain the memory address for
 *
 * header: singlezone.h
 */
extern long singlezone_address(SINGLEZONE *sz) {

	return (long) ((void *) sz);

}


/*
 * Runs the singlezone simulation under current user settings.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run
 *
 * Returns
 * =======
 * 0 on success, 1 on setup failure
 *
 * header: singlezone.h
 */
extern unsigned short singlezone_evolve(SINGLEZONE *sz) {

	if (singlezone_setup(sz)) return 1u; 	/* setup failed */
	singlezone_evolve_no_setup_no_clean(sz);

	/* Normalize the MDF, write it out, close the files */
	normalize_MDF(sz);
	write_mdf_output(*sz);
	singlezone_close_files(sz);
	singlezone_clean(sz);

	return 0u;

}


/*
 * Evolves a singlezone simulation under current user settings, but does not
 * write the MDF output or normalization.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run
 *
 * header: singlezone.h
 */
extern void singlezone_evolve_no_setup_no_clean(SINGLEZONE *sz) {

	long n = 0l; 	/* keep track of the number of outputs */
	while ((*sz).current_time <= (*sz).output_times[(*sz).n_outputs - 1l]) {
		/*
		 * Run the simulation until the time reaches the final output time
		 * specified by the user. Write to the history.out file whenever an
		 * output time is reached, or if the current timestep is closer to the
		 * next output time than the subsequent timestep.
		 */
		if ((*sz).current_time >= (*sz).output_times[n] ||
			2 * (*sz).output_times[n] < 2 * (*sz).current_time + (*sz).dt) {
			write_singlezone_history(*sz);
			n++;
		} else {}
		if (singlezone_timestepper(sz)) break;
		singlezone_verbosity(*sz);
	}
	singlezone_verbosity(*sz);
	write_singlezone_history(*sz);

}


/*
 * Advances all quantities in a singlezone object forward one timestep
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to advance one timestep
 *
 * Returns
 * =======
 * 0 while the simulation is running, 1 if the simulation is over
 */
static unsigned short singlezone_timestepper(SINGLEZONE *sz) {

	/*
	 * Timestep number and current time get moved LAST. This is taken into
	 * account in each of the following subroutines.
	 */
	unsigned int i;
	update_gas_evolution(sz);
	for (i = 0; i < (*sz).n_elements; i++) {
		update_element_mass(*sz, (*sz).elements[i]);
		/* Now the ISM and this element are at the next timestep */
		sz -> elements[i] -> Z[(*sz).timestep + 1l] = (
			(*(*sz).elements[i]).mass / (*(*sz).ism).mass);
	}
	update_MDF(sz);

	sz -> current_time += (*sz).dt;
	sz -> timestep++;

	return (*sz).current_time >= (*sz).output_times[(*sz).n_outputs - 1l];
	
}


/*
 * Setup the singlezone object for simulation.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to do the setup for
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * header: singlezone.h
 */
extern unsigned short singlezone_setup(SINGLEZONE *sz) {

	/* Open output files and write headers */
	if (singlezone_open_files(sz)) {
		return 1u;
	} else {
		write_history_header(*sz);
		sz -> current_time = 0.0;
		sz -> timestep = 0l;
		write_mdf_header(*sz);
	}

	/*
	 * Change Notes
	 * ============
	 * The for-loop in the final else statement of this function used to be
	 * here. It was moved to its current position after a primordial
	 * abundance was taken into account, for which the ISM mass is necessary.
	 * This is not set until after setup_gas_evolution() is called.
	 */

	/*
	 * Setup the cumulative return fraction, main sequence mass fraction,
	 * metallicity distribution function, SNe Ia rates, and gas evolution.
	 */

	if (setup_CRF(sz)) return 1u;
	if (setup_MSMF(sz)) return 1u;
	if (setup_MDF(sz)) return 1u;
	if (setup_RIa(sz)) return 1u;
	if (setup_gas_evolution(sz)) return 1u;
	unsigned int i;
	for (i = 0u; i < (*sz).n_elements; i++) {
		/*
		 * The singlezone object always allocates memory for 10 timesteps
		 * beyond the ending time as a safeguard against memory errors.
		 */
		if (malloc_Z(sz -> elements[i], n_timesteps(*sz))) return 1u;
		sz -> elements[i] -> mass = (
			(*(*sz).elements[i]).primordial * (*(*sz).ism).mass
		);
		sz -> elements[i] -> Z[0l] = (
			(*(*sz).elements[i]).mass / (*(*sz).ism).mass
		);
	}

	return 0u;

}


/*
 * Frees up the memory allocated in running a singlezone simulation. These
 * values are objects that are stored at the python level and copied at
 * runtime. This does not free up the memory stored by simpling having a
 * singlezone object in the python interpreter. That is cleared by calling
 * singlezone_free.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object to clean
 *
 * header: singlezone.h
 */
extern void singlezone_clean(SINGLEZONE *sz) {

	unsigned int i;
	for (i = 0; i < (*sz).n_elements; i++) {
		if ((*(*(*(*sz).elements[i]).agb_grid).interpolator).zcoords != NULL) {
			free(sz -> elements[i] -> agb_grid -> interpolator -> xcoords);
			free(sz -> elements[i] -> agb_grid -> interpolator -> ycoords);
			free(sz -> elements[i] -> agb_grid -> interpolator -> zcoords);
			sz -> elements[i] -> agb_grid -> interpolator -> xcoords = NULL;
			sz -> elements[i] -> agb_grid -> interpolator -> ycoords = NULL;
			sz -> elements[i] -> agb_grid -> interpolator -> zcoords = NULL;
		} else {}
		free(sz -> elements[i] -> Z);
		free(sz -> elements[i] -> Zin);
		free(sz -> elements[i] -> sneia_yields -> RIa);
		sz -> elements[i] -> Z = NULL;
		sz -> elements[i] -> Zin = NULL;
		sz -> elements[i] -> sneia_yields -> RIa = NULL;
	}
	free(sz -> ism -> specified);
	free(sz -> ism -> star_formation_history);
	free(sz -> ism -> eta);
	free(sz -> ism -> enh);
	free(sz -> ism -> tau_star);
	free(sz -> mdf -> abundance_distributions);
	free(sz -> mdf -> ratio_distributions);
	free(sz -> ssp -> crf);
	free(sz -> ssp -> msmf);
	free(sz -> output_times);
	sz -> ism -> specified = NULL;
	sz -> ism -> star_formation_history = NULL;
	sz -> ism -> eta = NULL;
	sz -> ism -> enh = NULL;
	sz -> ism -> tau_star = NULL;
	sz -> mdf -> abundance_distributions = NULL;
	sz -> mdf -> ratio_distributions = NULL;
	sz -> ssp -> crf = NULL;
	sz -> ssp -> msmf = NULL;
	sz -> output_times = NULL;
	sz -> current_time = 0;
	sz -> timestep = 0l;

}


/*
 * Undo the pieces of preparation to run a singlezone simulation that are
 * called from python. This function is invoked when the user cancels their
 * simulation by answering 'no' to whether or not they'd like to overwrite.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to cancel
 *
 * header: singlezone.h
 */
extern void singlezone_cancel(SINGLEZONE *sz) {

	/*
	 * This function gets called in various situations, and it is difficult
	 * to know which variables will be NULL, and which ones won't in any
	 * given situation. Hence we check for NULL values in all cases.
	 */

	unsigned int i;
	for (i = 0; i < (*sz).n_elements; i++) {
		if ((*(*sz).elements[i]).Zin != NULL) {
			free(sz -> elements[i] -> Zin);
			sz -> elements[i] -> Zin = NULL;
		} else {}
		if ((*(*(*sz).elements[i]).sneia_yields).RIa != NULL) {
			free(sz -> elements[i] -> sneia_yields -> RIa);
			sz -> elements[i] -> sneia_yields -> RIa = NULL;
		} else {}
		if ((*(*(*(*sz).elements[i]).agb_grid).interpolator).xcoords != NULL) {
			free(sz -> elements[i] -> agb_grid -> interpolator -> xcoords);
			sz -> elements[i] -> agb_grid -> interpolator -> xcoords = NULL;
		} else {}
		if ((*(*(*(*sz).elements[i]).agb_grid).interpolator).ycoords != NULL) {
			free(sz -> elements[i] -> agb_grid -> interpolator -> ycoords);
			sz -> elements[i] -> agb_grid -> interpolator -> ycoords = NULL;
		} else {}
		if ((*(*(*(*sz).elements[i]).agb_grid).interpolator).zcoords != NULL) {
			free(sz -> elements[i] -> agb_grid -> interpolator -> zcoords);
			sz -> elements[i] -> agb_grid -> interpolator -> zcoords = NULL;
		} else {}
	}

	if ((*(*sz).ism).specified != NULL) {
		free(sz -> ism -> specified);
		sz -> ism -> specified = NULL;
	} else {}
	if ((*(*sz).ism).eta != NULL) {
		free(sz -> ism -> eta);
		sz -> ism -> eta = NULL;
	} else {}
	if ((*(*sz).ism).enh != NULL) {
		free(sz -> ism -> enh);
		sz -> ism -> enh = NULL;
	} else {}
	if ((*(*sz).ism).tau_star != NULL) {
		free(sz -> ism -> tau_star);
		sz -> ism -> tau_star = NULL;
	} else {}

}


/*
 * Determine the number of timesteps that memory is allocated for in the
 * singlezone object.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for this simulation
 *
 * Returns
 * =======
 * The final output time divided by the timestep size plus 10.
 *
 * header: singlezone.h
 */
extern unsigned long n_timesteps(SINGLEZONE sz) {

	/*
	 * By design, memory is allocated for 10 timesteps beyond the final
	 * execution time so as to prevent memory errors.
	 */
	return BUFFER + (sz.output_times[sz.n_outputs - 1l] / sz.dt);

}


/*
 * Handles the progressbar for a singlezone object as it runs.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * header: singlezone.h
 */
extern void singlezone_verbosity(SINGLEZONE sz) {

	if (sz.verbose) {
		if (PB == NULL) {
			PB = progressbar_initialize(n_timesteps(sz) - BUFFER);
			PB -> custom_left_hand_side = 1u;
			PB -> eta_mode = 875u;
		} else {}
		char current_time[100];
		sprintf(current_time, "Current Time: %.2f Gyr", sz.current_time);
		progressbar_set_left_hand_side(PB, current_time);
		if (sz.timestep <= (*PB).maxval) progressbar_update(PB, sz.timestep);
		if (sz.timestep == (*PB).maxval) {
			progressbar_finish(PB);
			progressbar_free(PB);
			PB = NULL;
		} else {}
	} else {}

}


/*
 * Determine the stellar mass in a singlezone simulation
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * Returns
 * =======
 * The instantaneous stellar mass in Msun
 *
 * header: singlezone.h
 */
extern double singlezone_stellar_mass(SINGLEZONE sz) {

	/*
	 * Only previous timesteps are considered - stars currently forming not
	 * considered as stellar mass until at least one timestep old.
	 */
	unsigned long i;
	double mass = 0;
	for (i = 0l; i < sz.timestep; i++) {
		mass += ((*sz.ism).star_formation_history[sz.timestep - i - 1l] *
			sz.dt * (1 - (*sz.ssp).crf[i + 1l]));
	}
	return mass;

}

