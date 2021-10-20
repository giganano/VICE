/*
 * This file implements the simulations of enrichment from single stellar
 * populations in VICE.
 */

#include <stdlib.h>
#include "../ssp.h"
#include "../singlezone.h"
#include "ssp.h"

/*
 * Run a simulation of elemental production for a single element produced by a
 * single stellar population.
 *
 * Parameters
 * ==========
 * ssp: 		A pointer to an SSP object
 * e: 			A pointer to an element to run the simulation for
 * Z: 			The metallicity by mass of the stellar population
 * times: 		The times at which the simulation will evaluate
 * n_times: 	The number of elements in the times array
 * mstar: 		The mass of the stellar population in Msun
 *
 * Returns
 * =======
 * An array of the same length as times, where each element is the mass of the
 * given chemical element at the corresponding time. NULL on failure to
 * allocate memory.
 *
 * header: ssp.h
 */
extern double *single_population_enrichment(SSP *ssp, ELEMENT *e,
	double Z, double *times, unsigned long n_times, double mstar) {

	double *mass = (double *) malloc (n_times * sizeof(double));
	if (mass == NULL) return NULL; 	/* memory error */

	ssp -> msmf = (double *) malloc (n_times * sizeof(double));
	if ((*ssp).msmf == NULL) return NULL; /* memory error */
	double denominator = MSMFdenominator(*ssp);
	if (denominator < 0) { /* unrecognized IMF */
		free(mass);
		free(ssp -> msmf);
		return NULL;
	} else {
		unsigned long i;
		for (i = 0l; i < n_times; i++) {
			ssp -> msmf[i] = MSMFnumerator(*ssp, times[i]) / denominator;
		}
	}

	mass[0] = 0;
	double ia_yield = get_ia_yield(*e, Z);
	if (n_times >= 2l) {
		/* The contribution from CCSNe */
		mass[1] = get_cc_yield(*e, Z) * mstar;
		unsigned long i;
		for (i = 2l; i < n_times; i++) {
			mass[i] = mass[i - 1l]; 		/* previous timesteps */

			/* The contribution from SNe Ia */
			// mass[i] += ((*(*e).sneia_yields).yield_ *
			mass[i] += ia_yield * (*(*e).sneia_yields).RIa[i] * mstar;

			/* The contribution from AGB stars */
			mass[i] += (
				get_AGB_yield(*e, Z,
					dying_star_mass(times[i], (*ssp).postMS, Z)) *
				mstar * ((*ssp).msmf[i] - (*ssp).msmf[i + 1l])
			);

		}
	} else {}

	return mass;

}


