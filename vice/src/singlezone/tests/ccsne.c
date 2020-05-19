/* 
 * This file implements testing of the enrichment of elements from core 
 * collapse supernovae in the parent directory. 
 */ 

#include "../ccsne.h" 


/* 
 * Performs the quiescence edge-case test on the mdot_ccsne function at 
 * ../ccsne.h applicable to cases where the mass production should be zero. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: ccsne.h 
 */ 
extern unsigned short quiescence_test_m_ccsne(SINGLEZONE *sz) {

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mdot_ccsne(*sz, *(*sz).elements[i]) == 0; 
		if (!status) break; 
	} 
	return status; 

}

