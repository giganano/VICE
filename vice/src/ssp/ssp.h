
#ifndef SSP_SSP_H
#define SSP_SSP_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: ssp.c
 */
extern double *single_population_enrichment(SSP *ssp, ELEMENT *e,
	double Z, double *times, unsigned long n_times, double mstar);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_SSP_H */
