/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script handles the central functions to VICE's simulations of galactic 
 * chemical enrichment, stitching all of the numerical implementations of the 
 * model components into each timestep. 
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "stars.h"
#include "enrichment.h"
#include "io.h"
#include "utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static int setup(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times); 
static void update(INTEGRATION *run, MODEL m);
static void setup_gas_evolution(INTEGRATION *run, MODEL m);
static void update_gas_evolution(INTEGRATION *run, MODEL m);
static double get_tau_star(INTEGRATION run, MODEL m);
static void update_mass(INTEGRATION run, MODEL m);
static void update_single_mass(INTEGRATION run, ELEMENT *e, MODEL m, 
	int index);

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
 * end: 			The time at which the simulation ends
 * 
 * header: enrichment.h
 */
extern int enrich(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times, double *outtimes, double end) {

	/* Run the setup */ 
	int x = setup(run, m, name, times, num_times); 
	if (x) {
		return x; // Return the coded failure integer if the setup failed 
	} else { /* Python makes sure that everything else will go smoothly */ }

	/* Keep track of the number of outputs */ 
	long n = 0l;
	while ((*run).current_time <= end) {
		/* 
		 * Run the simulation until the time reaches the final output time 
		 * specified by the user. When it hits an output time, it will write 
		 * to the output file. 
		 * 
		 * Write output if the current time is larger than the next 
		 * specified output time, or if it is closer to the next specified 
		 * output time than the next timestep. 
		 */ 
		if ((*run).current_time >= outtimes[n] || 2 * outtimes[n] < 2 * 
			(*run).current_time + (*run).dt) {
			write_history_output(*run, *m); 
			n++; 
		} else {} 
		update(run, *m); /* Go forward one timestep */ 
	}
	/* 
	 * Normalize the MDF and write it out, then close the files, free up the 
	 * memory, and call it a day. 
	 */
	normalize_MDF(*run, m);
	write_mdf_output(*run, *m);
	close_files(run);
	clean_structs(run, m);
	return 0;

}

/* 
 * Runs a simulation of elemental production for a single element produced by a 
 * single stellar population. Fills the pointer *mass with the mass of the given 
 * element in Msun at every time. 
 * 
 * Args: 
 * =====
 * mass:		A pointer to the array to fill
 * run:		A dummy INTEGRATION object holding relevant parameters
 * m:			A dummy MODEL object holding relevant parameters
 * Z:			The metallicity of the stellar population
 * ria:		The SNe Ia DTD 
 * times:		The times at which the simulation will evaluate
 * num_times:	The number of elements in the *times array
 * mstar:		The mass of the stellar population that forms 
 * 
 * header: enrichment.h 
 */
extern int single_population(double *mass, INTEGRATION *run, MODEL *m, 
	double Z, double *ria, double *times, long num_times, double mstar) {

	long i;
	/* 
	 * Use dummy instances of the INTEGRATION and MODEL structs just to track 
	 * the relevant evolutionary parameters with time 
	 */ 
	setup_H(m, times, num_times);
	setup_single_AGB_grid(&((*run).elements[0]), (*run).elements[0].agb_grid, 
		times, num_times); 

	/* The contribution from CCSNe */ 
	mass[1] = get_cc_yield((*run).elements[0], Z) * mstar; 

	for (i = 2l; i < num_times; i++) {
		mass[i] = mass[i - 1l];

		/* the contribution from SNe Ia */
		mass[i] += (*run).elements[0].sneia_yield * ria[i] * mstar;

		/* the contribution from AGB stars */
		mass[i] += (get_AGB_yield((*run).elements[0], i, Z) * mstar * (
			(*m).H[i] - (*m).H[i + 1l]));
	}
	
	return 1;

}

/* 
 * Sets up the INTEGRATION and MODEL structs to run the timestep integration. 
 * 
 * Args:
 * ===== 
 * run: 			The INTEGRATION struct for this simulation
 * m: 				The MODEL struct for this simulation
 * name: 			The name of the simulation output 
 * times:			The times at which this INTEGRATION will evaluate
 * num_times:		The number of elements in the times array
 */ 
static int setup(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times) {

	if (open_files(run, name)) return 1;	// Open the output files and 
	write_history_header(*run, *m);			// write the headers  
	write_mdf_header(*run);					// immediately 

	/* 
	 * The cumulative return fraction and hydrogen burning mass fraction as 
	 * functions of time for single stellar populations 
	 */ 
	setup_R(m, times, num_times);
	setup_H(m, times, num_times); 

	/* Setup the stellar MDF and Zall tables for bookkeeping */ 
	setup_MDF(*run, m);
	setup_Zall(run, num_times);

	int i;
	for (i = 0; i < (*run).num_elements; i++) {
		/* Fill each element's AGB grid */ 
		setup_single_AGB_grid(&((*run).elements[i]), 
			(*run).elements[i].agb_grid, 
			times, num_times);
		/* 
		 * Initially nothing. VICE doesn't track any elements produced in big 
		 * bang nucleosynthesis, so this won't be a problem, but will need 
		 * changed if helium or lithium are added. 
		 */ 
		(*run).elements[i].m_tot = 0; // initially nothing
	}
	
	if (!strcmp((*m).dtd, "custom")) {} else {
		/* Fill the SNe DTD if the user hasn't customized it */ 
		if (setup_RIA(m, (*run).dt)) return 2;
	}
	run -> current_time = 0.0; 			// Final bookkeeping steps and 
	run -> timestep = 0l;				// calculating the IFR, SFR, and gas 
	setup_gas_evolution(run, *m);		// supply off of one another

	return 0; 

}

/* 
 * Retuns the stellar mass of the galaxy at the current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 * 
 * header: stars.h 
 */
extern double get_mstar(INTEGRATION run, MODEL m) {

	double mstar = 0;
	long i;
	/* 
	 * At all previous timesteps, the fraction of a stellar population's mass 
	 * that has not been returned to the ISM is given by 1 - r(t) where 
	 * r is the cumulative return fraction (see science documentation). 
	 * This mass includes stellar remntants. 
	 */ 
	for (i = 0l; i < run.timestep; i++) {
		mstar += run.mdotstar[run.timestep - i] * run.dt * (1 - m.R[i]);
	}
	return mstar;

}

/* 
 * Returns the outflow rate in Msun Gyr^-1 at the current timestep. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 * 
 * header: enrichment.h
 */
extern double get_outflow_rate(INTEGRATION run, MODEL m) {

	if (m.smoothing_time < run.dt) {
		/* 
		 * If the smoothing time is less than the timestep, there's no 
		 * timesteps to smooth over. 
		 */ 
		return m.eta[run.timestep] * run.SFR;
	} else {
		/* The number of timesteps to smooth over */ 
		long num_steps = (long) (m.smoothing_time / run.dt);
		long i;
		double avg = 0;
		if (num_steps > run.timestep) {
			/* If the simulation hasn't reached this many timesteps yet */ 
			for (i = 0l; i < run.timestep + 1; i++) {
				avg += run.mdotstar[run.timestep - i];
			} 
			avg /= run.timestep + 1;
		} else {
			/* 
			 * In both cases add up the previous star formation rates and 
			 * divide by the number of timesteps
			 */ 
			for (i = 0l; i < num_steps; i++) {
				avg += run.mdotstar[run.timestep - i];
			}
			avg /= num_steps;
		}
		/* outflow rate = eta * smoothed star formation rate */ 
		return m.eta[run.timestep] * avg;
	}

}

/*
 * Advances all quantities forward one timestep 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static void update(INTEGRATION *run, MODEL m) {

	update_mass(*run, m); 				// Update individual element masses, 
	update_MDF(*run, &m);				// the MDF, time, timestep, the infall 
	run -> current_time += (*run).dt; 	// rate, star formation rate, and gas 
	run -> timestep++;					// supply off of one another. 
	update_gas_evolution(run, m);
	int i;
	/* Also bookkeep the abundances of each element. */ 
	for (i = 0; i < (*run).num_elements; i++) {
		run -> Zall[i][(*run).timestep] = (*run).elements[i].m_tot/ (*run).MG;
	}

}

/*
 * Sets up the INTEGRATION parameters at timestep 0. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static void setup_gas_evolution(INTEGRATION *run, MODEL m) {

	/* SFR = MG * tau_star^-1 */

	if (!strcmp((*run).mode, "gas")) {
		run -> MG = (*run).spec[0];
		run -> SFR = (*run).MG / get_tau_star(*run, m);
		run -> IFR = 0.0; // No idea what the infall history is prior to t = 0 
	} else if (!strcmp((*run).mode, "ifr")) {
		/* The initial gas supply set in python in this case */ 
		run -> IFR = (*run).spec[0];
		run -> SFR = (*run).MG / get_tau_star(*run, m);
	} else {
		run -> SFR = (*run).spec[0];
		run -> MG = (*run).SFR * get_tau_star(*run, m);
		run -> IFR = 0.0; // No idea what the infall history is prior to t = 0
	}

}

/*
 * Updates the INTEGRATION parameters at timestep != 0. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static void update_gas_evolution(INTEGRATION *run, MODEL m) {

	/* 
	 * The star formation rate, infall rate, gas supply, timestep, outflow 
	 * rate, recycling rate, and star formation efficiency timescale are all 
	 * related in the following manner: 
	 * 
	 * SFR = MG * tau_star^-1 
	 * 
	 * dMG = (IFR - SFR - OFR) * dt + M_recycled
	 */ 

	if (!strcmp((*run).mode, "gas")) {
		run -> MG = (*run).spec[(*run).timestep];
		run -> SFR = (*run).MG / get_tau_star(*run, m);
		run -> IFR = (((*run).MG - (*run).spec[(*run).timestep - 1l]) / 
			(*run).dt + (*run).SFR - m_returned(*run, m, -1) + 
			get_outflow_rate(*run, m));
	} else if (!strcmp((*run).mode, "ifr")) {
		run -> IFR = (*run).spec[(*run).timestep];
		run -> MG += ((*run).IFR * (*run).dt - (*run).MG * (*run).dt / 
			get_tau_star(*run, m) + m_returned(*run, m, -1) - 
			get_outflow_rate(*run, m) * (*run).dt);
		run -> SFR = (*run).MG / get_tau_star(*run, m);
	} else {
		run -> SFR = (*run).spec[(*run).timestep];
		double dMG = (*run).SFR * get_tau_star(*run, m) - (*run).MG;
		run -> IFR = (dMG / (*run).dt + (*run).SFR - m_returned(*run, m, -1) / 
			(*run).dt + get_outflow_rate(*run, m));
		run -> MG += dMG;
	}

	/* Also bookkeep the star formation history */ 
	run -> mdotstar[(*run).timestep] = (*run).SFR;

}

/*
 * Gets the depletion time from whether or not the user has specified Schmidt Law 
 * Efficiency. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static double get_tau_star(INTEGRATION run, MODEL m) {

	/* 
	 * tau_star is an array filled off a user-specified function of time. 
	 * Scale it off of the specified Kennicutt-Schmidt Law parameters if 
	 * the user has enabled it. 
	 */ 
	if (m.schmidt) {
		return m.tau_star[run.timestep] * powf( run.MG / m.mgschmidt, 
			-m.schmidt_index);
	} else {
		return m.tau_star[run.timestep];
	}

}

/*
 * Updates the mass of each element at a given timestep. 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static void update_mass(INTEGRATION run, MODEL m) {

	int i;
	for (i = 0; i < run.num_elements; i++) {
		/* Just for loop over a function which does it for each element */ 
		update_single_mass(run, &run.elements[i], m, i);
	}

}

/*
 * Updates the mass of a single element at the current timestep 
 * 
 * Args:
 * =====
 * run: 		The INTEGRATION object for this simulation
 * m:			The MODEL object for this simulation 
 */
static void update_single_mass(INTEGRATION run, ELEMENT *e, MODEL m, 
	int index) {

	/* 
	 * Consider enrichment from core collapse supernovae, type Ia supernovae, 
	 * AGB stars, and recycling, depletion from star formation and outflows, 
	 * and dilution (or enrichment in metal-rich infall simulations) from 
	 * infall. 
	 */ 
	
	e -> m_tot += mdot_ccsne(run, m, index) * run.dt;
	e -> m_tot += mdot_ia(run, m, index) * run.dt;
	e -> m_tot += m_AGB(run, m, index);
	e -> m_tot += m_returned(run, m, index);
	e -> m_tot -= run.SFR * run.dt * (*e).m_tot / run.MG;
	e -> m_tot -= (m.enh[run.timestep] *  get_outflow_rate(run, m) * run.dt / 
		run.MG * (*e).m_tot);
	e -> m_tot += run.IFR * run.dt * m.Zin[index][run.timestep];

}



