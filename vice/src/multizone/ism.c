/* 
 * This file implements the time evolution of an interstellar medium (ISM) 
 * in VICE's multizone simulations. 
 */ 

#include <stdlib.h> 
#include "../multizone.h" 
#include "../singlezone.h" 
#include "../utils.h" 
#include "../ism.h" 
#include "ism.h" 


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
 * header: ism.h 
 */ 
extern unsigned short update_zone_evolution(MULTIZONE *mz) {

	/* 
	 * The relation between star formation rate, infall rate, gas supply, 
	 * timestep size, outflow rate, recycling rate, and star formation 
	 * efficiency timescale: 
	 * 
	 * SFR = MG * tau_star^-1 
	 * 
	 * dMG = (IFR - SFR - OFR) * dt + M_recycled 
	 * 
	 * Primordial inflow is taken into account prior to updating the infall and 
	 * gas supply so that there isn't a 1-timestep delay or advance in the 
	 * amount of helium added 
	 */ 
	
	unsigned int i; 
	double *mass_recycled = gas_recycled_in_zones(*mz); 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		SINGLEZONE *sz = mz -> zones[i]; 
		primordial_inflow(sz); 

		switch (checksum((*(*sz).ism).mode)) {

			case GAS: 
				sz -> ism -> mass = (*(*sz).ism).specified[(*sz).timestep + 1l]; 
				sz -> ism -> star_formation_rate = (
					(*(*sz).ism).mass / get_SFE_timescale(*sz) 
				); 
				sz -> ism -> infall_rate = (
					((*(*sz).ism).mass - (*(*sz).ism).specified[(*sz).timestep] 
						- mass_recycled[i]) / (*sz).dt + 
					(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz) 
				); 
				// enforce_sfr_floor(sz); 
				break; 

			case IFR: 
				sz -> ism -> mass += (
					((*(*sz).ism).infall_rate - 
						(*(*sz).ism).star_formation_rate - 
						get_outflow_rate(*sz)) * (*sz).dt + mass_recycled[i] 
				); 
				sz -> ism -> infall_rate = (
					*(*sz).ism).specified[(*sz).timestep + 1l]; 
				sz -> ism -> star_formation_rate = (
					(*(*sz).ism).mass / get_SFE_timescale(*sz) 
				); 
				// enforce_sfr_floor(sz); 
				break; 

			case SFR: 
				sz -> ism -> star_formation_rate = (
					*(*sz).ism).specified[(*sz).timestep + 1l]; 
				double dMg = get_ism_mass_SFRmode(*sz) - (*(*sz).ism).mass; 
				sz -> ism -> infall_rate = (
					(dMg - mass_recycled[i]) / (*sz).dt + 
					(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz) 
				); 
				sz -> ism -> mass += dMg; 
				break; 

			default: 
				free(mass_recycled); 
				return 1; 

		} 

		update_gas_evolution_sanitycheck(sz); 
		sz -> ism -> star_formation_history[(*sz).timestep + 1l] = (
			*(*sz).ism).star_formation_rate; 

	} 

	free(mass_recycled); 
	return 0; 

} 


/* 
 * Determine the mass outflow rate of each element in each zone of a multizone 
 * simulation due solely to entrainment. 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * mass: A 2D-pointer indexable via [zone][element] containing the mass 
 * outflow rate of the given element in Msun / Gyr 
 * 
 * header: ism.h 
 */ 
extern double **multizone_unretained(MULTIZONE mz) {

	unsigned int i, j; 
	double **unretained = (double **) malloc ((*mz.mig).n_zones * sizeof(
		double *)); 
	for (i = 0u; i < (*mz.mig).n_zones; i++) {
		unretained[i] = (double *) malloc ((*mz.zones[0]).n_elements * sizeof(
			double)); 
		for (j = 0u; j < (*mz.zones[0]).n_elements; j++) {
			unretained[i][j] = 0; 
		} 
	} 

	for (i = 0u; i < (*mz.zones[0]).n_elements; i++) {
		double *agb = m_AGB_from_tracers(mz, i); 
		double *sneia = m_sneia_from_tracers(mz, i); 
		for (j = 0u; j < (*mz.mig).n_zones; j++) {
			unretained[j][i] += (
				(1 - (*(*(*mz.zones[j]).elements[i]).agb_grid).entrainment) * 
				agb[j] / (*mz.zones[j]).dt 
			); 
			unretained[j][i] += (
				(1 - (*(*(*mz.zones[j]).elements[i]).ccsne_yields).entrainment) * 
				mdot_ccsne(*mz.zones[j], *(*mz.zones[j]).elements[i]) 
			); 
			unretained[j][i] += (
				(1 - (*(*(*mz.zones[j]).elements[i]).sneia_yields).entrainment) * 
				sneia[j] / (*mz.zones[j]).dt 
			); 
		} 
	} 
	return unretained; 

}


