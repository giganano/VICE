/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This header contains extern declarations for functions handling the stellar 
 * MDFs, turnoff mass and recycling. The functions which numerically 
 * calculate the time evolution of the cumulative return fraction and the 
 * hydrogen burning mass fraction for single stellar populations off of the 
 * assumed stellar IMF are also declared here. 
 */

#ifndef STARS_H
#define STARS_H

/* 
 * Retuns the stellar mass of the galaxy at the current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 * 
 * source: metals.c 
 */
extern double get_mstar(INTEGRATION run, MODEL m);






/* -------------------------- MDF FUNCTIONS ----------------------- */

/*
 * Updates the metallicity distribution function according to the mass of 
 * stars that form at the current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current exeuction 
 * 
 * source: mdf.c 
 */
extern void update_MDF(INTEGRATION run, MODEL *m);

/*
 * Normalizes the MDF prior to writing it to the output file. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current exeuction 
 * 
 * source: mdf.c 
 */
extern void normalize_MDF(INTEGRATION run, MODEL *m);

/*
 * Sets up the MDF at the beginning of the INTEGRATION 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution of the code
 * m:			The MODEL struct for the current execution of the code 
 * 
 * source: mdf.c 
 */
extern void setup_MDF(INTEGRATION run, MODEL *m);






/* --------------------- RECYCLING FUNCTIONS ----------------------- */

/*
 * Returns the turnoff mass in solar masses of a single population of stars a 
 * time t in Gyr following their formation.
 * 
 * source: recycling.c 
 */
extern double m_turnoff(double t);

/*
 * This function calculates the mass of a given element recycled to the 
 * ISM at the birth metallicity of stars as they go through stellar death. 
 * This function also calculates the mass of gas returned the ISM by not 
 * weighting the contribution from each timestep by metallicity when 
 * index == -1. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current execution
 * index:		The index of the element. -1 for gas. 
 * 
 * source: recycling.c  
 */
extern double m_returned(INTEGRATION run, MODEL m, int index);

/*
 * Sets up the array R for the INTEGRATION. This stores the value of the 
 * cumulative return fraction at all timesteps the simulation will evalute at. 
 * Each stellar population then draws from this array given the time it formed 
 * and the current timestep. 
 * 
 * Args:
 * =====
 * m:			A pointer to the MODEL struct for the current execution
 * times:		The times that the INTEGRATION will evaluate at
 * num_times:	The number of elements in the array times
 * 
 * source: recycling.c 
 */
extern void setup_R(MODEL *m, double *times, long num_times);

/*
 * Sets up the array H within the MODEL struct. This represents the mass 
 * fraction of a single stellar population that is still burning hydrogen in 
 * their cores at all timesteps following the formation of a single stellar 
 * population at time 0. This value does not have a simple analytic 
 * expression - see VICE science documentation for details. 
 * 
 * Args:
 * =====
 * m:				A pointer to the MODEL struct for this execution
 * times:			The array of times that this execution will visit
 * num_times:		The number of values in the array times
 * 
 * source: recycling.c 
 */
extern void setup_H(MODEL *m, double *times, long num_times);




#endif /* STARS_H */

