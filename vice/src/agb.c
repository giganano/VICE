/* 
 * This file implements the enrichment of arbitrary elements from asymptotic 
 * giant branch (AGB) stars. 
 */ 

#include <stdlib.h> 
#include "agb.h" 
#include "singlezone.h" 
#include "tracer.h" 
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
	agb_grid -> entrainment = 1; 

	return agb_grid; 

} 

/* 
 * Free up the memory stored in an AGB_YIELD_GRID struct 
 * 
 * header: agb.h 
 */ 
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) { 

	if (agb_grid != NULL) {

		if ((*agb_grid).grid != NULL) {
			free(agb_grid -> grid); 
			agb_grid -> grid = NULL; 
		} else {} 

		if ((*agb_grid).m != NULL) {
			free(agb_grid -> m); 
			agb_grid -> m = NULL; 
		} else {} 

		if ((*agb_grid).z != NULL) {
			free(agb_grid -> z); 
			agb_grid -> z = NULL; 
		} else {} 

		free(agb_grid); 
		agb_grid = NULL; 

	} else {} 

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
		unsigned long i; 
		double mass = 0; 
		for (i = 0l; i <= sz.timestep; i++) { 
			/* The metallicity of the stars that formed i timesteps ago */ 
			double Z = scale_metallicity(sz, sz.timestep - i); 

			/* From section 4.4 of VICE's science documentation */ 
			mass += (
				get_AGB_yield(e, Z, 
					main_sequence_turnoff_mass(i * sz.dt, (*sz.ssp).postMS)) * 
				(*sz.ism).star_formation_history[sz.timestep - i] * sz.dt * 
				((*sz.ssp).msmf[i] - (*sz.ssp).msmf[i + 1l])
			); 
			
		} 

		// return (*e.agb_grid).entrainment * mass; 
		return mass; 
	}

} 

#if 0
/* 
 * Enrich each element in each zone according to the AGB stars associated with 
 * tracer particles. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * header: agb.h 
 */ 
extern void agb_from_tracers(MULTIZONE *mz) {

	unsigned long i, timestep = (*(*mz).zones[0]).timestep; 
	for (i = 0l; i < (*(*mz).mig).tracer_count; i++) {
		/* 
		 * Get the tracer particle's current zone and metallicity. Use the SSP 
		 * evolutionary parameters from the zone in which the tracer particle 
		 * was born. 
		 */ 
		TRACER *t = mz -> mig -> tracers[i]; 
		SINGLEZONE *sz = mz -> zones[(*t).zone_current]; 
		SSP *ssp = mz -> zones[(*t).zone_origin] -> ssp; 
		double Z = tracer_metallicity(*mz, *t); 
		unsigned int j; 
		for (j = 0; j < (*sz).n_elements; j++) { 
			/* 
			 * n: The number of timesteps ago the tracer particle formed. This 
			 * times the timestep size is the age of the tracer particle in 
			 * Gyr. 
			 */ 
			unsigned long n = timestep - (*t).timestep_origin; 
			ELEMENT *e = sz -> elements[j]; 
			// e -> mass += (*(*e).agb_grid).entrainment * (
			e -> mass += (
				get_AGB_yield( *(*(*mz).zones[(*t).zone_origin]).elements[j], 
				Z, main_sequence_turnoff_mass(n * (*sz).dt, (*ssp).postMS) ) * 
				(*t).mass * 
				((*ssp).msmf[n] - (*ssp).msmf[n + 1l]) 
			); 
		}
	}

} 
#endif 

/* 
 * Determine the mass of a given element produced by AGB stars in each 
 * zone. 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object for the current simulation 
 * index: 		The index of the element to determine the mass production for 
 * 
 * Returns 
 * ======= 
 * The mass of the given element produced in each zone in the next timestep by 
 * AGB stars. 
 * 
 * header: agb.h 
 */ 
extern double *m_AGB_from_tracers(MULTIZONE mz, unsigned short index) {

	unsigned long i, timestep = (*mz.zones[0]).timestep; 
	double *mass = (double *) malloc ((*mz.mig).n_zones * sizeof(double)); 
	for (i = 0l; i < (*mz.mig).n_zones; i++) {
		mass[i] = 0; 
	}
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		/* 
		 * Get the tracer particle's current zone and metallicity. Use the SSP 
		 * evolutionary parameters from the zone in which the tracer particle 
		 * was born. 
		 * 
		 * n: The number of timesteps ago the tracer particle formed. 
		 */ 
		TRACER *t = mz.mig -> tracers[i]; 
		SINGLEZONE *sz = mz.zones[(*t).zone_current]; 
		SSP *ssp = mz.zones[(*t).zone_origin] -> ssp; 
		double Z = tracer_metallicity(mz, *t); 
		unsigned long n = timestep - (*t).timestep_origin; 
		mass[(*t).zone_current] += (
			get_AGB_yield( *(*mz.zones[(*t).zone_origin]).elements[index], 
				Z, main_sequence_turnoff_mass(n * (*sz).dt, (*ssp).postMS) ) * 
			(*t).mass * 
			((*ssp).msmf[n] - (*ssp).msmf[n + 1l]) 
		); 
	} 
	return mass; 

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
		long mass_bin = get_bin_number((*e.agb_grid).m, 
			(*e.agb_grid).n_m - 1l, turnoff_mass); 
		long z_bin = get_bin_number((*e.agb_grid).z, 
			(*e.agb_grid).n_z - 1l, Z_stars); 

		/* Put the masses and metallicities to interpolate from here */ 
		double masses[2]; 
		double metallicities[2]; 
		double yields[2][2]; 

		switch (z_bin) { 

			case -1l: 
				/* Stellar metallicity above/below grid, figure out which */ 
				if (Z_stars > (*e.agb_grid).z[(*e.agb_grid).n_z - 1l]) {
					/* 
					 * Stellar metallicity above the grid -> extrapolate to 
					 * high metallicities using the top two elements of the 
					 * grid 
					 */ 
					z_bin = (signed) (*e.agb_grid).n_z - 2l; 
					break; 
				} else if (Z_stars < (*e.agb_grid).z[0]) {
					/* 
					 * Stellar metallicity below the grid -> extrapolate to low 
					 * metallicities using the bottom two elements on the grid 
					 */ 
					z_bin = 0l; 
					break; 
				} else {
					return -1; /* error */ 
				} 

			default: 
				/* Stellar metallicity is on the grid, proceed as planned */ 
				break; 

		} 

		metallicities[0] = (*e.agb_grid).z[z_bin]; 
		metallicities[1] = (*e.agb_grid).z[z_bin + 1l]; 

		switch (mass_bin) {

			case -1l: 
				/* Turnoff mass above or below grid, figure out which */ 
				if (turnoff_mass > (*e.agb_grid).m[(*e.agb_grid).n_m - 1l]) {
					/* 
					 * Turnoff mass above the grid -> extrapolate to higher 
					 * masses, tying the yield down to 0 at 8 Msun 
					 */ 
					masses[0] = (*e.agb_grid).m[(*e.agb_grid).n_m - 1l]; 
					masses[1] = MAX_AGB_MASS; 
					yields[0][0] = (*e.agb_grid).grid[(
						*e.agb_grid).n_m - 1l][z_bin]; 
					yields[0][1] = (*e.agb_grid).grid[(
						*e.agb_grid).n_m - 1l][z_bin + 1l]; 
					yields[1][0] = 0; 
					yields[1][1] = 0; 
					break; 
				} else if (turnoff_mass < (*e.agb_grid).m[0]) {
					/* 
					 * Turnoff mass below the grid -> extrapolate to lower 
					 * masses, tying the yield down to 0 at 0 Msun 
					 */ 
					masses[0] = MIN_AGB_MASS; 
					masses[1] = (*e.agb_grid).m[0]; 
					yields[0][0] = 0; 
					yields[0][1] = 0; 
					yields[1][0] = (*e.agb_grid).grid[0][z_bin]; 
					yields[1][1] = (*e.agb_grid).grid[0][z_bin + 1l]; 
					break; 
				} else {
					return -1; /* error */ 
				} 

			default: 
				/* Turnoff mass on the grid, proceed as planned */ 
				masses[0] = (*e.agb_grid).m[mass_bin]; 
				masses[1] = (*e.agb_grid).m[mass_bin + 1l]; 
				yields[0][0] = (*e.agb_grid).grid[mass_bin][z_bin]; 
				yields[0][1] = (*e.agb_grid).grid[mass_bin][z_bin + 1l]; 
				yields[1][0] = (*e.agb_grid).grid[mass_bin + 1l][z_bin]; 
				yields[1][1] = (*e.agb_grid).grid[mass_bin + 1l][z_bin + 1l]; 
				break; 
		} 

		return interpolate2D(
			masses, 
			metallicities, 
			yields, 
			turnoff_mass, 
			Z_stars); 
		
	}

}

