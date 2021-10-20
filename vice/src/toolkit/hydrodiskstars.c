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
	unsigned short final_radii_column, unsigned short zform_column,
	unsigned short zfinal_column, unsigned short v_radcolumn,
	unsigned short v_phicolumn, unsigned short v_zcolumn,
	unsigned short decomp_column);
static unsigned short decomp_contains(unsigned short *decomp_values,
	unsigned short n_decomp_values, unsigned short test_value);
static unsigned long sum_(unsigned short *arr, unsigned long length);
static unsigned long candidate_search(HYDRODISKSTARS hds, double birth_radius,
	double birth_time, unsigned long **candidates, double max_radius,
	double max_time);
static unsigned short assess_candidate(HYDRODISKSTARS hds,
	double birth_radius, double birth_time, double max_radius,
	double max_time, unsigned long index);
static long assign_analog_min_radius(HYDRODISKSTARS hds,
	double birth_radius, double birth_time);
static double final_radius(HYDRODISKSTARS hds, double birth_radius,
	long analog_idx);

/* The number of subsample files present in the code base */
static unsigned short NSUBS = 30u;


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
 * zform_column: 		The column of disk heights of formation in kpc
 * zfinal_column: 		The column of present day disk heights in kpc
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
	unsigned short final_radii_column, unsigned short zform_column,
	unsigned short zfinal_column, unsigned short v_radcolumn,
	unsigned short v_phicolumn, unsigned short v_zcolumn,
	unsigned short decomp_column) {

	/*
	 * Bookkeeping
	 * ===========
	 * status: 		Ensures that the import proceeds as planned
	 * n: 			The number of files already imported
	 * included: 	The subsamples already imported
	 */
	unsigned short status = 1u, n = 0;
	unsigned short *included = (unsigned short *) malloc (
		sizeof(unsigned short));
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
		sprintf(filename, "%ssub%u.dat", filestem, subsample);
		status &= hydrodiskstars_import_sub(hds, filename, ids_column,
			birth_times_column, birth_radii_column, final_radii_column,
			zform_column, zfinal_column, v_radcolumn, v_phicolumn, v_zcolumn,
			decomp_column);
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
	unsigned short final_radii_column, unsigned short zform_column,
	unsigned short zfinal_column, unsigned short v_radcolumn,
	unsigned short v_phicolumn, unsigned short v_zcolumn,
	unsigned short decomp_column) {

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
				hds -> zform = (double *) malloc (n_lines * sizeof(double));
				hds -> zfinal = (double *) malloc (n_lines * sizeof(double));
				hds -> v_rad = (double *) malloc (n_lines * sizeof(double));
				hds -> v_phi = (double *) malloc (n_lines * sizeof(double));
				hds -> v_z = (double *) malloc (n_lines * sizeof(double));
				hds -> decomp = (unsigned short *) malloc (n_lines *
					sizeof(unsigned short));
			} else {
				/* This is not the first subsample import -> extend the data */
				hds -> ids = (unsigned long *) realloc (hds -> ids,
					(*hds).n_stars * sizeof(unsigned long));
				hds -> birth_times = (double *) realloc (hds -> birth_times,
					(*hds).n_stars * sizeof(double));
				hds -> birth_radii = (double *) realloc (hds -> birth_radii,
					(*hds).n_stars * sizeof(double));
				hds -> final_radii = (double *) realloc (hds -> final_radii,
					(*hds).n_stars * sizeof(double));
				hds -> zform = (double *) realloc (hds -> zform,
					(*hds).n_stars * sizeof(double));
				hds -> zfinal = (double *) realloc (hds -> zfinal,
					(*hds).n_stars * sizeof(double));
				hds -> v_rad = (double *) realloc (hds -> v_rad,
					(*hds).n_stars * sizeof(double));
				hds -> v_phi = (double *) realloc (hds -> v_phi,
					(*hds).n_stars * sizeof(double));
				hds -> v_z = (double *) realloc (hds -> v_z,
					(*hds).n_stars * sizeof(double));
				hds -> decomp = (unsigned short *) realloc (hds -> decomp,
					(*hds).n_stars * sizeof(unsigned short));
			}

			/* Copy it over */
			unsigned long i;
			for (i = 0u; i < n_lines; i++) {
				/* The position of this star particle in the data */
				unsigned long idx = (*hds).n_stars - n_lines + i;
				hds -> ids[idx] = raw[i][ids_column];
				hds -> birth_times[idx] = raw[i][birth_times_column];
				hds -> birth_radii[idx] = raw[i][birth_radii_column];
				hds -> final_radii[idx] = raw[i][final_radii_column];
				hds -> zform[idx] = raw[i][zform_column];
				hds -> zfinal[idx] = raw[i][zfinal_column];
				hds -> v_rad[idx] = raw[i][v_radcolumn];
				hds -> v_phi[idx] = raw[i][v_phicolumn];
				hds -> v_z[idx] = raw[i][v_zcolumn];
				hds -> decomp[idx] = raw[i][decomp_column];
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
 * Filter the hydrodiskstars data sample based on the kinematic decomposition
 * tags.
 *
 * Parameters
 * ==========
 * hds: 				The hydrodiskstars object to filter data from
 * decomp_values: 		The values of the "decomp" attribute that will remain
 * 						after the filter
 * n_decomp_values: 	The number of entries in the "decomp_values" array
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: hydrodiskstars.h
 */
extern unsigned short hydrodiskstars_decomp_filter(HYDRODISKSTARS *hds,
	unsigned short *decomp_values, unsigned short n_decomp_values) {

	/*
	 * Determine which star particles pass the filter. Store it as a simple
	 * array of boolean integers.
	 */
	unsigned short *which = (unsigned short *) malloc ((*hds).n_stars *
		sizeof(unsigned short));
	unsigned long i;
	for (i = 0ul; i < (*hds).n_stars; i++) {
		which[i] = decomp_contains(decomp_values, n_decomp_values,
			(*hds).decomp[i]);
	}

	/*
	 * Find the number of star particles which pass the filter, and allocate
	 * memory for a new arrays for each star particle's attributes.
	 */
	unsigned long n_pass = sum_(which, (*hds).n_stars);
	unsigned long *new_ids = (unsigned long *) malloc (n_pass * sizeof(
		unsigned long));
	double *new_birth_times = (double *) malloc (n_pass * sizeof(double));
	double *new_birth_radii = (double *) malloc (n_pass * sizeof(double));
	double *new_final_radii = (double *) malloc (n_pass * sizeof(double));
	double *new_zform = (double *) malloc (n_pass * sizeof(double));
	double *new_zfinal = (double *) malloc (n_pass * sizeof(double));
	double *new_v_rad = (double *) malloc (n_pass * sizeof(double));
	double *new_v_phi = (double *) malloc (n_pass * sizeof(double));
	double *new_v_z = (double *) malloc (n_pass * sizeof(double));
	unsigned short *new_decomp = (unsigned short *) malloc (n_pass * sizeof(
		unsigned short));

	/*
	 * Iterate over the current sample, and for those that passed the filter,
	 * copy them over to the new arrays.
	 */
	unsigned long n = 0ul;
	for (i = 0ul; i < (*hds).n_stars; i++) {
		if (which[i]) {
			new_ids[n] = hds -> ids[i];
			new_birth_times[n] = hds -> birth_times[i];
			new_birth_radii[n] = hds -> birth_radii[i];
			new_final_radii[n] = hds -> final_radii[i];
			new_zform[n] = hds -> zform[i];
			new_zfinal[n] = hds -> zfinal[i];
			new_v_rad[n] = hds -> v_rad[i];
			new_v_phi[n] = hds -> v_phi[i];
			new_v_z[n] = hds -> v_z[i];
			new_decomp[n] = hds -> decomp[i];
			n++;
		} else {}
	}

	/* Free up the old arrays and point the hds data at the new ones. */
	free(hds -> ids);
	free(hds -> birth_times);
	free(hds -> birth_radii);
	free(hds -> final_radii);
	free(hds -> zform);
	free(hds -> zfinal);
	free(hds -> v_rad);
	free(hds -> v_phi);
	free(hds -> v_z);
	free(hds -> decomp);
	hds -> ids = new_ids;
	hds -> birth_times = new_birth_times;
	hds -> birth_radii = new_birth_radii;
	hds -> final_radii = new_final_radii;
	hds -> zform = new_zform;
	hds -> zfinal = new_zfinal;
	hds -> v_rad = new_v_rad;
	hds -> v_phi = new_v_phi;
	hds -> v_z = new_v_z;
	hds -> decomp = new_decomp;
	hds -> n_stars = n_pass;

	/*
	 * The number of times n++ ran should be equal to n_pass. Return that as
	 * a success or failure message.
	 */
	return n == n_pass;

}


/*
 * Determines if an array of unsigned short integers contains a particular
 * unsigned short integer.
 *
 * Parameters
 * ==========
 * decomp_values: 		The array
 * n_decomp_values: 	The number of entries in decomp_values
 * test_value: 			The value which may or may not be in decomp_values
 *
 * Returns
 * =======
 * 1 if decomp_values contains test_value, 0 if not.
 */
static unsigned short decomp_contains(unsigned short *decomp_values,
	unsigned short n_decomp_values, unsigned short test_value) {

	unsigned short i;
	for (i = 0u; i < n_decomp_values; i++) {
		if (decomp_values[i] == test_value) return 1u;
	}
	return 0u;

}


/*
 * Calculate the sum of an array of unsigned shorts.
 *
 * Parameters
 * ==========
 * arr: 		The array to compute the sum of
 * length: 		The number of entries in the array.
 *
 * Returns
 * =======
 * The sum of all entries
 *
 * Notes
 * =====
 * This performs the same function as "sum" in vice/src/utils.h, but that
 * function accepts a double pointer, which is incompatible with an
 * unsigned short pointer.
 */
static unsigned long sum_(unsigned short *arr, unsigned long length) {

	unsigned long i, s = 0ul;
	for (i = 0ul; i < length; i++) {
		s += arr[i];
	}
	return s;

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
 * The index of the star particle in the hydrodiskstars data.
 *
 * Notes
 * =====
 * This function first searches for star particles born with R +/- 250 pc and
 * T +/- 250 Myr. If no candidate analog is found, it widens it to R +/- 500 pc
 * and T +/- 500 Myr. If no analog is found in this widened search, it assigns
 * the one with the smallest change in birth radius that still satisfies the
 * T +/- 500 Myr criterion.
 *
 * header: hydrodiskstars.h
 */
extern long hydrodiskstars_find_analog(HYDRODISKSTARS hds, double birth_radius,
	double birth_time) {

	/* Conduct the initial candidate search, default analog_idx of -1l */
	long analog_idx = -1l;
	unsigned long *candidates;
	unsigned long n_candidates;
	double search_radius = INITIAL_ANALOG_SEARCH_RADIUS;
	double search_time = INITIAL_ANALOG_SEARCH_TIME;
	do {
		n_candidates = candidate_search(hds, birth_radius, birth_time,
			&candidates, search_radius, search_time);
		if (n_candidates) {
			/* Candidates were found, take one of them at random */
			analog_idx = (signed) candidates[(unsigned long) rand_range(0,
				n_candidates)];
		} else {
			/*
			 * No candidates found; widen the search, but honor the limits
			 * imposed by the MAXIMUM_ANALOG_SEARCH_RADIUS and
			 * MAXIMUM_ANALOG_SEARCH_TIME macros defined in hydrodiskstars.h.
			 */
			search_radius += INCREMENT_ANALOG_SEARCH_RADIUS;
			search_time += INCREMENT_ANALOG_SEARCH_TIME;
			if (search_radius > MAXIMUM_ANALOG_SEARCH_RADIUS) {
				search_radius = MAXIMUM_ANALOG_SEARCH_RADIUS;
			} else {}
			if (search_time > MAXIMUM_ANALOG_SEARCH_TIME) {
				search_time = MAXIMUM_ANALOG_SEARCH_TIME;
			} else {}
		}
	} while (!n_candidates &&
		(search_radius < MAXIMUM_ANALOG_SEARCH_RADIUS ||
		search_time < MAXIMUM_ANALOG_SEARCH_TIME)
		);

	if (analog_idx == -1l) {
		/*
		 * No candidate found which satisfies the criteria so far. Take the one
		 * with the smallest difference in birth radius.
		 */
		analog_idx = assign_analog_min_radius(hds, birth_radius, birth_time);
	} else {}

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
		if (assess_candidate(hds, birth_radius, birth_time, max_radius,
			max_time, i)) {
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
 * Assess whether or not a given star particle passes the criteria to act as
 * an analog under the current candidate search - subroutine of the
 * hydrodiskstars_find_analog function.
 *
 * Parameters
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data
 * birth_radius: 	The radius of birth of the stellar population in kpc
 * birth_time: 		The time of birth of the stellar population in Gyr
 * max_radius: 		The maximum difference in radius of birth in kpc for this
 * 						candidate search.
 * max_time: 		The maximum difference in time of birth in Gyr for this
 * 						candidate search.
 * index: 			The index of the star particle in the data to test.
 *
 * Returns
 * =======
 * 1u if the star particle passes all criteria, 0 otherwise.
 *
 * Notes
 * =====
 * This functions assesses not only the difference in birth and final radii,
 * but whether or not the implied final radius by the given analog would be
 * within the allowed range in radii implied by the rad_bins attribute of the
 * hydrodiskstars object.
 */
static unsigned short assess_candidate(HYDRODISKSTARS hds,
	double birth_radius, double birth_time, double max_radius,
	double max_time, unsigned long index) {

	/* Start with a value of 1u for the test, and then &= it many times */
	unsigned short assessment = 1u;

	/*
	 * The most stringent tests first - whether or not the star particle is
	 * within the allowed range of birth radius and time.
	 */
	assessment &= absval(hds.birth_times[index] - birth_time) < max_time;
	assessment &= absval(hds.birth_radii[index] - birth_radius) < max_radius;

	/*
	 * If a star particle passes the tests so far, check the final radius
	 * implied by the change in radius of the star particle. It must be within
	 * the radial bins of the hydrodiskstars object to pass the test and be a
	 * candidate analog.
	 *
	 * Don't subtract 1 from hds.n_rad_bins because it's the number of bins in
	 * a binspace, so it's already 1 less than the length.
	 */
	if (assessment) {
		double rf = final_radius(hds, birth_radius, (signed) index);
		assessment &= rf >= hds.rad_bins[0];
		assessment &= rf <= hds.rad_bins[hds.n_rad_bins];
	} else {}

	return assessment;

}


/*
 * Finds the star particle which has the smallest difference in birth radius
 * while still passing the MAXIMUM_ANALOG_SEARCH_TIME criterion.
 *
 * Parameters
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data.
 * birth_radius: 	The radius of birth of the stellar population in kpc.
 * birth_time: 		The time of birth of the stellar population in Gyr.
 *
 * Returns
 * =======
 * The index of the star particle that was a) born in the time interval
 * implied by birth_time and MAXIMUM_ANALOG_SEARCH_TIME, and b) has the
 * smallest difference in birth radius.
 */
static long assign_analog_min_radius(HYDRODISKSTARS hds,
	double birth_radius, double birth_time) {

	/*
	 * This function is called only when the initial search within
	 * MAXIMUM_ANALOG_SEARCH_TIME and MAXIMUM_ANALOG_SEARCH_RADIUS fail to
	 * find a candidate analog star particle. Therefore start with an analog
	 * index of -1.
	 */
	unsigned long i;
	long analog_idx = -1l;
	for (i = 0ul; i < hds.n_stars; i++) {
		/*
		 * For each star particle in the data, check if it's birth radius is
		 * closer than the one with the current minimum. If there is no analog
		 * yet, take the current minimum to be infinity.
		 */
		double current_candidate_dr;
		if (analog_idx == -1l) {
			/* Linux distributions don't have INFINITY defined */
			#ifdef INFINITY
				current_candidate_dr = INFINITY;
			#else
				current_candidate_dr = 1e6;
			#endif
		} else {
			current_candidate_dr = absval(
				hds.birth_radii[analog_idx] - birth_radius
			);
		}
		if (assess_candidate(hds, birth_radius, birth_time,
			current_candidate_dr, MAXIMUM_ANALOG_SEARCH_TIME, i)) {
			/*
			 * If this star particle passes this call to assess_candidate,
			 * take it as the new candidate analog.
			 */
			analog_idx = (signed) i;
		} else {}
	}

	return analog_idx;

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
 * 						13.2 for consistency w/hydrosim)
 * analog_idx: 		The index of the analog star particle
 * time: 			The intermediate time in Gyr
 *
 * Returns
 * =======
 * The zone number of the stellar population at the intermediate time.
 *
 * Notes
 * =====
 * Although it shouldn't happen under this implementation, stellar populations
 * which do not find an analog are assumed to remain at their birth radius.
 *
 * header: hydrodiskstars.h
 */
extern long calczone_linear(HYDRODISKSTARS hds, double birth_time,
	double birth_radius, double end_time, long analog_idx, double time) {

	double radius = interpolate(birth_time, end_time, birth_radius,
		final_radius(hds, birth_radius, analog_idx), time);
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
 * time: 			The intermediate time in Gyr
 *
 * Returns
 * =======
 * The zone number of the stellar population at the intermediate time.
 *
 * Notes
 * =====
 * Although it shouldn't happen under this implementation, stellar populations
 * which do not find an analog are assumed to remain at their birth radius.
 *
 * header: hydrodiskstars.h
 */
extern long calczone_sudden(HYDRODISKSTARS hds, double migration_time,
	double birth_radius, long analog_idx, double time) {

	double radius;
	if (analog_idx > -1l && time >= migration_time) {
		radius = final_radius(hds, birth_radius, analog_idx);
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
 * 						13.2 for consistency w/hydrosim)
 * analog_idx: 		The index of the analog star particle
 * time: 			The intermediate time in Gyr
 *
 * Returns
 * =======
 * The zone number of the stellar population at the intermediate time.
 *
 * Notes
 * =====
 * Although it shouldn't happen under this implementation, stellar populations
 * which do not find an analog are assumed to remain at their birth radius.
 *
 * header: hydrodiskstars.h
 */
extern long calczone_diffusive(HYDRODISKSTARS hds, double birth_time,
	double birth_radius, double end_time, long analog_idx, double time) {

	double radius = interpolate_sqrt(birth_time, end_time, birth_radius,
		final_radius(hds, birth_radius, analog_idx), time);
	return get_bin_number(hds.rad_bins, hds.n_rad_bins, radius);

}


/*
 * Calculate the final radius of a stellar population according to its analog
 * in a hydrodiskstars object.
 *
 * Parameters
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data
 * birth_radius: 	The radius of the stellar population's birth in kpc
 * analog_idx: 		The index of the analog star particle
 * 						-1 if no analog is found.
 *
 * Returns
 * =======
 * The final radius of the stellar population.
 *
 * Notes
 * =====
 * Although it shouldn't happen under this implementation, this function
 * assumes the change in radius is zero for stellar populations which do not
 * find an analog as a failsafe.
 */
static double final_radius(HYDRODISKSTARS hds, double birth_radius,
	long analog_idx) {

	double dr;
	if (analog_idx > -1l) {
		/*
		 * Rather than the final radius of the analog itself, take its change
		 * in radius. This is more reflective of the dynamical history of the
		 * star particle.
		 */
		dr = hds.final_radii[analog_idx] - hds.birth_radii[analog_idx];
	} else {
		/* Although this shouldn't happen, let dr = 0 as a failsafe. */
		dr = 0;
	}

	return birth_radius + dr;

}

