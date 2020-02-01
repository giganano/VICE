/* 
 * This file implements the enrichment of arbitrary elements from type Ia 
 * supernovae. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <stdio.h> 
#include <math.h> 
#include "sneia.h" 
#include "utils.h" 
#include "tracer.h" 

/* ---------- static function comment headers not duplicated here ---------- */
// static double mdotstarIa(SINGLEZONE sz, ELEMENT e); 
static double RIa_builtin(ELEMENT e, double time); 

/* 
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct. 
 * Automatically initializes RIa and yield_ to NULL. Allocates memory for a 
 * 100-character dtd char * specifier. 
 * 
 * header: sneia.h 
 */ 
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void) {

	SNEIA_YIELD_SPECS *sneia_yields = (SNEIA_YIELD_SPECS *) malloc (sizeof(
		SNEIA_YIELD_SPECS)); 
	sneia_yields -> dtd = (char *) malloc (100 * sizeof(char)); 
	sneia_yields -> RIa = NULL; 

	sneia_yields -> yield_ = NULL; 

	/* 
	 * The number of elements on the yield grid between IA_YIELD_GRID_MIN and 
	 * IA_YIELD_GRID_MAX in steps of IA_YIELD_STEP (inclusve). 
	 */ 
	unsigned long num_grid_elements = (long) (
		(IA_YIELD_GRID_MAX - IA_YIELD_GRID_MIN) / IA_YIELD_STEP 
	) + 1l; 

	/* Fill the grid starting at IA_YIELD_GRID_MIN in steps of IA_YIELD_STEP */ 
	unsigned long i; 
	sneia_yields -> grid = (double *) malloc (num_grid_elements * sizeof(double)); 
	for (i = 0l; i < num_grid_elements; i++) {
		sneia_yields -> grid[i] = IA_YIELD_GRID_MIN + i * IA_YIELD_STEP; 
	} 

	sneia_yields -> entrainment = 1; 

	return sneia_yields; 

} 

/* 
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct. 
 * 
 * header: sneia.h 
 */ 
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields) { 

	if (sneia_yields != NULL) {

		if ((*sneia_yields).RIa != NULL) {
			free(sneia_yields -> RIa); 
			sneia_yields -> RIa = NULL; 
		} else {} 

		if ((*sneia_yields).dtd != NULL) {
			free(sneia_yields -> dtd); 
			sneia_yields -> dtd = NULL; 
		} else {} 

		if ((*sneia_yields).yield_ != NULL) {
			free(sneia_yields -> yield_); 
			sneia_yields -> yield_ = NULL; 
		} else {} 

		if ((*sneia_yields).grid != NULL) {
			free(sneia_yields -> grid); 
			sneia_yields -> grid = NULL; 
		} else {} 

		free(sneia_yields); 
		sneia_yields = NULL; 

	} else {} 

} 

/* 
 * Determine the rate of mass enrichment of a given element at the current 
 * timestep from SNe Ia. See section 4.3 of VICE's science documentation for 
 * further details. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * e: 		The element to find the rate of mass enrichment for 
 * 
 * Returns 
 * ======= 
 * The time-derivative of the type Ia supernovae mass enrichment term 
 * 
 * header: sneia.h 
 */ 
extern double mdot_sneia(SINGLEZONE sz, ELEMENT e) { 

	// return (*e.sneia_yields).yield_ * mdotstarIa(sz, e); 
	unsigned long i; 
	double mdotia = 0; 
	for (i = 0l; i < sz.timestep; i++) {
		mdotia += (
			get_ia_yield(e, scale_metallicity(sz, i)) * 
			(*sz.ism).star_formation_history[i] * 
			(*e.sneia_yields).RIa[sz.timestep - i] 
		); 
	} 
	// return (*e.sneia_yields).entrainment * mdotia; 
	return mdotia; 

} 

/* 
 * Obtain the IMF-integrated fractional mass yield of a given element from its 
 * internal yield table. 
 * 
 * Parameters 
 * ========== 
 * e: 			The element to find the yield for 
 * Z: 			The metallicity to look up on the grid 
 * 
 * Returns 
 * ======= 
 * The interpolated yield off of the stored yield grid within the ELEMENT 
 * struct. 
 * 
 * header: sneia.h  
 */ 
extern double get_ia_yield(ELEMENT e, double Z) {

	long lower_bound_idx; 
	if (Z < IA_YIELD_GRID_MIN) { 
		/* 
		 * Metallicity below the yield grid. Unless the user changes the 
		 * IA_YIELD_GRID_MIN in sneia.h to something other than zero, this 
		 * would be unphysical. Included as a failsafe for users modifying 
		 * VICE. Interpolate off bottom two elements of yield grid. 
		 */ 
		lower_bound_idx = 0l; 
	} else if (IA_YIELD_GRID_MIN <= Z && Z <= IA_YIELD_GRID_MAX) { 
		/* 
		 * Metallicity on the grid. This will always be true for simulations 
		 * even remotely realistic without modified grid parameters. 
		 * Interpolate off neighboring elements of yield grid. 
		 */ 
		lower_bound_idx = (long) (Z / IA_YIELD_STEP); 
	} else {
		/* 
		 * Metallicity above the grid. Without modified grid parameters, this 
		 * is unrealistically high, but included as a failsafe against 
		 * segmentation faults. Interpolate off top two elements of yield grid. 
		 */ 
		lower_bound_idx = (long) ((IA_YIELD_GRID_MAX - IA_YIELD_GRID_MIN) / 
			IA_YIELD_STEP) - 1l; 
	}

	return interpolate(
		lower_bound_idx * IA_YIELD_STEP, 
		lower_bound_idx * IA_YIELD_STEP + IA_YIELD_STEP, 
		(*e.sneia_yields).yield_[lower_bound_idx], 
		(*e.sneia_yields).yield_[lower_bound_idx + 1l], 
		Z 
	); 

} 

/* 
 * Determine the total mass production of a given element produced by SNe Ia 
 * in each zone. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * index: 	The index of the element to calculate the yield information for 
 * 
 * Returns 
 * ======= 
 * The total mass production of the given element in each zone 
 * 
 * header: sneia.h 
 */ 
extern double *m_sneia_from_tracers(MULTIZONE mz, unsigned short index) {

	unsigned long i, timestep = (*mz.zones[0]).timestep; 
	double *mass = (double *) malloc ((*mz.mig).n_zones * sizeof(double)); 
	for (i = 0l; i < (*mz.mig).n_zones; i++) {
		mass[i] = 0; 
	} 
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		TRACER *t = mz.mig -> tracers[i]; 
		SNEIA_YIELD_SPECS sneia = *(
			mz.zones[(*t).zone_current] -> elements[index] -> sneia_yields
		); 
		/* pull yield information from the zone this particle originated */ 
		mass[(*t).zone_current] += (
			get_ia_yield(*(*mz.zones[(*t).zone_origin]).elements[index], 
				tracer_metallicity(mz, *t)) * 
			(*t).mass * 
			sneia.RIa[timestep - (*t).timestep_origin] 
		); 
	} 
	return mass; 

}

#if 0 
/* 
 * Enrich each element in each zone according to the SNe Ia associated with 
 * tracer particles. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * header: sneia.h 
 */ 
extern void sneia_from_tracers(MULTIZONE *mz) {

	unsigned long i, timestep = (*(*mz).zones[0]).timestep; 
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) { 
		TRACER *t = mz -> mig -> tracers[i]; 
		unsigned int j; 
		/* 
		 * Enrich each element in the zone from SNe Ia associated with this 
		 * tracer particle. Pull the yield information from the zone in 
		 * which the tracer particle originated. 
		 */ 
		for (j = 0; j < (*(*mz).zones[(*t).zone_current]).n_elements; j++) {
			ELEMENT *e = mz -> zones[(*t).zone_current] -> elements[j]; 
			SNEIA_YIELD_SPECS *sneia = (mz -> zones[(*t).zone_origin] -> 
				elements[j] -> sneia_yields); 
			e -> mass += (
				// (*(*e).sneia_yields).entrainment * 
				get_ia_yield(*e, tracer_metallicity(*mz, *t)) * (*t).mass * 
				(*sneia).RIa[timestep - (*t).timestep_origin] 
			); 
		} 
	}

} 

/* 
 * Determine the star formation rate weighted by the SNe Ia rate. See section 
 * 4.3 of VICE's science documentation for more details. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * e: 		An ELEMENT struct containing the SNe Ia delay-time distribution 
 * 			information 
 * 
 * Returns 
 * ======= 
 * The time-averaged star formation history weighted by the SNe Ia rate as a 
 * double. 
 */ 
static double mdotstarIa(SINGLEZONE sz, ELEMENT e) {

	unsigned long i; 
	double sfria = 0; 
	for (i = 0l; i < sz.timestep; i++) {
		sfria += ((*e.sneia_yields).RIa[sz.timestep - i] * 
			(*sz.ism).star_formation_history[i]); 
	} 
	return sfria; 

} 
#endif 

/* 
 * Setup the SNe Ia rate in preparation for a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object that is about to be ran 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: sneia.h 
 */ 
extern unsigned short setup_RIa(SINGLEZONE *sz) {

	unsigned int j; 
	unsigned long i, length = (unsigned long) (RIA_MAX_EVAL_TIME / (*sz).dt); 
	for (j = 0; j < (*sz).n_elements; j++) { 

		switch (checksum((*(*(*sz).elements[j]).sneia_yields).dtd)) {

			case PLAW: 
				/* same as EXP */ 

			case EXP: 
				sz -> elements[j] -> sneia_yields -> RIa = (double *) malloc (
					length * sizeof(double)); 
				if ((*(*(*sz).elements[j]).sneia_yields).RIa == NULL) {
					return 1; 		/* memory error */ 
				} else {
					for (i = 0l; i < length; i++) {
						sz -> elements[j] -> sneia_yields -> RIa[i] = (
							RIa_builtin(*(*sz).elements[j], i * (*sz).dt) 
						); 
					} 
					normalize_RIa(sz -> elements[j], length); /* norm it */ 
				} 
				break; 

			case CUSTOM: 
				/* 
				 * Python will map the custom function into this array, so 
				 * simply normalize it here. 
				 */ 
				normalize_RIa(sz -> elements[j], length); 
				break; 

			default: 
				return 1; 

		} 

	} 

	return 0; 		/* success */ 

}

/* 
 * Returns the value of the SNe Ia delay-time distribution at a given time 
 * under arbitrary normalization. 
 * 
 * Parameters 
 * ========== 
 * e: 		An ELEMENT struct containing the delay-time information 
 * time: 	The time in Gyr following the formation of a single stellar 
 * 			population 
 * 
 * Returns 
 * ======= 
 * The value of the DTD prior to normalization 
 */ 
static double RIa_builtin(ELEMENT e, double time) { 

	if (time < (*e.sneia_yields).t_d) {
		/* Time is below minimum Ia delay time, force to zero */ 
		return 0; 
	} else {
		switch (checksum((*e.sneia_yields).dtd)) {

			case EXP: 
				/* exponential DTD w/user-specified e-folding timescale */ 
				return exp( -time / (*e.sneia_yields).tau_ia ); 

			case PLAW: 
				/* 
				 * power-law DTD w/index -1.1 Add 1e-12 to prevent numerical 
				 * errors allowing this function to evaluate at zero without 
				 * throwing an error. 
				 */ 
				return pow( time + 1e-12, -PLAW_DTD_INDEX ); 

			default: 
				return -1; 

		}
	} 

} 

/* 
 * Normalize the SNe Ia delay-time distribution once it is set according to 
 * an arbitrary normalization. 
 * 
 * Parameters 
 * ========== 
 * e: 			The ELEMENT struct to normalize the DTD for 
 * length: 		The length of the e -> sneia_yields -> RIa array 
 * 
 * header: sneia.h 
 */ 
extern void normalize_RIa(ELEMENT *e, unsigned long length) {

	unsigned long i; 
	double sum = 0; 
	for (i = 0l; i < length; i++) {
		sum += (*(*e).sneia_yields).RIa[i]; 
	} 
	for (i = 0l; i < length; i++) {
		 e -> sneia_yields -> RIa[i] /= sum; 
	} 

}

