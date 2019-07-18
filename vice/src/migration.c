/* 
 * This file implements the migration of tracer particles between zones in 
 * multizone simulations. 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "migration.h" 
#include "multizone.h" 
#include "tracer.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void migrate_tracer(MULTIZONE mz, TRACER *t); 
static void migrate_gas_element(MULTIZONE *mz, int index); 
static double **setup_changes(unsigned int n_zones); 
static double **get_changes(MULTIZONE mz, int index); 

/* 
 * Migrates all gas, elements, and tracer particles between zones at the 
 * current timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * header: migration.h 
 */ 
extern void migrate(MULTIZONE *mz) {

	/* Migrate gas and all elements between zones */ 
	int i; 
	for (i = -1; i < (*(*mz).zones[0]).n_elements; i++) {
		migrate_gas_element(mz, i); 
	} 

	/* Migrate all tracer particles between zones */ 
	long j, timestep = (*(*mz).zones[0]).timestep; 
	for (j = 0l; j < timestep * (*mz).n_zones * (*mz).n_tracers; j++) {
		migrate_tracer(*mz, mz -> tracers[j]); 
	} 

}

/* 
 * Moves a tracer particle with probability given by the migration matrix at 
 * the current timestep based on a random number generator. 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object for the current simulation 
 * t: 			A pointer to the tracer particle to potentially move between 
 * 				zones
 */ 
static void migrate_tracer(MULTIZONE mz, TRACER *t) { 

	/* 
	 * Bookkeeping 
	 * =========== 
	 * dice_roll: 	A random double between 0 and 1 
	 * timestep: 	The timestep number, pulled from one of the zones 
	 * i, j: 		The row and column indeces of the migration matrix 
	 */ 

	double dice_roll = (double) rand() / RAND_MAX; 
	long timestep = (*mz.zones[0]).timestep; 
	unsigned int j, i = (*t).zone_current; 

	/* Look at all elements of the relevant row in the migration matrix */ 
	for (j = 0; j < mz.n_zones; j++) { 
		if (j == i) {
			/* Migration to the same zone can be ignored */ 
			continue; 
		} else if (dice_roll < mz.migration_matrix[timestep][i][j]) {
			/* stop the for loop after the tracer particle migrates once */ 
			t -> zone_current = j; 
			break; 
		} else { 
			/* Keep checking to see if it migrated */ 
			continue; 
		} 
	} 

} 

/* 
 * Migrates ISM gas and ISM phase elements between zones. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * index: 	The index of the element to migrate between zones 
 * 			-1 for the gas reservoir itself 
 */ 
static void migrate_gas_element(MULTIZONE *mz, int index) {

	int i, j; 
	double **changes = get_changes(*mz, -1); 
	for (i = 0; i < (*mz).n_zones; i++) {
		for (j = 0; j < (*mz).n_zones; j++) {
			if (i == j) { 
				/* migration within zone */ 
				continue; 
			} else if (index == -1) { 
				/* gas leaves zone i and goes into zone j */ 
				mz -> zones[i] -> ism -> mass -= changes[i][j]; 
				mz -> zones[j] -> ism -> mass += changes[i][j]; 
			} else {
				/* element leaves zone i and goes into zone j */ 
				mz -> zones[i] -> elements[index] -> mass -= changes[i][j]; 
				mz -> zones[j] -> elements[index] -> mass += changes[i][j]; 
			} 
		} 
	} 
	free(changes); 

} 

/* 
 * Determine how much of the nebular phase mass migrates between all zones at 
 * the current timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 				The multizone object for the current simulation 
 * index: 			The index of the element to determine the changes for 
 * 					-1 for the gas reservoir 
 * 
 * Returns 
 * ======= 
 * An n_zones x n_zones 2D array of double where the [i][j]'th element is the 
 * amount of mass that moves from the i'th to the j'th zone at the current 
 * timestep. 
 */ 
static double **get_changes(MULTIZONE mz, int index) {

	unsigned int i, j; 
	long timestep = (*mz.zones[0]).timestep; 
	double **changes = setup_changes(mz.n_zones); 

	for (i = 0; i < mz.n_zones; i++) {
		for (j = 0; j < mz.n_zones; j++) {
			if (i == j) {
				/* migration within zone */ 
				continue; 
			} else if (index == -1) {
				/* gas reservoir */ 
				changes[i][j] = (
					mz.migration_matrix[timestep][i][j] * 
					(*(*mz.zones[i]).ism).mass 
				); 
			} else {
				/* element in the i'th zone */ 
				changes[i][j] = (
					mz.migration_matrix[timestep][i][j] * 
					(*(*mz.zones[i]).elements[index]).mass 
				); 
			} 
		} 
	} 
	return changes; 

} 

/* 
 * Sets up a n_zones x n_zones 2D-array of zeroes, within which the change in 
 * masses for ISM phase elements and gas can be temporarily stored. 
 * 
 * Parameters 
 * ========== 
 * n_zones: 	The number of zones in the simulation 
 * 
 * Returns 
 * ======= 
 * An n_zones x n_zones 2D double array where each element is set to zero. 
 */ 
static double **setup_changes(unsigned int n_zones) {

	unsigned int i, j; 
	double **changes = (double **) malloc (n_zones * sizeof(double *)); 
	for (i = 0; i < n_zones; i++) {
		changes[i] = (double *) malloc (n_zones * sizeof(double)); 
		for (j = 0; j < n_zones; j++) {
			changes[i][j] = 0.0; 
		} 
	} 
	return changes; 

} 


