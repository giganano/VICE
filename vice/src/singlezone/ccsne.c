/* 
 * This file implements the enrichment of arbitrary elements from core 
 * collapse supernovae (CCNSe) in VICE's singlezone simulations. 
 */ 

#include <stdlib.h> 
#include "../singlezone.h" 
#include "../ccsne.h" 
#include "../utils.h" 
#include "ccsne.h" 

/* 
 * Determine the rate of mass enrichment of an element X from core-collapse 
 * supernovae at the current timestep. This is implemented acording to the 
 * following formulation (see section 4.2 of VICE's science documentation): 
 * 
 * Mdot_x_CC = y_x_CC * SFR 
 * 
 * Parameters 
 * ========== 
 * sz: 			The SINGLEZONE object for the current integration 
 * e: 			The ELEMENT struct corresponding to the element to find the 
 * 				mass enrichment rate for  
 * 
 * Returns 
 * ======= 
 * The rate of mass enrichment in Msun/Gyr. 
 * 
 * header: ccsne.h 
 */ 
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e) {
	
	// return (*e.ccsne_yields).entrainment * (
	return (get_cc_yield(e, scale_metallicity(sz, sz.timestep)) * 
		(*sz.ism).star_formation_rate); 

}


/* 
 * Obtain the IMF-integrated fractional mass yield of a given element from its 
 * internal yield table.  
 * 
 * Parameters 
 * ========== 
 * e: 				The element to find the yield for 
 * Z: 				The metallicity to look up on the grid 
 * 
 * Returns 
 * ======= 
 * The interpolated yield off of the stored yield grid within the ELEMENT 
 * struct. 
 * 
 * header: ccsne.h 
 */ 
extern double get_cc_yield(ELEMENT e, double Z) { 

	long lower_bound_idx; 
	if (Z < CC_YIELD_GRID_MIN) {
		/* 
		 * Metallicity below the yield grid. Unless the user changes 
		 * CC_YIELD_GRID_MIN in ccsne.h to something other than zero, this 
		 * would be unphysical. Included as a failsafe for users modifying 
		 * VICE. Interpolate off bottom two elements of yield grid. 
		 */ 
		lower_bound_idx = 0l; 
	} else if (CC_YIELD_GRID_MIN <= Z && Z <= CC_YIELD_GRID_MAX) { 
		/* 
		 * Metallicity on the grid. This will always be true for simulations 
		 * even remotely realistic without modified grid parameters. 
		 * Interpolate off neighboring elements of yield grid. 
		 */ 
		lower_bound_idx = (long) ((Z - CC_YIELD_GRID_MIN) / CC_YIELD_STEP); 
	} else { 
		/* 
		 * Metallicity above the grid. Without modified grid parameters, this 
		 * is unrealistically high, but included as a failsafe against 
		 * segmentation faults. Interpolate off top two elements of yield 
		 * grid. 
		 */ 
		lower_bound_idx = (long) ((CC_YIELD_GRID_MAX - CC_YIELD_GRID_MIN) / 
			CC_YIELD_STEP) - 1l; 
	} 

	return interpolate(
		lower_bound_idx * CC_YIELD_STEP, 
		lower_bound_idx * CC_YIELD_STEP + CC_YIELD_STEP, 
		(*e.ccsne_yields).yield_[lower_bound_idx], 
		(*e.ccsne_yields).yield_[lower_bound_idx + 1l], 
		Z
	); 

} 

