
#ifndef TESTS_SINGLEZONE_SINGLEZONE_H 
#define TESTS_SINGLEZONE_SINGLEZONE_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Test the function which obtains the address of a singlezone object as a 
 * long. 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short test_singlezone_address(SINGLEZONE *test); 

/* 
 * Test the function which obtains the number of timesteps to allocate 
 * memory for. 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short test_n_timesteps(SINGLEZONE *test); 

/* 
 * Test the function which obtains the stellar mass in a singlezone object 
 * 
 * Parameters 
 * ========== 
 * test: 		The 1-timestep test object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: singlezone.h 
 */ 
extern unsigned short test_singlezone_stellar_mass(SINGLEZONE *test); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_SINGLEZONE_SINGLEZONE_H */ 
