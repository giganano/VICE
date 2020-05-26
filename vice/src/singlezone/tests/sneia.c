/* 
 * This file implements edge-case testing of the SNe Ia routines in the 
 * parent directory. 
 */ 

#include "../sneia.h" 

/* 
 * Performs the quiescence edge-case test on the mdot_sneia function in the 
 * parent directory. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: sneia.h 
 */ 
extern unsigned short quiescence_test_mdot_sneia(SINGLEZONE *sz) {

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mdot_sneia(*sz, *(*sz).elements[i]) == 0; 
		if (!status) break; 
	} 
	return status; 

}

