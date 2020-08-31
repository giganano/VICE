/* 
 * This file implements the interaction between the hydrodiskstars object and 
 * and the multizone object, specifically the fast-tracked star particle setup. 
 */ 


#include <stdlib.h> 
#include "hydrodiskstars.h" 
#include "../toolkit/hydrodiskstars.h" 
#include "../utils.h" 
#include "../singlezone.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static unsigned short setup_zone_history(TRACER *t, HYDRODISKSTARS hds, 
	MULTIZONE mz, unsigned int birth_zone, unsigned long birth_timestep); 


/* 
 * Setup the zone history for a single tracer particle according to the 
 * hydrodiskstars object, which assumes a series of annuli to describe a 
 * Milky Way-like disk galaxy. 
 * 
 * Parameters 
 * ==========
 * t: 				A pointer to the tracer object being setup 
 * hds: 			The hydrodiskstars object 
 * birth_zone: 		The zone of the tracer particle's birth 
 * birth_timestep: 	The timestep the tracer particle is born at 
 * dt: 				The timestep size 
 * simple: 			The attribute "simple" of the multizone object 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 */ 
static unsigned short setup_zone_history(TRACER *t, HYDRODISKSTARS hds, 
	MULTIZONE mz, unsigned int birth_zone, unsigned long birth_timestep) {

	/* The time and radius at which the star is born */ 
	double dt = (*mz.zones[0]).dt; 
	double birth_time = birth_timestep * dt; 
	double birth_radius = (
		(hds.rad_bins[birth_zone] + hds.rad_bins[birth_zone + 1]) / 2 
	); 

	/* In case of sudden migration, this can't be done in the for-loop */ 
	double migration_time = rand_range(birth_time, HYDRODISK_END_TIME); 

	/* Assign the analog and allocate memory for the zone_history pointer */ 
	long analog = hydrodiskstars_find_analog(hds, birth_radius, birth_time); 
	unsigned long i, N = n_timesteps(*mz.zones[0]); 
	t -> zone_history = (int *) malloc (N * sizeof(int)); 

	for (i = 0ul; i < N; i++) {
		if (i * dt < birth_time) { 
			/* Zone number is always -1 until it is born */ 
			t -> zone_history[i] = -1; 
		} else if (i >= N - BUFFER) { 
			/* Zone number if zone of birth for all stars born in the buffer */ 
			t -> zone_history[i] = (signed) birth_zone; 
		} else {

			switch(checksum(hds.mode)) { 

				/* 
				 * Under each mode, use the calczone_* functions that the 
				 * hydrodiskstars object employs anyway to determine the 
				 * zone number at each intermediate time. 
				 */ 

				case LINEAR_MIGRATION: 
					t -> zone_history[i] = (int) calczone_linear(hds, 
						birth_time, birth_radius, HYDRODISK_END_TIME, 
						analog, i * dt); 
					break; 

				case SUDDEN_MIGRATION: 
					t -> zone_history[i] = (int) calczone_sudden(hds, 
						migration_time, birth_radius, analog, i * dt); 
					break; 

				case DIFFUSION_MIGRATION: 
					t -> zone_history[i] = (int) calczone_diffusive(hds, 
						birth_time, birth_radius, HYDRODISK_END_TIME, 
						analog, i * dt); 
					break; 

				default: 
					return 0u; /* error handling */ 

			} 

		} 
	} 

	t -> timestep_origin = birth_timestep; 
	t -> zone_origin = birth_zone; 
	if (mz.simple) {
		t -> zone_current = (unsigned) t -> zone_history[N - BUFFER]; 
	} else {
		t -> zone_current = birth_zone; 
	} 
	return 1u; 

}

