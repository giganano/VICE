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
 * Re-enriches each zone in a multizone simulation. Zones with instantaneous
 * recycling will behave as such, but zones with continuous recycling will
 * produce tracer particles that re-enrich their current zone, even if that
 * zone has instantaneous recycling.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to re-enrich
 *
 * header: recycling.h
 */
extern void recycle_metals_from_tracers(MULTIZONE *mz, unsigned int index) {

	/*
	 * Look at each tracer particle and allow each that was born in a zone
	 * with continuous recycling to enrich its current zone via continuous
	 * recycling, regardless of the current zone's recycling prescription.
	 * Zones that have instantaneous recycling will retain their recycling
	 * as such as well as that from particles with continuous recycling that
	 * migrate into that zone.
	 */

	unsigned long i;
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) {
		TRACER *t = mz -> mig -> tracers[i];
		SSP *ssp = mz -> zones[(*t).zone_origin] -> ssp;

		if ((*ssp).continuous) {
			/* ------------------- Continuous recycling ------------------- */
			unsigned long n = (*(*mz).zones[0]).timestep - (*t).timestep_origin;
			/* The metallicity by mass of this element in the tracer */
			double Z = (
				(*(*(*mz).zones[(*t).zone_origin]).elements[index]).Z[(
					*t).timestep_origin]
			);
			mz -> zones[(*t).zone_current] -> elements[index] -> mass += (
				Z * (*t).mass * ((*ssp).crf[n + 1l] - (*ssp).crf[n])
			);
		} else {}

	}

	unsigned int j;
	for (j = 0; j < (*(*mz).mig).n_zones; j++) {
		SSP *ssp = mz -> zones[j] -> ssp;

		if (!(*ssp).continuous) {
			/* ------------------ Instantaneous recycling ------------------ */
			mz -> zones[j] -> elements[index] -> mass += (
				(*(*(*mz).zones[j]).ism).star_formation_rate *
				(*(*mz).zones[j]).dt *
				(*(*(*mz).zones[j]).ssp).R0 *
				(*(*(*mz).zones[j]).elements[index]).mass /
				(*(*(*mz).zones[j]).ism).mass
			);
		} else {}

	}

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

