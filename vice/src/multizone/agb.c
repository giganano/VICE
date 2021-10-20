/*
 * This file implements enrichment from asymptotic giant branch (AGB) stars
 * in VICE's multizone simulations.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "../utils.h"
#include "../ssp.h"
#include "agb.h"
#include "tracer.h"

/*
 * Determine the mass of a given element produced by AGB stars in each
 * zone.
 *
 * Parameters
 * ==========
 * mz: 			The multizone object for the current simulation
 * index: 		The index of the element to determine the mass production for
 *
 * Returns
 * =======
 * The mass of the given element produced in each zone in the next timestep by
 * AGB stars.
 *
 * header: agb.h
 */
extern double *m_AGB_from_tracers(MULTIZONE mz, unsigned short index) {

	unsigned long i, timestep = (*mz.zones[0]).timestep;
	double *mass = (double *) malloc ((*mz.mig).n_zones * sizeof(double));
	for (i = 0l; i < (*mz.mig).n_zones; i++) {
		mass[i] = 0;
	}
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		/*
		 * Get the tracer particle's current zone and metallicity. Use the SSP
		 * evolutionary parameters from the zone in which the tracer particle
		 * was born.
		 *
		 * n: The number of timesteps ago the tracer particle formed.
		 */
		TRACER *t = mz.mig -> tracers[i];
		SINGLEZONE *sz = mz.zones[(*t).zone_current];
		SSP *ssp = mz.zones[(*t).zone_origin] -> ssp;
		double Z = tracer_metallicity(mz, *t);
		unsigned long n = timestep - (*t).timestep_origin;
		mass[(*t).zone_current] += (
			get_AGB_yield( *(*mz.zones[(*t).zone_origin]).elements[index],
				Z, dying_star_mass(n * (*sz).dt, (*ssp).postMS, Z)) *
			(*t).mass *
			((*ssp).msmf[n] - (*ssp).msmf[n + 1l])
		);
	}
	return mass;

}

