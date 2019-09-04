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
static void multizone_evolve_simple(MULTIZONE *mz); 
static void multizone_evolve_full(MULTIZONE *mz); 
static unsigned short multizone_timestepper(MULTIZONE *mz); 
static void verbosity(MULTIZONE mz); 
static void multizone_write_history(MULTIZONE mz); 
// static void multizone_normalize_MDF(MULTIZONE *mz); 
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
	 * Memory is allocated for n singlezone objects, but they are not 
	 * initialized ere. When a multizone object is created through the python 
	 * interpreter, it creates an array of singlezone objects, then calls 
	 * link_zone to point each zone here to the proper memory addresses. 
	 */ 
	MULTIZONE *mz = (MULTIZONE *) malloc (sizeof(MULTIZONE)); 
	mz -> zones = (SINGLEZONE **) malloc (n * sizeof(SINGLEZONE *)); 
	mz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	mz -> mig = migration_initialize(n); 
	mz -> verbose = 0; 
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
		 * Since the singlezone object's __dealloc__ function calls 
		 * singlezone_free, the memory for each individual zone should not 
		 * be freed here. Doing so will cause a memory error upon system exit. 
		 */ 

		if ((*mz).name != NULL) {
			free(mz -> name); 
			mz -> name = NULL; 
		} else {} 

		if ((*mz).mig != NULL) {
			migration_free(mz -> mig); 
			mz -> mig = NULL; 
		}

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

/* 
 * Runs the multizone simulation under current user settings. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to run 
 * 
 * Returns
 * ======= 
 * 0 on success, 1 on zone setup failure, 2 on migration normalization 
 * error, 3 on tracer particle file I/O error. 
 * 
 * header: multizone.h 
 */ 
extern unsigned short multizone_evolve(MULTIZONE *mz) {

	/* 
	 * x differentiates between failed setup and migration matrix failing 
	 * the sanity check. 
	 */ 
	unsigned short x = multizone_setup(mz); 
	if (x) return x; 

	/* 
	 * Run either the simple or full evolution depending on the user's 
	 * specification at runtime. 
	 */ 
	if ((*mz).simple) {
		multizone_evolve_simple(mz); 
	} else {
		multizone_evolve_full(mz); 
	} 
	if ((*mz).verbose) printf("Computing distribution functions....\n"); 
	tracers_MDF(mz); 
	multizone_write_MDF(*mz); 

	/* Write the tracer particle data */ 
	if (!multizone_open_tracer_file(mz)) {
		write_tracers_header(*mz); 
		write_tracers_output(*mz); 
		multizone_close_tracer_file(mz); 
	} else {
		x = 3; 
	} 

	multizone_clean(mz); 
	if ((*mz).verbose) printf("Finished.\n"); 
	return x; 

}

/* 
 * Runs the multizone simulation under current user settings with tracer 
 * particles not tracked at each individual timestep 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to run 
 */ 
static void multizone_evolve_simple(MULTIZONE *mz) {

	unsigned int i; 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		if ((*mz).verbose) printf("Evolving zone %d...\n", i); 
		singlezone_evolve_no_setup_no_clean(mz -> zones[i]); 
	} 

	/* Set the tracer count to the proper value for computing the MDF */ 
	mz -> mig -> tracer_count = (
		(n_timesteps(*(*mz).zones[0]) - BUFFER) * 
		(*(*mz).mig).n_zones * 
		(*(*mz).mig).n_tracers 
	); 
	compute_tracer_masses(mz); 

}

/* 
 * Runs the multizone simulation under current user settings with tracer 
 * particle zones tracked at each individual timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to run 
 */ 
static void multizone_evolve_full(MULTIZONE *mz) {

	#if 0
	/* 
	 * x differentiates between failed setup and migration matrix failing the 
	 * sanity check 
	 */ 
	unsigned short x = multizone_setup(mz); 
	if (x) return x; 
	#endif 

	/* 
	 * Use the variable n to keep track of the number of outputs. Pull a 
	 * local copy of the first zone just for convenience. Lastly, tracer 
	 * particles are injected at the end of each timestep, so inject them at 
	 * the start of the simulation to account for the first timestep. 
	 */ 
	long n = 0l; 
	SINGLEZONE *sz = mz -> zones[0]; 
	// inject_tracers(mz); 
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
		if (multizone_timestepper(mz)) break; 
		verbosity(*mz); 
	} 
	if ((*mz).verbose) printf("\n"); 

	#if 0
	/* Normalize all MDFs and write them out */ 
	multizone_normalize_MDF(mz); 
	multizone_write_MDF(*mz); 

	/* Write the tracer data */ 
	if (!multizone_open_tracer_file(mz)) { 
		write_tracers_header(*mz); 
		write_tracers_output(*mz); 
		multizone_close_tracer_file(mz); 
	} else { 
		x = 3; 
	} 

	multizone_clean(mz); 
	return x; 
	#endif 

} 

/* 
 * Advances all quantities in a multizone object forward one timestep 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to move forward 
 * 
 * Returns 
 * ======= 
 * 0 while the simulation is running, 1 if the simulation is over  
 */ 
static unsigned short multizone_timestepper(MULTIZONE *mz) {

	update_elements(mz); 
	update_zone_evolution(mz); 

	/* 
	 * Now each element and the ISM in each zone are at the next timestep. 
	 * bookkeep the new metallicity and update the MDF in each zone. 
	 */ 
	unsigned int i, j; 

	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
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
	inject_tracers(mz); 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		mz -> zones[i] -> current_time += (*(*mz).zones[i]).dt; 
		mz -> zones[i] -> timestep++; 
	} 

	return ((*(*mz).zones[0]).current_time > 
		(*(*mz).zones[0]).output_times[(*(*mz).zones[0]).n_outputs - 1l]); 

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
extern unsigned short multizone_setup(MULTIZONE *mz) { 

	unsigned int i; 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		if (singlezone_setup(mz -> zones[i])) return 1; 
	} 

	if (migration_matrix_sanitycheck((*(*mz).mig).gas_migration, 
		n_timesteps((*(*mz).zones[0])), (*(*mz).mig).n_zones)) {
		return 2; 
	} else {
		mz -> mig -> tracer_count = 0l; 
		return 0; 
	}

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
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		singlezone_close_files(mz -> zones[i]); 
		singlezone_clean(mz -> zones[i]); 
	} 

	/* free up each tracer and set the pointer to NULL again */ 
	unsigned long j; 
	for (j = 0l; j < (*(*mz).mig).tracer_count; j++) { 
		tracer_free(mz -> mig -> tracers[j]); 
	} 
	free(mz -> mig -> tracers); 
	mz -> mig -> tracers = NULL; 

	/* free up the migration matrix */ 
	free(mz -> mig -> gas_migration); 
	mz -> mig -> gas_migration = NULL; 

} 

/* 
 * Undo the pieces of preparation to run a multizone simulation that are 
 * called from python. This function is invoked when the user cancels their 
 * simulation by answer 'no' to whether or not they'd like to overwrite. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to cancel 
 * 
 * header: multizone.h 
 */ 
extern void multizone_cancel(MULTIZONE *mz) {

	unsigned int i; 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		singlezone_cancel(mz -> zones[i]); 
	} 
	free(mz -> mig -> gas_migration); 
	mz -> mig -> gas_migration = NULL;  

} 

/* 
 * Prints the current time on the same line on the console if the user has 
 * specified verbosity. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 */ 
static void verbosity(MULTIZONE mz) {

	if (mz.verbose) { 
		printf("\rCurrent Time: %.2f Gyr", (*mz.zones[0]).current_time); 
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
	for (i = 0; i < (*mz.mig).n_zones; i++) { 
		write_history_output(*mz.zones[i]); 
	} 

} 

#if 0
/* 
 * Normalizes the stellar MDFs in all zones in a multizone object. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 */ 
static void multizone_normalize_MDF(MULTIZONE *mz) {

	unsigned int i; 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		normalize_MDF(mz -> zones[i]); 
	} 

} 
#endif 

/* 
 * Writes the stellar MDFs to all output files. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object to write the MDF from 
 */ 
static void multizone_write_MDF(MULTIZONE mz) {

	unsigned int i; 
	for (i = 0; i < (*mz.mig).n_zones; i++) {
		write_mdf_output(*mz.zones[i]); 
	}

} 



