/* 
 * This file implements the enrichment of arbitrary elements from type Ia 
 * supernovae. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <stdio.h> 
#include <math.h> 
#include "sneia.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double mdotstarIa(SINGLEZONE sz, ELEMENT e); 
static double RIa_builtin(ELEMENT e, double time); 

/* 
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct. 
 * Automatically initializes RIa to NULL. Allocates memory for a 100-character 
 * dtd char * specifier. 
 * 
 * header: sneia.h 
 */ 
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void) {

	SNEIA_YIELD_SPECS *sneia_yields = (SNEIA_YIELD_SPECS *) malloc (sizeof(
		SNEIA_YIELD_SPECS)); 
	sneia_yields -> dtd = (char *) malloc (100 * sizeof(char)); 
	sneia_yields -> RIa = NULL; 
	return sneia_yields; 

} 

/* 
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct. 
 * 
 * header: sneia.h 
 */ 
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields) {

	if ((*sneia_yields).RIa != NULL) free(sneia_yields -> RIa); 
	free(sneia_yields -> dtd); 
	free(sneia_yields); 

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

	return (*e.sneia_yields).yield_ * mdotstarIa(sz, e); 

} 

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
	for (i = 0l; i < timestep * (*mz).n_zones * (*mz).n_tracers; i++) { 
		TRACER *t = mz -> tracers[i]; 
		unsigned int j; 
		/* 
		 * Enrich each element in the zone from SNe Ia associated with this 
		 * tracer particle 
		 */ 
		for (j = 0; j < (*(*mz).zones[(*t).zone_current]).n_elements; j++) {
			ELEMENT *e = mz -> zones[(*t).zone_current] -> elements[j]; 
			e -> mass += (
				(*(*e).sneia_yields).yield_ * (*t).mass * 
				(*(*e).sneia_yields).RIa[timestep - (*t).timestep_origin] 
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
extern int setup_RIa(SINGLEZONE *sz) {

	unsigned int j; 
	unsigned long i, length = (unsigned long) (RIA_MAX_EVAL_TIME / (*sz).dt); 
	for (j = 0; j < (*sz).n_elements; j++) { 
		char *dtd = (*(*(*sz).elements[j]).sneia_yields).dtd; 
		if (!strcmp(dtd, "plaw") || !strcmp(dtd, "exp")) {
			/* built-in DTD, map it across time */ 
			sz -> elements[j] -> sneia_yields -> RIa = (double *) malloc (
				length * sizeof(double)); 
			if ((*(*(*sz).elements[j]).sneia_yields).RIa == NULL) {
				return 1; 		/* memory error */ 
			} else {
				for (i = 0l; i < length; i++) {
					sz -> elements[j] -> sneia_yields -> RIa[i] = RIa_builtin(
						*(*sz).elements[j], i * (*sz).dt); 
				} 
				normalize_RIa(sz -> elements[j], length); 	/* normalize it */ 
			} 
		} else if (!strcmp(dtd, "custom")) {
			/* 
			 * Python will map the custom function into this array, so simply 
			 * normalize it here. 
			 */ 
			normalize_RIa(sz -> elements[j], length); 
		} else {
			return 1; 		/* Error: unrecognized DTD specification */ 
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
	} else if (!strcmp((*e.sneia_yields).dtd, "exp")) {
		/* exponential DTD w/user-specified e-folding timescale */ 
		return exp( -time / (*e.sneia_yields).tau_ia ); 
	} else if (!strcmp((*e.sneia_yields).dtd, "plaw")) {
		/* power-law DTD w/index -1.1 Add 1e-12 to prevent numerical errors 
		 * allowing this function to evaluate at zero without throwing an 
		 * error. 
		 */ 
		return pow( time + 1e-12, -PLAW_DTD_INDEX ); 
	} else {
		return -1; 
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



