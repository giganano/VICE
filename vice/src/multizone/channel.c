/*
 * This file implements enrichment from a custom enrichment channel in VICE's
 * multizone simulations.
 */

#include "../multizone.h"
#include "../singlezone.h"
#include "channel.h"
#include "tracer.h"


/*
 * Enrichh all elements in a multizone simulation from all custom enrichment
 * channels from all tracer particles in the simulation.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 *
 * header: channel.h
 */
extern void from_tracers(MULTIZONE *mz) {

	unsigned long i, timestep = (*(*mz).zones[0]).timestep;
	for (i = 0lu; i < (*(*mz).mig).tracer_count; i++) {
		TRACER *t = mz -> mig -> tracers[i];
		unsigned int j;
		/*
		 * Enrich the j'th element in the tracer particle's current zone from
		 * all customs channels associated. Pull the yield information from
		 * the zone in which the tracer particle originated.
		 */
		for (j = 0u; j < (*(*mz).zones[(*t).zone_current]).n_elements; j++) {
			ELEMENT *e = mz -> zones[(*t).zone_current] -> elements[j];
			unsigned int k;
			for (k = 0u; k < (*e).n_channels; k++) {
				CHANNEL *ch = (mz -> zones[(*t).zone_origin] -> elements[j] ->
					channels[k]);
				e -> mass += (*(*e).channels[k]).entrainment * (
					get_yield(*ch, tracer_metallicity(*mz, *t) * (*t).mass *
						(*ch).rate[timestep - (*t).timestep_origin] )
				);
			}
		}
	}

}

