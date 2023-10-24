/*
 * This file implements recycling in VICE's multizone simulations.
 *
 * Notes
 * =====
 * Here recycling refers to only the return of already enriched metals from
 * stars to the ISM. These simulations are implemented such that the
 * enrichment rate is the return plus the net yield.
 */

#include <stdlib.h>
#include "../multizone.h"
#include "recycling.h"


/*
 * Compute the mass of the index'th element added back to the ISM by recycled
 * stellar envelopes. Zones with instantaneous recycling will behave as such,
 * but zones that produce tracer particles will re-enrich their current zone,
 * even if their current has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object to re-enrich
 * index: 	The element's index in each of mz's singlezone objects.
 *
 * Returns
 * =======
 * A pointer containing an entry for each of the zones in the multizone model.
 * Each element contains the mass in solar masses of the index'th element
 * re-enriched to the ISM by recycled stellar envelopes.
 *
 * header: recycling.h
 */
extern double *recycled_mass(MULTIZONE mz, unsigned int index) {

	/*
	 * Look at each tracer particle and allow each that was born in a zone
	 * with continuous recycling to enrich its current zone via continuous
	 * recycling, regardless of the current zone's recycling prescription.
	 * Zones that have instantaneous recycling will retain their recycling
	 * as such as well as that from particles with continuous recycling that
	 * migrate into that zone.
	 */

	unsigned long i;
	double *recycled = (double *) malloc ((*mz.mig).n_zones * sizeof(double));
	for (i = 0ul; i < (*mz.mig).n_zones; i++) recycled[i] = 0;
	for (i = 0ul; i < (*mz.mig).tracer_count; i++) {
		TRACER *t = mz.mig -> tracers[i];
		SSP *ssp = mz.zones[(*t).zone_origin] -> ssp;

		if ((*ssp).continuous) {
			/* ------------------- Continuous recycling -------------------
			 *
			 * The metallicity by mass of this element in the tracer particle
			 * and its age in units of the timestep size.
			 */
			double Z = (
				(*(*mz.zones[(*t).zone_origin]).elements[index]).Z[(
					*t).timestep_origin]
			);
			unsigned long n = (*mz.zones[0]).timestep - (*t).timestep_origin;
			recycled[(*t).zone_current] += Z * (*t).mass * (
				((*ssp).crf[n + 1ul] - (*ssp).crf[n])
			);
			// mz -> zones[(*t).zone_current] -> elements[index] -> mass += (
			// 	Z * (*t).mass * ((*ssp).crf[n + 1l] - (*ssp).crf[n])
			// );
		} else {}

	}

	for (i = 0ul; i < (*mz.mig).n_zones; i++) {
		SSP *ssp = mz.zones[i] -> ssp;

		if (!(*ssp).continuous) {
			/* ------------------ Instantaneous recycling ------------------ */
			recycled[i] += (
				(*(*mz.zones[i]).ism).star_formation_rate *
				(*mz.zones[i]).dt *
				(*(*mz.zones[i]).ssp).R0 *
				(*(*mz.zones[i]).elements[index]).mass /
				(*(*mz.zones[i]).ism).mass
			);
		}
	}

	return recycled;

}


/*
 * Determine the amount of ISM gas recycled from stars in each zone in a
 * multizone simulation. Just as is the case with re-enrichment of metals,
 * zones with instantaneous recycling will behave as such, but zones with
 * continuous recycling will produce tracer particles that re-enrich their
 * current zone, even if that zone has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for this simulation
 *
 * Returns
 * =======
 * An array of doubles, each element is the mass in Msun of ISM gas returned
 * to each zone at the current timestep.
 *
 * header: recycling.h
 */
extern double *gas_recycled_in_zones(MULTIZONE mz) {

	/* Store the mass recycled in each zone in this array */
	unsigned int j;
	double *mass = (double *) malloc ((*mz.mig).n_zones * sizeof(double));
	for (j = 0; j < (*mz.mig).n_zones; j++) {
		mass[j] = 0;
	}

	/* Look at each tracer particle for continuous recycling */
	unsigned long i;
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		TRACER *t = (*mz.mig).tracers[i];
		SSP *ssp = mz.zones[(*t).zone_origin] -> ssp;

		if ((*ssp).continuous) {
			/* ------------------- Continuous recycling ------------------- */
			unsigned long n = (*mz.zones[0]).timestep - (*t).timestep_origin;
			mass[(*t).zone_current] += (*t).mass * ((*ssp).crf[n + 1l] -
				(*ssp).crf[n]);
		} else {}

	}

	/* Look at each zone for instantaneous recycling */
	for (j = 0; j < (*mz.mig).n_zones; j++) {
		SSP *ssp = mz.zones[j] -> ssp;

		if (!(*ssp).continuous) {
			/* ------------------ Instantaneous recycling ------------------ */
			mass[j] += (
				(*(*mz.zones[j]).ism).star_formation_rate *
				(*mz.zones[j]).dt *
				(*(*mz.zones[j]).ssp).R0
			);
		} else {}

	}

	return mass;

}

