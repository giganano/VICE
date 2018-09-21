
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"

static double r(MODEL m, double t);
static double m_remnants(MODEL m, double m_up, double m_low, double a);
static double m_remnants_large(double m_up, double m_low, double a);
static double m_remnants_small(double m, double a);
static void set_M0(MODEL m);
static double m_f(double m_up, double m_low, double a);
static void setup_single_breakdown(ELEMENT *e, long num_times);
static double M0;


/*
Returns the turnoff mass in solar masses of a single population of stars a 
time t following their formation.
*/
extern double m_turnoff(double t) {

	return powf( t/10 , -1.0/3.5);

}

/*
Returns the mass in solar masses recycled into the ISM of a either a given 
element or gas at the current timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution
m:			The MODEL struct for the current execution
index:		The index of the element. -1 for gas. 
*/
extern double m_returned(INTEGRATION run, MODEL m, int index) {

	if (m.continuous) {
		long i;
		double mret = 0;
		for (i = 0l; i < run.timestep; i++) {
			if (index != -1) {
				mret += run.mdotstar[run.timestep - i] * run.dt * (m.R[i + 1l] 
					- m.R[i]) * run.Zall[index][run.timestep - i];
			} else {
				mret += run.mdotstar[run.timestep - i] * run.dt * (m.R[i + 1l] - 
					m.R[i]);
			}
		}
		return mret;
	} else {
		if (index != -1) {
			return (run.SFR * run.dt * m.R0 * run.elements[index].m_tot / 
				run.MG);
		} else {
			return run.SFR * run.dt * m.R0;
		}
	}

}

/*
Sets up the array R for the INTEGRATION. This represents the cumulative 
return fraction at all times the INTEGRATION will evaluate at given the 
formation of a single stellar population at time 0.

Args:
=====
m:			A pointer to the MODEL struct for the current execution
times:		The times that the INTEGRATION will evaluate at
num_times:	The number of elements in the array times
*/
extern void setup_R(MODEL *m, double *times, long num_times) {

	long i;
	set_M0(*m);
	m -> R = (double *) malloc (num_times * sizeof(double));
	m -> R[0] = 0;
	for (i = 1l; i < num_times; i++) {
		m -> R[i] = r(*m, times[i]);
	}

}

/*
Returns the cumulative return fraction given the MODEL specifications and the 
time since formation of a single stellar population.

Args:
=====
m:		The MODEL struct for the current execution
t:		The time since the formation of the single stellar population
*/
static double r(MODEL m, double t) {

	double mr;
	if (!strcmp(m.imf, "salpeter")) {
		mr = m_remnants(m, m.m_upper, m_turnoff(t), 2.35);
	} else if (!strcmp(m.imf, "kroupa")) {
		double mto = m_turnoff(t);
		if (mto > 0.5) {
			mr = m_remnants(m, m.m_upper, mto, 2.3);
		} else if (0.08 <= mto && mto <= 0.5) {
			mr = m_remnants(m, m.m_upper, 0.5, 2.3) + m_remnants(m, 0.5, mto, 
				1.3);
		} else {
			mr = m_remnants(m, m.m_upper, 0.5, 2.3) + m_remnants(m, 0.5, 0.08, 
				1.3) + m_remnants(m, 0.08, mto, 0.3);
		}
	} else {
		printf("Unrecognized IMF: %s\n", m.imf);
		exit(0);
	}
	// printf("%lf\n", M0);
	return mr / M0;

}

/*
Returns the total mass of remnants given the limit of the mass and the 
effective power law index of the IMF over that mass range.
*/
static double m_remnants(MODEL m, double m_up, double m_low, double a) {

	if (m_low < 8) {
		return m_remnants_large(m_up, 8, a) + m_remnants_small(m_low, a);
	} else if (m_low > m.m_upper) {
		return 0;
	} else {
		return m_remnants_large(m_up, m_low, a);
	}

}

/*
Finds the total remnants mass when the turnoff mass is large, given the upper 
mass limit, the turnoff mass (m_low), and the power law index of the IMF in 
that range a.
*/
static double m_remnants_large(double m_up, double m_low, double a) {

	return (1/(2 - a) * powf(m_up, 2 - a) - 1.44/(1 - a) * powf(m_up, 1 - a) - 
		1/(2 - a) * powf(m_low, 2 - a) + 1.44/(1 - a) * powf(m_low, 1 - a));

}

/*
Finds the total remnants mass from stars less massive than 8 Msun when the 
turnoff mass is below that point. m denotes the turnoff mass and a denotes the 
power law index in that mass range.
*/
static double m_remnants_small(double m, double a) {

	return (0.891/(2 - a) * powf(8, 2 - a) - 0.394/(1 - a) * powf(8, 1 - a) - 
		0.891/(2 - a) * powf(m, 2 - a) + 0.394/(1 - a) * powf(m, 1 - a));

}

/*
Sets the variable M0 - the mass of stars formed in a single stellar 
population up to a normalization constant given the MODEL parameters 
contained in m.
*/
static void set_M0(MODEL m) {

	if (!strcmp(m.imf, "salpeter")) {
		M0 = m_f(m.m_upper, m.m_lower, 2.35);
	} else if (!strcmp(m.imf, "kroupa")) {
		if (m.m_lower > 0.5) {
			M0 = m_f(m.m_upper, m.m_lower, 2.3);
		} else if (0.08 <= m.m_lower && m.m_lower <= 0.5) {
			M0 = m_f(m.m_upper, 0.5, 2.3) + m_f(0.5, m.m_lower, 1.3);
		} else {
			M0 = m_f(m.m_upper, 0.5, 2.3) + m_f(0.5, 0.08, 1.3) + m_f(0.08, 
				m.m_lower, 0.3);
		}
	} else {
		printf("Unrecognized IMF: %s\n", m.imf);
		exit(0);
	}


}

/*
Returns the mass of stars formed in a single stellar population up to a 
normalization constant given the mass range and the power law index that is 
effective over that mass range.
*/
static double m_f(double m_up, double m_low, double a) {

	return 1/(2 - a) * (powf(m_up, 2 - a) - powf(m_low, 2 - a));

}

/*
Sets up the array H within the MODEL struct. This represents the mass fraction 
of a single stellar population that is still burning hydrogen in their cores 
at all timesteps following the formation of a single stellar population at 
time 0.

Args:
=====
m:			A pointer to the MODEL struct for this execution
times:		The array of times that this execution will visit
num_times:	The number of values in the array times
*/
extern void setup_H(MODEL *m, double *times, long num_times) {

	double m_upper = m -> m_upper;
	double m_lower = m -> m_lower;
	double den;
	if (!strcmp(m -> imf, "salpeter")) {
		den = 1.0/(2 - 2.35) * (powf(m_upper, 2 - 2.35) - powf(m_lower, 
			2 - 2.35));
	} else if (!strcmp(m -> imf, "kroupa")) {
		if (m_lower > 0.5) {
			den = 1.0/(2 - 2.3) * (powf(m_upper, 2-2.3) - powf(m_lower, 
				2-2.3));
		} else if (0.08 <= m_lower && m_lower <= 0.5) {
			den = (
				1.0/(2 - 2.3) * (powf(m_upper, 2-2.3) - powf(0.5, 2-2.3)) + 
				1.0/(2 - 1.3) * (powf(0.5, 2-1.3) - powf(m_lower, 2-1.3))
			);
		} else {
			den = (
				1.0/(2 - 2.3) * (powf(m_upper, 2-2.3) - powf(0.5, 2-2.3)) + 
				1.0/(2 - 1.3) * (powf(0.5, 2-1.3) - powf(0.08, 2 - 1.3)) +
				1.0/(2 - 0.3) * (powf(0.08, 2-0.3) - powf(m_lower, 2-0.3))
			);
		}
	} else {
		printf("Unrecognized IMF: %s\n", m -> imf);
		exit(0);
	}

	m -> H = (double *) malloc ((num_times + 1) * sizeof(double));
	long i;
	m -> H[0] = 1.0;
	for (i = 1l; i < num_times; i++) {
		double mto = m_turnoff(times[i]);
		if (mto >= m_upper) {
			m -> H[i] = 1.0;
			continue;
		} else if (mto <= m_lower) {
			m -> H[i] = 0.0;
			continue;
		} else {}

		if (!strcmp(m -> imf, "salpeter")) {
			m -> H[i] = 1.0/(2 - 2.35) * (powf(mto, 2 - 2.35) - 
				powf(m_lower, 2 - 2.35)) / den;
		} else if (!strcmp(m -> imf, "kroupa")) {
			if (m_lower > 0.5) {
				m -> H[i] = 1.0/(2 - 2.3) * (powf(mto, 2 - 2.3) - 
					powf(m_lower, 2 - 2.3)) / den;
			} else if (0.08 <= m_lower && m_lower <= 0.5) {
				if (mto >= 0.5) {
					m -> H[i] = (
						1.0/(2 - 2.3) * (powf(mto, 2 - 2.3) - 
							powf(0.5, 2 - 2.3)) + 
						1.0/(2 - 1.3) * (powf(0.5, 2 - 1.3) - 
							powf(m_lower, 2 - 1.3))
					) / den;
				} else {
					m -> H[i] = (
						1.0/(2 - 1.3) * (powf(mto, 2 - 1.3) - 
							powf(m_lower, 2 - 1.3))
					) / den;
				}
			} else {
				if (mto > 0.5) {
					m -> H[i] = (
						1.0/(2 - 2.3) * (powf(mto, 2 - 2.3) - 
							powf(0.5, 2 - 2.3)) + 
						1.0/(2 - 1.3) * (powf(0.5, 2 - 1.3) - 
							powf(0.08, 2 - 1.3)) + 
						1.0/(2 - 0.3) * (powf(0.08, 2 - 0.3) - 
							powf(m_lower, 2 - 0.3))
					) / den;
				} else if (0.08 <= mto && mto <= 0.5) {
					m -> H[i] = (
						1.0/(2 - 1.3) * (powf(mto, 2 - 1.3) - 
							powf(0.08, 2 - 1.3)) + 
						1.0/(2 - 0.3) * (powf(0.08, 2 - 0.3) - 
							powf(m_lower, 2 - 0.3))
					) / den;
				} else {
					m -> H[i] = (
						1.0/(2 - 0.3) * (powf(mto, 2 - 0.3) - 
							powf(m_lower, 2 - 0.3))
					) / den;
				}
			}
		} else {
			printf("Unrecognized IMF: %s\n", m -> imf);
			exit(0);
		}
	}

}

/*
Sets up the breakdown array for each element struct within the run.

Args:
=====
run:		The INTEGRATION struct for this iteration of the code
num_times:	The number of times that the iteration will evaluate at
*/
extern void setup_breakdown(INTEGRATION run, long num_times) {

	int i;
	for (i = 0; i < run.num_elements; i++) {
		setup_single_breakdown(&run.elements[i], num_times);
	}

}

/*
Sets up the breakdown array for a single element struct.

Args:
=====
e:			The element struct
num_times:	The number of times that the iteration will evaluate at
*/
static void setup_single_breakdown(ELEMENT *e, long num_times) {

	long i;
	e -> breakdown = (double **) malloc (num_times * sizeof(double *));
	for (i = 0l; i < num_times; i++) {
		e -> breakdown[i] = (double *) malloc (3 * sizeof(double));
	}

}

/*
Sets up the Zall array for the INTEGRATION struct.

Args:
=====
run:		A pointer to the INTEGRATION struct
num_times:	The number of times that the iteration will evaluate at
*/
extern void setup_Zall(INTEGRATION *run, long num_times) {

	int i;
	run -> Zall = (double **) malloc ((*run).num_elements * sizeof(double *));
	for (i = 0; i < (*run).num_elements; i++) {
		run -> Zall[i] = (double *) malloc (num_times * sizeof(double));
	}

}


