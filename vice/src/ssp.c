/* 
 * This file implements the time evolution of quantities relevant to single 
 * stellar populations (SSPs). In the current version of VICE, this includes 
 * the single stellar population enrichment function, the main sequence mass 
 * fraction, and the cumulative return fraction. In general, these features 
 * ease the computational expense of singlezone simulations. 
 * 
 * NOTES 
 * ===== 
 * There are factors of 0.08 and 0.04 on the Kroupa IMF for the 0.08 Msun < 
 * m < 0.5 Msun and m > 0.5 Msun mass ranges. This ensures that the IMF 
 * returns the same values on either side of 0.08 and 0.5 Msun. These factors 
 * are independent of the normalization of the IMF and must appear for the 
 * distribution of stellar masses to be consistent. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "agb.h" 
#include "ccsne.h" 
#include "sneia.h"  
#include "ssp.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double CRFnumerator_Kalirai08(SSP ssp, double time); 
static double CRFnumerator_Kalirai08_IMFrange(double m_upper, 
	double turnoff_mass, double m_lower, double a); 
static double CRFnumerator_Kalirai08_above_8Msun(double m_upper, 
	double turnoff_mass, double a); 
static double CRFnumerator_Kalirai08_below_8Msun(double m_upper, 
	double turnoff_mass, double a); 
static double CRFdenominator(SSP ssp); 
static double CRFdenominator_IMFrange(double m_upper, double m_lower, 
	double a); 
static double MSMFdenominator(SSP ssp); 
static double MSMFnumerator(SSP ssp, double time); 

/* 
 * Allocate memory for and return a pointer to an SSP struct. Automatically 
 * sets both crf and msmf to NULL. Allocates memory for a 100-element char * 
 * IMF specifier. 
 * 
 * header: ssp.h 
 */ 
extern SSP *ssp_initialize(void) { 

	SSP *ssp = (SSP *) malloc (sizeof(SSP)); 
	ssp -> imf = (char *) malloc (100 * sizeof(char)); 
	ssp -> crf = NULL; 
	ssp -> msmf = NULL; 
	return ssp; 

} 

/* 
 * Free up the memory stored in an SSP struct. 
 * 
 * header: ssp.h 
 */ 
extern void ssp_free(SSP *ssp) {

	if ((*ssp).crf != NULL) free(ssp -> crf); 
	if ((*ssp).msmf != NULL) free(ssp -> msmf); 
	free(ssp -> imf); 
	free(ssp); 

} 

/* 
 * Determine the main sequence turnoff mass in solar masses of a single 
 * stellar population at a time t in Gyr following their formation. 
 * 
 * Parameters 
 * ========== 
 * t: 		Time in Gyr 
 * 
 * Returns 
 * ======= 
 * Main sequence turnoff mass in solar masses via (t / 10 Gyr)^(-1/3.5) 
 * 
 * Notes 
 * ===== 
 * 10 Gyr and 3.5 are values that can be changed in ssp.h 
 * 
 * header: utils.h 
 */ 
extern double main_sequence_turnoff_mass(double time) {

	/* m_to = (t / 10 Gyr)^(-1/3.5) */ 
	return pow( time/SOLAR_LIFETIME, -1.0/MASS_LIFETIME_PLAW_INDEX ); 

} 

/* 
 * Run a simulation of elemental production for a single element produced by a 
 * single stellar population. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		A pointer to an SSP object 
 * e: 			A pointer to an element to run the simulation for 
 * Z: 			The metallicity by mass of the stellar population 
 * times: 		The times at which the simulation will evaluate 
 * n_times: 	The number of elements in the times array 
 * mstar: 		The mass of the stellar population in Msun 
 * 
 * Returns 
 * ======= 
 * An array of the same length as times, where each element is the mass of the 
 * given chemical element at the corresponding time. NULL on failure to 
 * allocate memory. 
 * 
 * header: ssp.h 
 */ 
extern double *single_population_enrichment(SSP *ssp, ELEMENT *e, 
	double Z, double *times, long n_times, double mstar) {

	double *mass = (double *) malloc (n_times * sizeof(double)); 
	if (mass == NULL) return NULL; 	/* memory error */ 

	ssp -> msmf = (double *) malloc (n_times * sizeof(double)); 
	if ((*ssp).msmf == NULL) return NULL; /* memory error */ 

	long i; 
	for (i = 0l; i < n_times; i++) {
		ssp -> msmf[i] = MSMF(*ssp, times[i]); 
	} 

	mass[0] = 0; 
	if (n_times >= 2l) { 
		/* The contribution from CCSNe */ 
		mass[1] = get_cc_yield(*e, Z) * mstar; 
		for (i = 2l; i < n_times; i++) {
			mass[i] = mass[i - 1l]; 		/* previous timesteps */ 

			/* The contribution from SNe Ia */ 
			mass[i] += ((*(*e).sneia_yields).yield_ * 
				(*(*e).sneia_yields).RIa[i] * mstar); 

			/* The contribution from AGB stars */ 
			mass[i] += (
				get_AGB_yield(*e, Z, main_sequence_turnoff_mass(times[i])) * 
				mstar * ((*ssp).msmf[i] - (*ssp).msmf[i + 1l])); 

		}
	} else {} 

	return mass; 

}

/* 
 * Determine the mass recycled from all previous generations of stars for 
 * either a given element or the gas supply. For details, see section 3.3 of 
 * VICE's science documentation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * e: 		A pointer to the element to find the recycled mass. NULL to find 
 * 			it for the total ISM gas. 
 * 
 * Returns 
 * ======= 
 * The recycled mass in Msun 
 * 
 * header: ssp.h 
 */ 
extern double mass_recycled(SINGLEZONE sz, ELEMENT *e) {

	/* ----------------------- Continuous recycling ----------------------- */ 
	if ((*sz.ssp).continuous) {
		long i; 
		double mass = 0; 
		/* 
		 * From each previous timestep, there's a dCRF contribution 
		 * Start at i = 1 because only previous generations of stars are 
		 * recycling. 
		 */ 
		for (i = 0l; i <= sz.timestep; i++) {
			if (e == NULL) { 		/* This is the gas supply */ 
				mass += ((*sz.ism).star_formation_history[sz.timestep - i] * 
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i])); 
			} else { 			/* element -> weight by Z */ 
				mass += ((*sz.ism).star_formation_history[sz.timestep - i] * 
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i]) * 
					(*e).Z[sz.timestep - i]); 
			} 
		} 
		return mass; 
	/* ---------------------- Instantaneous recycling ---------------------- */ 
	} else {
		if (e == NULL) {			/* gas supply */ 
			return (*sz.ism).star_formation_rate * sz.dt * (*sz.ssp).R0; 
		} else { 				/* element -> weight by Z */ 
			return ((*sz.ism).star_formation_rate * sz.dt * (*sz.ssp).R0 * 
				(*e).mass / (*sz.ism).mass); 
		}
	}

} 

/* 
 * Evaluate the cumulative return fraction across all timesteps in preparation 
 * of a singlezone simulation. This will store the CRF in the SSP struct 
 * within the singlezone object. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A singlezone object to setup the CRF within 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: ssp.h 
 */ 
extern int setup_CRF(SINGLEZONE *sz) {

	double denominator = CRFdenominator((*(*sz).ssp)); 
	if (denominator < 0) {
		/* 
		 * denominator will be -1 in the case of an unrecognized IMF; return 
		 * 1 on failure 
		 */ 
		return 1; 
	} else { 
		/* 
		 * By design, the singlezone object fills arrays of time-varying 
		 * quantities for ten timesteps beyond the endpoint of the simulation. 
		 * This is a safeguard against memory errors. 
		 */ 
		long i, n = 10l + (long) (
			(*sz).output_times[(*sz).n_outputs - 1l] / (*sz).dt); 

		sz -> ssp -> crf = (double *) malloc (n * sizeof(double)); 
		for (i = 0l; i < n; i++) {
			sz -> ssp -> crf[i] = CRFnumerator_Kalirai08(
				(*(*sz).ssp), i * (*sz).dt) / denominator; 
		} 
		return 0; 

	}

}

/* 
 * Determine the cumulative return fraction from a single stellar population 
 * a given time in Gyr after its formation. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		An SSP struct containing information on the stallar IMF and 
 * 				the mass range of star formation 
 * time: 		The age of the stellar population in Gyr 
 * 
 * Returns 
 * ======= 
 * The value of the CRF at that time for the IMF assumptions encoded into the 
 * SSP struct. -1 in the case of an unrecognized IMF 
 * 
 * header: ssp.h 
 */ 
extern double CRF(SSP ssp, double time) { 

	double numerator = CRFnumerator_Kalirai08(ssp, time); 
	if (numerator < 0) {
		/* numerator will be -1 in the case of an unrecognized IMF */ 
		return -1; 
	} else {
		return numerator / CRFdenominator(ssp); 
	}

}

/* 
 * Determine the total mass returned to the ISM from a single stellar 
 * population from all stars a time t in Gyr following their formation. This 
 * is determined by subtracting the Kalirai et al. (2008) model for stellar 
 * remnant masses from the initial mass of stars in this mass range, then 
 * weighting the stellar IMF by this quantity and integrating over the mass 
 * range of star formation. The prefactors are determined in this manner; see 
 * section 2.2 of VICE's science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		The SSP struct containing information on the stellar IMF and 
 * 				the mass range of star formation 
 * time: 		The time in Gyr following the single stellar population's 
 * 				formation. 
 * 
 * Returns 
 * ======= 
 * The total returned mass in solar masses up to the normalization of the 
 * stellar IMF. -1 in the case of an unrecognized IMF. 
 * 
 * Notes 
 * ===== 
 * This implementation differs mildly from the analytic expression presented 
 * in section 2.2 of VICE's science documentation. This implementation solves 
 * the integral from the turnoff mass to the 8 Msun plus the integral from 
 * 8 Msun to the upper mass limit. 
 * 
 * References 
 * ========== 
 * Kalirai et al. (2008), ApJ, 676, 594 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double CRFnumerator_Kalirai08(SSP ssp, double time) {

	double turnoff_mass = main_sequence_turnoff_mass(time); 

	if (!strcmp(ssp.imf, "salpeter")) {
		/* Salpeter IMF */
		return CRFnumerator_Kalirai08_IMFrange(
			ssp.m_upper, 
			turnoff_mass, 
			ssp.m_lower, 
			2.35); 
	} else if (!strcmp(ssp.imf, "kroupa")) {
		/* kroupa IMF */ 
		if (turnoff_mass > 0.5) {
			return 0.04 * CRFnumerator_Kalirai08_IMFrange(
				ssp.m_upper, 
				turnoff_mass, 
				ssp.m_lower, 
				2.3); 
		} else if (0.08 <= turnoff_mass && turnoff_mass <= 0.5) {
			return (0.04 * CRFnumerator_Kalirai08_IMFrange(
				ssp.m_upper, 
				turnoff_mass, 
				0.5, 
				2.3) 
			+ 0.08 * CRFnumerator_Kalirai08_IMFrange(
				0.5, 
				turnoff_mass, 
				ssp.m_lower, 
				1.3)); 
		} else {
			return (0.04 * CRFnumerator_Kalirai08_IMFrange(
				ssp.m_upper, 
				turnoff_mass, 
				0.5, 
				2.3) 
			+ 0.08 * CRFnumerator_Kalirai08_IMFrange(
				0.5, 
				turnoff_mass, 
				0.08, 
				1.3) 
			+ CRFnumerator_Kalirai08_IMFrange(
				0.08, 
				turnoff_mass, 
				ssp.m_lower, 
				0.3)); 
		} 
	} else {
		/* unrecognized IMF, return -1 on failure */ 
		return -1; 
	}

}

/* 
 * Determine the total mass returned to the ISM from a single stellar 
 * population from a given range of stellar initial mass. This is determined 
 * by subtracting the Kalirai et al. (2008) model for stellar remnant masses 
 * from the initial mass of stars in this mass range, then weighting the 
 * stellar IMF by this quantity and integrating over the mass range of star 
 * formation. The prefactors are determined in this manner; see section 2.2 
 * of VICE's science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * m_upper: 		The upper mass limit on star formation in Msun 
 * turnoff_mass: 	The main sequence turnoff mass in Msun 
 * m_lower: 		The lower mass limit on star formation in Msun 
 * a: 				The power law index of the stellar IMF. This implementation 
 * 					allows routines that call it to be generalized for 
 * 					piece-wise IMFs like Kroupa (2001). 
 * 
 * Returns 
 * ======= 
 * The total returned mass in solar masses up to the normalization of the 
 * stellar IMF. 
 * 
 * Notes 
 * ===== 
 * This implementation differs mildly from the analytic expression presented 
 * in section 2.2 of VICE's science documentation. This implementation solves 
 * the integral from the turnoff mass to the 8 Msun plus the integral from 
 * 8 Msun to the upper mass limit. 
 * 
 * References 
 * ========== 
 * Kalirai et al. (2008), ApJ, 676, 594 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double CRFnumerator_Kalirai08_IMFrange(double m_upper, 
	double turnoff_mass, double m_lower, double a) { 

	/* 
	 * These functions likely could have been condensed into one method, but 
	 * this is the implementation that seemed to maximize readability 
	 */ 

	if (turnoff_mass < m_lower) { 
		/* 
		 * No more remnants once all stars have died, so report only those 
		 * formed from the relevant range of initial stellar masses. In this 
		 * way, this function can be called with the true turnoff mass, 
		 * letting m_upper and m_lower be the mass bounds on a given 
		 * piece-wise range of the IMF, and the proper value will always be 
		 * returned. 
		 */ 
		return CRFnumerator_Kalirai08_IMFrange(m_upper, m_lower, m_lower, a); 
	} else if (turnoff_mass > m_upper) {
		/* No remnants yet */ 
		return 0; 
	} else if (turnoff_mass >= 8) { 
		/* Stars have died, but only those above 8 Msun */ 
		return CRFnumerator_Kalirai08_above_8Msun(m_upper, turnoff_mass, a); 
	} else { 
		if (m_upper > 8) {
			/* All stars above 8 Msun have died */ 
			return (CRFnumerator_Kalirai08_above_8Msun(m_upper, 8, a) + 
				CRFnumerator_Kalirai08_below_8Msun(8, turnoff_mass, a)); 
		} else {
			/* There never were any stars above 8 Msun to begin with */ 
			return (CRFnumerator_Kalirai08_below_8Msun(m_upper, 
				turnoff_mass, a)); 
		}
			
	}

}

/* 
 * Determine the total mass returned to the ISM from a single stellar 
 * population from stars with initial stellar masses above 8 Msun. This is 
 * determined by subtracting the Kalirai et al. (2008) model for stellar 
 * remnant masses from the initial mass of stars in this mass range, then 
 * weighting the stellar IMF by this quantity and integrating over the mass 
 * range of star formation. The prefactors are determined in this manner; see 
 * section 2.2 of VICE's science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * m_upper: 			The upper mass limit on star formation in Msun 
 * turnoff_mass: 		The main sequence turnoff mass in Msun 
 * a: 					The power law index of the stellar IMF below 8 Msun. 
 * 
 * Returns 
 * ======= 
 * The returned mass in solar masses up to the normalization of the 
 * stellar IMF 
 * 
 * References 
 * ========== 
 * Kalirai et al. (2008), ApJ, 676, 594 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double CRFnumerator_Kalirai08_above_8Msun(double m_upper, 
	double turnoff_mass, double a) { 

	return (1/(2 - a) * pow(m_upper, 2 - a) - 1.44/(1 - a) * 
		pow(m_upper, 1 - a) - 1/(2 - a) * pow(turnoff_mass, 2 - a) + 
		1.44/(1 - a) * pow(turnoff_mass, 1 - a));

}

/* 
 * Determine the total mass returned to the ISM from a single stellar 
 * population from stars with initial stellar masses below 8 Msun. This is 
 * determined by subtracting the Kalirai et al. (2008) model for stellar 
 * remnant masses from the initial mass of stars in this mass range, then 
 * weighting the stellar IMF by this quantity and integrating over the mass 
 * range of star formation. The prefactors are determined in this manner; see 
 * section 2.2 of VICE's science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * m_upper: 			The upper mass bound (should always be 8 unless 
 * 						simulating models with no stars above 8 Msun) 
 * turnoff_mass: 		The main sequence turnoff mass in Msun 
 * a: 					The power law index on the stellar IMF below 8 Msun. 
 * 
 * Returns 
 * ======= 
 * The returned mass in solar masses up to the normalization of the 
 * stellar IMF 
 * 
 * References  
 * ========== 
 * Kalirai et al. (2008), ApJ, 676, 594 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double CRFnumerator_Kalirai08_below_8Msun(double m_upper, 
	double turnoff_mass, double a) {

	return (0.891/(2 - a) * pow(m_upper, 2 - a) - 0.394/(1 - a) * 
		pow(m_upper, 1 - a) - 0.891/(2 - a) * pow(turnoff_mass, 2 - a) + 
		0.394/(1 - a) * pow(turnoff_mass, 1 - a));	

} 

/* 
 * Determine the denominator of the cumulative return fraction. This is the 
 * total mass of a single stellar population up to the normalization 
 * constant of the IMF. This is determined by the mass range of star 
 * formation and the IMF itself. See section 2.2 of VICE's science 
 * documentation for details. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		The SSP struct containing information on the IMF and the 
 * 				allowed mass ranges of star formation 
 * 
 * Returns 
 * ======= 
 * The denominator of the cumulative return fraction. When the returned mass 
 * determined by functions in this module is divided by this value, the 
 * CRF is determined. -1 in the case of an unrecognized IMF. 
 */ 
static double CRFdenominator(SSP ssp) {

	if (!strcmp(ssp.imf, "salpeter")) {
		return CRFdenominator_IMFrange(ssp.m_upper, ssp.m_lower, 2.35); 
	} else if (!strcmp(ssp.imf, "kroupa")) {
		if (ssp.m_lower > 0.5) {
			return 0.04 * CRFdenominator_IMFrange(ssp.m_upper, ssp.m_lower, 
				2.3); 
		} else if (0.08 <= ssp.m_lower && ssp.m_lower <= 0.5) {
			return (0.04 * CRFdenominator_IMFrange(ssp.m_upper, 0.5, 2.3) + 
				0.08 * CRFdenominator_IMFrange(0.5, ssp.m_lower, 1.3)); 
		} else {
			return (0.04 * CRFdenominator_IMFrange(ssp.m_upper, 0.5, 2.3) + 
				0.08 * CRFdenominator_IMFrange(0.5, 0.08, 1.3) + 
				CRFdenominator_IMFrange(0.08, ssp.m_lower, 0.3)); 
		} 
	} else {
		return -1; 
	}

}

/* 
 * Determine one term in the denominator of the cumulative return fraction. 
 * See section 2.2 of VICE's science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * m_upper: 		The upper mass limit on this range of star formation 
 * m_lower: 		The lower mass limit on this range of star formation 
 * a: 				The power law index on the stellar IMF here 
 * 
 * Returns 
 * ======= 
 * The total initial main sequence mass formed in a given range of star 
 * formation, up to the normalization constant of the IMF. 
 */ 
static double CRFdenominator_IMFrange(double m_upper, double m_lower, 
	double a) {

	return 1 / (2 - a) * (pow(m_upper, 2 - a) - pow(m_lower, 2- a)); 

} 

/* 
 * Evaluate the main sequence mass fraction across all timesteps in preparation 
 * of a singlezone simulation. This will store the MSMF in the SSP struct 
 * within the singlezone object. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A singlezone object to setup the MSMF within 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: ssp.h 
 */ 
extern int setup_MSMF(SINGLEZONE *sz) {

	double denominator = MSMFdenominator((*(*sz).ssp)); 
	if (denominator < 0) {
		/* 
		 * denominator will be -1 in the case of an unrecognized IMF; return 
		 * 1 on failure. 
		 */ 
		return 1; 
	} else {
		/* 
		 * By design, the singlezone object fills arrays of time-varying 
		 * quantities for ten timesteps beyond the endpoint of the simulation. 
		 * This is a safeguard against memory errors. 
		 */ 
		long i, n = 10l + (long) (
			(*sz).output_times[(*sz).n_outputs - 1l] / (*sz).dt); 

		sz -> ssp -> msmf = (double *) malloc (n * sizeof(double)); 
		for (i = 0l; i < n; i++) {
			sz -> ssp -> msmf[i] = MSMFnumerator((*(*sz).ssp), 
				i * (*sz).dt) / denominator; 
		} 
		return 0; 
	}

}

/* 
 * Determine the main sequence mass fraction of a stellar population a some 
 * time following its formation. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		A SSP struct containing information on the stellar IMF and 
 * 				the mass range of star formation 
 * time: 		The age of the stellar population in Gyr 
 * 
 * Returns 
 * ======= 
 * The value of the main sequence mass fraction at the specified age. -1 in 
 * the case of an unrecognized IMF. 
 * 
 * header: ssp.h 
 */ 
extern double MSMF(SSP ssp, double time) { 

	double denominator = MSMFdenominator(ssp); 
	if (denominator < 0) { 
		/* MSMFdenominator returns -1 for an unrecognized IMF */ 
		return -1; 
	} else { 
		return MSMFnumerator(ssp, time) / denominator; 
	}

}

/* 
 * Determine the denominator of the main sequence mass fraction. This is 
 * the total initial mass of the main sequence; see section 2.2 of VICE's 
 * science documentation for further details. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		A SSP struct containing information on the stellar IMF and 
 * 				mass range of star formation 
 * 
 * Returns 
 * ======= 
 * The total initial main sequence mass of the stellar population, up to the 
 * normalization constant of the IMF. -1 in the case of an unrecognized IMF. 
 */ 
static double MSMFdenominator(SSP ssp) {

	/* 
	 * The main sequence mass fraction has the same denominator as the 
	 * cumulative return fraction. 
	 */ 
	return CRFdenominator(ssp); 

} 

/* 
 * Determine the numerator of the main sequence mass fraction. This is the 
 * total mass of stars still on the main sequence; see section 2.2 of VICE's 
 * science documentation for further details. 
 * 
 * Parameters
 * ========== 
 * ssp: 		A SSP struct containing information on the stellar IMF and 
 * 				mass range of star formation 
 * time: 		The age of the stellar population in Gyr 
 * 
 * Returns 
 * ======= 
 * The total main sequence mass of the stellar population at the given age, up 
 * to the normalization constant of the IMF. 
 */ 
static double MSMFnumerator(SSP ssp, double time) {

	/* 
	 * The integrated form of the numerator of the main sequence mass fraction 
	 * has the same form as the denominator as the cumulative return fraction, 
	 * but with different bounds. Thus CRFdenominator_IMFrange can be called 
	 * for each of the relevant mass ranges. 
	 */ 

	double turnoff_mass = main_sequence_turnoff_mass(time); 

	if (!strcmp(ssp.imf, "salpeter")) { 
		if (turnoff_mass > ssp.m_upper) {
			return MSMFdenominator(ssp); /* no stars evolved off of MS yet */ 
		} else if (turnoff_mass < ssp.m_lower) {
			return 0; 		/* all stars evolved off MS */ 
		} else { 
			return CRFdenominator_IMFrange(turnoff_mass, ssp.m_lower, 2.35); 
		}
	} else if (!strcmp(ssp.imf, "kroupa")) { 
		if (turnoff_mass > ssp.m_upper) {
			return MSMFdenominator(ssp); 
		} else if (turnoff_mass < ssp.m_lower) {
			return 0; 
		} else { 
			if (ssp.m_lower < 0.08) { 
				/* Need to consider all 3 portions of the Kroupa IMF */ 
				if (turnoff_mass > 0.5) {
					return (0.04 * CRFdenominator_IMFrange(turnoff_mass, 0.5, 
						2.3) + 0.08 * CRFdenominator_IMFrange(0.5, 0.08, 1.3) + 
						CRFdenominator_IMFrange(0.08, ssp.m_lower, 0.3)); 
				} else if (0.08 <= turnoff_mass && turnoff_mass <= 0.5) {
					return (0.08 * CRFdenominator_IMFrange(turnoff_mass, 0.08, 
						1.3) + CRFdenominator_IMFrange(0.08, ssp.m_lower, 0.3)); 
				} else {
					return CRFdenominator_IMFrange(turnoff_mass, ssp.m_lower, 
						0.3); 
				} 
			} else if (0.08 <= ssp.m_lower && ssp.m_lower <= 0.5) { 
				/* Only two portions of the Kroupa IMF to worry about */ 
				if (turnoff_mass > 0.5) {
					return (0.04 * CRFdenominator_IMFrange(turnoff_mass, 0.5, 
						2.3) + 0.08 * CRFdenominator_IMFrange(0.5, 
						ssp.m_lower, 1.3)); 
				} else {
					return (0.08 * CRFdenominator_IMFrange(turnoff_mass, 
						ssp.m_lower, 1.3)); 
				} 
			} else { 
				/* Only the high mass end of the Kroupa IMF to consider */ 
				return 0.04 * CRFdenominator_IMFrange(turnoff_mass, 0.5, 2.3); 
			}
		} 
	} else { 
		/* Unrecognized IMF, return -1 on failure */ 
		return -1; 
	}
}

