/* 
 * This file implements all of the arbitrary enrichment channel functions. 
 */ 

#include <stdlib.h> 
#include <stdio.h> 
#include <math.h> 
#include "channel.h" 
#include "utils.h" 
#include "tracer.h" 

/* 
 * Allocate memory for and return a pointer to a CHANNEL object. 
 * Automatically initializes yield_ and rate to NULL. Allocates memory for and 
 * fills the grid_. 
 * 
 * header: channel.h 
 */ 
extern CHANNEL *channel_initialize(void) {

	CHANNEL *ch = (CHANNEL *) malloc (sizeof(CHANNEL)); 
	ch -> yield_ = NULL; 
	ch -> rate = NULL; 

	/* 
	 * The number of metallicities on the grid between CHANNEL_YIELD_GRID_MIN 
	 * and CHANNEL_YIELD_GRID_MAX in steps of CHANNEL_YIELD_GRID_STEP 
	 * (inclusive) 
	 */ 
	unsigned long n_grid_elements = (long) (
		(CHANNEL_YIELD_GRID_MAX - CHANNEL_YIELD_GRID_MIN) / 
		CHANNEL_YIELD_GRID_STEP
	) + 1l; 

	/* 
	 * Fill the grid starting at CHANNEL_YIELD_GRID_MIN in steps of 
	 * CHANNEL_YIELD_GRID_STEP 
	 */ 
	unsigned long i; 
	ch -> grid = (double *) malloc (n_grid_elements * sizeof(double)); 
	for (i = 0l; i < n_grid_elements; i++) {
		ch -> grid[i] = CHANNEL_YIELD_GRID_MIN + i * CHANNEL_YIELD_GRID_STEP; 
	} 

	return ch; 

} 

/* 
 * Free up the memory in a CHANNEL object. 
 * 
 * header: channel.h 
 */ 
extern void channel_free(CHANNEL *ch) {

	if (ch != NULL) {

		if ((*ch).yield_ != NULL) {
			free(ch -> yield_); 
			ch -> yield_ = NULL; 
		} else {} 

		if ((*ch).grid != NULL) {
			free(ch -> grid); 
			ch -> grid = NULL; 
		} else {} 

		if ((*ch).rate != NULL) {
			free(ch -> rate); 
			ch -> rate = NULL; 
		} else {} 

		free(ch); 
		ch = NULL; 

	} else {} 

} 

/* 
 * Determine the rate of mass enrichment of a given element at the current 
 * timestep from all arbitrary enrichment channels. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * e: 		The element to find the rate of mass enrichment for 
 * 
 * Returns 
 * ======= 
 * The time-derivative of the arbitrary enrichment channels mass enrichment 
 * term 
 * 
 * header: channel.h 
 */ 
extern double mdot(SINGLEZONE sz, ELEMENT e) {

	unsigned short i; 
	double mdot_ = 0; 
	for (i = 0lu; i < e.n_channels; i++) {
		unsigned long j; 
		for (j = 0l; j < sz.timestep; j++) {
			mdot_ += (*e.channels[i]).entrainment * (
				get_yield((*e.channels[i]), scale_metallicity(sz, j)) * 
				(*sz.ism).star_formation_history[j] * 
				(*e.channels[i]).rate[sz.timestep - j] 
			); 
		} 
	} 
	return mdot_; 

}

/* 
 * Obtain the IMF-integrated fractional mass yield of a given element from 
 * its internal yield table. 
 * 
 * Parameters 
 * ========== 
 * e: 		The element to find the yield for 
 * Z: 		The metallicity to look up on the grid 
 * 
 * Returns 
 * ======= 
 * The interpolated yield off of the stored yield grid within the CHANNEL 
 * struct. 
 * 
 * header: channel.h 
 */ 
extern double get_yield(CHANNEL ch, double Z) {

	unsigned long lower_bound_idx; 
	if (Z < CHANNEL_YIELD_GRID_MIN) {
		/* 
		 * Metallicity below the channel yield grid. Unless the user changes 
		 * the CHANNEL_YIELD_GRID_MIN in channel.h to something other than 
		 * zero, this would be unphysical. Included as a failsafe for users 
		 * modifying VICE. Interpolate off bottom two elements of yield grid. 
		 */ 
		lower_bound_idx = 0lu; 
	} else if (CHANNEL_YIELD_GRID_MIN <= Z && Z <= CHANNEL_YIELD_GRID_MAX) {
		/* 
		 * Metallicity on the grid. This will always be true for simulations 
		 * even remotely realistic without modified grid parameters. 
		 * Interpolate off neighboring elements of yield grid. 
		 */ 
		lower_bound_idx = (unsigned long) (Z / CHANNEL_YIELD_GRID_STEP); 
	} else {
		/* 
		 * Metallicity above the grid. Without modified grid parameters, this 
		 * is unrealistically high, but included as a failsafe against 
		 * segmentation faults. Interpolate off top two elements of yield 
		 * grid. 
		 */ 
		lower_bound_idx = (unsigned long) (
			(CHANNEL_YIELD_GRID_MAX - CHANNEL_YIELD_GRID_MIN) / 
			CHANNEL_YIELD_GRID_STEP 
		) - 1l; 
	} 

	return interpolate(
		lower_bound_idx * CHANNEL_YIELD_GRID_STEP, 
		lower_bound_idx * CHANNEL_YIELD_GRID_STEP + CHANNEL_YIELD_GRID_STEP, 
		ch.yield_[lower_bound_idx], 
		ch.yield_[lower_bound_idx + 1l], 
		Z 
	); 

} 

/* 
 * Enrichh all elements in a multizone simulation from all custom enrichment 
 * channels from all tracer particles in the simulation. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * header: channel.h 
 */ 
extern void from_tracers(MULTIZONE *mz) { 

	unsigned long i, timestep = (*(*mz).zones[0]).timestep; 
	for (i = 0lu; i < (*(*mz).mig).tracer_count; i++) { 
		TRACER *t = mz -> mig -> tracers[i]; 
		unsigned int j; 
		/* 
		 * Enrich the j'th element in the tracer particle's current zone from 
		 * all customs channels associated. Pull the yield information from 
		 * the zone in which the tracer particle originated. 
		 */ 
		for (j = 0u; j < (*(*mz).zones[(*t).zone_current]).n_elements; j++) {
			ELEMENT *e = mz -> zones[(*t).zone_current] -> elements[j]; 
			unsigned int k; 
			for (k = 0u; k < (*e).n_channels; k++) { 
				CHANNEL *ch = (mz -> zones[(*t).zone_origin] -> elements[j] -> 
					channels[k]); 
				e -> mass += (*(*e).channels[k]).entrainment * (
					get_yield(*ch, tracer_metallicity(*mz, *t) * (*t).mass * 
						(*ch).rate[timestep - (*t).timestep_origin] )
				); 
			}
		} 
	} 

}

/* 
 * Normalize the rate once it is set according to an arbitrary normalization 
 * by the user in python. 
 * 
 * Parameters 
 * ========== 
 * e: 			The ELEMENT struct to normalize the rate for. 
 * length: 		The length of the e -> channels[i] -> rate array 
 * 
 * header: channel.h 
 */ 
extern void normalize_rates(ELEMENT *e, unsigned long length) {

	unsigned short i; 
	for (i = 0u; i < (*e).n_channels; i++) {
		unsigned long j; 
		double sum = 0; 
		for (j = 0lu; j < length; j++) {
			sum += (*(*e).channels[i]).rate[j]; 
		} 
		for (j = 0lu; j < length; j++) {
			e -> channels[i] -> rate[j] /= sum; 
		} 
	} 

}




