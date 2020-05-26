/* 
 * This file implements testing of the mass_recycled function in the parent 
 * directory. 
 */ 

#include "../recycling.h" 


/* 
 * Performs the quiescence edge-case test on the mass_recycled routine in the 
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
 * header: recycling.h 
 */ 
extern unsigned short quiescence_test_mass_recycled(SINGLEZONE *sz) {

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mass_recycled(*sz, (*sz).elements[i]) == 0; 
		if (!status) break; 
	} 
	if (status) status &= mass_recycled(*sz, NULL) == 0; 
	return status; 

}

