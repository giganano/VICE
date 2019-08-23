/* 
 * This file implements the functions of element objects. 
 */ 

#include <stdlib.h> 
#include "element.h" 
#include "ccsne.h" 
#include "sneia.h" 
#include "agb.h" 
#include "ssp.h" 
#include "ism.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void update_element_mass_sanitycheck(ELEMENT *e); 

/* 
 * Allocate memory for an return a pointer to an ELEMENT struct. This also 
 * allocates memory for the AGB_YIELD_GRID, CCSNE_YIELD_SPECS, and 
 * SNEIA_YIELD_SPECS stored in the ELEMENT struct. Allocates memory for a 
 * 5-element string for each element's symbol. 
 * 
 * header: element.h 
 */ 
extern ELEMENT *element_initialize(void) {

	ELEMENT *e = (ELEMENT *) malloc (sizeof(ELEMENT)); 
	e -> symbol = (char *) malloc (5 * sizeof(char)); 
	e -> agb_grid = agb_yield_grid_initialize(); 
	e -> ccsne_yields = ccsne_yield_initialize(); 
	e -> sneia_yields = sneia_yield_initialize(); 
	return e; 

} 

/*
 * Free up the memory stored in an ELEMENT struct 
 * 
 * header: element.h 
 */ 
extern void element_free(ELEMENT *e) { 

	if (e != NULL) {

		agb_yield_grid_free(e -> agb_grid); 
		ccsne_yield_free(e -> ccsne_yields); 
		sneia_yield_free(e -> sneia_yields); 

		if ((*e).symbol != NULL) {
			free(e -> symbol); 
			e -> symbol = NULL; 
		} else {} 

		free(e); 
		e = NULL; 

	} else {} 

} 

/* 
 * Allocates memory for bookkeeping each elements previous ISM metallicity 
 * and sets each element to zero. 
 * 
 * Parameters 
 * ========== 
 * e: 				A pointer to the element to setup the Z array for 
 * n_timesteps: 	The number of elements in this array (i.e. the total 
 * 					number of timesteps in the simulation) 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: element.h 
 */ 
extern unsigned short malloc_Z(ELEMENT *e, unsigned long n_timesteps) {

	e -> Z = (double *) malloc (n_timesteps * sizeof(double)); 
	if ((*e).Z == NULL) { 
		return 1; 
	} else { 
		unsigned long i; 
		for (i = 0l; i < n_timesteps; i++) { 
			e -> Z[i] = 0; 
		} 
		return 0; 
	} 

} 

/* 
 * Updates the mass of a single element at the current timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object currently being simulated 
 * e: 		A pointer to the element to update 
 * 
 * header: element.h 
 */ 
extern void update_element_mass(SINGLEZONE sz, ELEMENT *e) {

	e -> mass += mdot_ccsne(sz, *e) * sz.dt; 
	e -> mass += mdot_sneia(sz, *e) * sz.dt; 
	e -> mass += m_AGB(sz, *e); 
	e -> mass += mass_recycled(sz, e); 
	e -> mass -= ((*sz.ism).star_formation_rate * sz.dt * 
		(*e).mass / (*sz.ism).mass); 
	e -> mass -= ((*sz.ism).enh[sz.timestep] * get_outflow_rate(sz) * sz.dt / 
		(*sz.ism).mass * (*e).mass); 
	e -> mass += (*sz.ism).infall_rate * sz.dt * (*e).Zin[sz.timestep]; 
	update_element_mass_sanitycheck(e); 

} 

/* 
 * Updates the mass of each element in each zone to the proper value at the 
 * next timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * header: element.h 
 */ 
extern void update_elements(MULTIZONE *mz) {

	unsigned int i, j; 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		for (j = 0; j < (*(*mz).zones[i]).n_elements; j++) { 
			/* 
			 * Instantaneous pieces that don't require tracer particles: 
			 * 
			 * Enrichment from core collapse supernovae 
			 * depletion from star formation 
			 * depletion from outflows 
			 * metal-rich infall 
			 */ 
			mz -> zones[i] -> elements[j] -> mass += (
				mdot_ccsne((*(*mz).zones[i]), *(*(*mz).zones[i]).elements[j]) * 
				(*(*mz).zones[i]).dt 
			); 
			mz -> zones[i] -> elements[j] -> mass -= (
				(*(*(*mz).zones[i]).ism).star_formation_rate * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).mass / 
				(*(*(*mz).zones[i]).ism).mass 
			); 
			mz -> zones[i] -> elements[j] -> mass -= (
				(*(*(*mz).zones[i]).ism).enh[(*(*mz).zones[i]).timestep] * 
				get_outflow_rate(*(*mz).zones[i]) * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).mass / 
				(*(*(*mz).zones[i]).ism).mass 
			); 
			mz -> zones[i] -> elements[j] -> mass += (
				(*(*(*mz).zones[i]).ism).infall_rate * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).Zin[(*(*mz).zones[i]).timestep]
			); 
		} 
	} 

	/* 
	 * Non-instantaneous pieces that do require tracer particles: 
	 * 
	 * Enrichment from AGB stars 
	 * Enrichment from SNe Ia 
	 * Re-enrichment from recycling 
	 */ 
	agb_from_tracers(mz); 
	sneia_from_tracers(mz); 
	for (i = 0; i < (*(*mz).zones[0]).n_elements; i++) {
		recycle_metals_from_tracers(mz, i); 
	} 

	/* sanity check each element in each zone */ 
	for (i = 0; i < (*(*mz).mig).n_zones; i++) { 
		for (j = 0; j < (*(*mz).zones[i]).n_elements; j++) { 
			update_element_mass_sanitycheck(mz -> zones[i] -> elements[j]); 
		}
	}

}

#if 0
/* 
 * Updates the mass of each element in each zone to the proper value at the 
 * next timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * header: element.h 
 */ 
extern void update_elements(MULTIZONE *mz) {

	unsigned int i, j; 
	for (i = 0; i < (*mz).n_zones; i++) { 
		for (j = 0; j < (*(*mz).zones[i]).n_elements; j++) { 
			/* 
			 * Instantaneous pieces that don't require tracer particles: 
			 * 
			 * Enrichment from core collapse supernovae 
			 * depletion from star formation 
			 * depletion from outflows 
			 * metal-rich infall 
			 */ 
			mz -> zones[i] -> elements[j] -> mass += (
				mdot_ccsne((*(*mz).zones[i]), *(*(*mz).zones[i]).elements[j]) * 
				(*(*mz).zones[i]).dt 
			); 
			mz -> zones[i] -> elements[j] -> mass -= (
				(*(*(*mz).zones[i]).ism).star_formation_rate * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).mass / 
				(*(*(*mz).zones[i]).ism).mass 
			); 
			mz -> zones[i] -> elements[j] -> mass -= (
				(*(*(*mz).zones[i]).ism).enh[(*(*mz).zones[i]).timestep] * 
				get_outflow_rate(*(*mz).zones[i]) * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).mass / 
				(*(*(*mz).zones[i]).ism).mass 
			); 
			mz -> zones[i] -> elements[j] -> mass += (
				(*(*(*mz).zones[i]).ism).infall_rate * 
				(*(*mz).zones[i]).dt * 
				(*(*(*mz).zones[i]).elements[j]).Zin[(*(*mz).zones[i]).timestep]
			); 
		} 
	} 

	/* 
	 * Non-instantaneous pieces that do require tracer particles: 
	 * 
	 * Enrichment from AGB stars 
	 * Enrichment from SNe Ia 
	 * Re-enrichment from recycling 
	 */ 
	agb_from_tracers(mz); 
	sneia_from_tracers(mz); 
	for (i = 0; i < (*(*mz).zones[0]).n_elements; i++) {
		recycle_metals_from_tracers(mz, i); 
	} 

	/* sanity check each element in each zone */ 
	for (i = 0; i < (*mz).n_zones; i++) { 
		for (j = 0; j < (*(*mz).zones[i]).n_elements; j++) { 
			update_element_mass_sanitycheck(mz -> zones[i] -> elements[j]); 
		}
	}

}
#endif 

/* 
 * Performs a sanity check on a given element immediately after it's mass 
 * was updated for the next timestep. 
 * 
 * Parameters 
 * ========== 
 * e: 		A pointer to the element to sanity check 
 */ 
static void update_element_mass_sanitycheck(ELEMENT *e) {

	/* 
	 * Allowing a zero element mass does not produce numerical artifacts in 
	 * the ISM evolution -> just -infs in the associated [X/H] values. 
	 * Moreover, 10^-12 Msun may be quite a bit of mass for some particularly 
	 * heavy elements. Thus a lower bound of a true zero is implemented here. 
	 */ 
	if ((*e).mass < 0) e -> mass = 0; 	

}

