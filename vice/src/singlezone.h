/* 
 * This is the main header file associated with the singlezone object 
 */ 

#ifndef SINGLEZONE_H 
#define SINGLEZONE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

/* Maximum amount of time in Gyr that VICE supports singlezone simulations */ 
#ifndef SINGLEZONE_MAX_EVAL_TIME 
#define SINGLEZONE_MAX_EVAL_TIME 15 
#endif /* SINGLEZONE_MAX_EVAL_TIME */ 

/* 
 * The number of timesteps beyond the final evaluation time that memory is 
 * allocated for as a safeguard against memory errors 
 */ 
#ifndef BUFFER 
#define BUFFER 10l 
#endif /* BUFFER */ 

#include "objects.h" 

extern void singlezone_printname(SINGLEZONE sz); 

/* 
 * Allocate memory for and return a pointer to a SINGLEZONE struct. 
 * Automatically initializes all fields to NULL. 
 * 
 * source: singlezone.c 
 */ 
extern SINGLEZONE *singlezone_initialize(void); 

/* 
 * Free up the memory associated with a singlezone object. 
 * 
 * source: singlezone.c 
 */ 
extern void singlezone_free(SINGLEZONE *sz); 

/* 
 * Obtain the memory address of a singlezone object as a long. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object to obtain the memory address for 
 * 
 * source: singlezone.c 
 */ 
extern long singlezone_address(SINGLEZONE *sz); 

/* 
 * Runs the singlezone simulation under current user settings. Most of VICE is 
 * built around calling this function. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to run 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on setup failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short singlezone_evolve(SINGLEZONE *sz); 

/* 
 * Evolves a singlezone simulation under current user settings, but does not 
 * write the MDF output or normalization. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to run 
 * 
 * source: singlezone.c 
 */ 
extern void singlezone_evolve_no_setup_no_clean(SINGLEZONE *sz); 

/* 
 * Setup the singlezone object for simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to do the setup for 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short singlezone_setup(SINGLEZONE *sz); 

/* 
 * Frees up the memory allocated in running a singlezone simulation. This does 
 * not free up the memory stored by simpling having a singlezone object in the 
 * python interpreter. That is cleared by calling singlezone_free. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object to clean 
 * 
 * source: singlezone.h 
 */ 
extern void singlezone_clean(SINGLEZONE *sz); 

/* 
 * Undo the pieces of preparation to run a singlezone simulation that are 
 * called from python. This function is invoked when the user cancels their 
 * simulation by answering 'no' to whether or not they'd like to overwrite. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone simulation to cancel 
 * 
 * source: singlezone.c 
 */ 
extern void singlezone_cancel(SINGLEZONE *sz); 

/* 
 * Determine the number of timesteps that memory is allocated for in the 
 * singlezone object. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for this simulation 
 * 
 * Returns 
 * ======= 
 * The final output time divided by the timestep size plus 10. 
 * 
 * source: singlezone.c 
 */ 
extern unsigned long n_timesteps(SINGLEZONE sz); 

/* 
 * Determine the stellar mass in a singlezone simulation 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The instantaneous stellar mass in Msun 
 * 
 * source: singlezone.c 
 */ 
extern double get_stellar_mass(SINGLEZONE sz); 

#ifdef __cplusplus 
} 
#endif 

#endif /* SINGLEZONE_H */ 


