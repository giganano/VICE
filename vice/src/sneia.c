/*
 * This script handles the numerical implementation of enrichment from type 
 * Ia supernovae. 
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double mdotstarIa(INTEGRATION run, MODEL m);
static double R_SNe_Ia(MODEL m, double t);

/*
 * Returns the time derivative of the mass of a given element at the current 
 * timestep from SNe Ia alone. This is equal to the yield times the star 
 * formation rate weighted by the SNe Ia delay-time distribution. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution.
 * index:		The index of the element in question. 
 * 
 * header: enrichment.h 
 */
extern double mdot_ia(INTEGRATION run, MODEL m, int index) {

	return run.elements[index].sneia_yield * mdotstarIa(run, m);

}

/*
 * Returns the star formation rate weighted by the SNe Ia rate. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution.
 */
static double mdotstarIa(INTEGRATION run, MODEL m) {

	double sfria = 0;
	long i;
	for (i = 0l; i < run.timestep; i++) {
		/* SFR(t) * RIa(lookback time) */ 
		sfria += m.ria[run.timestep - i] * run.mdotstar[i];
	}
	return sfria;

}

/*
 * Sets up the array RIA containing the SNe Ia rate at all times following the 
 * formation of a single stellar population at time 0. 
 * 
 * This routine will not be called if the user has specified a custom DTD. In 
 * that case it will be filled by Python and insterted directly into the 
 * MODEL struct. 
 * 
 * Args:
 * =====
 * m:		The MODEL struct for this execution
 * dt:		The timestep size 
 * 
 * header: enrichment.h 
 */
extern int setup_RIA(MODEL *m, double dt) {

	if (R_SNe_Ia(*m, dt) == -1) {
		return 1; 		// error 
	} else {
		long i;
		/* 
		 * VICE by design only fills the RIa array up to 15 Gyr. It is not 
		 * designed to simulate evolution on longer timescales and Python will 
		 * raise a warning to the user if they try to do so. 
		 * 
		 * The array will always be filled to 15 Gyr regardless of the final 
		 * time of the simulation. 
		 */ 
		long length = (long) (15.0 / dt); 
		m -> ria = (double *) malloc (length * sizeof(double));
		for (i = 0l; i < length; i++) {
			if (i * dt <= 13.8) {
				m -> ria[i] = R_SNe_Ia(*m, i * dt);
			} else {
				m -> ria[i] = 0;
			}
		}

		/* Normalize the DTD */
		double sum = 0;
		for (i = 0l; i < length; i++) {
			sum += (*m).ria[i];
		}
		for (i = 0l; i < length; i++) {
			m -> ria[i] /= sum;
		}
		return 0;
	}

}

/* 
 * Sets the elements SNe Ia yield parameter to the specified value 
 * 
 * Args:
 * =====
 * run:		A pointer to the INTEGRATION struct for this execution
 * index:		The index of the element to set the yield for
 * value:		The yield itself 
 * 
 * header: enrichment.h
 */
extern int set_sneia_yield(INTEGRATION *run, int index, double value) {

	ELEMENT *e = &((*run).elements[index]);
	e -> sneia_yield = value;
	return 0;

}

/* 
 * Returns the SNe Ia rate at some time t following the formation of a single 
 * stellar population at time 0 given the MODEL specifications contained in m. 
 * 
 * Args:
 * =====
 * m:		The MODEL struct for this execution
 * t:		The time following the formation of the population in Gyr.
 */
static double R_SNe_Ia(MODEL m, double t) {

	if (t < m.t_d) {
		return 0;
	} else if (!strcmp(m.dtd, "exp")) {
		/* An exponential DTD with user specified e-folding timescale */ 
		return exp( -t / m.tau_ia);
	} else if (!strcmp(m.dtd, "plaw")) {
		/* 
		 * A power law DTD. 1e-12 is added to the time so that it can evaluate 
		 * at zero without throwing an error 
		 */ 
		return powf(t + 1e-12, -1.1);
	} else {
		return -1;
	}

}



