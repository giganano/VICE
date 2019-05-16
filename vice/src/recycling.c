/*
 * This script handles the numerical implementation of recycling from 
 * previous generations of stars. 
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double r(MODEL m, double t);
static double m_remnants(MODEL m, double m_up, double m_low, double a);
static double m_remnants_large(double m_up, double m_low, double a);
static double m_remnants_small(double m, double a);
static void set_M0(MODEL m);
static double m_f(double m_up, double m_low, double a);

/* The normalization of the IMF is stored here */
static double M0;


/*
 * Returns the turnoff mass in solar masses of a single population of stars a 
 * time t in Gyr following their formation.
 * 
 * header: stars.h 
 */
extern double m_turnoff(double t) {

	/* m_to = (t/10 Gyr)^(-1/3.5) */
	return powf( t/10 , -1.0/3.5);

}

/*
 * This function calculates the mass of a given element recycled to the 
 * ISM at the birth metallicity of stars as they go through stellar death. 
 * This function also calculates the mass of gas returned the ISM by not 
 * weighting the contribution from each timestep by metallicity when 
 * index == -1. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current execution
 * index:		The index of the element. -1 for gas. 
 * 
 * header: stars.h 
 */
extern double m_returned(INTEGRATION run, MODEL m, int index) {

	/* ----------------------- Continuous recycling ----------------------- */ 
	if (m.continuous) {
		long i;
		double mret = 0;
		/* From each previous timestep */ 
		for (i = 0l; i < run.timestep; i++) {
			if (index != -1) { 		// if this is an element ... 
				mret += run.mdotstar[run.timestep - i] * run.dt * (m.R[i + 1l] 
					- m.R[i]) * run.Zall[index][run.timestep - i];
			} else {				// ... or the gas supply 
				mret += run.mdotstar[run.timestep - i] * run.dt * (m.R[i + 1l] - 
					m.R[i]);
			}
		}
		return mret;
	/* ---------------------- Instantaneous recycling ---------------------- */ 
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
 * Sets up the array R for the INTEGRATION. This stores the value of the 
 * cumulative return fraction at all timesteps the simulation will evalute at. 
 * Each stellar population then draws from this array given the time it formed 
 * and the current timestep. 
 * 
 * Args:
 * =====
 * m:			A pointer to the MODEL struct for the current execution
 * times:		The times that the INTEGRATION will evaluate at
 * num_times:	The number of elements in the array times
 * 
 * header: stars.h 
 */
extern void setup_R(MODEL *m, double *times, long num_times) {
 
	long i;
	set_M0(*m); 	// Normalization of the IMF
	/* Allocate memory and just map the function across each timestep */ 
	m -> R = (double *) malloc (num_times * sizeof(double));
	m -> R[0] = 0;
	for (i = 1l; i < num_times; i++) {
		m -> R[i] = r(*m, times[i]);
	}

}

/*
 * Returns the cumulative return fraction given the MODEL specifications and the 
 * time since formation of a single stellar population. The cumulative return 
 * fraction does not have a simple analytic form - for details see VICE's science 
 * documentation. 
 * 
 * Args:
 * =====
 * m:		The MODEL struct for the current execution
 * t:		The time since the formation of the single stellar population
 */
static double r(MODEL m, double t) {

	double mr;		// The mass tied up in remnants 
	if (!strcmp(m.imf, "salpeter")) {
		/* 
		 * The Salpeter IMF has a power law index of 2.35 for all stellar 
		 * masses, so there is no necessary piecewise treatment. 
		 */ 
		mr = m_remnants(m, m.m_upper, m_turnoff(t), 2.35);
	} else if (!strcmp(m.imf, "kroupa")) {
		/* 
		 * The Kroupa IMF is piecewise, adopting a power law index of 2.3 
		 * above 0.5 Msun, 1.3 between 0.08 and 0.5 Msun, and 0.3 below that. 
		 * 
		 * Here we simply add up the remnant mass in each range based on the 
		 * turnoff mass. 
		 */
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
		/* This should be caught by Python anyway */ 
		printf("Unrecognized IMF: %s\n", m.imf);
		exit(0);
	}
	return mr / M0;

}

/*
 * Returns the total mass of remnants given the limit of the mass and the 
 * effective power law index of the IMF over that mass range. Remnant masses 
 * are modeled off of Kalirai et al. (2008), ApJ, 676, 594. See VICE science 
 * documentation for details. 
 * 
 * Args:
 * =====
 * m:			The MODEL struct for this integration 
 * m_up:		The upper mass limit on star formation
 * m_low:		The lower mass limit on star formation 
 * a:			The power law index of the IMF in this mass range
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
 * Finds the total remnants mass when the turnoff mass is large, given the upper 
 * mass limit, the turnoff mass (m_low), and the power law index of the IMF in 
 * that range a. The prefactors here are determined by integrating the IMF 
 * modeling the remnant masses of the stars according to Kalirai et al. (2008), 
 * ApJ, 676, 594. See VICE science documentation for details. 
 * 
 * Args: 
 * =====
 * m_up:			The upper mass limit for the relevant range of masses
 * m_low: 			The lower mass limit for the relevant range of masses
 * a:				The power law index of the IMF in this range 
 */
static double m_remnants_large(double m_up, double m_low, double a) {

	return (1/(2 - a) * powf(m_up, 2 - a) - 1.44/(1 - a) * powf(m_up, 1 - a) - 
		1/(2 - a) * powf(m_low, 2 - a) + 1.44/(1 - a) * powf(m_low, 1 - a));

}

/*
 * Finds the total remnants mass from stars less massive than 8 Msun when the 
 * turnoff mass is below that point. m denotes the turnoff mass and a denotes the 
 * power law index in that mass range. The prefactors here are determined by 
 * integrating the IMF modeling the remnant masses of the stars according to 
 * Kalirai et al. (2008), ApJ, 676, 594. See VICE science documentation for 
 * details. 
 * 
 * Args:
 * =====
 * m: 		The lower mass limit for the relevant range of masses
 * a:		The power law index of the IMF in this range. 
 * 
 * Note that there is no upper mass limit required, because according to the 
 * Kalirai et al. (2008) model, the upper limit in this range is 8 Msun. 
 */
static double m_remnants_small(double m, double a) {

	return (0.891/(2 - a) * powf(8, 2 - a) - 0.394/(1 - a) * powf(8, 1 - a) - 
		0.891/(2 - a) * powf(m, 2 - a) + 0.394/(1 - a) * powf(m, 1 - a));

}

/*
 * Sets the normalization of the IMF M0 - this represents the total mass of 
 * stars formed by a single stellar population divided by the true 
 * normalization constant of the IMF. 
 * 
 * Args: 
 * =====
 * m: 		The MODEL struct for this simulation
 */
static void set_M0(MODEL m) {

	if (!strcmp(m.imf, "salpeter")) {
		/* 
		 * The Salpeter IMF has a power law index of 2.35 over the entire 
		 * range of stellar masses that form 
		 */ 
		M0 = m_f(m.m_upper, m.m_lower, 2.35);
	} else if (!strcmp(m.imf, "kroupa")) {
		/* 
		 * The Kroupa IMF is piecewise, with power law indeces of 2.3 above 
		 * 0.5 Msun, 1.3 between 0.08 and 0.5 Msun, and 0.3 below 0.08 Msun. 
		 */ 
		if (m.m_lower > 0.5) {
			M0 = m_f(m.m_upper, m.m_lower, 2.3);
		} else if (0.08 <= m.m_lower && m.m_lower <= 0.5) {
			M0 = m_f(m.m_upper, 0.5, 2.3) + m_f(0.5, m.m_lower, 1.3);
		} else {
			M0 = m_f(m.m_upper, 0.5, 2.3) + m_f(0.5, 0.08, 1.3) + m_f(0.08, 
				m.m_lower, 0.3);
		}
	} else {
		/* This should be caught by Python anyway */ 
		printf("Unrecognized IMF: %s\n", m.imf);
		exit(0);
	}


}

/*
 * Returns the mass of stars formed in a single stellar population up to a 
 * normalization constant given the mass range and the power law index that is 
 * effective over that mass range. This is the analytic expression associated 
 * with a simple integration of m(dN/dm) for the adopted IMF. 
 * 
 * Args: 
 * =====
 * m_up:		The upper mass limit on this range of stellar masses
 * m_low:		The lower mass limit on this range of stellar masses
 * a:			The power law index on the IMF in this range 
 */
static double m_f(double m_up, double m_low, double a) {

	return 1/(2 - a) * (powf(m_up, 2 - a) - powf(m_low, 2 - a));

}

/*
 * Sets up the array H within the MODEL struct. This represents the mass 
 * fraction of a single stellar population that is still burning hydrogen in 
 * their cores at all timesteps following the formation of a single stellar 
 * population at time 0. This value does not have a simple analytic 
 * expression - see VICE science documentation for details. 
 * 
 * Args:
 * =====
 * m:				A pointer to the MODEL struct for this execution
 * times:			The array of times that this execution will visit
 * num_times:		The number of values in the array times
 * 
 * header: stars.h 
 */
extern void setup_H(MODEL *m, double *times, long num_times) {

	/* 
	 * Referencing these variables a lot here ---> delcare them on the 
	 * stack for ease 
	 */ 
	double m_upper = m -> m_upper;
	double m_lower = m -> m_lower;

	/* Determine the numerator and denominator of h separately */ 
	double den;
	if (!strcmp(m -> imf, "salpeter")) {
		/* Salpeter IMF ---> analytically integrated form */ 
		den = 1.0/(2 - 2.35) * (powf(m_upper, 2 - 2.35) - powf(m_lower, 
			2 - 2.35));
	} else if (!strcmp(m -> imf, "kroupa")) { 
		/* Kroupa IMF ---> analytically integrated form */ 
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
		/* Python should have caught this anyway */ 
		printf("Unrecognized IMF: %s\n", m -> imf);
		exit(0);
	}

	/* Allocate memory for the array */ 
	m -> H = (double *) malloc ((num_times + 1) * sizeof(double));
	long i;
	m -> H[0] = 1.0; // H(0) = 1 by definition 
	for (i = 1l; i < num_times; i++) {
		double mto = m_turnoff(times[i]);
		if (mto >= m_upper) {
			m -> H[i] = 1.0; // If no stars have died yet, h = 1 still 
			continue;
		} else if (mto <= m_lower) {
			m -> H[i] = 0.0; // If they've all died, h = 0
			continue;
		} else {}

		if (!strcmp(m -> imf, "salpeter")) {
			/* 
			 * Salpeter IMF ---> analytically integrated form from the 
			 * lower mass limit to the turnoff mass 
			 */ 
			m -> H[i] = 1.0/(2 - 2.35) * (powf(mto, 2 - 2.35) - 
				powf(m_lower, 2 - 2.35)) / den;
		} else if (!strcmp(m -> imf, "kroupa")) {
			/* 
			 * Kroupa IMF ---> analytically integrated form from the 
			 * lower mass limit to the turnoff mass. 
			 * 
			 * Each if statement here does the same thing, just with 
			 * careful treatment about where both the turnoff mass 
			 * and lower stellar mass limit lie with respect to the 
			 * piecewise breaks in the Kroupa (2001) IMF. 
			 */ 
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
			/* 
			 * If somehow not caught by Python, this also would've been 
			 * caught earlier in this function 
			 */ 
			printf("Unrecognized IMF: %s\n", m -> imf);
			exit(0);
		}
	}

}





