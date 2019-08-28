/* 
 * This file implements the time evolution of a singlezone zone simulation 
 * using the singlezone object declared in objects.h. 
 */ 

#include <stdlib.h>
#include <string.h>  
#include <stdio.h> 
#include "singlezone.h" 
#include "element.h" 
#include "ccsne.h" 
#include "sneia.h" 
#include "agb.h" 
#include "ism.h" 
#include "mdf.h" 
#include "ssp.h" 
#include "io.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static unsigned short singlezone_timestepper(SINGLEZONE *sz); 
static void verbosity(SINGLEZONE sz); 

/* 
 * Allocate memory for and return a pointer to a SINGLEZONE struct. 
 * Automatically initializes all fields to NULL. 
 * 
 * header: singlezone.h 
 */ 
extern SINGLEZONE *singlezone_initialize(void) { 

	SINGLEZONE *sz = (SINGLEZONE *) malloc (sizeof(SINGLEZONE)); 
	sz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	sz -> history_writer = NULL; 
	sz -> mdf_writer = NULL; 
	sz -> output_times = NULL; 
	sz -> elements = NULL; 		/* set by python */ 
	sz -> ism = ism_initialize(); 
	sz -> mdf = mdf_initialize(); 
	sz -> ssp = ssp_initialize(); 
	return sz; 

} 

/* 
 * Free up the memory associated with a singlezone object. 
 * 
 * header: singlezone.h 
 */ 
extern void singlezone_free(SINGLEZONE *sz) { 

	if (sz != NULL) {

		singlezone_close_files(sz); 

		if ((*sz).elements != NULL) { 
			unsigned int i; 
			for (i = 0; i < (*sz).n_elements; i++) { 
				element_free(sz -> elements[i]); 
			} 
			free(sz -> elements); 
			sz -> elements = NULL; 
		} else {} 

		ism_free(sz -> ism); 
		mdf_free(sz -> mdf); 
		ssp_free(sz -> ssp); 

		if ((*sz).name != NULL) { 
			free(sz -> name); 
			sz -> name = NULL; 
		} else {} 

		free(sz); 
		sz = NULL; 

	}

} 

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

	if (singlezone_setup(sz)) return 1; 	/* setup failed */ 
	singlezone_evolve_no_setup_no_clean(sz); 

	/* Normalize the MDF, write it out, close the files */ 
	normalize_MDF(sz); 
	write_mdf_output(*sz); 
	singlezone_close_files(sz); 
	singlezone_clean(sz); 

	return 0; 

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
			write_history_output(*sz); 
			n++; 
		} else {} 
		if (singlezone_timestepper(sz)) break; 
		verbosity(*sz); 
	} 
	if ((*sz).verbose) printf("\n"); 

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

	return (*sz).current_time > (*sz).output_times[(*sz).n_outputs - 1l]; 
	
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
		return 1; 
	} else { 
		write_history_header(*sz); 
		sz -> current_time = 0.0; 
		sz -> timestep = 0l; 
		write_mdf_header(*sz); 
	} 

	unsigned int i; 
	for (i = 0; i < (*sz).n_elements; i++) { 
		/* 
		 * The singlezone object always allocates memory for 10 timesteps 
		 * beyond the ending time as a safeguard against memory errors. 
		 */ 
		if (malloc_Z(sz -> elements[i], n_timesteps(*sz))) { 
			return 1; 
		} else {
			sz -> elements[i] -> mass = 0.0; 
			sz -> elements[i] -> Z[0l] = 0.0; 
		} 
	} 

	/* 
	 * Setup the cumulative return fraction, main sequence mass fraction, 
	 * metallicity distribution function, SNe Ia rates, and gas evolution. 
	 */ 
	if (setup_CRF(sz)) { 
		return 1; 
	} else if (setup_MSMF(sz)) { 
		return 1; 
	} else if (setup_MDF(sz)) { 
		return 1; 
	} else if (setup_RIa(sz)) { 
		return 1; 
	} else if (setup_gas_evolution(sz)) { 
		return 1; 
	} else { 
		return 0; 
	}

} 

/* 
 * Frees up the memory allocated in running a singlezone simulation. This does 
 * not free up the memory stored by simpling having a singlezone object in the 
 * python interpreter. That is cleared by calling singlezone_free. 
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
		free(sz -> elements[i] -> Z); 
		free(sz -> elements[i] -> Zin); 
		free(sz -> elements[i] -> ccsne_yields -> yield_); 
		free(sz -> elements[i] -> sneia_yields -> RIa); 
		free(sz -> elements[i] -> agb_grid -> grid); 
		free(sz -> elements[i] -> agb_grid -> m); 
		free(sz -> elements[i] -> agb_grid -> z); 
		sz -> elements[i] -> Z = NULL; 
		sz -> elements[i] -> Zin = NULL; 
		sz -> elements[i] -> ccsne_yields -> yield_ = NULL; 
		sz -> elements[i] -> sneia_yields -> RIa = NULL; 
		sz -> elements[i] -> agb_grid -> grid = NULL; 
		sz -> elements[i] -> agb_grid -> m = NULL; 
		sz -> elements[i] -> agb_grid -> z = NULL; 
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

	unsigned int i; 
	for (i = 0; i < (*sz).n_elements; i++) {
		free(sz -> elements[i] -> Zin); 
		free(sz -> elements[i] -> ccsne_yields -> yield_); 
		if (!strcmp((*(*(*sz).elements[i]).sneia_yields).dtd, "custom")) { 
			/* RIa needs freed only if it was custom */ 
			free(sz -> elements[i] -> sneia_yields -> RIa); 
			sz -> elements[i] -> sneia_yields -> RIa = NULL; 
		} else {} 
		free(sz -> elements[i] -> agb_grid -> grid); 
		free(sz -> elements[i] -> agb_grid -> m); 
		free(sz -> elements[i] -> agb_grid -> z); 
		sz -> elements[i] -> Zin = NULL; 
		sz -> elements[i] -> ccsne_yields -> yield_ = NULL; 
		sz -> elements[i] -> sneia_yields -> RIa = NULL; 
		sz -> elements[i] -> agb_grid -> grid = NULL; 
		sz -> elements[i] -> agb_grid -> m = NULL; 
		sz -> elements[i] -> agb_grid -> z = NULL; 
	} 
	free(sz -> ism -> specified); 
	free(sz -> ism -> eta); 
	free(sz -> ism -> enh); 
	free(sz -> ism -> tau_star); 

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
 * Prints the current time on the same line on the console if the user has 
 * specified verbosity. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 */ 
static void verbosity(SINGLEZONE sz) {

	if (sz.verbose) {
		printf("\rCurrent Time: %.2f Gyr", sz.current_time); 
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
extern double get_stellar_mass(SINGLEZONE sz) {

	unsigned long i; 
	double mass = 0; 
	for (i = 0l; i < sz.timestep; i++) {
		mass += ((*sz.ism).star_formation_history[sz.timestep - i] * sz.dt * 
			(1 - (*sz.ssp).crf[i])); 
	} 
	return mass; 

} 


