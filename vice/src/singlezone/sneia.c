/* 
 * This file implements the enrichment from type Ia supernovae (SNe Ia) in 
 * VICE's singlezone simulations. 
 */ 

#include <stdlib.h> 
#include <stdio.h> 
#include <math.h> 
#include "../singlezone.h" 
#include "../callback.h" 
#include "../sneia.h" 
#include "../utils.h" 
#include "sneia.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double RIa_builtin(ELEMENT e, double time); 


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

	#if 0 
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
	#endif 

	if ((*e.sneia_yields).functional_yield != NULL) { 
		return callback_1arg_evaluate(*(*e.sneia_yields).functional_yield, Z); 
	} else { 
		return (*e.sneia_yields).constant_yield; 
	} 

} 


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

