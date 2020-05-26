/* 
 * This file implements edge-case testing of routines of the singlezone object 
 * in the parent directory. 
 */ 

#include "../singlezone.h" 

/* 
 * Performs the quiescence edge-case test on the singlezone_stellar_mass 
 * function in the parent directory. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: singlezone.h 
 */ 
extern unsigned short quiescence_test_singlezone_stellar_mass(SINGLEZONE *sz) {

	return singlezone_stellar_mass(*sz) == 0; 

}

