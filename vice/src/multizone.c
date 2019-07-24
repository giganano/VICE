/* 
 * This file implements the multizone object and the simulations thereof 
 */ 

#include <stdlib.h> 
#include "multizone.h" 
#include "singlezone.h" 
#include "migration.h" 
#include "element.h" 
#include "tracer.h" 
#include "utils.h" 
#include "ism.h" 
#include "mdf.h" 
#include "io.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void multizone_timestepper(MULTIZONE *mz); 
static void verbosity(MULTIZONE mz); 
static void multizone_write_history(MULTIZONE mz); 
static void multizone_normalize_MDF(MULTIZONE *mz); 
static void multizone_write_MDF(MULTIZONE mz); 

/* 
 * Allocates memory for and returns a pointer to a multizone object 
 * 
 * Parameters 
 * ========== 
 * n: 		The number of zones in the simulation 
 * 
 * header: multizone.h 
 */ 
extern MULTIZONE *multizone_initialize(unsigned int n) {

	/* 
	 * Memory is allocated for n SINGLEZONE structs, but they are not 
	 * initialized here. When a multizone object is created through the 
	 * python interpreter, it creates an array of singlezone objects, then 
	 * calls link_zone to point each zone here to proper memory address. 
	 */ 

	MULTIZONE *mz = (MULTIZONE *) malloc (sizeof(MULTIZONE)); 
	mz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	mz -> zones = (SINGLEZONE **) malloc (n * sizeof(SINGLEZONE *)); 
	mz -> n_zones = n; 
	mz -> migration_matrix_gas = NULL; 
	mz -> migration_matrix_tracers = NULL; 
	mz -> tracer_count = 0l; 
	mz -> tracers = NULL; 
	return mz; 

} 

/*
 * Frees the memory stored in a multizone object 
 * 
 * header: multizone.h 
 */ 
extern void multizone_free(MULTIZONE *mz) { 

	if (mz != NULL) {

		/* 
		 * Since the singlezone object's __dealloc__ function call's 
		 * singlezone_free, the memory for each individual zone should not 
		 * be freed here. Doing so will cause a memory error upon system exit. 
		 */ 

		if ((*mz).name != NULL) {
			free(mz -> name); 
			mz -> name = NULL; 
		} else {} 

		if ((*mz).migration_matrix_gas != NULL) {
			free(mz -> migration_matrix_gas); 
			mz -> migration_matrix_gas = NULL; 
		} else {} 

		if ((*mz).migration_matrix_tracers != NULL) {
			free(mz -> migration_matrix_tracers); 
			mz -> migration_matrix_tracers = NULL; 
		} else {} 

		if ((*mz).tracers != NULL) {
			unsigned long i; 
			for (i = 0; i < (*mz).tracer_count; i++) {
				tracer_free(mz -> tracers[i]); 
			} 
			free(mz -> tracers); 
			mz -> tracers = NULL; 
			mz -> tracer_count = 0l; 
		} else {} 

		free(mz); 
		mz = NULL; 

	} 

} 

/* 
 * Links an individual zone in a multizone object to the proper address of a 
 * singlezone struct. 
 * 
 * Parameters 
 * ========== 
 * mz: 			A pointer to the multizone object 
 * address: 	The address of the singlezone object to link 
 * zone_index: 	The zone number this singlezone object should correspond to 
 * 
 * header: multizone.h 
 */ 
extern void link_zone(MULTIZONE *mz, unsigned long address, 
	unsigned int zone_index) {

	mz -> zones[zone_index] = (SINGLEZONE *) address; 

} 

#if 0 
extern void test_linker(MULTIZONE mz) {

	unsigned int i; 
	for (i = 0; i < mz.n_zones; i++) {
		printf("Address of zones[%d] = %p\n", i, (void *) mz.zones[i]); 
	}

	for (i = 0; i < mz.n_zones; i++) {
		printf("zones[%d].name = %s\n", i, (*mz.zones[i]).name); 
	} 

}
#endif 

/* 
 * Runs the multizone simulation under current user settings. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to run 
 * 
 * Returns
 * ======= 
 * 0 on success, 1 on setup failure 
 * 
 * header: multizone.h 
 */ 
extern int multizone_evolve(MULTIZONE *mz) {

	int x = multizone_setup(mz); 
	/* 
	 * x differentiates between failed setup and migration matrix failing the 
	 * sanity check 
	 */ 
	if (x) return x; 

	long n = 0l; 		/* keep track of the number of outputs */ 
	SINGLEZONE *sz = mz -> zones[0]; 		/* for convenience/readability */ 
	while ((*sz).current_time <= (*sz).output_times[(*sz).n_outputs - 1l]) {
		/* 
		 * Run the simulation until the time reaches the final output time 
		 * specified by the user. Write to each zone's history.out file 
		 * whenever an output time is reached, or if the current timestep is 
		 * closer to the next output time than the subsequent timestep. 
		 */ 
		if ((*sz).current_time >= (*sz).output_times[n] || 
			2 * (*sz).output_times[n] < 2 * (*sz).current_time + (*sz).dt) {
			multizone_write_history(*mz); 
			n++; 
		} else {} 
		multizone_timestepper(mz); 
		verbosity(*mz); 
	} 
	if ((*mz).verbose) printf("\n"); 

	/* Normalize all MDFs, write them out, and clean up */ 
	multizone_normalize_MDF(mz); 
	multizone_write_MDF(*mz); 
	multizone_clean(mz); 
	return 0; 

}

/* 
 * Advances all quantities in a multizone object forward one timestep 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to move forward 
 */ 
static void multizone_timestepper(MULTIZONE *mz) {

	update_elements(mz); 
	update_zone_evolution(mz); 

	/* 
	 * Now each element and the ISM in each zone are at the next timestep. 
	 * bookkeep the new metallicity and update the MDF in each zone. 
	 */ 
	unsigned int i, j; 
	for (i = 0; i < (*mz).n_zones; i++) { 
		SINGLEZONE *sz = mz -> zones[i]; 
		for (j = 0; j < (*sz).n_elements; j++) {
			sz -> elements[j] -> Z[(*sz).timestep + 1l] = (
				(*(*sz).elements[j]).mass / (*(*sz).ism).mass 
			); 
		} 
		update_MDF(sz); 
	} 
	
	/* 
	 * Migration must be done before incrementing the timestep number as that 
	 * is used to determine the number of tracer particles present. Migrating 
	 * first also ensures that newly injected tracer particles never migrate 
	 * at the timestep they're born. 
	 */ 
	migrate(mz); 
	for (i = 0; i < (*mz).n_zones; i++) {
		mz -> zones[i] -> current_time += (*(*mz).zones[i]).dt; 
		mz -> zones[i] -> timestep++; 
	} 
	inject_tracers(mz); 

} 

/*
 * Sets up every zone in a multizone object for simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object itself 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: multizone.h 
 */ 
extern int multizone_setup(MULTIZONE *mz) { 

	unsigned int i; 
	for (i = 0; i < (*mz).n_zones; i++) {
		if (singlezone_setup(mz -> zones[i])) {
			return 1; 
		} else { 
			continue; 
		} 
	} 
	unsigned long n_times = 10l + (unsigned long) (
		(*(*mz).zones[0]).n_outputs / (*(*mz).zones[0]).dt 
	); 
	if (migration_matrix_sanitycheck((*mz).migration_matrix_gas, 
		n_times, (*mz).n_zones)) {
		return 2; 
	} else if (migration_matrix_sanitycheck((*mz).migration_matrix_tracers, 
		n_times, (*mz).n_zones)) {
		return 2; 
	} 
	seed_random(); 
	return 0; 

} 

/* 
 * Frees up the memory allocated in running a multizone simulation. This does 
 * not free up the memory stored by simplying having a multizone object in the 
 * python interpreter. That is cleared by calling multizone_free. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to clean 
 * 
 * header: multizone.h 
 */ 
extern void multizone_clean(MULTIZONE *mz) {

	/* clean each singlezone object */ 
	unsigned int i; 
	for (i = 0; i < (*mz).n_zones; i++) { 
		singlezone_close_files(mz -> zones[i]); 
		singlezone_clean(mz -> zones[i]); 
	} 

	/* free up each tracer and set the pointer to NULL again */ 
	unsigned long j; 
	for (j = 0l; 
		j < (*(*mz).zones[0]).timestep * (*mz).n_zones * (*mz).n_tracers; 
		j++) {
		tracer_free(mz -> tracers[j]); 
	} 
	free(mz -> tracers); 
	mz -> tracers = NULL; 

	/* free up the migration matrices */ 
	free(mz -> migration_matrix_gas); 
	free(mz -> migration_matrix_tracers); 
	mz -> migration_matrix_gas = NULL; 
	mz -> migration_matrix_tracers = NULL; 

} 

/* 
 * Prints the current time on the same line on the console if the user has 
 * specified verbosity. 
 */ 
static void verbosity(MULTIZONE mz) {

	if (mz.verbose) { 
		/* '\t' characters injected to flush round-off errors */ 
		printf("\rCurrent Time: %g Gyr\t\t\t", (*mz.zones[0]).current_time); 
	} else {} 

}

/* 
 * Writes history output for each zone in a multizone simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object to write output from 
 */ 
static void multizone_write_history(MULTIZONE mz) { 

	unsigned int i; 
	for (i = 0; i < mz.n_zones; i++) {
		write_history_output(*mz.zones[i]); 
	} 

} 

/* 
 * Normalizes the stellar MDFs in all zones in a multizone object. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 */ 
static void multizone_normalize_MDF(MULTIZONE *mz) {

	unsigned int i; 
	for (i = 0; i < (*mz).n_zones; i++) {
		normalize_MDF(mz -> zones[i]); 
	} 

} 

/* 
 * Writes the stellar MDFs to all output files. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object to write the MDF from 
 */ 
static void multizone_write_MDF(MULTIZONE mz) {

	unsigned int i; 
	for (i = 0; i < mz.n_zones; i++) {
		write_mdf_output(*mz.zones[i]); 
	}

}



