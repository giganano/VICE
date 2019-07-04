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
#endif 

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
extern int singlezone_evolve(SINGLEZONE *sz); 

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


