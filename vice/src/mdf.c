/* 
 * This file implemements the calculation of stellar metallicity distribution 
 * functions (MDFs). 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "element.h" 
#include "mdf.h" 
#include "utils.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void update_MDF_from_tracer(MULTIZONE *mz, TRACER t); 
static void reset_MDF(SINGLEZONE *sz); 

/* 
 * Allocate memory for and return a pointer to an MDF struct. Initializes all 
 * fields to NULL. 
 * 
 * header: mdf.h 
 */ 
extern MDF *mdf_initialize(void) {

	MDF *mdf = (MDF *) malloc (sizeof(MDF)); 
	mdf -> abundance_distributions = NULL; 
	mdf -> ratio_distributions = NULL; 
	mdf -> bins = NULL; 
	return mdf; 

} 

/* 
 * Free up the memory stored in an MDF struct. 
 * 
 * header: mdf.h 
 */ 
extern void mdf_free(MDF *mdf) { 

	if (mdf != NULL) {

		if ((*mdf).abundance_distributions != NULL) {
			free(mdf -> abundance_distributions); 
			mdf -> abundance_distributions = NULL; 
		} else {} 

		if ((*mdf).ratio_distributions != NULL) {
			free(mdf -> ratio_distributions); 
			mdf -> ratio_distributions = NULL; 
		} else {} 

		if ((*mdf).bins != NULL) {
			free(mdf -> bins); 
			mdf -> bins = NULL; 
		} else {} 

		free(mdf); 
		mdf = NULL; 

	} else {}  

} 

/* 
 * Setup the metallicity distribution functions. This does nothing more and 
 * nothing less than give each abundance and ratio distribution an array of 
 * zeroes representing the value in each bin. These arrays will be modified 
 * at each timestep as the simulation evolves. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: mdf.h 
 */ 
extern unsigned short setup_MDF(SINGLEZONE *sz) {

	/* 
	 * The number of bins and binspace will be set by python. Give each element 
	 * an array for the abundance distribution in each bin and initialize its 
	 * value to zero. 
	 */ 
	unsigned long i; 
	unsigned int j; 
	sz -> mdf -> abundance_distributions = (double **) malloc ((*sz).n_elements * 
		sizeof(double *)); 
	if ((*(*sz).mdf).abundance_distributions == NULL) {
		return 1; 
	} else {
		for (j = 0; j < (*sz).n_elements; j++) {
			sz -> mdf -> abundance_distributions[j] = (double *) malloc (
				(*(*sz).mdf).n_bins * sizeof(double)); 
			if ((*(*sz).mdf).abundance_distributions[j] == NULL) {
				return 1; 
			} else {
				for (i = 0l; i < (*(*sz).mdf).n_bins; i++) {
					sz -> mdf -> abundance_distributions[j][i] = 0.0; 
				} 
			} 
		} 
	} 

	/* 
	 * The number of abundance ratios is n choose 2 = n(n - 1)/2. Initialize 
	 * each abundance ratio to an array of zeroes as well. 
	 */ 
	// unsigned int n_ratios = (*sz).n_elements * ((*sz).n_elements - 1) / 2; 
	unsigned int n_ratios = choose((*sz).n_elements, 2); 
	sz -> mdf -> ratio_distributions = (double **) malloc (n_ratios * 
		sizeof(double *)); 
	if ((*(*sz).mdf).ratio_distributions == NULL) {
		return 1; 
	} else {
		for (j = 0; j < n_ratios; j++) {
			sz -> mdf -> ratio_distributions[j] = (double *) malloc (
				(*(*sz).mdf).n_bins * sizeof(double)); 
			if ((*(*sz).mdf).ratio_distributions == NULL) {
				return 1; 
			} else {
				for (i = 0l; i < (*(*sz).mdf).n_bins; i++) {
					sz -> mdf -> ratio_distributions[j][i] = 0.0; 
				} 
			} 
		} 
	} 

	return 0; 

}

/* 
 * Update the metallicity distribution function. This simply determines the bin 
 * number for each [X/H] abundance and [X/Y] abundance ratio in the specified 
 * binspace and increments it by the star formation rate. The prefactors are 
 * ignored because they cancel in normalization at the end of the simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to update the MDF for 
 * 
 * header: mdf.h 
 */ 
extern void update_MDF(SINGLEZONE *sz) {

	/* ---------------------- for each tracked element ---------------------- */ 
	unsigned int i, j; 
	for (i = 0; i < (*sz).n_elements; i++) {
		#if 0
		double onH = log10( 		/* [X/H] for this element */ 
			((*(*sz).elements[i]).mass / (*(*sz).ism).mass) / 
			(*(*sz).elements[i]).solar
		); 
		#endif 
		double onH1 = onH(*sz, *(*sz).elements[i]); 
		/* The bin number for [X/H] */ 
		long bin = get_bin_number((*(*sz).mdf).bins, 
			(*(*sz).mdf).n_bins, onH1); 
		if (bin != -1l) {
			/* 
			 * Increment the bin number by the star formation rate. Prefactors 
			 * cancel in normalization at the end of the simulation 
			 */ 
			sz -> mdf -> abundance_distributions[i][bin] += (
				*(*sz).ism).star_formation_rate; 
		} else {} 
	} 

	/* ---------------------- for each abundance ratio ---------------------- */ 
	unsigned int n = 0; 
	for (i = 1; i < (*sz).n_elements; i++) {
		for (j = 0; j < i; j++) {
			#if 0
			double onH1 = log10(		/* [X/H] for this element */ 
				((*(*sz).elements[i]).mass / (*(*sz).ism).mass) / 
				(*(*sz).elements[i]).solar
			); 
			double onH2 = log10(		/* [Y/H] for this element */ 
				((*(*sz).elements[j]).mass / (*(*sz).ism).mass) / 
				(*(*sz).elements[j]).solar
			); 
			#endif 
			double onH1 = onH(*sz, *(*sz).elements[i]); 
			double onH2 = onH(*sz, *(*sz).elements[j]); 
			/* The bin number for [X/Y] */ 
			long bin = get_bin_number((*(*sz).mdf).bins, 
				(*(*sz).mdf).n_bins, onH1 - onH2); 
			if (bin != -1l) {
				/* 
				 * Again increment the bin number by the star formation rate. 
				 * Prefactors cancel in normalization at the end of the 
				 * simulation. 
				 */ 
				sz -> mdf -> ratio_distributions[n][bin] += (
					*(*sz).ism).star_formation_rate; 
			} else {} 
			n++; 
		}
	}

} 

/* 
 * Normalize the metallicity distribution functions stored within a singlezone 
 * object in prep for write-out at the end of a simulation. This converts each 
 * distribution into a probability distribution function where the integral 
 * over the extent of the user-specified binspace is equal to 1. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object whose simulation just finished 
 * 
 * header: mdf.h 
 */ 
extern void normalize_MDF(SINGLEZONE *sz) {

	/* ---------------------- for each tracked element ---------------------- */ 
	unsigned long i; 
	unsigned int j; 
	for (j = 0; j < (*sz).n_elements; j++) { 
		double integral = 0.0; 
		for (i = 0l; i < (*(*sz).mdf).n_bins; i++) { 
			/* Sum up the value of the distribution times each bin width */ 
			integral += (*(*sz).mdf).abundance_distributions[j][i] * (
				(*(*sz).mdf).bins[i + 1l] - (*(*sz).mdf).bins[i]); 
		} 
		for (i = 0l; i < (*(*sz).mdf).n_bins; i++) {
			/* Divide by the total integral to convert to a PDF */ 
			sz -> mdf -> abundance_distributions[j][i] /= integral; 
		} 
	} 

	/* ---------------------- for each abundance ratio ---------------------- */
	unsigned int n_ratios = choose((*sz).n_elements, 2); 
	for (j = 0; j < n_ratios; j++) {
		double integral = 0.0; 
		for (i = 0l; i < (*(*sz).mdf).n_bins; i++) {
			/* Sum up the value of the distribution times each bin width */ 
			integral += (*(*sz).mdf).ratio_distributions[j][i] * (
				(*(*sz).mdf).bins[i + 1l] - (*(*sz).mdf).bins[i]); 
		} 
		for (i = 0l; i < (*(*sz).mdf).n_bins; i++) {
			/* Divide by the total integral to convert to a PDF */ 
			sz -> mdf -> ratio_distributions[j][i] /= integral; 
		} 
	} 

}

/* 
 * Resets all MDFs in a multizone object and fills them with the data from 
 * its tracer particles. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to redo the MDF for 
 * 
 * header: mdf.h 
 */ 
extern void tracers_MDF(MULTIZONE *mz) {

	unsigned long i; 
	for (i = 0l; i < (*(*mz).mig).n_zones; i++) { 
		/* First reset the MDF in each zone ... */ 
		reset_MDF(mz -> zones[i]); 
	} 
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) {
		/* ... then update with each tracer particle ... */ 
		update_MDF_from_tracer(mz, *(*(*mz).mig).tracers[i]); 
		if ((*mz).verbose) {
			printf("\rProgress: %.1f%%", 
				i * 100.0 / (*(*mz).mig).tracer_count); 
		} else {} 
	} 
	if ((*mz).verbose) printf("\n"); 
	for (i = 0l; i < (*(*mz).mig).n_zones; i++) {
		/* ... and finally normalize it within each zone */ 
		normalize_MDF(mz -> zones[i]); 
	}

} 

/* 
 * Updates the MDF of a multizone object given a tracer particle. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object with the MDF to update 
 * t: 		The tracer particle to update the MDF from 
 */ 
static void update_MDF_from_tracer(MULTIZONE *mz, TRACER t) {

	SINGLEZONE *origin = (*mz).zones[t.zone_origin]; 
	SINGLEZONE *final = (*mz).zones[t.zone_current]; 

	unsigned int i; 
	/* ---------------------- for each tracked element ---------------------- */
	for (i = 0; i < (*origin).n_elements; i++) {

		/* 
		 * The value of [X/H] of the ISM for the i'th element at the timestep 
		 * and in the zone that the tracer particle formed. Get the bin number 
		 * of this value and increment that bin in the FINAL zone by the mass 
		 * of the tracer particle (prefactors cancel in normalization). 
		 */ 
		double onH_ = log10( 
			/* trailing underscore to not override function in element.h */ 
			(*(*origin).elements[i]).Z[t.timestep_origin] / 
			(*(*origin).elements[i]).solar 
		); 

		long bin = get_bin_number(
			(*(*final).mdf).bins, 
			(*(*final).mdf).n_bins, 
			onH_
		); 
		if (bin != -1l) {
			final -> mdf -> abundance_distributions[i][bin] += t.mass; 
		} else {} 

	} 

	unsigned int n = 0; 
	/* ---------------------- for each abundance ratio ---------------------- */ 
	for (i = 1; i < (*origin).n_elements; i++) {
		unsigned int j; 
		for (j = 0; j < i; j++) {
			double onH1 = log10(
				(*(*origin).elements[i]).Z[t.timestep_origin] / 
				(*(*origin).elements[i]).solar 
			); 
			double onH2 = log10(
				(*(*origin).elements[j]).Z[t.timestep_origin] / 
				(*(*origin).elements[j]).solar 
			); 
			long bin = get_bin_number(
				(*(*final).mdf).bins, 
				(*(*final).mdf).n_bins, 
				onH1 - onH2
			); 
			if (bin != -1l) {
				final -> mdf -> ratio_distributions[n][bin] += t.mass; 
			} else {} 
			n++; 
		}
	}

}

/* 
 * Reset the MDF in a singlezone object such that the value within each bin 
 * is equal to zero. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object whose MDF is to be reset 
 */ 
static void reset_MDF(SINGLEZONE *sz) {

	unsigned long i, j; 
	for (i = 0l; i < (unsigned long) (*sz).n_elements; i++) {
		for (j = 0l; j < (*(*sz).mdf).n_bins; j++) {
			sz -> mdf -> abundance_distributions[i][j] = 0.0; 
		} 
	} 

	unsigned long n = choose((*sz).n_elements, 2); 
	for (i = 0l; i < n; i++) {
		for (j = 0l; j < (*(*sz).mdf).n_bins; j++) {
			sz -> mdf -> ratio_distributions[i][j] = 0.0; 
		} 
	} 

}

