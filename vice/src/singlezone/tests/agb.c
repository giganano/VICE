/* 
 * This file implements testing of the enrichment from asymptotic giant 
 * branch stars in the parent directory. 
 */ 

#include "../../utils.h" 
#include "../../ssp.h" 
#include "../agb.h" 


/* 
 * Performs the quiescence edge-case test on the m_AGB function at ../agb.h 
 * applicable to cases where the mass production should be zero. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: agb.h 
 */ 
extern unsigned short quiescence_test_m_AGB(SINGLEZONE *sz) { 

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) { 
		status &= m_AGB(*sz, *(*sz).elements[i]) == 0; 
		if (!status) break; 
	} 
	return status; 

}


/* 
 * Performs the max age SSP edge-case test on the m_AGB function at ../agb.h 
 * applicable to cases where star formation is nonzero for the first timestep 
 * and zero thereafter. 
 * 
 * Parameters 
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: agb.h 
 */ 
extern unsigned short max_age_ssp_test_m_AGB(SINGLEZONE *sz) {

	unsigned short i, status = 1u; 
	for (i = 0u; i < (*sz).n_elements; i++) {
		double mass = (
			get_AGB_yield(*(*sz).elements[i], 0, 
				main_sequence_turnoff_mass(((*sz).timestep) * (*sz).dt, 
				(*(*sz).ssp).postMS)) * 
			(*(*sz).ism).star_formation_history[0] * (*sz).dt * 
			(
				(*(*sz).ssp).msmf[(*sz).timestep] - 
				(*(*sz).ssp).msmf[(*sz).timestep + 1l]
			) 
		); 
		status &= m_AGB(*sz, *(*sz).elements[i]) == mass; 
		if (!status) break; 
	} 
	return status; 

}

