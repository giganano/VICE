
#ifndef ISM_H 
#define ISM_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

/* hash-code for gas-mode */ 
#ifndef GAS 
#define GAS 315 
#endif /* GAS */ 

/* hash-code for infall-mode */ 
#ifndef IFR 
#define IFR 321 
#endif /* IFR */ 

/* hash-code for star formation-mode */ 
#ifndef SFR 
#define SFR 331 
#endif /* SFR */ 

/* 
 * The minimum mass of a single stellar population to be formed in one 
 * timestep. If the star formation rate is below this value, VICE accepts it 
 * with likelihood SFR * dt / MIN_SSP_MASS 
 */ 
#ifndef MIN_SSP_MASS 
#define MIN_SSP_MASS 100.0 
#endif /* MIN_SSP_MASS */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to an ISM struct. Automatically 
 * initializes all fields to NULL. Allocates memory for a 5-element char * 
 * mode specifier. 
 * 
 * source: ism.c 
 */ 
extern ISM *ism_initialize(void); 

/* 
 * Free up the memory stored in an ISM struct. 
 * 
 * source: ism.c 
 */ 
extern void ism_free(ISM *ism); 

/* 
 * Initialize the ISM mass, star formation rate, and infall rate in 
 * preparation of a singlezone simulation 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to setup the evolution for 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on an unrecognized mode 
 * 
 * source: ism.c 
 */ 
extern unsigned short setup_gas_evolution(SINGLEZONE *sz); 

/* 
 * Moves the infall rate, total gas mass, and star formation rate in a 
 * singlezone simulation forward one timestep 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on an unrecognized mode 
 * 
 * source: ism.c 
 */ 
extern unsigned short update_gas_evolution(SINGLEZONE *sz); 

/* 
 * Moves the infall rate, total gas mass, and star formation rate in all zones 
 * in a multizone simulation forward one timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on an unrecognized mode 
 * 
 * source: ism.c 
 */ 
extern unsigned short update_zone_evolution(MULTIZONE *mz); 

/* 
 * Determine the ISM mass outflow rate in a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The mass outflow rate in Msun/Gyr 
 * 
 * source: ism.c 
 */ 
extern double get_outflow_rate(SINGLEZONE sz); 

/* 
 * Determines the outflow rate of each element in a singlezone simulation due 
 * solely to entrainment. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * mass: An array containing each element's outflowing mass in Msun 
 * 
 * source: ism.c 
 */ 
extern double *singlezone_unretained(SINGLEZONE sz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* ISM_H */ 

