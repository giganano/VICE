/* 
 * This file implements the evolution of element objects in VICE's singlezone 
 * simulations. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "../singlezone.h" 
#include "../ssp.h" 
#include "../element.h" 
#include "element.h" 


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

	e -> mass += (*(*e).ccsne_yields).entrainment * mdot_ccsne(sz, *e) * sz.dt; 
	e -> mass += (*(*e).sneia_yields).entrainment * mdot_sneia(sz, *e) * sz.dt; 
	e -> mass += (*(*e).agb_grid).entrainment * m_AGB(sz, *e); 
	e -> mass += mass_recycled(sz, e); 
	e -> mass -= ((*sz.ism).star_formation_rate * sz.dt * 
		(*e).mass / (*sz.ism).mass); 
	/* don't eject helium at an enhanced metallicity */ 
	if (strcmp((*e).symbol, "he")) {
		e -> mass -= ((*sz.ism).enh[sz.timestep] * get_outflow_rate(sz) * 
			sz.dt / (*sz.ism).mass * (*e).mass); 
	} else {
		e -> mass -= get_outflow_rate(sz) * sz.dt / (*sz.ism).mass * (*e).mass; 
	} 
	e -> mass += (*sz.ism).infall_rate * sz.dt * (*e).Zin[sz.timestep]; 
	update_element_mass_sanitycheck(e); 

} 


/* 
 * Performs a sanity check on a given element immediately after it's mass 
 * was updated for the next timestep. 
 * 
 * Parameters 
 * ========== 
 * e: 		A pointer to the element to sanity check 
 * 
 * header: element.h 
 */ 
extern void update_element_mass_sanitycheck(ELEMENT *e) {

	/* 
	 * Allowing a zero element mass does not produce numerical artifacts in 
	 * the ISM evolution -> just -infs in the associated [X/H] values. 
	 * Moreover, 10^-12 Msun may be quite a bit of mass for some particularly 
	 * heavy elements. Thus a lower bound of a true zero is implemented here. 
	 */ 
	if ((*e).mass < 0) e -> mass = 0; 	

} 

/* 
 * Determine the [X/H] value for a given element in a zone. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object to pull the ISM mass from 
 * e: 		The element to find the [X/H] value for 
 * 
 * Returns 
 * ======= 
 * [X/H] = log10( mass(element) / mass(ISM) / solar ) 
 * 
 * header: element.h 
 */ 
extern double onH(SINGLEZONE sz, ELEMENT e) {

	/* 
	 * Take into account the intrinsic mathematical domain of the log function 
	 * to prevent floating point errors 
	 */ 
	if ((*sz.ism).mass) { 
		return log10( (e.mass / (*sz.ism).mass) / e.solar ); 
	} else { 
		return -INFINITY; 
	} 

}

