/* 
 * This file implements the tracer particles used in multizone simulations. 
 */ 

#include <stdlib.h> 
#include "singlezone.h" 
#include "tracer.h" 
#include "utils.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
// static void realloc_tracers(MULTIZONE *mz); 

/* 
 * Allocates memory for and returns a pointer to a TRACER particle. 
 * 
 * header: tracer.h 
 */ 
extern TRACER *tracer_initialize(void) { 

	TRACER *t = (TRACER *) malloc (sizeof(TRACER)); 
	t -> mass = 0; 
	t -> zone_history = NULL; 
	return t; 

} 

/* 
 * Frees up the memory stored by the tracer particle. 
 * 
 * header: tracer.h 
 */ 
extern void tracer_free(TRACER *t) {

	if (t != NULL) { 

		if ((*t).zone_history != NULL) {
			free(t -> zone_history); 
			t -> zone_history = NULL; 
		}

		free(t); 
		t = NULL; 
		
	} else {} 

}

#if 0
extern void print_tracer(TRACER *t) {

	printf("======================================\n"); 
	printf("address = %p\n", (void *) t); 
	printf("zone_origin = %d\n", (*t).zone_origin); 
	printf("zone_current = %d\n", (*t).zone_current); 
	printf("timestep_origin = %d\n", (*t).timestep_origin); 

}
#endif 

#if 0
extern void tracer_free(TRACER *t) {

	if (t != NULL) {
		free(t); 
		t = NULL; 
	} else {} 

}
#endif 

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

#if 0
extern void inject_tracers(MULTIZONE *mz) {

	realloc_tracers(mz); 	/* need more memory */ 
	
	/* Give each new tracer particle it's mass and zone number */ 
	unsigned int i, j; 
	unsigned long start_index = (
		(*mz).tracer_count - (*mz).n_zones * (*mz).n_tracers 
	); 
	for (i = 0; i < (*mz).n_zones; i++) {
		for (j = 0; j < (*mz).n_tracers; j++) { 

			/* The index of this tracer in the array */ 
			unsigned long index = start_index + (*mz).n_tracers * i + j; 
			
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
#endif 

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

#if 0
/* 
 * Adds memory to a multizone object's array of tracer particles to make 
 * room for those in the next timestep
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 */ 
static void realloc_tracers(MULTIZONE *mz) { 

	mz -> tracer_count += (*mz).n_zones * (*mz).n_tracers; 
	mz -> tracers = (TRACER **) realloc (mz -> tracers, 
		(*mz).tracer_count * sizeof(TRACER *)); 

	unsigned long i; 
	for (i = (*mz).tracer_count - (*mz).n_zones * (*mz).n_tracers; 
		i < (*mz).tracer_count; 
		i++) {

		mz -> tracers[i] = tracer_initialize(); 

	}

}
#endif 

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

/*
 * Setup the zone history of a tracer particle assuming uniform migration 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object for the current simulation 
 * t: 			A pointer to the tracer particle to setup the zone history for 
 * origin: 		The zone of origin for the tracer particle 
 * final: 		The final zone number for the tracer particle 
 * birth: 		The timestep at which the tracer particle is born 
 * 
 * Returns 
 * ======= 
 * An error code: 0 for success; 1 for a birth timestep that's too large; 
 * 2 for a zone of origin that's too large; and 3 for a final zone that's 
 * too large 
 * 
 * header: tracer.h 
 */ 
extern unsigned short setup_zone_history(MULTIZONE mz, TRACER *t, 
	unsigned long origin, unsigned long final, unsigned long birth) {

	if (birth > n_timesteps(*mz.zones[0])) { 
		/* birth timestep too large */ 
		return 1; 
	} else if (origin > (*mz.mig).n_zones) {
		/* zone of origin too large */ 
		return 2; 
	} else if (final >= (*mz.mig).n_zones) {
		/* final zone too large */ 
		return 3; 
	} else { 
		unsigned long i, n = n_timesteps(*mz.zones[0]); 
		t -> zone_history = (int *) malloc (n * sizeof(int)); 
		for (i = 0l; i < birth; i++) { 
			/* Zone number is -1 until the tracer particle is born */ 
			t -> zone_history[i] = -1; 
		} 
		for (i = birth; i < n - BUFFER; i++) { 
			/* 
			 * Use the interpolate function to draw the line between the 
			 * zone of birth and the final zone 
			 */ 
			t -> zone_history[i] = (int) interpolate(birth, n - BUFFER, 
				origin, final, i); 
		} 
		for (i = n - BUFFER; i < n; i++) {
			/* 
			 * Put the tracer particle in its final zone for the 10 final 
			 * timesteps 
			 */ 
			t -> zone_history[i] = (int) final; 
		} 
		t -> zone_origin = origin; 
		if (mz.simple) { 
			t -> zone_current = final; 
		} else {
			t -> zone_current = origin; 
		} 
		t -> timestep_origin = birth; 
		return 0; 
	} 

} 
