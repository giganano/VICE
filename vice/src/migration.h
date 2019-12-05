
#ifndef MIGRATION_H 
#define MIGRATION_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

/* 
 * ij'th element represents likelihood gas or particle will migrate in a 10 Myr 
 * time interval 
 */ 
#ifndef NORMALIZATION_TIME_INTERVAL 
#define NORMALIZATION_TIME_INTERVAL 0.01 
#endif /* NORMALIZATOIN_TIME_INTERVAL */ 

#include "objects.h" 

/* 
 * Allocate memory for an return a pointer to a migration object. 
 * 
 * Parameters 
 * ========== 
 * n:		The number of zones in the multizone simulation 
 * 
 * source: migration.c 
 */ 
extern MIGRATION *migration_initialize(unsigned int n); 

/* 
 * Free up the memory stored in a migration object. 
 * 
 * source: migration.c 
 */ 
extern void migration_free(MIGRATION *mig); 

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
extern unsigned short migration_matrix_sanitycheck(double ***migration_matrix, 
	unsigned long n_times, unsigned int n_zones); 

/* 
 * Allocates memory for the gas migration matrix. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * source: migration.c 
 */ 
extern void malloc_gas_migration(MULTIZONE *mz); 

#if 0
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
#endif 

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
 * 1 if the normalization results in a probabiliy above 1 or below 0. 0 if 
 * successful. 
 * 
 * source: migration.c 
 */ 
extern unsigned short setup_migration_element(MULTIZONE mz, 
	double ***migration_matrix, unsigned int row, unsigned int column, 
	double *arr); 

#if 0
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
#endif 

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
