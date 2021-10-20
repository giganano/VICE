/*
 * This file implements the mass-lifetime relation as quantified by Kodama &
 * Arimoto (1997) using stellar evolution tracks computed using the code
 * presented in Iwamoto & Saio (1999).
 *
 * References
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41
 * Iwamoto & Saio (1999), ApJ, 521, 297
 */

#include <stdlib.h>
#include <stdio.h>
#include "ka1997.h"
#include "root.h"
#include "../../toolkit/interp_scheme_2d.h"
#include "../../objects/interp_scheme_2d.h"

static const unsigned short N_MASSES = 41u;
static const unsigned short N_METALLICITIES = 9u;
static INTERP_SCHEME_2D *KA1997 = NULL;


/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the stellar evolution models of Kodama & Arimoto (1997).
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
 * Although the lifetimes are computed analytically by a 2-D interpolation
 * scheme, such a formalism is not analytically intertible. This solution is
 * thus computed numerically using the bisection method (header file: root.h).
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * The Kodama & Arimoto (1997) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41
 *
 * header: ka1997.h
 */
extern double ka1997_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {
		/* Enforce postMS = 0 -> see note */
		return bisection(&ka1997_lifetime, BISECTION_INITIAL_LOWER_BOUND,
			BISECTION_INITIAL_UPPER_BOUND, time, 0.0, Z);
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
 * Compute the lifetime of a star of known mass according to the stellar
 * evolution models of Kodama & Arimoto (1997).
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
 * The Kodama & Arimoto (1997) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41
 *
 * header: ka1997.h
 */
extern double ka1997_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {
		return interp_scheme_2d_evaluate(*KA1997, Z, mass);
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
 * Import the Kodama & Arimoto (1997) data into a 2-dimension interpolation
 * scheme. This function must be called from python before ka1997_lifetime or
 * ka1997_turnoffmass can be called, otherwise a segmentation fault will occur.
 *
 * Parameters
 * ==========
 * filename: 	The full path to the file holding the data.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * References
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41
 *
 * header: ka1997.h
 */
extern unsigned short ka1997_import(char *filename) {

	FILE *in = fopen(filename, "r");
	if (in == NULL) return 1u;

	KA1997 = interp_scheme_2d_initialize();
	KA1997 -> n_x_values = N_METALLICITIES;
	KA1997 -> n_y_values = N_MASSES;

	KA1997 -> xcoords = (double *) malloc (N_METALLICITIES * sizeof(double));
	KA1997 -> ycoords = (double *) malloc (N_MASSES * sizeof(double));
	KA1997 -> zcoords = (double **) malloc (N_METALLICITIES * sizeof(double));

	unsigned short i, j;
	for (i = 0u; i < N_METALLICITIES; i++) {
		KA1997 -> zcoords[i] = (double *) malloc (N_MASSES * sizeof(double));
		for (j = 0u; j < N_MASSES; j++) {
			fscanf(in, "%lf %lf %lf\n",
				&(KA1997 -> ycoords[j]),
				&(KA1997 -> xcoords[i]),
				&(KA1997 -> zcoords[i][j])
			);
			KA1997 -> zcoords[i][j] *= 1.0e-9; /* yr -> Gyr */
		}
	}

	fclose(in);
	return 0u;

}


/*
 * Free up the memory stored by the Kodama & Arimoto (1997) data.
 *
 * References
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41
 *
 * header: ka1997.h
 */
extern void ka1997_free(void) {

	interp_scheme_2d_free(KA1997);
	KA1997 = NULL;

}

