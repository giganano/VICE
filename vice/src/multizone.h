
#ifndef MULTIZONE_H 
#define MULTIZONE_H 

#ifdef __cplusplus 
extern "C"{
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocates memory for and returns a pointer to a multizone object 
 * 
 * Parameters 
 * ========== 
 * n: 		The number of zones in the simulation 
 * 
 * source: multizone.c 
 */ 
extern MULTIZONE *multizone_initialize(unsigned int n); 

/*
 * Frees the memory stored in a multizone object 
 * 
 * source: multizone.c 
 */ 
extern void multizone_free(MULTIZONE *mz); 

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
 * source: multizone.c 
 */ 
extern void link_zone(MULTIZONE *mz, unsigned long address, 
	unsigned int zone_index); 

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
 * source: multizone.c 
 */ 
extern int multizone_evolve(MULTIZONE *mz); 

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
 * source: multizone.c 
 */ 
extern int multizone_setup(MULTIZONE *mz); 

/* 
 * Frees up the memory allocated in running a multizone simulation. This does 
 * not free up the memory stored by simplying having a multizone object in the 
 * python interpreter. That is cleared by calling multizone_free. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to clean 
 * 
 * source: multizone.c 
 */ 
extern void multizone_clean(MULTIZONE *mz); 

/* 
 * Undo the pieces of preparation to run a multizone simulation that are 
 * called from python. This function is invoked when the user cancels their 
 * simulation by answer 'no' to whether or not they'd like to overwrite. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object to cancel 
 * 
 * source: multizone.c 
 */ 
extern void multizone_cancel(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MULTIZONE_H */ 



