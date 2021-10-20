/*
 * This file implements calculations of the main sequence mass fraction of a
 * single stellar population in VICE.
 */

#include <stdlib.h>
#include <math.h>
#include "../ssp.h"
#include "../imf.h"
#include "../singlezone.h"
#include "../yields/integral.h"
#include "../utils.h"
#include "msmf.h"
#include "mlr.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double MSMFnumerator_integrand(double m);
static IMF_ *ADOPTED_IMF = NULL;


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
extern unsigned short setup_MSMF(SINGLEZONE *sz) {

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
		unsigned long i, n = n_timesteps(*sz);

		sz -> ssp -> msmf = (double *) malloc (n * sizeof(double));
		for (i = 0l; i < n; i++) {
			sz -> ssp -> msmf[i] = MSMFnumerator((*(*sz).ssp),
				i * (*sz).dt) / denominator;
		}
		return 0;
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
 *
 * header: msmf.h
 */
extern double MSMFdenominator(SSP ssp) {

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
 *
 * Notes
 * =====
 * This calculation assumes solar metallicity in computing the main sequence
 * turnoff mass (0.014; Asplund et al. 2009). This drastically reduces
 * computing times by not requiring calculation of the CRF for all previous
 * timesteps. The effect of metallicity on the CRF is small, anyway.
 *
 * References
 * ==========
 * Asplund et al. (2009), ARA&A, 47, 481
 *
 * header: msmf.h
 */
extern double MSMFnumerator(SSP ssp, double t) {

	/*
	 * The integrated form of the numerator of the main sequence mass fraction
	 * has the same form as the denominator as the cumulative return fraction,
	 * but with different bounds. Thus CRFdenominator_IMFrange can be called
	 * for each of the relevant mass ranges.
	 */

	double turnoff_mass = dying_star_mass(t, ssp.postMS, 0.014);

	/*
	 * First check if it's ouside the mass range of star formation and handle
	 * appropriately
	 */
	if (turnoff_mass > (*ssp.imf).m_upper) {
		return MSMFdenominator(ssp);
	} else if (turnoff_mass < (*ssp.imf).m_lower) {
		return 0;
	}

	switch(checksum((*ssp.imf).spec)) {

		case SALPETER:
			/* Salpeter IMF */
			return CRFdenominator_IMFrange(turnoff_mass, (*ssp.imf).m_lower,
				2.35);

		case KROUPA:
			/* Kroupa IMF */
			if ((*ssp.imf).m_lower < 0.08) {
				/* Need to consider all 3 portions of the Kroupa IMF */
				if (turnoff_mass > 0.5) {
					return (
						0.04 * CRFdenominator_IMFrange(turnoff_mass, 0.5, 2.3) +
						0.08 * CRFdenominator_IMFrange(0.5, 0.08, 1.3) +
						CRFdenominator_IMFrange(0.08, (*ssp.imf).m_lower, 0.3)
					);
				} else if (0.08 <= turnoff_mass && turnoff_mass <= 0.5) {
					return (
						0.08 * CRFdenominator_IMFrange(turnoff_mass, 0.08, 1.3)
						+ CRFdenominator_IMFrange(0.08, (*ssp.imf).m_lower, 0.3)
					);
				} else {
					return CRFdenominator_IMFrange(turnoff_mass,
						(*ssp.imf).m_lower, 0.3);
				}
			} else if (0.08 <= (*ssp.imf).m_lower && (*ssp.imf).m_lower <= 0.5) {
				/* Only two portions of the Kroupa IMF to worry about */
				if (turnoff_mass > 0.5) {
					return (
						0.04 * CRFdenominator_IMFrange(turnoff_mass, 0.5, 2.3) +
						0.08 * CRFdenominator_IMFrange(0.5, (*ssp.imf).m_lower,
							1.3)
					);
				} else {
					return 0.08 * CRFdenominator_IMFrange(turnoff_mass,
						(*ssp.imf).m_lower, 1.3);
				}
			} else {
				/* Only the high mass end of the Kroupa IMF to consider */
				return 0.04 * CRFdenominator_IMFrange(turnoff_mass,
					(*ssp.imf).m_lower, 2.3);
			}

		case CUSTOM:
			/* custom IMF -> no assumptions made, must integrate numerically */
			ADOPTED_IMF = ssp.imf;
			INTEGRAL *numerator = integral_initialize();
			numerator -> func = &MSMFnumerator_integrand;
			numerator -> a = (*ssp.imf).m_lower;
			numerator -> b = turnoff_mass;
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
 * The integrand of the numerator of the main sequence mass fraction (MSMF).
 *
 * Parameters
 * ==========
 * m: 			The initial stellar mass in Msun
 *
 * Returns
 * =======
 * The initial stellar mass weighted by the adopted IMF
 *
 * See Also
 * ========
 * Section 2.3 of Science Documentation: The Main Sequence Mass Fraction
 */
static double MSMFnumerator_integrand(double m) {

	return m * imf_evaluate(*ADOPTED_IMF, m);

}

