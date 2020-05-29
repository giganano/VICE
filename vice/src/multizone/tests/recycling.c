/* 
 * This file implements testing of the recycling routines in the parent 
 * directory. 
 */ 

#include <stdlib.h> 
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

	/* First take a copy of each element's mass in each zone, ... */ 
	double **actual = (double **) malloc (
		(*(*mz).mig).n_zones * sizeof(double *)); 
	unsigned int i, j; 
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
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
	 * a singlezone simulation if stars aren't migrating. 
	 * 
	 * This test typically passes with %-differences on the order of 1e-12. 
	 */ 
	double *actual = gas_recycled_in_zones(*mz); 
	if (actual != NULL) {
		unsigned short i, status = 1u; 
		for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
			double expected = mass_recycled(*(*mz).zones[i], NULL); 
			double percent_difference = absval(
				(actual[i] - expected) / expected 
			); 
			status &= percent_difference < 1e-3; 
			if (!status) break; 
		} 
		return status; 
	} else {
		return 0u; 
	}

}

