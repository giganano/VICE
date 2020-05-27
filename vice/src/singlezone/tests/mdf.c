/* 
 * This file implements testing of the MDF routines in the parent directory 
 */ 

#include <math.h> 
#include "../../utils.h" 
#include "../mdf.h" 


/* 
 * Performs the quiescence edge-case test on the MDF routines in the parent 
 * directory. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: mdf.h 
 */ 
extern unsigned short quiescence_test_MDF(SINGLEZONE *sz) {

	/* 
	 * The value of the metallicity distribution after normalizing to a 
	 * simulation in which no stars form will be NaN in all bins for all 
	 * reported distributions. 
	 */ 

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) {
		unsigned long j; 
		for (j = 0u; j < (*(*sz).mdf).n_bins; j++) {
			status &= isnan((*(*sz).mdf).abundance_distributions[i][j]); 
			if (!status) break; 
		} 
		if (!status) break; 
	} 
	for (i = 0u; i < choose((*sz).n_elements, 2); i++) {
		unsigned long j; 
		for (j = 0u; j < (*(*sz).mdf).n_bins; j++) {
			status &= isnan((*(*sz).mdf).ratio_distributions[i][j]); 
			if (!status) break; 
		} 
		if (!status) break; 
	} 
	return status; 

} 


/* 
 * Performs the max age SSP edge-case test on the MDF routines in the parent 
 * directory. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: mdf.h 
 */ 
extern unsigned short max_age_ssp_test_MDF(SINGLEZONE *sz) {

	/* 
	 * The single stellar population formed is zero metallicity, so the 
	 * distribution should be the same as in the quiescent case. 
	 */ 
	return quiescence_test_MDF(sz); 

}

