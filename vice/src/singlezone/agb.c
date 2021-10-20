/*
 * This file implements the enrichment of arbitrary elements from asymptotic
 * giant branch (AGB) stars in VICE's singlezone simulations.
 */

#include <stdlib.h>
#include "../singlezone.h"
#include "../callback.h"
#include "../agb.h"
#include "../ssp.h"
#include "../toolkit.h"
#include "../utils.h"
#include "agb.h"

/*
 * Determine the mass of a given element produced by AGB stars at the current
 * timestep of a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 			The SINGLEZONE struct associated with the current simulation
 * e: 			The ELEMENT struct to find the total mass yield for
 *
 * Returns
 * =======
 * The mass of the given element in solar masses produced by AGB stars in one
 * timestep from all previous generations of stars.
 *
 * header: agb.h
 */
extern double m_AGB(SINGLEZONE sz, ELEMENT e) {

	if (sz.timestep == 0l) {
		return 0; /* No star's yet */
	} else {
		unsigned long i;
		double mass = 0;
		for (i = 0l; i <= sz.timestep; i++) {
			/* The metallicity of the stars that formed i timesteps ago */
			double Z = scale_metallicity(sz, sz.timestep - i);

			/* From section 4.4 of VICE's science documentation */
			mass += (
				get_AGB_yield(e, Z,
					dying_star_mass(i * sz.dt, (*sz.ssp).postMS, Z)) *
				(*sz.ism).star_formation_history[sz.timestep - i] * sz.dt *
				((*sz.ssp).msmf[i] - (*sz.ssp).msmf[i + 1l])
			);
			
		}

		return mass;
		
	}

}



/*
 * Determine the fractional yield of a given element from AGB stars at a
 * given mass and metallicity.
 *
 * Parameters
 * ==========
 * e: 				The element struct containing AGB yield information
 * Z_stars: 		The metallicity by mass Z of the AGB stars
 * turnoff_mass:	The mass of the AGB stars
 *
 * Returns
 * =======
 * The fraction of each AGB star's mass that is converted into the element e
 * under the current yield settings.
 *
 * header: agb.h
 */
extern double get_AGB_yield(ELEMENT e, double Z_stars, double turnoff_mass) {

	if (turnoff_mass < MIN_AGB_MASS || turnoff_mass > MAX_AGB_MASS) {

		/*
		 * By default, only stars between 0 and 8 Msun have an AGB phase in
		 * VICE. Changing these requires altering these #define statements
		 * in agb.h.
		 */
		return 0;

	} else if ((*(*e.agb_grid).custom_yield).user_func != NULL) {

		/*
		 * User-specified AGB star yield as a function of stellar mass and
		 * metallicity
		 */
		return callback_2arg_evaluate(*(*e.agb_grid).custom_yield,
			turnoff_mass, Z_stars);

	} else {

		/*
		 * Let the 2-D interpolation scheme handle the meat of this
		 * calculation to not repeat code. For many AGB elements though, this
		 * tends to extrapolate to negative yields near ~1 Msun, when it's
		 * probably more physical for the yields to flatten off. To mitigate
		 * this issue, we don't allow negative AGB star yields below 1.5 Msun.
		 */
		double yield = interp_scheme_2d_evaluate(*(*e.agb_grid).interpolator,
			turnoff_mass, Z_stars);
		if (turnoff_mass < 1.5 && yield < 0) {
			return 0;
		} else {
			return yield;
		}
		
	}

}

