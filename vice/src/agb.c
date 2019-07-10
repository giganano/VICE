/* 
 * This file implements the enrichment of arbitrary elements from asymptotic 
 * giant branch (AGB) stars. 
 */ 

#include <stdlib.h> 
#include "agb.h" 
#include "singlezone.h" 
#include "ssp.h" 
#include "utils.h" 

/* 
 * Allocate memory for and return a pointer to an AGB_YIELD_GRID struct and 
 * initialize all fields to NULL. 
 * 
 * header: agb.h 
 */ 
extern AGB_YIELD_GRID *agb_yield_grid_initialize(void) {

	AGB_YIELD_GRID *agb_grid = (AGB_YIELD_GRID *) malloc (sizeof(
		AGB_YIELD_GRID)); 

	agb_grid -> grid = NULL; 
	agb_grid -> m = NULL; 
	agb_grid -> z = NULL; 

	return agb_grid; 

} 

/* 
 * Free up the memory stored in an AGB_YIELD_GRID struct 
 * 
 * header: agb.h 
 */ 
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) {

	if ((*agb_grid).grid != NULL) free(agb_grid -> grid); 
	if ((*agb_grid).m != NULL) free(agb_grid -> m); 
	if ((*agb_grid).z != NULL) free(agb_grid -> z); 
	free(agb_grid); 

} 

/* 
 * Determine the mass of a given element produced by AGB stars at the current 
 * timestep of a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 			The SINGLEZONE struct associated with the current simulation 
 * e: 			The ELEMENT struct to find the total mass yield for 
 * 
 * Returns 
 * ======= 
 * The mass of the given element in solar masses produced by AGB stars in one 
 * timestep from all previous generations of stars. 
 * 
 * header: agb.h 
 */ 
extern double m_AGB(SINGLEZONE sz, ELEMENT e) {

	if (sz.timestep == 0l) {
		return 0; /* No star's yet */ 
	} else { 
		long i; 
		double mass = 0; 
		for (i = 0l; i <= sz.timestep; i++) { 
			/* The metallicity of the stars that formed i timesteps ago */ 
			double Z = scale_metallicity(sz, sz.timestep - i); 

			/* From section 4.4 of VICE's science documentation */ 
			mass += (
				get_AGB_yield(e, Z, main_sequence_turnoff_mass(i * sz.dt)) * 
				(*sz.ism).star_formation_history[sz.timestep - i] * sz.dt * 
				((*sz.ssp).msmf[i] - (*sz.ssp).msmf[i + 1l])
			); 
			
		} 

		return mass; 
	}

} 

/* 
 * Determine the fractional yield of a given element from AGB stars at a 
 * given mass and metallicity. 
 * 
 * Parameters 
 * ========== 
 * e: 				The element struct containing AGB yield information 
 * Z_stars: 		The metallicity by mass Z of the AGB stars 
 * turnoff_mass:	The mass of the AGB stars 
 * 
 * Returns
 * ======= 
 * The fraction of each AGB star's mass that is converted into the element e 
 * under the current yield settings. 
 * 
 * header: agb.h 
 */ 
extern double get_AGB_yield(ELEMENT e, double Z_stars, double turnoff_mass) {

	if (turnoff_mass < MIN_AGB_MASS || turnoff_mass > MAX_AGB_MASS) { 

		/* 
		 * By default, only stars between 0 and 8 Msun have an AGB phase in 
		 * VICE. Changing these requires altering these #define statements 
		 * in agb.h. 
		 */ 
		return 0; 

	} else { 
		/* bin numbers of turnoff mass and metallicities on the yield grid */ 
		long mass_bin = get_bin_number((*e.agb_grid).m, (*e.agb_grid).n_m - 1l, 
			turnoff_mass); 
		long z_bin = get_bin_number((*e.agb_grid).z, (*e.agb_grid).n_z - 1l, 
			Z_stars); 

		/* Put the masses and metallicities to interpolate from here */ 
		double masses[2]; 
		double metallicities[2]; 
		double yields[2][2]; 

		if (z_bin == -1l) {
			/* Stellar metallicity above or below grid, figure out which */ 
			if (Z_stars > (*e.agb_grid).z[(*e.agb_grid).n_z - 1l]) {
				/* 
				 * Stellar metallicity above the grid -> extrapolate to high 
				 * metallicities using the top two elements of the grid 
				 */ 
				z_bin = (*e.agb_grid).n_z - 2l; 
			} else if (Z_stars < (*e.agb_grid).z[0]) {
				/* 
				 * Stellar metallicity below the grid -> extrapolate to low 
				 * metallicities using the bottom two elements on the grid 
				 */ 
				z_bin = 0l; 
			} else {
				return -1; /* error */ 
			} 
		} else {
			/* Stellar metallicity on the grid, proceed as planned */ 
		} 

		metallicities[0] = (*e.agb_grid).z[z_bin]; 
		metallicities[1] = (*e.agb_grid).z[z_bin + 1l]; 

		if (mass_bin == -1l) {
			/* Turnoff mass above or below grid, figure out which */ 
			if (turnoff_mass > (*e.agb_grid).m[(*e.agb_grid).n_m - 1l]) {
				/* 
				 * Turnoff mass above the grid -> extrapolate to higher masses, 
				 * tying the yield down to 0 at 8 Msun 
				 */ 
				masses[0] = (*e.agb_grid).m[(*e.agb_grid).n_m - 1l]; 
				masses[1] = MAX_AGB_MASS; 
				yields[0][0] = (*e.agb_grid).grid[(*e.agb_grid).n_m - 1l][z_bin]; 
				yields[0][1] = (*e.agb_grid).grid[(
					*e.agb_grid).n_m - 1l][z_bin + 1l]; 
				yields[1][0] = 0; 
				yields[1][1] = 0; 
			} else if (turnoff_mass < (*e.agb_grid).m[0]) {
				/* 
				 * Turnoff mass below the grid -> extrapolate to lower masses, 
				 * tying the yield down to 0 at 0 Msun 
				 */ 
				masses[0] = MIN_AGB_MASS; 
				masses[1] = (*e.agb_grid).m[0]; 
				yields[0][0] = 0; 
				yields[0][1] = 0; 
				yields[1][0] = (*e.agb_grid).grid[0][z_bin]; 
				yields[1][1] = (*e.agb_grid).grid[0][z_bin + 1l]; 
			} else {
				return -1; /* error */ 
			} 
		} else {
			/* Turnoff mass on the grid, proceed as planned */ 
			masses[0] = (*e.agb_grid).m[mass_bin]; 
			masses[1] = (*e.agb_grid).m[mass_bin + 1l]; 
			yields[0][0] = (*e.agb_grid).grid[mass_bin][z_bin]; 
			yields[0][1] = (*e.agb_grid).grid[mass_bin][z_bin + 1l]; 
			yields[1][0] = (*e.agb_grid).grid[mass_bin + 1l][z_bin]; 
			yields[1][1] = (*e.agb_grid).grid[mass_bin + 1l][z_bin + 1l]; 
		}

		return interpolate2D(
			masses, 
			metallicities, 
			yields, 
			turnoff_mass, 
			Z_stars); 
	}

}



