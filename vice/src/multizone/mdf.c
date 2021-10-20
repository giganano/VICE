/*
 * This file implements the calculation of stellar metallicity distribution
 * functions (MDFs) in VICE's multizone simulations.
 */

#include <stdio.h>
#include <math.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "../utils.h"
#include "../mdf.h"
#include "../io.h"
#include "mdf.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static void update_MDF_from_tracer(MULTIZONE *mz, TRACER t);
static void reset_MDF(SINGLEZONE *sz);


/*
 * Resets all MDFs in a multizone object and fills them with the data from
 * its tracer particles.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to redo the MDF for
 *
 * header: mdf.h
 */
extern void tracers_MDF(MULTIZONE *mz) {

	unsigned long i;
	for (i = 0l; i < (*(*mz).mig).n_zones; i++) {
		/* First reset the MDF in each zone ... */
		reset_MDF(mz -> zones[i]);
	}

	/*
	 * Allocate memory for the progressbar regardless of verbosity to avoid it
	 * being used uninitialized as a failsafe.
	 */
	PROGRESSBAR *pb = progressbar_initialize((*(*mz).mig).tracer_count);
	if ((*mz).verbose) printf("Computing distribution functions....\n");
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) {
		/* ... then update with each tracer particle ... */
		update_MDF_from_tracer(mz, *(*(*mz).mig).tracers[i]);
		if ((*mz).verbose) progressbar_update(pb, i + 1ul);
	}
	if ((*mz).verbose) progressbar_finish(pb);
	progressbar_free(pb);
	
	for (i = 0l; i < (*(*mz).mig).n_zones; i++) {
		/* ... and finally normalize it within each zone */
		normalize_MDF(mz -> zones[i]);
	}

}


/*
 * Updates the MDF of a multizone object given a tracer particle.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object with the MDF to update
 * t: 		The tracer particle to update the MDF from
 */
static void update_MDF_from_tracer(MULTIZONE *mz, TRACER t) {

	SINGLEZONE *origin = (*mz).zones[t.zone_origin];
	SINGLEZONE *final = (*mz).zones[t.zone_current];

	unsigned int i;
	/* --------------------- for each tracked element --------------------- */
	for (i = 0; i < (*origin).n_elements; i++) {

		/*
		 * The value of [X/H] of the ISM for the i'th element at the timestep
		 * and in the zone that the tracer particle formed. Get the bin number
		 * of this value and increment that bin in the FINAL zone by the mass
		 * of the tracer particle (prefactors cancel in normalization).
		 */
		double onH_ = log10(
			/* trailing underscore to not override function in element.h */
			(*(*origin).elements[i]).Z[t.timestep_origin] /
			(*(*origin).elements[i]).solar
		);

		long bin = get_bin_number(
			(*(*final).mdf).bins,
			(*(*final).mdf).n_bins,
			onH_
		);
		if (bin != -1l) {
			final -> mdf -> abundance_distributions[i][bin] += t.mass;
		} else {}

	}

	unsigned int n = 0;
	/* --------------------- for each abundance ratio --------------------- */
	for (i = 1; i < (*origin).n_elements; i++) {
		unsigned int j;
		for (j = 0; j < i; j++) {
			double onH1 = log10(
				(*(*origin).elements[i]).Z[t.timestep_origin] /
				(*(*origin).elements[i]).solar
			);
			double onH2 = log10(
				(*(*origin).elements[j]).Z[t.timestep_origin] /
				(*(*origin).elements[j]).solar
			);
			long bin = get_bin_number(
				(*(*final).mdf).bins,
				(*(*final).mdf).n_bins,
				onH1 - onH2
			);
			if (bin != -1l) {
				final -> mdf -> ratio_distributions[n][bin] += t.mass;
			} else {}
			n++;
		}
	}

}


/*
 * Reset the MDF in a singlezone object such that the value within each bin
 * is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object whose MDF is to be reset
 */
static void reset_MDF(SINGLEZONE *sz) {

	unsigned long i, j;
	for (i = 0l; i < (unsigned long) (*sz).n_elements; i++) {
		for (j = 0l; j < (*(*sz).mdf).n_bins; j++) {
			sz -> mdf -> abundance_distributions[i][j] = 0.0;
		}
	}

	unsigned long n = choose((*sz).n_elements, 2);
	for (i = 0l; i < n; i++) {
		for (j = 0l; j < (*(*sz).mdf).n_bins; j++) {
			sz -> mdf -> ratio_distributions[i][j] = 0.0;
		}
	}

}

