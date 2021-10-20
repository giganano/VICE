/*
 * This file implements calculations of the cumulative return fraction from a
 * single stellar population in VICE.
 */

#include <stdlib.h>
#include <math.h>
#include "../ssp.h"
#include "../singlezone.h"
#include "../imf.h"
#include "../yields/integral.h"
#include "../utils.h"
#include "crf.h"
#include "mlr.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double CRFdenominator_integrand(double m);
static double CRFnumerator_integrand(double m);
static double CRFnumerator_Kalirai08(SSP ssp, double time);
static double CRFnumerator_Kalirai08_IMFrange(double m_upper,
	double turnoff_mass, double m_lower, double a);
static double CRFnumerator_Kalirai08_above_8Msun(double m_upper,
	double turnoff_mass, double a);
static double CRFnumerator_Kalirai08_below_8Msun(double m_upper,
	double turnoff_mass, double a);
static IMF_ *ADOPTED_IMF = NULL;

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
extern unsigned short setup_CRF(SINGLEZONE *sz) {

	double denominator = CRFdenominator((*(*sz).ssp));
	if (denominator < 0) {
		/*
		 * denominator will be -1 in the case of an unrecognized IMF; return
		 * 1 on failure
		 */
		return 1u;
	} else {
		/*
		 * By design, the singlezone object fills arrays of time-varying
		 * quantities for ten timesteps beyond the endpoint of the simulation.
		 * This is a safeguard against memory errors.
		 */
		unsigned long i, n = n_timesteps(*sz);

		sz -> ssp -> crf = (double *) malloc (n * sizeof(double));
		for (i = 0l; i < n; i++) {
			sz -> ssp -> crf[i] = CRFnumerator_Kalirai08(
				(*(*sz).ssp), i * (*sz).dt) / denominator;
		}
		return 0u;

	}

}


/*
 * The integrand of the numerator of the cumulative return fraction (CRF).
 *
 * Parameters
 * ==========
 * m: 		The initial stellar mass in Msun
 *
 * Returns
 * =======
 * The difference in the initial stellar mass and remnant mass weighted by
 * the adopted IMF
 *
 * See Also
 * ========
 * Section 2.2 of Science Documentation: The Cumulative Return Fraction
 */
static double CRFnumerator_integrand(double m) {

	return (m - Kalirai08_remnant_mass(m)) * imf_evaluate(*ADOPTED_IMF, m);

}


/*
 * The integrand of the denominator of the cumulative return fraction (CRF).
 *
 * Parameters
 * ==========
 * m: 		The initial stellar mass in Msun
 *
 * Returns
 * =======
 * The initial stellar mass weighted by the adopted IMF
 *
 * See Also
 * ========
 * Section 2.2 of Science Documentation: The Cumulative Return Fraction
 */
static double CRFdenominator_integrand(double m) {

	return m * imf_evaluate(*ADOPTED_IMF, m);

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
 * This calculation assumes solar metallicity in computing the main sequence
 * turnoff mass (0.014; Asplund et al. 2009). This drastically reduces
 * computing times by not requiring calculation of the CRF for all previous
 * timesteps. The effect of metallicity on the CRF is small, anyway.
 *
 * References
 * ==========
 * Asplund et al. (2009), ARA&A, 47, 481
 * Kalirai et al. (2008), ApJ, 676, 594
 * Kroupa (2001), MNRAS, 322, 231
 */
static double CRFnumerator_Kalirai08(SSP ssp, double t) {

	double turnoff_mass = dying_star_mass(t, ssp.postMS, 0.014);
	if (turnoff_mass > (*ssp.imf).m_upper) return 0;
	switch (checksum((*ssp.imf).spec)) {

		case SALPETER:
			/* Salpeter IMF */
			return CRFnumerator_Kalirai08_IMFrange(
				(*ssp.imf).m_upper,
				turnoff_mass,
				(*ssp.imf).m_lower,
				2.35
			);

		case KROUPA:
			/*
			 * Kroupa IMF
			 *
			 * Prefactors here come from ensuring continuity at the breaks in
			 * the power-law indeces of the mass distribution
			 */
			if (turnoff_mass > 0.5) {
				return 0.04 * CRFnumerator_Kalirai08_IMFrange(
					(*ssp.imf).m_upper,
					turnoff_mass,
					(*ssp.imf).m_lower,
					2.3
				);
			} else if (0.08 <= turnoff_mass && turnoff_mass <= 0.5) {
				return 0.04 * CRFnumerator_Kalirai08_IMFrange(
					(*ssp.imf).m_upper,
					turnoff_mass,
					0.5,
					2.3
				) + 0.08 * CRFnumerator_Kalirai08_IMFrange(
					0.5,
					turnoff_mass,
					(*ssp.imf).m_lower,
					1.3
				);
			} else {
				return 0.04 * CRFnumerator_Kalirai08_IMFrange(
					(*ssp.imf).m_upper,
					turnoff_mass,
					0.5,
					2.3
				) + 0.08 * CRFnumerator_Kalirai08_IMFrange(
					0.5,
					turnoff_mass,
					0.08,
					1.3
				) + CRFnumerator_Kalirai08_IMFrange(
					0.08,
					turnoff_mass,
					(*ssp.imf).m_lower,
					0.3
				);
			}

		case CUSTOM:
			/* custom IMF -> no assumptions made, must integrate numerically */
			ADOPTED_IMF = ssp.imf;
			INTEGRAL *numerator = integral_initialize();
			numerator -> func = &CRFnumerator_integrand;
			numerator -> a = turnoff_mass;
			numerator -> b = (*ssp.imf).m_upper;
			/* default values for these parameters */
			numerator -> tolerance = SSP_TOLERANCE;
			numerator -> method = SSP_METHOD;
			numerator -> Nmin = SSP_NMIN;
			numerator -> Nmax = SSP_NMAX;
			quad(numerator);
			double x = (*numerator).result;
			integral_free(numerator);
			ADOPTED_IMF = NULL;
			return x;

		default:
			/* error handling */
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
 *
 * header: crf.h
 */
extern double CRFdenominator(SSP ssp) {

	switch (checksum((*ssp.imf).spec)) {

		case SALPETER:
			/* Salpeter IMF */
			return CRFdenominator_IMFrange((*ssp.imf).m_upper,
				(*ssp.imf).m_lower, 2.35);

		case KROUPA:
			/* Kroupa IMF */
			if ((*ssp.imf).m_lower > 0.5) {
				return 0.04 * CRFdenominator_IMFrange(
					(*ssp.imf).m_upper, (*ssp.imf).m_lower, 2.3
				);
			} else if (0.08 <= (*ssp.imf).m_lower &&
				(*ssp.imf).m_lower <= 0.5) {
				return (
					0.04 * CRFdenominator_IMFrange((*ssp.imf).m_upper, 0.5, 2.3)
					+ 0.08 * CRFdenominator_IMFrange(0.5, (*ssp.imf).m_lower,
						1.3)
				);
			} else {
				return (0.04 * CRFdenominator_IMFrange((*ssp.imf).m_upper, 0.5,
					2.3) + 0.08 * CRFdenominator_IMFrange(0.5, 0.08, 1.3) +
					CRFdenominator_IMFrange(0.08, (*ssp.imf).m_lower, 0.3)
				);
			}

		case CUSTOM:
			/* custom IMF -> no assumptions made, must integrate numerically */
			ADOPTED_IMF = ssp.imf;
			INTEGRAL *denominator = integral_initialize();
			denominator -> func = &CRFdenominator_integrand;
			denominator -> a = (*ssp.imf).m_lower;
			denominator -> b = (*ssp.imf).m_upper;
			/* default values for these properties */
			denominator -> tolerance = SSP_TOLERANCE;
			denominator -> method = SSP_METHOD;
			denominator -> Nmin = SSP_NMIN;
			denominator -> Nmax = SSP_NMAX;
			quad(denominator);
			double x = (*denominator).result;
			integral_free(denominator);
			ADOPTED_IMF = NULL;
			return x;

		default:
			/* error handling */
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
 *
 * header: crf.h
 */
extern double CRFdenominator_IMFrange(double m_upper, double m_lower,
	double a) {

	return 1 / (2 - a) * (pow(m_upper, 2 - a) - pow(m_lower, 2 - a));

}

