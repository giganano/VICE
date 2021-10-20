/*
 * This file implements a form of the simple analytic power-law mass-lifetime
 * relation that is derived in many undergraduate astronomy courses, given by:
 *
 * \tau / \tau_\odot = (1 + \alpha_MS) (M / M_\odot)^(-\gamma)
 *
 * where \tau, \tau_\odot, M, and M_\odot are the lifetimes and masses of
 * the sun and another star. \alpha_MS denotes the ratio of the post main
 * sequence lifetime to the main sequence lifetime, allowing calculation of
 * total as well as the hydrogen burning lifetimes. \gamma is a power-law index
 * with mass which can be derived from an assumed power-law regarding the
 * mass-luminosity relation.
 */


#include <math.h>
#include "../../ssp.h"
#include "powerlaw.h"


/*
 * Determine the mass of dying stars in a star cluster of known age according
 * to the simple power-law formulation (see source file header).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Versions >= 1.1: This is the mass of a dying star taking into account their
 * 		post main sequence lifetimes.
 * Versions >= 1.2.1: This function handles errors more robustly in the event
 * 		that the age is either zero or negative. For zero age, it returns
 * 		INFINITY (500 if not defined), and for negative age, it returns NAN
 * 		(0 if not defined).
 * Versions >= 1.3.0: In prior versions, this was the only mass-lifetime
 * 		relation built into VICE. In subsequent versions, the user can choose
 * 		between this and other formalisms.
 *
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * This function depends on the compile-time constants SOLAR_LIFETIME and
 * MASS_LIFETIME_PLAW_INDEX declared in vice/src/ssp.h.
 *
 * header: powerlaw.h
 */
extern double powerlaw_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {
		/* analytic solution -> see file header */
		return pow(
			time / ((1 + postMS) * SOLAR_LIFETIME),
			-1.0 / MASS_LIFETIME_PLAW_INDEX
		);
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
		 * Stellar population has zero age, meaning no stars have died yet.
		 * Return infinity if its defined, and if not, a sufficiently high
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
 * Compute the lifetime of a star of known mass according to the simple
 * power-law formulation (see source file header).
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
 * This function depends on the compile-time constants SOLAR_LIFETIME and
 * MASS_LIFETIME_PLAW_INDEX declared in vice/src/ssp.h.
 *
 * header: powerlaw.h
 */
extern double powerlaw_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {
		/* analytic solution -> see file header */
		return (1 + postMS) * SOLAR_LIFETIME * pow(mass,
			-MASS_LIFETIME_PLAW_INDEX);
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

