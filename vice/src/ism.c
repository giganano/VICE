
#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "ism.h" 
#include "ssp.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void update_gas_evolution_sanitycheck(SINGLEZONE *sz); 
static double get_SFE_timescale(SINGLEZONE sz); 
static double get_ism_mass_SFRmode(SINGLEZONE sz); 

/* 
 * Allocate memory for and return a pointer to an ISM struct. Automatically 
 * initializes all fields to NULL. Allocates memory for a 5-element char * 
 * mode specifier. 
 * 
 * header: ism.h 
 */ 
extern ISM *ism_initialize(void) {

	ISM *ism = (ISM *) malloc (sizeof(ISM)); 
	ism -> mode = (char *) malloc (5 * sizeof(char)); 
	ism -> specified = NULL; 
	ism -> star_formation_history = NULL; 
	ism -> eta = NULL; 
	ism -> enh = NULL; 
	ism -> tau_star = NULL; 
	return ism; 

} 

/* 
 * Free up the memory stored in an ISM struct. 
 * 
 * header: ism.h 
 */ 
extern void ism_free(ISM *ism) {

	if ((*ism).specified != NULL) free(ism -> specified); 
	if ((*ism).star_formation_history != NULL) free(
		ism -> star_formation_history); 
	if ((*ism).eta != NULL) free(ism -> eta); 
	if ((*ism).enh != NULL) free(ism -> enh); 
	if ((*ism).tau_star != NULL) free(ism -> tau_star); 
	free(ism -> mode); 
	free(ism); 

} 

/* 
 * Initialize the ISM mass, star formation rate, and infall rate in 
 * preparation of a singlezone simulation 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to setup the evolution for 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on an unrecognized mode 
 * 
 * header: ism.h 
 */ 
extern int setup_gas_evolution(SINGLEZONE *sz) {

	/* SFR = MG * tau_star^-1 */ 
	if (!strcmp((*(*sz).ism).mode, "gas")) { 
		/* 
		 * Set initial mass and star formation rate. If we only know the 
		 * initial mass, there's no way to define an infall rate at t = 0. 
		 */ 
		sz -> ism -> mass = (*(*sz).ism).specified[0]; 
		sz -> ism -> star_formation_rate = ((*(*sz).ism).mass / 
			get_SFE_timescale(*sz)); 
		sz -> ism -> infall_rate = NAN; /* lower bound at 10^-12 */  
	} else if (!strcmp((*(*sz).ism).mode, "ifr")) {
		/* initial gas supply set by python in this case */ 
		sz -> ism -> infall_rate = (*(*sz).ism).specified[0]; 
		sz -> ism -> star_formation_rate = ((*(*sz).ism).mass / 
			get_SFE_timescale(*sz)); 
	} else if (!strcmp((*(*sz).ism).mode, "sfr")) { 
		sz -> ism -> star_formation_rate = (*(*sz).ism).specified[0]; 
		sz -> ism -> mass = get_ism_mass_SFRmode(*sz); 
		sz -> ism -> infall_rate = NAN; 
	} else {
		return 1; 		/* unrecognized mode */ 
	} 

	/* Run the sanity checks to impose the lower bound */ 
	update_gas_evolution_sanitycheck(sz); 

	/* Allocate memory for the star formation history at each timestep */ 
	sz -> ism -> star_formation_history = (double *) malloc (
		((long) ((*sz).output_times[(*sz).n_outputs - 1l] / (*sz).dt) + 10l) * 
		sizeof(double)); 
	sz -> ism -> star_formation_history[0l] = (*(*sz).ism).star_formation_rate; 
	return 0; 

} 

/* 
 * Moves the infall rate, total gas mass, and star formation rate in a 
 * singlezone simulation forward one timestep 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on an unrecognized mode 
 * 
 * header: ism.h 
 */ 
extern int update_gas_evolution(SINGLEZONE *sz) {

	/* 
	 * The relation between star formation rate, infall rate, gas supply, 
	 * timestep size, outflow rate, recycling rate, and star formation 
	 * efficiency timescale: 
	 * 
	 * SFR = MG * tau_star^-1 
	 * 
	 * dMG = (IFR - SFR - OFR) * dt + M_recycled 
	 */ 

	if (!strcmp((*(*sz).ism).mode, "gas")) {
		sz -> ism -> mass = (*(*sz).ism).specified[(*sz).timestep + 1l]; 
		sz -> ism -> star_formation_rate = ((*(*sz).ism).mass / 
			get_SFE_timescale(*sz)); 
		sz -> ism -> infall_rate = (
			((*(*sz).ism).mass - (*(*sz).ism).specified[(*sz).timestep] - 
				mass_recycled(*sz, NULL)) / (*sz).dt + 
			(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz)
		); 
	} else if (!strcmp((*(*sz).ism).mode, "ifr")) {
		sz -> ism -> mass += (
			((*(*sz).ism).infall_rate - (*(*sz).ism).star_formation_rate - 
				get_outflow_rate(*sz)) * (*sz).dt + mass_recycled(*sz, NULL)
		); 
		sz -> ism -> infall_rate = (*(*sz).ism).specified[(*sz).timestep + 1l]; 
		sz -> ism -> star_formation_rate = ((*(*sz).ism).mass / 
			get_SFE_timescale(*sz)); 
	} else if (!strcmp((*(*sz).ism).mode, "sfr")) {
		sz -> ism -> star_formation_rate = (
			*(*sz).ism).specified[(*sz).timestep + 1l];  
		double dMg = get_ism_mass_SFRmode(*sz) - (*(*sz).ism).mass; 
		sz -> ism -> infall_rate = (
			(dMg - mass_recycled(*sz, NULL)) / (*sz).dt + 
			(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz)
		); 
		sz -> ism -> mass += dMg; 
	}

	update_gas_evolution_sanitycheck(sz); 
	sz -> ism -> star_formation_history[(*sz).timestep + 1l] = (
		*(*sz).ism).star_formation_rate; 
	return 0; 

} 

/* 
 * Determine the star formation efficiency timescale at the NEXT timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The timescale relating star formation rate and gas supply in Gyr at the 
 * next timestep. 
 */ 
static double get_SFE_timescale(SINGLEZONE sz) {

	if ((*sz.ism).schmidt) { 
		/* Single-zone implementation of Kennicutt-Schmidt Law */ 
		return ((*sz.ism).tau_star[sz.timestep + 1l] * pow((*sz.ism).mass / 
			(*sz.ism).mgschmidt, -(*sz.ism).schmidt_index)); 
	} else { 
		/* Instantaneous star formation efficiency */ 
		return (*sz.ism).tau_star[sz.timestep + 1l]; 
	}

} 

/* 
 * Determines the mass of the ISM at the NEXT timestep when the simulation is 
 * ran in SFR mode. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The mass of the ISM at the next timestep 
 */ 
static double get_ism_mass_SFRmode(SINGLEZONE sz) { 

	/* 
	 * The following are the analytically determined solutions for the gas 
	 * supply under the equations in section 3.1 of VICE's science 
	 * documentation. Special consideration must be taken aside from a simple 
	 * SFR x get_SFE_timescale approach because this introduces numerical 
	 * artifacts when the star formation rate is low. 
	 */ 

	if ((*sz.ism).schmidt) { 
		return pow( 
			(*sz.ism).star_formation_rate * 
			(*sz.ism).tau_star[sz.timestep + 1l] * 
			pow((*sz.ism).mgschmidt, (*sz.ism).schmidt_index), 
			1 / (1 + (*sz.ism).schmidt_index)); 
	} else {
		return ((*sz.ism).star_formation_rate * 
			(*sz.ism).tau_star[sz.timestep + 1l]); 
	}

}

/* 
 * Performs a sanity check on the ISM parameters immediately after they 
 * were updated one timestep in a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to sanity check 
 */ 
static void update_gas_evolution_sanitycheck(SINGLEZONE *sz) {

	/* 
	 * All three of the ISM mass, the star formation rate, and infall rate 
	 * are forced to be positive definite by imposing a lower bound at 
	 * 10^-12 in the adopted unit system. This avoids unphysical parameter 
	 * spaces and numerical artifacts at zero. 
	 */ 
	if ((*(*sz).ism).mass < 1e-12) { 
		sz -> ism -> mass = 1e-12; 
	} else {} 
	if ((*(*sz).ism).star_formation_rate < 1e-12) { 
		sz -> ism -> star_formation_rate = 1e-12;  
	} else {} 
	if ((*(*sz).ism).infall_rate < 1e-12) {
		sz -> ism -> infall_rate = 1e-12; 
	} else {} 


}

/* 
 * Determine the ISM mass outflow rate in a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * The mass outflow rate in Msun/Gyr 
 * 
 * header: ism.h 
 */ 
extern double get_outflow_rate(SINGLEZONE sz) {

	if ((*sz.ism).smoothing_time < sz.dt) {
		/* 
		 * If the smoothing time is less than the timestep, there's no 
		 * timesteps to smooth over. 
		 * 
		 * outflow_rate = eta * smoothed star formation rate 
		 */ 
		return (*sz.ism).eta[sz.timestep] * (*sz.ism).star_formation_rate; 
	} else {
		/* The number of timesteps to smooth over */ 
		long i, n = (long) ((*sz.ism).smoothing_time / sz.dt); 
		double mean_sfr = 0; 
		if (n > sz.timestep) {
			/* If the simulation hasn't reached this many timesteps yet. 
			 * 
			 * In either case, simply add up the previous star formation rates 
			 * and divide by the number of timesteps. 
			 */ 
			for (i = 0l; i <= sz.timestep; i++) {
				mean_sfr += (*sz.ism).star_formation_history[sz.timestep - i]; 
			} 
			mean_sfr /= sz.timestep + 1l; 
		} else {
			for (i = 0l; i <= n; i++) {
				mean_sfr += (*sz.ism).star_formation_history[sz.timestep - i]; 
			} 
			mean_sfr /= n + 1l; 
		} 
		return (*sz.ism).eta[sz.timestep] * mean_sfr; 
	}

} 

