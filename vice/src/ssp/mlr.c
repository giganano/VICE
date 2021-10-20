/*
 * This file implements the stellar mass-lifetime relationship (MLR) in VICE.
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "../ssp.h"
#include "mlr.h"

/* The hash-code for the current MLR setting: default is Larson (1974) */
static unsigned short MLR_SETTING = LARSON1974;

/*
 * Determine the mass of dying stars from a single stellar population of known
 * age under the current mass-lifetime relationship setting.
 *
 * Parameters
 * ==========
 * time: 			The age of the stellar population in Gyr
 * postMS: 			The ratio of a star's post main sequence lifetime to its
 * 					main sequence lifetime. Zero for main sequence turnoff mass.
 * Z: 				The metallicity by mass of the stellar population.
 *
 * Returns
 * =======
 * The mass of stars in solar masses whose lifetime is given by the first
 * parameter.
 *
 * Notes
 * =====
 * Although not all mass-lifetime relationships implemented in VICE are
 * metallicity dependent and some take into account the post main sequence
 * lifetime already, this function accepts all three as parameters as do they
 * so that any can be called with a function pointer.
 * See header files in ./vice/src/ssp/mlr/ for details.
 *
 * header: mlr.h
 */
extern double dying_star_mass(double time, double postMS, double Z) {

	/*
	 * Simply construct a function pointer to the current MLR setting and call
	 * it directly.
	 */

	double (*mlr)(double, double, double);

	switch (MLR_SETTING) {

		case POWERLAW:
			mlr = &powerlaw_turnoffmass;
			break;

		case VINCENZO2016:
			mlr = &vincenzo2016_turnoffmass;
			break;

		case HPT2000:
			mlr = &hpt2000_turnoffmass;
			break;

		case KA1997:
			mlr = &ka1997_turnoffmass;
			break;

		case PM1993:
			mlr = &pm1993_turnoffmass;
			break;

		case MM1989:
			mlr = &mm1989_turnoffmass;
			break;

		case LARSON1974:
			mlr = &larson1974_turnoffmass;
			break;

		default:
			/* Should be prevented by python, but as a failsafe */
			#ifdef NAN
				return NAN;
			#else
				return -1;
			#endif

	}

	return mlr(time, postMS, Z);

}


/*
 * Get the hashcode of the current mass-lifetime relationship setting. Their
 * values are #define'd in ./vice/src/ssp/mlr.h.
 *
 * header: mlr.h
 */
extern unsigned short get_mlr_hashcode(void) {

	return MLR_SETTING;

}


/*
 * Set the global mass-lifetime relationship setting via the hashcodes
 * attached to each of them #define'd in ./vice/src/ssp/mlr.h.
 *
 * Parameters
 * ==========
 * hashcode: 		The hashcode corresponding to the desired MLR. See header
 * 					file for allowed values.
 *
 * Returns
 * =======
 * 0 on success, 1 on an unrecognized hashcode.
 *
 * header: mlr.h
 */
extern unsigned short set_mlr_hashcode(unsigned short hashcode) {

	if (hashcode == POWERLAW || hashcode == VINCENZO2016 ||
		hashcode == HPT2000 || hashcode == KA1997 || hashcode == PM1993 ||
		hashcode == MM1989 || hashcode == LARSON1974) {
		MLR_SETTING = hashcode;
		return 0u;
	} else {
		return 1u; /* unrecognized MLR -> ValueError in Python */
	}

}

