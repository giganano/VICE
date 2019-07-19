
#ifndef MIGRATION_H 
#define MIGRATION_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Performs a sanity check on a given migration matrix by making sure the sum 
 * of migration probabilities out of a given zone at all times is <= 1. 
 * 
 * Parameters 
 * ========== 
 * migration_matrix: 		The migration matrix to sanity check 
 * n_times: 				The number of times the simulation will evaluate 
 * n_zones: 				The number of zones in the simulation 
 * 
 * Returns 
 * ======= 
 * 0 on passing sanity check, 1 on failure 
 * 
 * header: migration.h 
 */ 
extern int migration_matrix_sanitycheck(double ***migration_matrix, 
	long n_times, int n_zones); 

/* 
 * Migrates all gas, elements, and tracer particles between zones at the 
 * current timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * source: migration.c 
 */ 
extern void migrate(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MIGRATION_H */ 

