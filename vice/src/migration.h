
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
 * source: migration.c 
 */ 
extern int migration_matrix_sanitycheck(double ***migration_matrix, 
	unsigned long n_times, unsigned int n_zones); 

/* 
 * Allocates memory for the migration matrices. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * source: migration.c 
 */ 
extern void malloc_migration_matrices(MULTIZONE *mz); 

/* 
 * Sets up an element of the migration matrix at each timestep that it has 
 * memory allocated for. 
 * 
 * Parameters 
 * ========== 
 * mz: 					The multizone object for the current simulation 
 * migration_matrix: 	Pointer to the migration matrix itself 
 * row: 				The row number of this element 
 * column: 				The column number of this element 
 * arr: 				The value of the migration matrix at each timestep 
 * 
 * Returns 
 * ======= 
 * 0 if all elements of arr are between 0 and 1 at all timesteps, 1 otherwise 
 * 
 * source: migration.c 
 */ 
extern int setup_migration_element(MULTIZONE mz, double ***migration_matrix, 
	unsigned int row, unsigned int column, double *arr); 

/* 
 * Determines the number of elements in a migration matrix. This is also the 
 * number of timesteps that all VICE simulations have allocated memory for. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The number of timesteps to the final output time plus 10. By design, VICE 
 * always allocates memory for 10 extra timesteps as a safeguard against 
 * memory errors 
 * 
 * source: migration.c 
 */ 
extern unsigned long migration_matrix_length(MULTIZONE mz); 

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

