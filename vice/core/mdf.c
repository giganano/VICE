/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#include <stdlib.h>
#include <math.h>
#include "specs.h"
#include "stars.h"

static long get_bin_number(MODEL m, double onH);

/*
Updates the metallicity distribution function according to the mass of stars 
that form at the current timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution
m:			The MODEL struct for the current exeuction
*/
extern void update_MDF(INTEGRATION run, MODEL *m) {

	int i, j;
	for (i = 0; i < run.num_elements; i++) {
		double onH = log10( (run.elements[i].m_tot/run.MG) / 
			run.elements[i].solar);
		long bin = get_bin_number(*m, onH);
		if (bin != -1l) m -> mdf[i][bin] += run.SFR;
	}
	int n = run.num_elements;
	for (i = 1; i < run.num_elements; i++) {
		for (j = 0; j < i; j++) {
			double onH1 = log10( (run.elements[i].m_tot/run.MG) / 
				run.elements[i].solar);
			double onH2 = log10( (run.elements[j].m_tot/run.MG) / 
				run.elements[j].solar);
			double onH = onH1 - onH2;
			long bin = get_bin_number(*m, onH);
			if (bin != -1) m -> mdf[n][bin] += run.SFR;
			n++;
		}
	}

}

/*
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
*/

/*
Returns the bin number of the given [X/Y] value within the MDF. -1 if the 
value is not within the range of the MDF.

Args:
=====
m:			The MODEL struct for the current exeuction
onH:		The given [X/Y] value
*/
static long get_bin_number(MODEL m, double onH) {

	long i;
	for (i = 0l; i < m.num_bins; i++) {
		if (m.bins[i] <= onH && onH <= m.bins[i + 1]) {
			return i;
		} else {
			continue;
		}
	}
	return -1l;

}

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
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	for (i = 0; i < num_mdfs; i++) {
		double sum = 0;
		for (j = 0l; j < (*m).num_bins; j++) {
			sum += (*m).mdf[i][j] * ( (*m).bins[j + 1] - (*m).bins[j] );
		}
		for (j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] /= sum;
		}
	}

}
/*
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
*/

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
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	m -> mdf = (double **) malloc (num_mdfs * sizeof(double *));
	for (i = 0; i < num_mdfs; i++) {
		m -> mdf[i] = (double *) malloc ((*m).num_bins * sizeof(double));
		for (j = 0l; j < (*m).num_bins; j++) {
			m -> mdf[i][j] = 0;
		}
	}

}

/*
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
*/





