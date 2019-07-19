/* 
 * This file implements the tracer particles used in multizone simulations. 
 */ 

#include <stdlib.h> 
#include "tracer.h" 
#include "utils.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void realloc_tracers(MULTIZONE *mz); 

/* 
 * Allocates memory for and returns a pointer to a TRACER particle. 
 * 
 * header: tracer.h 
 */ 
extern TRACER *tracer_initialize(void) {

	return (TRACER *) malloc (sizeof(TRACER)); 

} 

/* 
 * Frees up the memory stored by the tracer particle. 
 * 
 * header: tracer.h 
 */ 
extern void tracer_free(TRACER *t) {

	free(t); 

}

/* 
 * Injects tracer particles into a multizone object for the current timestep 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * header: tracer.h 
 */ 
extern void inject_tracers(MULTIZONE *mz) {

	realloc_tracers(mz); 	/* need more memory */ 
	
	/* Give each new tracer particle it's mass and zone number */ 
	int i, j; 
	long start_index = (
		((*(*mz).zones[0]).timestep - 1l) * (*mz).n_zones * (*mz).n_tracers 
	); 
	for (i = 0; i < (*mz).n_zones; i++) {
		for (j = 0; j < (*mz).n_tracers; j++) { 

			/* The index of this tracer in the array */ 
			long index = start_index + (*mz).n_tracers * i + j; 
			
			/* 
			 * The given zone is creating SFR * dt of mass in stars. Divide 
			 * this up amongst each tracer particle. 
			 */ 
			mz -> tracers[index] -> mass = (
				(*(*(*mz).zones[i]).ism).star_formation_rate * 
				(*(*mz).zones[i]).dt / (*mz).n_tracers 
			); 

			/* Bookkeeping */ 
			mz -> tracers[index] -> zone_origin = i; 
			mz -> tracers[index] -> zone_current = i; 
			mz -> tracers[index] -> timestep_origin = (
				*(*mz).zones[0]).timestep; 
		}
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
 * Adds memory to a multizone object's array of tracer particles to make 
 * room for those in the next timestep
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 */ 
static void realloc_tracers(MULTIZONE *mz) {

	long i, timestep = (*(*mz).zones[0]).timestep; 
	mz -> tracers = (TRACER **) realloc (mz -> tracers, 
		timestep * (*mz).n_zones * (*mz).n_tracers * sizeof(TRACER *)); 
	for (i = (timestep - 1l) * (*mz).n_zones * (*mz).n_tracers; 
		i < timestep * (*mz).n_zones * (*mz).n_tracers; 
		i++) {
		mz -> tracers[i] = tracer_initialize(); 
	} 

}



