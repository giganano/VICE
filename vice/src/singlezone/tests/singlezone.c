/* 
 * This file implements testing of the core routines of the singlezone 
 * object. The basic outline of the test algorithm is that a simulation of one 
 * timestep is ran, and each attribute inspected. 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "../../singlezone.h" 
#include "singlezone.h" 


/* 
 * Test the function which obtains the address of a singlezone object as a 
 * long. 
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
extern unsigned short test_singlezone_address(SINGLEZONE *test) { 

	/* left-hand side is exact return statement in function */ 
	return (long) ((void *) test) == singlezone_address(test); 

} 


/* 
 * Test the function which obtains the number of timesteps to allocate 
 * memory for. 
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
extern unsigned short test_n_timesteps(SINGLEZONE *test) { 

	/* A 1-timestep simulation should always return this */ 
	return n_timesteps(*test) == BUFFER + (
		(*test).output_times[(*test).n_outputs - 1l] / (*test).dt); 

} 


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
extern unsigned short test_singlezone_stellar_mass(SINGLEZONE *test) { 

	return (singlezone_stellar_mass(*test) == 
		(*(*test).ism).star_formation_history[0] * (*test).dt * 
		(1 - (*(*test).ssp).crf[1])); 

} 

