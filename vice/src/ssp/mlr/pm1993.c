/*
 * This file implements the mass-lifetime relation as parameterized in
 * Padovani & Matteucci (1993), given by:
 *
 * t_m = 10^((alpha - sqrt(beta - gamma * (eta - log(m))))/mu)
 *
 * for masses below 6.6 Msun, and
 *
 * t_m = 1.2m^-1.85 + 0.003
 *
 * for masses above 6.6 Msun. Below 0.6
 *
 * t_m is in Gyr. Though this form is originally
 * from Padovani & Matteucci (1993), the form implemented here is taken from
 * Romano et al. (2005).
 *
 * References
 * ==========
 * Padovani & Matteucci (1993), ApJ, 416, 26
 * Romano et al. (2005), A&A, 430, 491
 */


#include <math.h>
#include "pm1993.h"
#include "root.h"

static const double ALPHA = 0.334;
static const double BETA = 1.790;
static const double GAMMA = 0.2232;
static const double ETA = 7.764;
static const double MU = 0.1116;


/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism of Padovani & Matteucci (1993).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * References
 * ==========
 * Padovani & Matteucci (1993), ApJ, 416, 26
 *
 * header: pm1993.h
 */
extern double pm1993_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {

		/* Take into account the post main sequence lifetime */
		time /= 1 + postMS;

		if (time <= 0.003) {
			/*
			 * Under this parameterization, stars reach a minimum lifetime of
			 * 3 Myr with increasing mass.
			 */
			#ifdef INFINITY
				return INFINITY;
			#else
				return 500;
			#endif
		} else if (time == 160) {
			/*
			 * Here the relation flattens off at t = 160 Gyr for stars at and
			 * below 0.6 Msun.
			 */
			return 0.6;
		} else if (time > 160) {
			/*
			 * Under this formalism there is no stellar mass at which the
			 * lifetime exceeds 160 Gyr.
			 */
			#ifdef NAN
				return NAN;
			#else
				return 0;
			#endif
		} else {
			/*
			 * Solve for the mass assuming it is less than 6.6 Msun. If it
			 * comes out higher, switch to the form appropriate for that mass
			 * range.
			 */
			double mass = pow(10,
				ETA - 1 / GAMMA * (BETA - pow(ALPHA - MU * log10(time), 2))
			);
			if (mass > 6.6) mass = pow((time - 0.003) / 1.2, -1.0 / 1.85);
			return mass;
		}
	} else if (time < 0) {
		/*
		 * There was an error somewhere. This function shouldn't ever receive a
		 * negative age as that's unphysical.
		 */
		#ifdef NAN
			return NAN;
		#else
			return 0;
		#endif
	} else {
		/*
		 * Stellar population has zero age, meaning no stars have died yet.
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
 * Compute the lifetime of a star of known mass according to the formalism
 * of Padovani & Matteucci (1993).
 *
 * Parameters
 * ==========
 * mass: 		The mass of the star in solar masses.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * References
 * ==========
 * Padovani & Matteucci (1993), ApJ, 416, 26
 *
 * header: pm1993.h
 */
extern double pm1993_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {
		double tau;
		if (mass > 6.6) {
			tau = 1.2 * pow(mass, -1.85) + 0.003;
		} else if (0.60 < mass && mass <= 6.6) {
			tau = pow(10,
				(ALPHA - sqrt(BETA - GAMMA * (ETA - log10(mass)))) / MU
			);
		} else {
			tau = 160;
		}
		return (1 + postMS) * tau;
	} else if (mass < 0) {
		/*
		 * There was an error somewhere. This function shouldn't ever receive a
		 * negative mass as that's unphysical.
		 */
		#ifdef NAN
			return NAN;
		#else
			return 0;
		#endif
	} else {
		/*
		 * Based on analytic formulae, a zero mass star should have an infinite
		 * lifetime. Return infinity if it's defined, and if not, a lifetime
		 * sufficiently longer than the Hubble time.
		 */
		#ifdef INFINITY
			return INFINITY;
		#else
			return 500;
		#endif
	}

}

