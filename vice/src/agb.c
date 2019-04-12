/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script handles the numerical implementation of enrichment by asymptotic 
 * giant branch stars. 
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "specs.h"
#include "stars.h"
#include "enrichment.h"

/* ---------- static function comment headers not duplicated here ---------- */
static int *get_bounds(double *arr, double value, int length);
static double interpolate(double mz1, double mzto, double mz2, double y1, 
	double y2);

/* 
 * Returns the mass of a given element produced by AGB stars at the current 
 * timestep. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for this simulation
 * m:			The MODEL struct for this simulation
 * index:		The index of the element being tracked 
 * 
 * header: enrichment.h 
 */
extern double m_AGB(INTEGRATION run, MODEL m, int index) {

	if (run.timestep == 0) {
		return 0; 		// Not enough time has passed for AGB stars yet 
	} else {
		double mass = 0; 		// mass of the element in Msun 
		double solar = 0;		// Solar metallicity
		long i;
		int j;
		for (j = 0; j < run.num_elements; j++) {
			/* 
			 * Determine the solar abundance given only the elements tracked 
			 * by this simulation. 
			 */
			solar += run.elements[j].solar; 
		}
		/* Previous timesteps <---> Previous generations of stars */ 
		for (i = 0l; i < run.timestep; i++) {
			double Z = 0; 		// The abundance of tracked elements 
			for (j = 0; j < run.num_elements; j++) {
				Z += run.Zall[j][run.timestep - i];
			}
			/* Scale it off the solar abundance of tracked elements */ 
			Z *= m.Z_solar / solar; 

			/*
			 * AGB stars enrich the ISM at a time t with mass dm of a given 
			 * element according to a yield y as a function of turnoff mass 
			 * and metallicity. The prefactor is set by the hydrogen burning 
			 * mass fraction h (see documentation). 
			 * 
			 * dm = y(M,Z) * mstar * dh
			 */
			mass += (get_AGB_yield(run.elements[index], i, Z) * 
				run.mdotstar[run.timestep - i] * run.dt * (m.H[i] - 
					m.H[i + 1l]));
		}
		return mass;
	}

}

/*
 * Returns the effective fractional AGB yield of the given element at the 
 * lookback time time_index timesteps ago. 
 * 
 * Args:
 * =====
 * e:				The element whose yield is to be determined
 * time_index:		The number of timesteps ago that the stellar population 
 * 					formed
 * zto:				The metallicity of the stellar population that formed
 * 
 * header: enrichment.h 
 */
extern double get_AGB_yield(ELEMENT e, long time_index, double zto) {

	/* Get the indeces of the adjacent elements of the metallicity grid. */
	int *bounds = get_bounds(e.agb_z, zto, e.num_agb_z);
	if (bounds[0] == -1) {
		/*
		 * These lines used to tie the yields down to 0 at z = 0. This is probably 
		 * a good assumption for s-process elements like strontium, but not for 
		 * others like carbon, where the yields decrease with increasing 
		 * metallicity. 
		 * 
		 * It is also not unphysical to expect negative yields of a given 
		 * element. This simply means that the evolution of the star resulted in a 
		 * net consumption of the element in the production of yet heavier 
		 * elements. For example, the Cristallo et al. (2011) yields predict 
		 * negative yields of Carbon for more massive AGB stars at solar 
		 * metallicity. 
		 * 
		 * double yield = interpolate(0, zto, 
		 * 	e.agb_z[bounds[1]], 
		 * 	0, e.agb_grid[time_index][bounds[1]]);
		 * free(bounds);
		 * return yield;
		 */
		free(bounds);
		/* Extrapolate from the lowest metallicity elements of the grid */ 
		return interpolate(e.agb_z[0], zto, e.agb_z[1], 
			e.agb_grid[time_index][0], e.agb_grid[time_index][1]);
	} else {
		/* If the metallicity is above the grid, extrapolate from there too */ 
		if (bounds[1] == e.num_agb_z) {
			bounds[0]--;
			bounds[1]--;
		} else {}
		/* Otherwise interpolate normally */ 
		double yield = interpolate(e.agb_z[bounds[0]], zto, e.agb_z[bounds[1]], 
			e.agb_grid[time_index][bounds[0]], 
			e.agb_grid[time_index][bounds[1]]
		);
		free(bounds);
		return yield;
	}

}

/*
 * Sets up the yield grid for a single element.
 * 
 * Args:
 * =====
 * e:			A pointer to the element struct to hold the grid
 * grid:		The grid sampled at various masses and metallicities for this 
 * 				element
 * times:		The times that the integration will evaluate at
 * num_times:	The number of elements in the array times.
 * 
 * header: enrichment.h 
 */
extern void setup_single_AGB_grid(ELEMENT *e, double **grid, double *times, 
	long num_times) {

	/*
	 * The yields are sampled on mass-metallicity grids. At a given 
	 * metallicity, the yields are a function of turnoff mass, which is to say 
	 * that they are a function of time. Before the integration even begins, 
	 * VICE maps the yields from a single stellar population at the sampled 
	 * metallicities across all of the times that it will evaluate at by 
	 * interpolating linearly between the yields. 
	 * 
	 * At each timestep in the simulation, the yield is determined via 
	 * linear interpolation between the sampled yields at the adjacent 
	 * metallicities, the same process applied to the masses of the stars. 
	 */
	long i;
	int j;
	/* Re-initialize the grid */ 
	// printf("a\n");
	e -> agb_grid = (double **) malloc (num_times * sizeof(double *));
	for (i = 0l; i < num_times; i++) {
		// printf("%ld\n", i);
		/* The first dimension of the array will be the time_index */ 
		e -> agb_grid[i] = (double *) malloc (e -> num_agb_z * sizeof(double));
		double mto = m_turnoff(times[i]);
		int *bounds = get_bounds(e -> agb_m, mto, e -> num_agb_m);
		/* 
		 * At each turnoff mass, do the interpolation for each metallicity 
		 * on the grid. 
		 */ 
		for (j = 0; j < (*e).num_agb_z; j++) {
			// printf("%d\n", j);
			if (mto > 8) {
				/* Tie it down to 0 at m > 8 Msun */
				e -> agb_grid[i][j] = 0;
			} else if (bounds[0] == -1) {
				/* Tie it down to y = 0 at m = 0 */
				e -> agb_grid[i][j] = interpolate(0, mto, e -> agb_m[0], 
					0, grid[0][j]);
			} else if (bounds[1] == (*e).num_agb_m) {
				/* Tie it down to y = 0 at 8 Msun */
				e -> agb_grid[i][j] = interpolate((*e).agb_m[bounds[0]], mto, 
					8, grid[bounds[0]][j], 0);
			} else {
				/* Interpolate normally otherwise */ 
				e -> agb_grid[i][j] = interpolate(e -> agb_m[bounds[0]], mto, 
					e -> agb_m[bounds[1]], grid[bounds[0]][j], 
					grid[bounds[1]][j]);
			}
		}
		free(bounds);
	}

}

/*
 * Returns a pointer to two integers. The first is the index of the number in the 
 * array that is the largest number smaller than the value. The second is the 
 * index of the number in the array the is the smaller number larger than the 
 * value. In other words, they're the bounding indeces that can be used for 
 * interpolation. 
 * 
 * This function assumes that the array arr is organized from least to 
 * greatest. This will always be true by how VICE is written.  
 * 
 * Args:
 * =====
 * arr:		The array to find bounding indeces within
 * value:		The value to find bounding indeces for
 * length:		The number of elements in the array arr
 */
static int *get_bounds(double *arr, double value, int length) {

	/* Allocate memory to be returned */ 
	int *indeces = (int *) malloc (2 * sizeof(int));

	if (value < arr[0]) { 		// If the value is below the grid 
		indeces[0] = -1;
		indeces[1] = 0;
		return indeces;
	} else {
		int i;
		for (i = 0; i < length; i++) { 
			if (arr[i] >= value) { 			// If it is on the grid 
				indeces[0] = i - 1;
				indeces[1] = i;
				return indeces;
			} else {
				continue;
			}
		}
		/* If the code gets here, the value is above the grid */ 
		indeces[0] = length - 1;
		indeces[1] = length;
		return indeces;
	}

}

/*
 * Interpolates between two yields in either mass or metallicity space. This is 
 * the basic interpolation function in one dimension. 
 * 
 * Args:
 * =====
 * mz1:		The lower mass/metallicity to interpolate from
 * mzto:		The mass/metallicity dependent yield being approximated
 * mz2:		The upper mass/metallicity to interpolate from
 * y1:			The yield at mz1
 * y2:			The yield at mz2
 */
static double interpolate(double mz1, double mzto, double mz2, double y1, 
	double y2) {

	return y1 + (y2 - y1) / (mz2 - mz1) * (mzto - mz1);

}





