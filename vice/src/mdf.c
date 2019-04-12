/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script handles the numerical implementation of stellar metallicity 
 * distribution functions.  
 */

#include <stdlib.h>
#include <math.h>
#include "specs.h"
#include "stars.h"

/* ---------- static function comment headers not duplicated here ---------- */
static long get_bin_number(MODEL m, double onH);

/*
 * Updates the metallicity distribution function according to the mass of stars 
 * that form at the current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current exeuction 
 * 
 * header: stars.h 
 */
extern void update_MDF(INTEGRATION run, MODEL *m) {

	int i, j;
	/* --------------------- for each tracked element --------------------- */ 
	for (i = 0; i < run.num_elements; i++) { 
		/* Determine the associated [X/H] value */ 
		double onH = log10( (run.elements[i].m_tot/run.MG) / 
			run.elements[i].solar);
		long bin = get_bin_number(*m, onH);
		/* If it lies on the MDF binspace, increment that bin by the SFR */ 
		if (bin != -1l) m -> mdf[i][bin] += run.SFR;
	}
	/* The number of updates done so far */ 
	int n = run.num_elements; 

	/* --------------------- for each tracked element --------------------- */ 
	for (i = 1; i < run.num_elements; i++) {
		/* 
		 * Also track abundance ratios --- determine [X/Y] for each 
		 * combination of elements. 
		 */ 
		for (j = 0; j < i; j++) { 
			double onH1 = log10( (run.elements[i].m_tot/run.MG) / 
				run.elements[i].solar);
			double onH2 = log10( (run.elements[j].m_tot/run.MG) / 
				run.elements[j].solar);
			/* [X/Y] = [X/H] - [Y/H] */ 
			double onH = onH1 - onH2;
			long bin = get_bin_number(*m, onH);
			/* If it lies on the MDF binspace, increment that bin by the SFR. */ 
			if (bin != -1) m -> mdf[n][bin] += run.SFR;
			n++;
		}
	}

}

#if 0
Updates the metallicity distribution function according to the mass of stars 
that form at the current timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution
m:			The MODEL struct for the current exeuction

header: stars.h 
*/
extern void update_MDF(INTEGRATION run, MODEL *m) {

	int i;
	for (i = 0; i < run.num_elements; i++) {
		double onH = log10( (run.elements[i].m_tot/run.MG) / 
			run.elements[i].solar);
		long bin = get_bin_number(*m, onH);
		if (bin != -1) m -> mdf[i][bin] += run.SFR;
	}
	for (i = 1; i < run.num_elements; i++) {
		double onH1 = log10( (run.elements[i].m_tot/run.MG) / 
			run.elements[i].solar);
		double onH2 = log10( (run.elements[0].m_tot/run.MG) / 
			run.elements[0].solar);
		double onH = onH1 - onH2;
		long bin = get_bin_number(*m, onH);
		if (bin != -1) m -> mdf[i + run.num_elements - 1][bin] += run.SFR;
	}

}
#endif

/*
 * Normalizes the MDF prior to writing it to the output file. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current exeuction 
 * 
 * header: stars.h
 */
extern void normalize_MDF(INTEGRATION run, MODEL *m) {

	int i;
	long j;
	/* The number of MDFs that the simulation has tracked */ 
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	for (i = 0; i < num_mdfs; i++) {
		double sum = 0;
		/* Integrate each MDF */ 
		for (j = 0l; j < (*m).num_bins; j++) {
			sum += (*m).mdf[i][j] * ( (*m).bins[j + 1] - (*m).bins[j] );
		}
		/* Normalize it */ 
		for (j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] /= sum;
		}
	}

}

#if 0
/*
Normalizes the MDF prior to writing it to the output file. 

Args:
=====
run:		The INTEGRATION struct for the current execution
m:			The MODEL struct for the current exeuction
*/
extern void normalize_MDF(INTEGRATION run, MODEL *m) {

	int i;
	long j;
	for (i = 0; i < 2 * run.num_elements - 1; i++) {
		double sum = 0;
		for (j = 0l; j < (*m).num_bins; j++) {
			sum += (*m).mdf[i][j] * ( (*m).bins[j + 1] - (*m).bins[j] );
		}
		// printf("%e\n", sum);
		for(j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] /= sum;
		}
	}

	// double *sum = (double *) malloc ((2 * run.num_elements - 1) * sizeof(double));
	// int i;
	// long j;
	// for (i = 0; i < 2 * run.num_elements - 1; i++) {
	// 	sum[i] = 0;
	// 	for (j = 0l; j < (*m).num_bins; j++) {
	// 		sum[i] += (*m).mdf[i][j] * ( (*m).bins[i + 1] - (*m).bins[i] );
	// 	}
	// 	for (j = 0l; j < (*m).num_bins; j++) {
	// 		m -> mdf[i][j] /= sum[i];
	// 	}
	// }
	// free(sum);

}
#endif


/*
 * Sets up the MDF at the beginning of the INTEGRATION 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution of the code
 * m:			The MODEL struct for the current execution of the code* 
 * 
 * header: stars.h 
 */
extern void setup_MDF(INTEGRATION run, MODEL *m) {

	int i;
	long j;
	/* 
	 * The number of MDFs tracked by the simulation. VICE tracks star 
	 * formation at individual abundances as well as abundance ratios. 
	 */ 
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	m -> mdf = (double **) malloc (num_mdfs * sizeof(double *));
	for (i = 0; i < num_mdfs; i++) {
		/* 
		 * Set each MDF as an array across the binspace where each element is 
		 * initially zero. 
		 */ 
		m -> mdf[i] = (double *) malloc ((*m).num_bins * sizeof(double));
		for (j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] = 0;
		}
	}

}

#if 0
/*
Sets up the MDF at the beginning of the INTEGRATION

Args:
=====
run:		The INTEGRATION struct for the current execution of the code
m:			The MODEL struct for the current execution of the code
*/
extern void setup_MDF(INTEGRATION run, MODEL *m) {

	int i;
	long j;
	m -> mdf = (double **) malloc ((2 * run.num_elements - 1) * sizeof(
		double *));
	for (i = 0; i < 2 * run.num_elements - 1; i++) {
		m -> mdf[i] = (double *) malloc ((*m).num_bins * sizeof(double));
		for (j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] = 0;
		}
	}

}
#endif

/*
 * Returns the bin number of the given [X/Y] value within the MDF. -1 if the 
 * value is not within the range of the MDF. This is similar in concept but 
 * different in implementation to the get_bounds function used for 
 * interpolation in agb.c. 
 * 
 * Args:
 * =====
 * m:			The MODEL struct for the current exeuction
 * onH:			The given [X/Y] value
 */
static long get_bin_number(MODEL m, double onH) {

	long i;
	for (i = 0l; i < m.num_bins; i++) {
		/* If the [X/Y] value lies between the bin edges ... */ 
		if (m.bins[i] <= onH && onH <= m.bins[i + 1]) {
			/* ... send that bin number back. */ 
			return i;
		} else {
			continue;
		}
	}
	/* 
	 * If the code gets to this point, it didn't find a bin for the given 
	 * [X/Y] value ===> It doesn't lie on the binspace. 
	 */ 
	return -1l;

}



