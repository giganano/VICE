/*
 * This header contains extern declarations for functions which run the 
 * integrations as well as model type Ia supernovae, core collapse supernovae, 
 * and AGB star enrichment channels. 
 */

#ifndef ENRICHMENT_H
#define ENRICHMENT_H


/* ------------------ EVOLUATIONARY FUNCTIONS -------------------- */

/*
 * This acts as the main method as far as the wrapper is concerned. When this 
 * function is called, it runs the integrator on all of the parameters inside 
 * the structs. This is the function that runs the time-evolution of GCE. 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for this iteration of the code
 * m:				The MODEL struct for this iteration of the code
 * name:			The name of this INTEGRATION
 * times:			The times at which this INTEGRATION will evaluate
 * num_times:		The number of elements in the times array
 * outtimes:		The array of output times 
 * 
 * source: metals.c 
 */
extern int enrich(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times, double *outtimes, double end);

/* 
 * Runs a simulation of elemental production for a single element produced by a 
 * single stellar population. Fills the pointer *mass with the mass of the given 
 * element in Msun at every time. 
 * 
 * Args: 
 * =====
 * mass:		A pointer to the array to fill
 * run:			A dummy INTEGRATION object holding relevant parameters
 * m:			A dummy MODEL object holding relevant parameters
 * Z:			The metallicity of the stellar population
 * ria:			The SNe Ia DTD 
 * times:		The times at which the simulation will evaluate
 * num_times:	The number of elements in the *times array
 * mstar:		The mass of the stellar population that forms 
 * 
 * source: metals.c
 */
extern int single_population(double *mass, INTEGRATION *run, MODEL *m, 
	double Z, double *ria, double *times, long num_times, double mstar);

/* 
 * Returns the outflow rate in Msun Gyr^-1 at the current timestep. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 * 
 * source: metals.c
 */ 
extern double get_outflow_rate(INTEGRATION run, MODEL m);













/* ---------------- SNE IA ENRICHMENT FUNCTIONS -------------------- */

/*
 * Returns the time derivative of the mass of a given element at the current 
 * timestep from SNe Ia alone. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution.
 * index:		The index of the element in question. 
 * 
 * source: sneia.c 
 */
extern double mdot_ia(INTEGRATION run, MODEL m, int index);

/*
 * Sets up the array RIA containing the SNe Ia rate at all times following the 
 * formation of a single stellar population at time 0. 
 * 
 * Args:
 * =====
 * m:			The MODEL struct for this execution
 * dt:			The timestep size 
 * 
 * source: sneia.c 
 */
extern int setup_RIA(MODEL *m, double dt);

/* 
 * Sets the elements SNe Ia yield parameter to the specified value 
 * 
 * Args:
 * =====
 * run:			A pointer to the INTEGRATION struct for this execution
 * index:		The index of the element to set the yield for
 * value:		The yield itself 
 * 
 * source: sneia.c 
 */
extern int set_sneia_yield(INTEGRATION *run, int index, double value);









/* ----------------- CCSNE ENRICHMENT FUNCTIONS -------------------- */

/*
 * Returns the time-derivative of the mass of an element from CCSNe at the 
 * current timestep. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION structure for the current execution
 * m:			The MODEL structure for the current execution
 * index:		The index of the element 
 * 
 * source: ccsne.c
 */
extern double mdot_ccsne(INTEGRATION run, MODEL m, int index);

/*
 * Fills the core-collapse yield grid as a function of metallicity up to 
 * Z = 0.5. 
 * 
 * Args:
 * =====
 * run:			A pointer to the INTEGRATION struct for this integration
 * index:		The index of the element to set the yield grid for
 * arr:			The array containing the yield at each sampled metallicity 
 * 
 * source: ccsne.c
 */
extern int fill_cc_yield_grid(INTEGRATION *run, int index, double *arr);

/*
 * Gets the CC yield interpolated off of the grid 
 * 
 * Args:
 * =====
 * e:		The element struct whose yield is being interpolated
 * Z:		The metallicity of the ISM by mass, properly scaled 
 * 
 * source: ccsne.c
 */
extern double get_cc_yield(ELEMENT e, double Z);









/* -------------------- AGB ENRICHMENT FUNCTIONS --------------------- */

/* 
 * Returns the mass of a given element produced by AGB stars at the current 
 * timestep. 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for this simulation
 * m:				The MODEL struct for this simulation
 * index:			The index of the element being tracked 
 * 
 * source: agb.c 
 */
extern double m_AGB(INTEGRATION run, MODEL m, int index);

/*
 * Sets up the yield grid for a single element. 
 * 
 * Args:
 * =====
 * e:				A pointer to the element struct to hold the grid
 * grid:			The grid sampled at various masses and metallicities for 
 *  						this element
 * times:			The times that the integration will evaluate at
 * num_times:		The number of elements in the array times. 
 * 
 * source: agb.c 
 */
extern void setup_single_AGB_grid(ELEMENT *e, double **grid, double *times, 
	long num_times);

/*
Returns the effective fractional AGB yield of the given element at the 
lookback time time_index timesteps ago. 

Args:
=====
e:				The element whose yield is to be determined
time_index:		The number of timesteps ago that the stellar population formed
zto:			The metallicity of the stellar population that formed

source: agb.c 
*/
extern double get_AGB_yield(ELEMENT e, long time_index, double zto);


#endif /* ENRICHMENT_H */

