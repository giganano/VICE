/* 
 * This file implements the core routines of the hydrodiskstars object. 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../utils.h" 
#include "../io/utils.h" 
#include "hydrodiskstars.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static unsigned long candidate_search(HYDRODISKSTARS hds, double birth_radius, 
	double birth_time, unsigned long **candidates, double max_radius, 
	double max_time); 


/* 
 * Read the raw data describing hydrodynamical simulation star particles into 
 * the hydrodiskstars object. 
 * 
 * Parameters 
 * ==========
 * hds: 				A pointer to the hydrodiskstars object to import into 
 * filename: 			The name of the file holding the data 
 * birth_times_column: 	The column of times in Gyr each star particle was born 
 * birth_radii_column: 	The column of radii in kpc each star particle was born at 
 * final_radii_column: 	The column of radii in kpc each star particle ends at 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: hydrodiskstars.h 
 */ 
extern unsigned short hydrodiskstars_import(HYDRODISKSTARS *hds, char *filename, 
	unsigned short birth_times_column, unsigned short birth_radii_column, 
	unsigned short final_radii_column) {

	unsigned long n_lines = (unsigned long) (
		line_count(filename) - header_length(filename)
	); 
	if (n_lines) { 
		double **raw = read_square_ascii_file(filename); 
		if (raw != NULL) { 
			hds -> n_stars = n_lines; 
			hds -> birth_times = (double *) malloc (n_lines * sizeof(double)); 
			hds -> birth_radii = (double *) malloc (n_lines * sizeof(double)); 
			hds -> final_radii = (double *) malloc (n_lines * sizeof(double)); 
			unsigned long i; 
			for (i = 0ul; i < n_lines; i++) { 
				hds -> birth_times[i] = raw[i][birth_times_column]; 
				hds -> birth_radii[i] = raw[i][birth_radii_column]; 
				hds -> final_radii[i] = raw[i][final_radii_column]; 
			} 
			free(raw); 
			return 1u; 
		} else {
			return 0u; 
		} 
	} else {
		return 0u; 
	} 

} 


/* 
 * Find an analog star particle from the hydrodynamical simulation given a 
 * birth radius and time of a stellar population in a multizone simulation. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing the star particle data 
 * birth_radius: 	The radius of birth in kpc 
 * birth_time: 		The time of birth in Gyr 
 * 
 * Returns 
 * =======
 * The index of the star particle in the hydrodiskstars data. -1 if no analog 
 * is found in either initial or widened searches. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern long hydrodiskstars_find_analog(HYDRODISKSTARS hds, double birth_radius, 
	double birth_time) {

	/* Conduct the initial candidate search, default analog_idx of -1l */ 
	long analog_idx = -1l; 
	unsigned long *candidates; 
	unsigned long n_candidates = candidate_search(hds, birth_radius, birth_time, 
		&candidates, INITIAL_ANALOG_SEARCH_RADIUS, INITIAL_ANALOG_SEARCH_TIME); 
	if (n_candidates) {
		/* Candidates were found, take one of them at random */ 
		analog_idx = (signed) candidates[(unsigned long) rand_range(0, 
			n_candidates)]; 
	} else {
		/* No candidates found in initial search, conduct widened search */ 
		n_candidates = candidate_search(hds, birth_radius, birth_time, 
			&candidates, WIDENED_ANALOG_SEARCH_RADIUS, 
			WIDENED_ANALOG_SEARCH_TIME); 
		if (n_candidates) {
			/* Candidates were found take one of them at random */ 
			analog_idx = (signed) candidates[(unsigned long) rand_range(0, 
				n_candidates)]; 
		} else { /* no candidates found, leave analog_idx at -1l */ } 
	} 
	if (n_candidates) free(candidates); 
	return analog_idx; 

}


/* 
 * Conduct a candidate search for analog star particles - subroutine of the 
 * hydrodiskstars_find_analog function. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * birth_radius: 	The radius of birth of the stellar population in kpc 
 * birth_time: 		The time of birth of the stellar population in Gyr 
 * candidates: 		A pointer to the array of candidate indeces (should always 
 * 						be NULL when this function is called). 
 * max_radius: 		The maximum difference in radius of birth in kpc for this 
 * 						candidate search. 
 * max_time: 		The maximum difference in time of birth in Gyr for this 
 * 						candidate search. 
 * 
 * Returns 
 * =======
 * The number of candidates found. Their indeces will be placed in the 
 * candidates pointer, which will still be NULL if no candidates are found. 
 */ 
static unsigned long candidate_search(HYDRODISKSTARS hds, double birth_radius, 
	double birth_time, unsigned long **candidates, double max_radius, 
	double max_time) {

	unsigned long i, n_candidates = 0ul; 

	for (i = 0ul; i < hds.n_stars; i++) {
		if (absval(hds.birth_times[i] - birth_time) < max_time && 
			absval(hds.birth_radii[i] - birth_radius) < max_radius) {
			if (n_candidates) {
				*candidates = (unsigned long *) realloc (*candidates, 
					(n_candidates + 1ul) * sizeof(unsigned long)); 
			} else {
				*candidates = (unsigned long *) malloc (sizeof(unsigned long)); 
			}
			(*candidates)[n_candidates] = i; 
			n_candidates++; 
		} 
	} 

	return n_candidates; 

}


/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the linear migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * birth_time: 		The time the stellar population was born in Gyr 
 * birth_radius: 	The radius of the stellar population's birth in kpc 
 * end_time: 		The time of the end of the simulation (should always be 
 * 						12.8 for consistency w/hydrosim) 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The radius of the stellar population at the intermediate time. 
 * 
 * Note 
 * ====
 * Stars which find no analog are assumed to not migrate. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern long calczone_linear(HYDRODISKSTARS hds, double birth_time, 
	double birth_radius, double end_time, long analog_idx, double time) {

	double radius; 
	// printf("birth_time = %.5e\n", birth_time); 
	// printf("birth_radius = %.5e\n", birth_radius); 
	// printf("end_time = %5e\n", end_time); 
	// printf("analog_idx = %ld\n", analog_idx); 
	// printf("time = %.5e\n", time); 
	if (analog_idx > -1l) {
		// printf("A\n"); 
		radius = interpolate(birth_time, end_time, birth_radius, 
			hds.final_radii[analog_idx], time); 
		// printf("B\n"); 
	} else {
		radius = birth_radius; 
	}
	// printf("C\n"); 

	return get_bin_number(hds.rad_bins, hds.n_rad_bins, radius); 

}


/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the sudden migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * migration_time: 	The time at which the star particle migrates 
 * birth_radius: 	The radius of the stellar population's birth 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The radius of the stellar population at the intermediate time. 
 * 
 * Note 
 * ==== 
 * Stars which find no analog are assumed to not migrate. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern long calczone_sudden(HYDRODISKSTARS hds, double migration_time, 
	double birth_radius, long analog_idx, double time) {

	double radius; 
	if (analog_idx > -1l && time >= migration_time) {
		radius = hds.final_radii[analog_idx]; 
	} else {
		radius = birth_radius; 
	}

	return get_bin_number(hds.rad_bins, hds.n_rad_bins, radius); 

} 


/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the diffusive migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * birth_time: 		The time the stellar population was born in Gyr 
 * birth_radius: 	The radius of the stellar population's birth in kpc 
 * end_time: 		The time of the end of the simulation (should always be 
 * 						12.8 for consistency w/hydrosim) 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The radius of the stellar population at the intermediate time. 
 * 
 * Note 
 * ====
 * Stars which find no analog are assumed to not migrate. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern long calczone_diffusive(HYDRODISKSTARS hds, double birth_time, 
	double birth_radius, double end_time, long analog_idx, double time) {

	double radius; 
	if (analog_idx > -1l) {
		radius = (hds.final_radii[analog_idx] - birth_radius) * sqrt(
			(time - birth_time) / (end_time - birth_time) 
		) + birth_radius; 
	} else {
		radius = birth_radius; 
	}

	return get_bin_number(hds.rad_bins, hds.n_rad_bins, radius); 

}

