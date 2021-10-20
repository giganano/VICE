/*
 * This file implements recycling in VICE's singlezone simulations.
 *
 * Notes
 * =====
 * Here recycling refers to only the return of already enriched metals from
 * stars to the ISM. These simulations are implemented such that the
 * enrichment rate is the return plus the net yield.
 */

#include "../singlezone.h"
#include "recycling.h"


/*
 * Determine the mass recycled from all previous generations of stars for
 * either a given element or the gas supply. For details, see section 3.3 of
 * VICE's science documentation.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 * e: 		A pointer to the element to find the recycled mass. NULL to find
 * 			it for the total ISM gas.
 *
 * Returns
 * =======
 * The recycled mass in Msun
 *
 * header: recycling.h
 */
extern double mass_recycled(SINGLEZONE sz, ELEMENT *e) {

	/* ----------------------- Continuous recycling ----------------------- */
	if ((*sz.ssp).continuous) {
		unsigned long i;
		double mass = 0;
		/* From each previous timestep, there's a dCRF contribution */
		for (i = 0l; i <= sz.timestep; i++) {
			if (e == NULL) { 		/* This is the gas supply */
				mass += ((*sz.ism).star_formation_history[sz.timestep - i] *
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i]));
			} else { 			/* element -> weight by Z */
				mass += ((*sz.ism).star_formation_history[sz.timestep - i] *
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i]) *
					(*e).Z[sz.timestep - i]);
			}
		}
		return mass;
	/* ---------------------- Instantaneous recycling ---------------------- */
	} else {
		if (e == NULL) {			/* gas supply */
			return (*sz.ism).star_formation_rate * sz.dt * (*sz.ssp).R0;
		} else { 				/* element -> weight by Z */
			return ((*sz.ism).star_formation_rate * sz.dt * (*sz.ssp).R0 *
				(*e).mass / (*sz.ism).mass);
		}
	}

}

