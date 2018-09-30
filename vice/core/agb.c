
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "specs.h"
#include "stars.h"
#include "enrichment.h"

static double get_AGB_yield(INTEGRATION run, int index, long time_index, 
	double zto);
// static void setup_single_AGB_grid(element *e, double **grid, double *times, 
// 	long num_times);
static int *get_bounds(double *arr, double value, int length);
static double interpolate(double mz1, double mzto, double mz2, double y1, 
	double y2);



extern double m_AGB(INTEGRATION run, MODEL m, int index) {

	if (run.timestep == 0) {
		return 0;
	} else {
		double mass = 0, solar = 0;
		long i;
		int j;
		for (j = 0; j < run.num_elements; j++) {
			solar += run.elements[j].solar;
		}
		for (i = 0l; i < run.timestep; i++) {
			double Z = 0;
			for (j = 0; j < run.num_elements; j++) {
				Z += run.Zall[j][run.timestep - i];
			}
			Z *= m.Z_solar / solar;
			// double y = get_AGB_yield(run, index, i, Z);
			mass += (get_AGB_yield(run, index, i, Z) * 
				run.mdotstar[run.timestep - i] * run.dt * (m.H[i] - 
					m.H[i + 1]));
		}
		return mass;
	}

}

/*
Returns the effective fractional AGB yield of the given element at the 
lookback time time_index timesteps ago.

Args:
=====
run:		The integration struct for the current execution
index:		The index of the element being enriched
time_index:	The number of timesteps ago that the stellar population formed
zto:		The metallicity of the stellar population that formed.
*/
static double get_AGB_yield(INTEGRATION run, int index, long time_index, 
	double zto) {

	int *bounds = get_bounds(run.elements[index].agb_z, zto, 
		run.elements[index].num_agb_z);
	if (bounds[0] == -1) {
		/*
		These lines used to tie the yields down to 0 at z = 0. This is probably 
		a good assumption for s-process elements like strontium, but not for 
		others like carbon, where the yields decrease with increasing 
		metallicity 

		double yield = interpolate(0, zto, 
			run.elements[index].agb_z[bounds[1]], 
			0, run.elements[index].agb_grid[time_index][bounds[1]]);
		free(bound);
		return yield;
		*/

		free(bounds);
		return interpolate(run.elements[index].agb_z[0], zto, 
			run.elements[index].agb_z[1], 
			run.elements[index].agb_grid[time_index][0], 
			run.elements[index].agb_grid[time_index][1]);
	} else {
		if (bounds[1] == run.elements[index].num_agb_z) {
			bounds[0]--;
			bounds[1]--;
		} else {}
		double yield = interpolate(run.elements[index].agb_z[bounds[0]], zto, 
			run.elements[index].agb_z[bounds[1]], 
			run.elements[index].agb_grid[time_index][bounds[0]], 
			run.elements[index].agb_grid[time_index][bounds[1]]
		);
		free(bounds);
		return yield;
	}

}

#if 0
Sets up the AGB yield grids for each element.

Args:
=====
run:		The integration struct for the current execution
grids:		The grids sampled at various inital stellar masses and 
			metallicities
times:		The times that the integration will evaluate at
num_times:	The number of elements in the array times

extern int setup_AGB_grids(integration *run, double ***grids, double *times, 
	long num_times) {

	int i;
	for (i = 0; i < (*run).num_elements; i++) {
		setup_single_AGB_grid(&(*run).elements[i], grids[i], times, num_times);
	}
	return 0;

}
#endif

/*
Sets up the yield grid for a single element.

Args:
=====
e:			A pointer to the element struct to hold the grid
grid:		The grid sampled at various masses and metallicities for this 
			element
times:		The times that the integration will evaluate at
num_times:	The number of elements in the array times.
*/
extern void setup_single_AGB_grid(ELEMENT *e, double **grid, double *times, 
	long num_times) {

	/*
	The grid is composed of an array of yields for each turnoff mass that the 
	integration will see given the times that it will evaluate at. It is then 
	sampled at the metallicities within the grid and interpolated between 
	at each timestep.

	Within each element's grid is a row of yields at the corresponding turn 
	off mass for each metallicity sampled on the grid.
	*/
	long i;
	int j;
	e -> agb_grid = (double **) malloc (num_times * sizeof(double *));
	for (i = 0l; i < num_times; i++) {
		e -> agb_grid[i] = (double *) malloc (e -> num_agb_z * sizeof(double));
		double mto = m_turnoff(times[i]);
		int *bounds = get_bounds(e -> agb_m, mto, e -> num_agb_m);
		for (j = 0; j < (*e).num_agb_z; j++) {
			if (mto > 8) {
				/* Tie it doen to 0 at m > 8 Msun */
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
Returns a pointer to two integers. The first is the index of the number in the 
array that is the largest number smaller than the value. The second is the 
index of the number in the array the is the smaller number larger than the 
value. In other words, they're the bounding indeces that can be used for 
interpolation.

Args:
=====
arr:		The array to find bounding indeces within
value:		The value to find bounding indeces for
length:		The number of elements in the array arr
*/
static int *get_bounds(double *arr, double value, int length) {

	int *indeces = (int *) malloc (2 * sizeof(int));
	if (value < arr[0]) {
		indeces[0] = -1;
		indeces[1] = 0;
		return indeces;
	} else {
		int i;
		for (i = 0; i < length; i++) {
			if (arr[i] >= value) {
				indeces[0] = i - 1;
				indeces[1] = i;
				return indeces;
			} else {
				continue;
			}
		}
		indeces[0] = length - 1;
		indeces[1] = length;
		return indeces;
	}

}

/*
Interpolates between two yields in either mass or metallicity space.

Args:
=====
mz1:		The lower mass/metallicity to interpolate from
mzto:		The mass/metallicity dependent yield being approximated
mz2:		The upper mass/metallicity to interpolate from
y1:			The yield at mz1
y2:			The yield at mz2
*/
static double interpolate(double mz1, double mzto, double mz2, double y1, 
	double y2) {

	return y1 + (y2 - y1) / (mz2 - mz1) * (mzto - mz1);

}

