/*
 * This file implements testing of the recycling routines in the parent
 * directory.
 */

#include <stdlib.h>
#include <math.h>
#include "../recycling.h"
#include "../../utils.h"
#include "../../singlezone/recycling.h"


/*
 * Performs the no migration edge-case test on the recycle_metals_from_tracers
 * function the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short no_migration_test_recycle_metals_from_tracers(
	MULTIZONE *mz) {

	/*
	 * This test ensures that the mass recycled in each zone matches that
	 * expected from a one-zone model. However, because multizone simulations
	 * leave out accidental populations that formed after the last output,
	 * there is one timestep that needs removed. This function decrements the
	 * timestep number, then re-increments it at the end to achieve its
	 * purposes.
	 */

	/* First take a copy of each element's mass in each zone, ... */
	double **actual = (double **) malloc (
		(*(*mz).mig).n_zones * sizeof(double *));
	unsigned int i, j;
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> timestep--;
		actual[i] = (double *) malloc (
			(*(*mz).zones[i]).n_elements * sizeof(double));
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			actual[i][j] = (*(*(*mz).zones[i]).elements[j]).mass;
		}
	}

	/*
	 * ... recycle each element, then compute the difference to get the amount
	 * of mass recycled, ...
	 */
	unsigned short status = 1u;
	for (j = 0u; j < (*(*mz).zones[0]).n_elements; j++) {
		/* This must only be called once per element -> outermost for-loop */
		recycle_metals_from_tracers(mz, j);
		for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
			actual[i][j] *= -1;
			actual[i][j] += (*(*(*mz).zones[i]).elements[j]).mass;
			/* should be similar to found by singlezone function */
			double expected = mass_recycled(
				*(*mz).zones[i],
				(*(*mz).zones[i]).elements[j]
			);
			double percent_difference = absval(
				(actual[i][j] - expected) / expected
			);
			/*
			 * ... and finally base the test on a maximum percent difference.
			 * This test typically passes with %-differences on the
			 * order of 1e-12.
			 */
			status &= percent_difference < 1e-3;
			if (!status) break;
		}
		if (!status) break;
	}
	free(actual);
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> timestep++; /* see comment at top */
	}
	return status;

}


/*
 * Performs the separation edge case test on the recycle_metals_from_tracers
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short separation_test_recycle_metals_from_tracers(
	MULTIZONE *mz) {

	/* First take a copy of each element's mass in each zone, ... */
	double **recycled = (double **) malloc (
		(*(*mz).mig).n_zones * sizeof(double *));
	unsigned int i, j;
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		recycled[i] = (double *) malloc (
			(*(*mz).zones[i]).n_elements * sizeof(double));
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			recycled[i][j] = (*(*(*mz).zones[i]).elements[j]).mass;
		}
	}

	/*
	 * ... recycle each element, then compute the difference to get the amount
	 * of mass recycled.
	 */
	unsigned short status = 1u;
	for (j = 0u; j < (*(*mz).zones[0]).n_elements; j++) {
		/* This must be called only once per element -> outermost for-loop */
		recycle_metals_from_tracers(mz, j);
		for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
			recycled[i][j] *= -1;
			recycled[i][j] += (*(*(*mz).zones[i]).elements[j]).mass;
		}
		/*
		 * There are many more stars in the quiescent zone, but the bulk of
		 * the mass recycled comes from the high mass stars that are in the
		 * star forming zone before they migrate to the quiescent zone. The
		 * amount of mass recycled should be comparable, at least within an
		 * order of magnitude.
		 */
		status &= absval(log10(recycled[1][j]) - log10(recycled[0][j])) < 1;
		if (!status) break;
	}
	free(recycled);
	return status;

}


/*
 * Performs the no migration edge case test on the gas_recycled_in_zone
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short no_migration_test_gas_recycled_in_zones(MULTIZONE *mz) {

	/*
	 * The gas mass recycled in each zone should always match that expected in
	 * a singlezone simulation if stars aren't migrating. However, because
	 * multizone simulations leave out accidental populations that formed after
	 * the last output, there is one timestep that needs removed. This function
	 * decrements the timestep number, then re-increments it at the end to
	 * achieve its purposes.
	 *
	 * This test typically passes with %-differences on the order of 1e-12.
	 */
	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> timestep--;
	}
	double *actual = gas_recycled_in_zones(*mz);
	if (actual != NULL) {
		for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
			double expected = mass_recycled(*(*mz).zones[i], NULL);
			double percent_difference = absval(
				(actual[i] - expected) / expected
			);
			status &= percent_difference < 1e-3;
			if (!status) break;
		}
	} else {
		status = 0u;
	}
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> timestep++; /* see comment at top */
	}

	return status;

}


/*
 * Performs the separation test on the gas_recycled_in_zones function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short separation_test_gas_recycled_in_zones(MULTIZONE *mz) {

	/*
	 * Similar to the metals recycled in the separation test, the amount of
	 * gas recycled should be comparable - a few massive stars roughly
	 * balances with many more lower mass stars for recycling.
	 */
	double *recycled = gas_recycled_in_zones(*mz);
	if (recycled != NULL) {
		unsigned short status = (
			absval(log10(recycled[1]) - log10(recycled[0])) < 1
		);
		free(recycled);
		return status;
	} else {
		return 0u;
	}

}

