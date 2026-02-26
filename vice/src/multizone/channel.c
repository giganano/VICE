/*
 * This file is part of the VICE package.
 * Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
 * License: MIT License. See LICENSE in top-level directory
 * at: https://github.com/giganano/VICE.git.
 *
 * This file implements enrichment from a custom enrichment channel in VICE's
 * multizone simulations.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "channel.h"
#include "tracer.h"


/*
 * Determine the total mass of a given element produced through custom
 * enrichment channels in each zone.
 *
 * Parameters
 * ==========
 * mz:		The multizone object for the current simulation.
 * index: 	The index of the element to calculate the yield information for
 *
 * Returns
 * =======
 * The total mass production of the given element in each zone.
 *
 * Notes
 * =====
 * This function also adds the unretained mass from each additional enrichment
 * channel to the outflow, following the built-in AGB star, CCSN, and SN Ia
 * enrichment channels.
 *
 * header: channel.h
 */
extern double *m_channels_from_tracers(MULTIZONE *mz, unsigned short index) {

	unsigned long timestep = (*(*mz).zones[0]).timestep;
	double *mass = (double *) malloc ((*(*mz).mig).n_zones * sizeof(double));
	for (unsigned long i = 0ul; i < (*(*mz).mig).n_zones; i++) mass[i] = 0;
	for (unsigned long i = 0ul; i < (*(*mz).mig).tracer_count; i++) {
		TRACER t = *(*(*mz).mig).tracers[i];
		ELEMENT e = *(*(*mz).zones[t.zone_origin]).elements[index];
		for (unsigned short j = 0u; j < e.n_channels; j++) {
			CHANNEL ch = *e.channels[j];
			double mass_produced = (
				get_channel_yield(ch, tracer_metallicity(*mz, t)) *
				t.mass * ch.rate[timestep - t.timestep_origin]
			);
			double entrainment = (*(*(*(*
				mz).zones[t.zone_current]).elements[index]).channels[j]).entrainment;
			mass[t.zone_current] += mass_produced * entrainment;
			mz -> zones[t.zone_current] -> elements[index] -> unretained += (
				mass_produced * (1 - entrainment)
			);
		}
	}
	return mass;

}


#if 0
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
extern void channels_from_tracers(MULTIZONE *mz) {

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
#endif
