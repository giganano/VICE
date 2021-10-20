/*
 * This file implements the mass-lifetime as quantified in Vincenzo et al.
 * (2016) according to the form:
 *
 * tau = A * exp(B * m^-C)
 *
 * where A, B, and C are functions of metallicity. Their values are sampled on
 * a grid of metallicities which are implemented here as independent
 * 1-dimensional interpolation schema. These values are computed using
 * isochrones computed using the PARSEC stellar evolution code (Bressan et al.
 * 2012; Tang et al. 2014; Chen et al. 2015) and were used in combination with
 * a one-zone chemical evolution model to reproduce the color-magnitude
 * diagram of the Sculptor dwarf galaxy.
 *
 * References
 * ==========
 * Bressan et al. (2012), MNRAS, 427, 127
 * Chen et al. (2015), MNRAS, 452, 1068
 * Tang et al. (2014), MNRAS, 445, 4287
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../objects/interp_scheme_1d.h"
#include "../../toolkit/interp_scheme_1d.h"
#include "../../io/utils.h"
#include "vincenzo2016.h"

/*
 * VINCENZO_A: The interpolation scheme for the values of A
 * VINCENZO_B: The interpolation scheme for the values of B
 * VINCENZO_C: The interpolation scheme for the values of C
 */
static INTERP_SCHEME_1D *VINCENZO_A = NULL;
static INTERP_SCHEME_1D *VINCENZO_B = NULL;
static INTERP_SCHEME_1D *VINCENZO_C = NULL;


/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the Vincenzo et al. (2016) formalism (see source file for analytic form).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence turnoff mass.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * The Vincenzo et al. (2016) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * header: vincenzo2016.h
 */
extern double vincenzo2016_turnoffmass(double time, double postMS, double Z) {

	if (time > 0) {

		double a = interp_scheme_1d_evaluate(*VINCENZO_A, Z);
		double b = interp_scheme_1d_evaluate(*VINCENZO_B, Z);
		double c = interp_scheme_1d_evaluate(*VINCENZO_C, Z);

		/* analytic solution, see file header */
		double mass = pow(log(time / a)  / b, -1.0 / c);

		/*
		 * The condition checks for NaN even when isnan isn't defined. This is
		 * necessary because time may be small enough but still non-zero that
		 * the turnoff mass isn't defined mathematically.
		 */
		if (mass != mass) {
			#ifdef INFINITY
				return INFINITY;
			#else
				return 500;
			#endif
		} else {
			return mass;
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
 * Compute the lifetime of a star of known mass according to the Vincenzo et
 * al. (2016) formalism (see source file for analytic form).
 *
 * Parameters
 * ==========
 * mass: 		Stellar mass in solar masses.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetimes. Zero for just the main sequence lifetime.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * The Vincenzo et al. (2016) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * header: vincenzo2016.h
 */
extern double vincenzo2016_lifetime(double mass, double postMS, double Z) {

	if (mass > 0) {

		double a = interp_scheme_1d_evaluate(*VINCENZO_A, Z);
		double b = interp_scheme_1d_evaluate(*VINCENZO_B, Z);
		double c = interp_scheme_1d_evaluate(*VINCENZO_C, Z);

		return a * exp(b * pow(mass, -c));

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


/*
 * Import the Vincenzo et al. (2016) data. This function must be called from
 * python before vincenzo2016_lifetime or vincenzo2016_turnoff mass can be
 * called, otherwise a segmentation fault will occur.
 *
 * Parameters
 * ==========
 * filename: 		The full path to the file holding the data.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * header: vincenzo2016.h
 */
extern unsigned short vincenzo2016_import(char *filename) {

	int hlength = header_length(filename);
	if (hlength == -1) return 1u;
	int flength = line_count(filename);
	if (flength == -1) return 1u;
	unsigned long n_points = (unsigned long) flength - (unsigned long) hlength;

	VINCENZO_A = interp_scheme_1d_initialize();
	VINCENZO_B = interp_scheme_1d_initialize();
	VINCENZO_C = interp_scheme_1d_initialize();

	VINCENZO_A -> n_points = (unsigned long) n_points;
	VINCENZO_B -> n_points = (unsigned long) n_points;
	VINCENZO_C -> n_points = (unsigned long) n_points;

	VINCENZO_A -> xcoords = (double *) malloc (n_points * sizeof(double));
	VINCENZO_A -> ycoords = (double *) malloc (n_points * sizeof(double));
	VINCENZO_B -> xcoords = (double *) malloc (n_points * sizeof(double));
	VINCENZO_B -> ycoords = (double *) malloc (n_points * sizeof(double));
	VINCENZO_C -> xcoords = (double *) malloc (n_points * sizeof(double));
	VINCENZO_C -> ycoords = (double *) malloc (n_points * sizeof(double));

	FILE *in = fopen(filename, "r");
	if (in == NULL) return 1u;
	unsigned short i;
	for (i = 0u; i < n_points; i++) {
		double z, a, b, c;
		fscanf(in, "%lf %lf %lf %lf\n", &z, &a, &b, &c);
		VINCENZO_A -> xcoords[i] = z;
		VINCENZO_A -> ycoords[i] = a;
		VINCENZO_B -> xcoords[i] = z;
		VINCENZO_B -> ycoords[i] = b;
		VINCENZO_C -> xcoords[i] = z;
		VINCENZO_C -> ycoords[i] = c;
	}

	fclose(in);
	return 0u;

}


/*
 * Free up the memory stored by the Vincenzo et al. (2016) schema.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * header: vincenzo2016.h
 */
extern void vincenzo2016_free(void) {

	interp_scheme_1d_free(VINCENZO_A);
	interp_scheme_1d_free(VINCENZO_B);
	interp_scheme_1d_free(VINCENZO_C);

	VINCENZO_A = NULL;
	VINCENZO_B = NULL;
	VINCENZO_C = NULL;

}

