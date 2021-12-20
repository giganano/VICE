/*
 * This file implements recycling in VICE's singlezone simulations.
 *
 * Notes
 * =====
 * Here recycling refers to only the return of already enriched metals from
 * stars to the ISM. These simulations are implemented such that the
 * enrichment rate is the return plus the net yield.
 */

#include <stdlib.h>
#include "../singlezone.h"
#include "../utils.h"
#include "../multithread.h"
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

	/*
	 * With continuous recycling, this is a performance critical function.
	 * To minimize computing time, parallelized openMP threads are constructed,
	 * and rather than computing the change in mass with the
	 * `#pragma omp atomic` compiler directive, each thread increments one
	 * value in an array which is then summed at the end of the calculation.
	 * This allows each thread to proceed unimpeded by synchronization
	 * requirements.
	 */

	/* ----------------------- Continuous recycling ----------------------- */
	if ((*sz.ssp).continuous) {
		unsigned long i;
		#if defined(_OPENMP)
			double *mass = (double *) malloc (sz.nthreads * sizeof(double));
			for (i = 0ul; i < sz.nthreads; i++) mass[i] = 0;
			#pragma omp parallel for num_threads(sz.nthreads)
		#else
			double mass = 0;
		#endif
		/* From each previous timestep, there's a dCRF contribution */
		for (i = 0l; i <= sz.timestep; i++) {
			double dm;
			if (e == NULL) { 		/* This is the gas supply */
				dm = ((*sz.ism).star_formation_history[sz.timestep - i] *
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i]));
			} else { 			/* element -> weight by Z */
				dm = ((*sz.ism).star_formation_history[sz.timestep - i] *
					sz.dt * ((*sz.ssp).crf[i + 1l] - (*sz.ssp).crf[i]) *
					(*e).Z[sz.timestep - i]);
			}

			#if defined(_OPENMP)
				mass[omp_get_thread_num()] += dm;
			#else
				mass += dm;
			#endif

		}

		#if defined(_OPENMP)
			double result = sum(mass, sz.nthreads);
			free(mass);
			return result;
		#else
			return mass;
		#endif

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

