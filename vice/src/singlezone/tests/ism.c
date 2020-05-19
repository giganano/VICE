/* 
 * This file implements testing of the ISM evolution routines at ism.h in 
 * the parent directory. 
 */ 

#include <stdlib.h> 
#include "../ism.h" 


/* 
 * Performs the quiescence test on the update_gas_evolution function in the 
 * parent directory by ensuring the star formation rate is equal to zero. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: ism.h 
 */ 
extern unsigned short quiescence_test_update_gas_evolution(SINGLEZONE *sz) {

	return (*(*sz).ism).star_formation_rate == 0; 

} 


/* 
 * Performs the quiescence test on the get_outflow_rate function in the parent 
 * directory by ensuring the outflow rate is equal to zero. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: ism.h 
 */ 
extern unsigned short quiescence_test_get_outflow_rate(SINGLEZONE *sz) {

	return get_outflow_rate(*sz) == 0; 

} 


/* 
 * Performs the quiescence test on the singlezone_unretained function in the 
 * parent directory by ensuring the unretained production is equal to zero. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: ism.h 
 */ 
extern unsigned short quiescence_test_singlezone_unretained(SINGLEZONE *sz) {

	unsigned short i, status = 1u; 
	double *unretained = singlezone_unretained(*sz); 
	if (unretained != NULL) {
		for (i = 0u; i < (*sz).n_elements; i++) {
			status &= unretained[i] == 0; 
			if (!status) break; 
		} 
		free(unretained); 
		return status; 
	} else {
		return 0u; 
	}

}

