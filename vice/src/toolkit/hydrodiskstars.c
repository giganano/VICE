/* 
 * This file implements the core routines of the hydrodiskstars object. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "../utils.h" 
#include "../io.h" 
#include "hydrodiskstars.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static unsigned short already_included(unsigned short *included, 
	const unsigned short subsample, const unsigned short n_subsamples); 
static unsigned short hydrodiskstars_import_sub(HYDRODISKSTARS *hds, 
	char *filename, unsigned short ids_column, 
	unsigned short birth_times_column, unsigned short birth_radii_column, 
	unsigned short final_radii_column, unsigned short zfinal_column, 
	unsigned short v_radcolumn, unsigned short v_phicolumn, 
	unsigned short v_zcolumn); 
static unsigned long candidate_search(HYDRODISKSTARS hds, double birth_radius, 
	double birth_time, unsigned long **candidates, double max_radius, 
	double max_time); 

/* The number of subsample files present in the code base */ 
static unsigned short NSUBS = 68u; 


/* 
 * Read the raw data describing hydrodynamical simulation star particles into 
 * the hydrodiskstars object. 
 * 
 * Parameters 
 * ==========
 * hds: 				A pointer to the hydrodiskstars object to import into 
 * Nstars: 				The number of star particles necessary for the model 
 * filestem: 			The path to the files to import, minus the "_subN.dat" 
 * ids_column: 			The column of star particle IDs 
 * birth_times_column: 	The column of times in Gyr each star particle was born 
 * birth_radii_column: 	The column of radii in kpc each star particle was born at 
 * final_radii_column: 	The column of radii in kpc each star particle ends at 
 * zfinal_column: 		The column of disk heights in kpc 
 * v_radcolumn: 		The column of radial velocities in km/sec 
 * v_phicolumn: 		The column of azimuthal velocities in km/sec 
 * v_zcolumn: 			The column of vertical velocities in km/sec 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: hydrodiskstars.h 
 */ 
extern unsigned short hydrodiskstars_import(HYDRODISKSTARS *hds, 
	unsigned long Nstars, char *filestem, unsigned short ids_column, 
	unsigned short birth_times_column, unsigned short birth_radii_column, 
	unsigned short final_radii_column, unsigned short zfinal_column, 
	unsigned short v_radcolumn, unsigned short v_phicolumn, 
	unsigned short v_zcolumn) {

	/* 
	 * Bookkeeping 
	 * ===========
	 * status: 		Ensures that the import proceeds as planned 
	 * n: 			The number of files already imported 
	 * included: 	The subsamples already imported 
	 */ 
	unsigned short status = 1u, n = 0; 
	unsigned short *included = (unsigned short *) malloc (sizeof(unsigned short)); 
	do {
		/* Find which subsample to import */ 
		unsigned short subsample; 
		do {
			subsample = (unsigned short) rand_range(0, (double) NSUBS); 
		} while (already_included(included, subsample, n)); 
		included[n] = subsample; 
		n++; 
		included = (unsigned short *) realloc (included, 
			(n + 1u) * sizeof(unsigned short)); 
		
		/* Construct the name of the file to import */ 
		char *filename = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
		sprintf(filename, "%s_sub%u.dat", filestem, subsample); 
		status &= hydrodiskstars_import_sub(hds, filename, ids_column, 
			birth_times_column, birth_radii_column, final_radii_column, 
			zfinal_column, v_radcolumn, v_phicolumn, v_zcolumn); 
		free(filename); 
	} while ((*hds).n_stars < Nstars && status); 
	free(included); 

	return status; 

} 


/* 
 * Determines if a subsample of the data was already imported. 
 * 
 * Parameters 
 * ==========
 * included: 		The numbers of subsamples already included 
 * subsample: 		The subsample to test if it has been included 
 * n_subsamples: 	The number of subsamples thus far imported 
 * 
 * Returns 
 * =======
 * 1 if the subsample is already imported, 0 if it has not been imported. 
 */ 
static unsigned short already_included(unsigned short *included, 
	const unsigned short subsample, const unsigned short n_subsamples) {

	unsigned short i; 
	for (i = 0u; i < n_subsamples; i++) {
		if (included[i] == subsample) return 1u; 
	} 
	return 0u; 

}


/* 
 * Imports a single subsample data file into the hydrodiskstars object. 
 * 
 * Parameters 
 * ==========
 * hds: 				A pointer to the hydrodiskstars object to import into 
 * filename: 			The path to the file to import 
 * ids_column: 			The column of star particle IDs 
 * birth_times_column: 	The column of times in Gyr each star particle was born 
 * birth_radii_column: 	The column of radii in kpc each star particle was born at 
 * final_radii_column: 	The column of radii in kpc each star particle ends at 
 * zfinal_column: 		The column of disk heights in kpc 
 * v_radcolumn: 		The column of radial velocities in km/sec 
 * v_phicolumn: 		The column of azimuthal velocities in km/sec 
 * v_zcolumn: 			The column of vertical velocities in km/sec 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 */ 
static unsigned short hydrodiskstars_import_sub(HYDRODISKSTARS *hds, 
	char *filename, unsigned short ids_column, 
	unsigned short birth_times_column, unsigned short birth_radii_column, 
	unsigned short final_radii_column, unsigned short zfinal_column, 
	unsigned short v_radcolumn, unsigned short v_phicolumn, 
	unsigned short v_zcolumn) {

	unsigned long n_lines = (unsigned long) (
		line_count(filename) - header_length(filename) 
	); 

	if (n_lines) {

		/* Read in the data if the file is populated */ 
		double **raw = read_square_ascii_file(filename); 
		if (raw != NULL) {
			
			(*hds).n_stars += n_lines; 
			if ((*hds).n_stars == n_lines) {
				/* This is the first subsample import -> initialize the data */ 
				hds -> ids = (unsigned long *) malloc (n_lines * 
					sizeof(unsigned long)); 
				hds -> birth_times = (double *) malloc (n_lines * 
					sizeof(double)); 
				hds -> birth_radii = (double *) malloc (n_lines * 
					sizeof(double)); 
				hds -> final_radii = (double *) malloc (n_lines * 
					sizeof(double)); 
				hds -> zfinal = (double *) malloc (n_lines * sizeof(double)); 
				hds -> v_rad = (double *) malloc (n_lines * sizeof(double)); 
				hds -> v_phi = (double *) malloc (n_lines * sizeof(double)); 
				hds -> v_z = (double *) malloc (n_lines * sizeof(double)); 
			} else {
				/* This is not the first subsample import -> extend the data */ 
				hds -> ids = (unsigned long *) realloc (hds -> ids, 
					(*hds).n_stars * sizeof(unsigned long)); 
				hds -> birth_times = (double *) realloc (hds -> birth_times, 
					(*hds).n_stars * sizeof(double)); 
				hds -> birth_radii = (double *) realloc (hds -> birth_radii, 
					(*hds).n_stars * sizeof(double)); 
				hds -> zfinal = (double *) realloc (hds -> zfinal, 
					(*hds).n_stars * sizeof(double)); 
				hds -> v_rad = (double *) realloc (hds -> v_rad, 
					(*hds).n_stars * sizeof(double)); 
				hds -> v_phi = (double *) realloc (hds -> v_phi, 
					(*hds).n_stars * sizeof(double)); 
				hds -> v_z = (double *) realloc (hds -> v_z, 
					(*hds).n_stars * sizeof(double)); 
			} 

			/* Copy it over */ 
			unsigned long i; 
			for (i = 0u; i < n_lines; i++) { 
				/* The position of this star particle in the data */ 
				unsigned long idx = (*hds).n_stars - n_lines + i; 
				hds -> ids[idx] = raw[i][ids_column]; 
				hds -> birth_times[i] = raw[i][birth_times_column]; 
				hds -> birth_radii[i] = raw[i][birth_radii_column]; 
				hds -> final_radii[i] = raw[i][final_radii_column]; 
				hds -> zfinal[i] = raw[i][zfinal_column]; 
				hds -> v_rad[i] = raw[i][v_radcolumn]; 
				hds -> v_phi[i] = raw[i][v_phicolumn]; 
				hds -> v_z[i] = raw[i][v_zcolumn]; 
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
	if (analog_idx > -1l) {
		radius = interpolate(birth_time, end_time, birth_radius, 
			hds.final_radii[analog_idx], time); 
	} else {
		radius = birth_radius; 
	}

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

