/*
 * This file implements the mass-lifetime relation as described in Hurley,
 * Pols & Tout (2000) according to (see their section 5.1):
 *
 * t_MS = t_BGB * max(mu, x)
 *
 * t_BGB = (a_1 + a_2 * m^4 + a_3 * m^5.5 + m^7) / (a_4 * m^2 + a_5 * m^7)
 *
 * mu = max(0.5, 1.0 - 0.01 * max[a_6 / m^(a_7), a_8 + a_9 / m^(a_10)])
 *
 * x = max(0.95, min[0.95 - 0.03 * (\zeta + 0.30103), 0.99])
 *
 * where \zeta is the log-scaled solar abundance ratio (i.e. log10(Z/Zsun)),
 * and a_n are coefficients quantified in Appendix A of the associated paper.
 * The values necessary for this implementation are recorded in hpt2000.dat in
 * this directory.
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "hpt2000.h"
#include "../../io/utils.h"
#include "root.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double hpt2000_x(double Z);
static double hpt2000_mu(double mass, double Z);
static double a_n(unsigned short n, double Z);
static double zeta(double Z);

/* The metallicity of the sun as in Hurley, Pols & Tout (2000) */
static const double Z_SOLAR = 0.02;
static double **HPT2000TABLE = NULL;
static const unsigned short HPT2000TABLE_DIMENSION = 4u;


/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism in section 5.1 of of Hurley, Pols & Tout (2000).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Notes
 * =====
 * Although the lifetime is computed analytically from a star of known mass
 * under the Hurley, Pols & Tout (2000) formalism, the equation is not
 * invertible analytically. This solution is thus computed numerically using
 * the bisection method (header file: root.h).
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 *
 * header: hpt2000.h
 */
extern double hpt2000_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {
		return bisection(&hpt2000_lifetime, BISECTION_INITIAL_LOWER_BOUND,
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
 * Compute the lifetime of a star of known mass according to the formalism
 * in section 5.1 of Hurley, Pols & Tout (2000).
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
 * header: hpt2000.h
 */
extern double hpt2000_lifetime(double mass, double postMS, double Z) {

	/*
	 * Due to the polynomial dependence of the coefficients a_n on metallicity
	 * Z, this form reaches numerical instability at Z / Zsun < 0.001.
	 * Therefore, as a safeguard, this function enforces a minimum value of
	 * zeta of -3.
	 */
	if (zeta(Z) < -3) return hpt2000_lifetime(mass, postMS, 2.0e-5);

	if (mass > 0) {

		/* Analytic form -> see file header */
		double coeff = fmax(hpt2000_mu(mass, Z), hpt2000_x(Z));
		double tbgb = (
			a_n(1, Z) + a_n(2, Z) * pow(mass, 4) + a_n(3, Z) * pow(mass, 5.5) +
			pow(mass, 7)
		) / (
			a_n(4, Z) * pow(mass, 2) + a_n(5, Z) * pow(mass, 7)
		);
		return 1.0e-3 * (1 + postMS) * coeff * tbgb; /* 1e-3: Myr -> Gyr */

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
 * Compute the value of the coefficient x (see file header).
 *
 * Parameters
 * ==========
 * Z: 		The metallicity by mass.
 */
static double hpt2000_x(double Z) {

	return fmax(0.95, fmin(0.95 - 0.03 * (zeta(Z) + 0.30103), 0.99));

}


/*
 * Compute the value of the coefficient mu (see file header).
 *
 * Parameters
 * ==========
 * Z: 		The metallicity by mass.
 */
static double hpt2000_mu(double mass, double Z) {

	return fmax(0.5, 1.0 - 0.01 * fmax(a_n(6, Z) / pow(mass, a_n(7, Z)),
		a_n(8, Z) + a_n(9, Z) / pow(mass, a_n(10, Z))));

}


/*
 * Compute the value of the coefficient a_n, whose metallicity dependence is
 * given by:
 *
 * a_n = \alpha + \beta * \zeta + \gamma * \zeta^2 + \eta * \zeta^3
 *
 * where the values of \alpha, \beta, \gamma, and \delta are given in the file
 * hpt2000.dat in this directory.
 */
static double a_n(unsigned short n, double Z) {

	double a = 0, zeta_ = zeta(Z);
	unsigned short i;
	for (i = 0u; i < HPT2000TABLE_DIMENSION; i++) {
		a += HPT2000TABLE[n - 1][i] * pow(zeta_, i);
	}
	return a;

}


/*
 * Calculate the value of zeta, the log-scaled solar abundance ratio.
 *
 * Parameters
 * ==========
 * Z: 		The metallicity by mass
 *
 * Notes
 * =====
 * This function assumes the solar metallicity to be 0.02 as in Hurley, Pols &
 * Tout (2000).
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 */
static double zeta(double Z) {

	return log10(Z / Z_SOLAR);

}


/*
 * Import the Hurley, Pols & Tout (2000) data. This function must be called
 * from python before hpt2000_lifetime or hpt2000_turnoffmass can be called,
 * otherwise a segmentation fault will occur.
 *
 * Parameters
 * ==========
 * filename: 	The full path to the file holding the data.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * header: hpt2000.h
 */
extern unsigned short hpt2000_import(char *filename) {

	HPT2000TABLE = read_square_ascii_file(filename);
	return HPT2000TABLE == NULL;

}


/*
 * Free up the memory stored by the Hurley, Pols & Tout (2000) data.
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 *
 * header: hpt2000.h
 */
extern void hpt2000_free(void) {

	free(HPT2000TABLE);
	HPT2000TABLE = NULL;

}

