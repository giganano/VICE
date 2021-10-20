/*
 * This file implements the mass-lifetime relation as parameterized by
 * Larson (1974), which is a fit to the compilation of evolutionary lifetimes
 * presented in Tinsley (1972).
 *
 * Under this formalism, the main sequence lifetime t of a star of mass m is
 * given by:
 *
 * log(t) = alpha + (beta + gamma * log(m)) * log(m)
 *
 * where t is in Gyr and m is in solar masses.
 *
 * References
 * ==========
 * Larson (1974), MNRAS, 166, 585
 * Tinsley (1972), A&A, 20, 383
 */

#include <math.h>
#include "../../ssp.h"
#include "larson1974.h"

/*
 * The values of beta, and gamma in the Larson (1974) relation, taken from
 * Kobayashi (2004) and David, Forman & Jones (1990). The value of alpha, which
 * quantifies the main sequence lifetime of the sun, is calculated at runtime
 * from the compile-time constant SOLAR_LIFETIME in vice/src/ssp.h. With the
 * value of 10 that VICE is distributed with, alpha = 1.0 rather than than 10.0
 * as in Kobayashi (2004); this difference arises from her use of yr rather
 * than Gyr as the time unit.
 *
 * References
 * ==========
 * David, Forman & Jones (1990), ApJ, 359, 29
 * Kobayashi (2004), MNRAS, 347, 74
 * Larson (1974), MNRAS, 166, 585
 */
static const double BETA = -3.42;
static const double GAMMA = 0.88;


/*
 * Calculate the mass of dying stars in a single stellar population of known
 * age according to the Larson (1974) analytic form with parameters taken
 * from Kobayashi (2004).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of the post main sequence lifetime to the main
 * 				sequence lifetime. Zero for main sequence turnoff mass alone.
 * Z: 			The metallicity of the stellar population.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Though the Larson (1974) MLR is metallicity-independent, all mass-lifetime
 * relations in VICE are implemented as functions of both mass and metallicity.
 * See source file for the analytic form.
 *
 * References
 * ==========
 * Kobayashi (2004), MNRAS, 347, 74
 * Larson (1974), MNRAS, 166, 585
 *
 * header: larson1974.h
 */
extern double larson1974_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {

		double ALPHA = log10(SOLAR_LIFETIME);

		/* Take into account the post main sequence lifetime */
		time /= 1 + postMS;

		/*
		 * Determined via the quadratic formula from the analytic form (see
		 * file header), where the version with the minus sign is the physical
		 * answer. If the plus sign is taken from the quadratic, then the
		 * turnoff mass increases with time.
		 */
		double logm = (
			-BETA - sqrt(pow(BETA, 2) - 4 * GAMMA * (ALPHA - log10(time)))
		) / (
			2 * GAMMA
		);

		/*
		 * The condition checks for NaN even when isnan isn't defined. This is
		 * necessary because time may be small enough but still non-zero that
		 * the turnoff mass isn't defined.
		 */
		if (logm != logm) {
			#ifdef INFINITY
				return INFINITY;
			#else
				return 500;
			#endif
		} else {
			return pow(10, logm);
		}

	} else if (time < 0) {

		/*
		 * There was an error somewhere. This function shouldn't ever receive
		 * a negative age as that's unphysical.
		 */
		#ifdef NAN
			return NAN;
		#else
			return 0;
		#endif

	} else {

		/*
		 * The stellar population has zero age, so no stars have died yet.
		 * Return infinity if it's defined, and if not, a sufficiently high
		 * mass that it's above most IMF upper bounds anyway.
		 */
		#ifdef INFINITY
			return INFINITY;
		#else
			return 500;
		#endif

	}

}


/*
 * Calculate the lifetime of a star of known mass in Gyr according to the
 * Larson (1974) analytic form with parameters taken from Kobayashi (2004).
 *
 * Parameters
 * ==========
 * mass: 		The mass of the star in solar masses
 * postMS: 		The ratio of the post main sequence lifetime to the main
 * 				sequence lifetime. Zero for main sequence lifetime alone.
 * Z: 			The metallicity of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * Though the Larson (1974) MLR is metallicity-independent, all mass-lifetime
 * relations in VICE are implemented as functions of both mass and metallicity.
 * See source file for the analytic form.
 *
 * References
 * ==========
 * Kobayashi (2004), MNRAS, 347, 74
 * Larson (1972), MNRAS, 166, 585
 *
 * header: larson1974.h
 */
extern double larson1974_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {

		double ALPHA = log10(SOLAR_LIFETIME);

		/* See file header */
		double logt = ALPHA + (BETA + GAMMA * log10(mass)) * log10(mass);
		return (1 + postMS) * pow(10, logt);

	} else if (mass < 0) {

		/*
		 * There was an error somewhere. This function shouldn't ever receive
		 * a negative mass as that's unphysical.
		 */
		#ifdef NAN
			return NAN;
		#else
			return 0;
		#endif

	} else {

		/*
		 * Based on the analytic formula, a zero mass star should have an
		 * infinite lifetime. Return infinity if it's defined, and if not, a
		 * lifetime sufficiently longer than the Hubble time.
		 */
		#ifdef INFINITY
			return INFINITY;
		#else
			return 500;
		#endif

	}

}

