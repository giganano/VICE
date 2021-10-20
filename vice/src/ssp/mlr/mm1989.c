/*
 * This file implements the mass-lifetime relation from Maeder & Meynet (1989),
 * of the general form:
 *
 * \tau = 10^(\alpha * log(m) + \beta) (m < 60 Msun)
 *
 * where \alpha and \beta change in different mass ranges. Above 60 Msun the
 * relation becomes:
 *
 * \tau = 1.2m^-1.85 + 3 Myr
 *
 * In all cases \tau is in Gyr.
 *
 * Note: Though this is the functional form from Maeder & Meynet (1989), it's
 * form was taken from section 3 of Romano et al. (2005).
 *
 * References
 * ==========
 * Maeder & Meynet (1989), A&A, 210, 155
 * Romano et al. (2005), A&A, 430, 491
 */


#include <math.h>
#include "mm1989.h"
#include "root.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double alpha(double mass);
static double beta(double mass);


/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism of Maeder & Meynet (1989).
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
 * Maeder & Meynet (1989), A&A, 210, 155
 *
 * header: mm1989.h
 */
extern double mm1989_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {
		/*
		 * With no knowledge of the mass, the values of alpha and beta cannot
		 * be easily determined, so we fall back on the numerical root-finder.
		 */
		return bisection(&mm1989_lifetime, BISECTION_INITIAL_LOWER_BOUND,
			BISECTION_INITIAL_UPPER_BOUND, time, postMS, Z);
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
 * Compute the lifetime of a star of known mass according to the formula from
 * Maeder & Meynet (1989).
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
 * Maeder & Meynet (1989), A&A, 210, 155
 *
 * header: mm1989.h
 */
extern double mm1989_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {
		double lifetime;
		if (mass <= 60) {
			lifetime = pow(10, alpha(mass) * log10(mass) + beta(mass));
		} else {
			lifetime = 1.2 * pow(mass, -1.85) + 0.003;
		}
		return (1 + postMS) * lifetime;
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


/*
 * Look up the value of the coefficient alpha for a given stellar mass in solar
 * masses (see file header).
 */
static double alpha(double mass) {

	if (mass <= 1.3) {
		return -0.6545;
	} else if (1.3 < mass && mass <= 3) {
		return -3.7;
	} else if (3 < mass && mass <= 7) {
		return -2.51;
	} else if (7 < mass && mass <= 15) {
		return -1.78;
	} else if (15 < mass && mass <= 60) {
		return -0.86;
	} else {
		/* Something went wrong */
		#ifdef NAN
			return NAN;
		#else
			return -1;
		#endif
	}

}


/*
 * Look up the value of the coefficient beta for a given stellar mass in solar
 * masses (see file header).
 */
static double beta(double mass) {

	if (mass <= 1.3) {
		return 1;
	} else if (1.3 < mass && mass <= 3) {
		return 1.35;
	} else if (3 < mass && mass <= 7) {
		return 0.77;
	} else if (7 < mass && mass <= 15) {
		return 0.17;
	} else if (15 < mass && mass <= 60) {
		return -0.94;
	} else {
		/* Something went wrong */
		#ifdef NAN
			return NAN;
		#else
			return -1;
		#endif
	}

}

