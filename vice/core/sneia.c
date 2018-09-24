
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"

static double mdotstarIa(INTEGRATION run, MODEL m);
static double R_SNe_Ia(MODEL m, double t);
// static double *RIA;

/*
Returns the time derivative of the mass of a given element at the current 
timestep from SNe Ia alone.

Args:
=====
run:		The INTEGRATION struct for the current execution.
index:		The index of the element in question.
*/
extern double mdot_ia(INTEGRATION run, MODEL m, int index) {

	return run.elements[index].sneia_yield * mdotstarIa(run, m);

}

/*
Returns the star formation rate weighted by the SNe Ia rate.

Args:
=====
run:		The INTEGRATION struct for the current execution.
*/
static double mdotstarIa(INTEGRATION run, MODEL m) {

	double sfria = 0;
	long i;
	for (i = 0l; i < run.timestep; i++) {
		sfria += m.ria[run.timestep - i] * run.mdotstar[i];
	}
	return sfria;

}

#if 0
/*
Sets up the array RIA containing the SNe Ia rate at all times following the 
formation of a single stellar population at time 0.

Args:
=====
m:			The MODEL struct for this execution
times:		The times that the INTEGRATION will evaluate at
num_times:	The number of elements in the times array
*/
extern int setup_RIA(MODEL *m, double *times, long num_times) {

	if (R_SNe_Ia(*m, times[0]) == -1) {
		return 1;
	} else {
		long i;
		m -> ria = (double *) malloc (num_times * sizeof(double));
		for (i = 0l; i < num_times; i++) {
			m -> ria[i] = R_SNe_Ia(*m, times[i]);
		}
		double sum = 0;
		for (i = 0l; i < num_times; i++) {
			sum += (*m).ria[i];
		}
		for (i = 0l; i < num_times; i++) {
			m -> ria[i] /= sum;
		}
		return 0;
	}

}
#endif

/*
Sets up the array RIA containing the SNe Ia rate at all times following the 
formation of a single stellar population at time 0. 

Args:
=====
m:		The MODEL struct for this execution
dt:		The timestep size
*/
extern int setup_RIA(MODEL *m, double dt) {

	if (R_SNe_Ia(*m, dt) == -1) {
		return 1;
	} else {
		long i;
		long length = (long) 12.5 / dt;
		m -> ria = (double *) malloc (length * sizeof(double));
		for (i = 0l; i < length; i++) {
			m -> ria[i] = R_SNe_Ia(*m, i * dt);
		}
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
Returns the SNe Ia rate at some time t following the formation of a single 
stellar population at time 0 given the MODEL specifications contained in m.

Args:
=====
m:		The MODEL struct for this execution
t:		The time following the formation of the population in Gyr.
*/
static double R_SNe_Ia(MODEL m, double t) {

	if (t < m.t_d) {
		return 0;
	} else if (!strcmp(m.dtd, "exp")) {
		return exp( -t / m.tau_ia);
	} else if (!strcmp(m.dtd, "plaw")) {
		return powf(t + 1e-12, -1.1);
	} else {
		return -1;
	}

}

/* 
Sets the elements SNe Ia yield parameter to the specified value 

Args:
=====
e:			A pointer to the element struct to hold the yield
value:		The yield itself
*/
extern int set_sneia_yield(INTEGRATION *run, int index, double value) {

	ELEMENT *e = &((*run).elements[index]);
	e -> sneia_yield = value;
	return 0;

}

