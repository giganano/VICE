/*
 * This file implements enrichment from type Ia supernovae (SNe Ia) in
 * VICE's multizone simulations.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../sneia.h"
#include "sneia.h"
#include "tracer.h"

/*
 * Determine the total mass production of a given element produced by SNe Ia
 * in each zone.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 * index: 	The index of the element to calculate the yield information for
 *
 * Returns
 * =======
 * The total mass production of the given element in each zone
 *
 * header: sneia.h
 */
extern double *m_sneia_from_tracers(MULTIZONE mz, unsigned short index) {

	unsigned long i, timestep = (*mz.zones[0]).timestep;
	double *mass = (double *) malloc ((*mz.mig).n_zones * sizeof(double));
	for (i = 0l; i < (*mz.mig).n_zones; i++) {
		mass[i] = 0;
	}
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		TRACER *t = mz.mig -> tracers[i];
		SNEIA_YIELD_SPECS sneia = *(
			mz.zones[(*t).zone_origin] -> elements[index] -> sneia_yields
		);
		/* pull yield information from the zone this particle originated */
		mass[(*t).zone_current] += (
			get_ia_yield(*(*mz.zones[(*t).zone_origin]).elements[index],
				tracer_metallicity(mz, *t)) *
			(*t).mass *
			sneia.RIa[timestep - (*t).timestep_origin]
		);
	}
	return mass;

}

