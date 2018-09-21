
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "specs.h"
#include "stars.h"
#include "enrichment.h"
#include "io.h"
#include "utils.h"

static void update(INTEGRATION *run, MODEL m);
static void setup_params(INTEGRATION *run, MODEL m);
static void update_params(INTEGRATION *run, MODEL m);
static double get_tau_star(INTEGRATION run, MODEL m);
static void update_mass(INTEGRATION run, MODEL m);
static void update_single_mass(INTEGRATION run, ELEMENT *e, MODEL m, 
	int index);


/*
This acts as the main method as far as the wrapper is concerned. When this 
function is called, it runs the integrator on all of the parameters inside 
the structs. 

Args:
=====
run:			The INTEGRATION struct for this iteration of the code
m:				The MODEL struct for this iteration of the code
name:			The name of this INTEGRATION
times:			The times at which this INTEGRATION will evalute
num_times:		The number of elements in the times array
outtimes:		The array of output times
*/
extern int enrich(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times, double *outtimes) {

	if (open_files(run, name)) return 1;
	
	write_history_header(*run, *m);
	write_mdf_header(*run);
	int i;
	run -> Zall = (double **) malloc ((*run).num_elements * sizeof(double *));
	for (i = 0; i < (*run).num_elements; i++) {
		setup_single_AGB_grid(&((*run).elements[i]), 
			(*run).elements[i].agb_grid, 
			times, num_times);
		(*run).elements[i].m_ccsne = 0;
		(*run).elements[i].m_sneia = 0;
		(*run).elements[i].m_agb = 0;
		(*run).elements[i].m_tot = 0;
		run -> Zall[i] = (double *) malloc (num_times * sizeof(double));
		run -> Zall[i][0] = (*run).elements[i].m_tot / (*run).MG;
	}
	setup_MDF(*run, m);
	setup_R(m, times, num_times);
	setup_H(m, times, num_times);
	setup_breakdown(*run, num_times);
	setup_Zall(run, num_times);
	if (setup_RIA(m, times, num_times)) return 2;
	run -> current_time = 0.0;
	run -> timestep = 0l;
	setup_params(run, *m);
	long n = 0l;
	while ((*run).current_time <= times[num_times - 1l]) {
		if ((*run).current_time >= outtimes[n]) {
			write_history_output(*run, *m);
			// write_breakdown_output(*run);
			n++;
		} else {}
		update(run, *m);
	}
	normalize_MDF(*run, m);
	write_mdf_output(*run, *m);
	close_files(*run);
	clean_structs(run, m);
	return 0;

}

/*
Advances all quantities forward one timestep
*/
static void update(INTEGRATION *run, MODEL m) {

	update_mass(*run, m);
	update_MDF(*run, &m);
	run -> current_time += (*run).dt;
	run -> timestep++;
	update_params(run, m);
	int i;
	for (i = 0; i < (*run).num_elements; i++) {
		run -> Zall[i][(*run).timestep] = (*run).elements[i].m_tot/ (*run).MG;
	}
	// printf("%ld %e\n", (*run).timestep, (*run).Zall[2][(*run).timestep]);

}

/*
Sets up the INTEGRATION parameters at timestep 0.
*/
static void setup_params(INTEGRATION *run, MODEL m) {

	if (!strcmp((*run).mode, "gas")) {
		run -> MG = (*run).spec[0];
		run -> SFR = (*run).MG / get_tau_star(*run, m);
		run -> IFR = NAN; // No idea what the infall history is prior to t = 0 
	} else if (!strcmp((*run).mode, "ifr")) {
		run -> IFR = (*run).spec[0];
		run -> SFR = (*run).MG / get_tau_star(*run, m);
	} else {
		run -> SFR = (*run).spec[0];
		run -> MG = (*run).SFR * get_tau_star(*run, m);
		run -> IFR = NAN;
	}

}

/*
Updates the INTEGRATION parameters at timestep != 0.
*/
static void update_params(INTEGRATION *run, MODEL m) {

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
	run -> mdotstar[(*run).timestep] = (*run).SFR;

}

/*
Gets the depletion time from whether or not the user has specified Schmidt Law 
Efficiency. 
*/
static double get_tau_star(INTEGRATION run, MODEL m) {

	if (m.schmidt) {
		return m.tau_star[run.timestep] * powf( run.MG / m.mgschmidt, 
			-m.schmidt_index);
	} else {
		return m.tau_star[run.timestep];
	}

}

/*
Updates the mass of each element at a given timestep.
*/
static void update_mass(INTEGRATION run, MODEL m) {

	int i;
	for (i = 0; i < run.num_elements; i++) {
		update_single_mass(run, &run.elements[i], m, i);
	}

}

/*
Updates the mass of a single element 
*/
static void update_single_mass(INTEGRATION run, ELEMENT *e, MODEL m, 
	int index) {

	// long i;
	// e -> m_ccsne += mdot_ccsne(run, index) * run.dt;
	// e -> m_sneia += mdot_ia(run, m, index) * run.dt;
	// e -> m_agb += m_AGB(run, m, index);
	// for (i = 0l; i < run.timestep; i++) {
	// 	// double dm_r = run.mdotstar[run.timestep - i] * run.dt * (m.R[i + 1l] - 
	// 	// 	m.R[i]) * run.Zall[i][run.timestep - i];
	// }
	// double loss = ((get_outflow_rate(run, m) + run.SFR) * run.dt * 
	// 	(*e).m_tot / run.MG);

	// e -> m_ccsne -= loss * e -> breakdown[run.timestep][0];
	// e -> m_sneia -= loss * e -> breakdown[run.timestep][1];
	// e -> m_agb -= loss * e -> breakdown[run.timestep][2];
	// e -> m_tot = e -> m_ccsne + e -> m_sneia + e -> m_agb;
	// e -> breakdown[run.timestep + 1l][0] = e -> m_ccsne / e -> m_tot;
	// e -> breakdown[run.timestep + 1l][1] = e -> m_sneia / e -> m_tot;
	// e -> breakdown[run.timestep + 1l][2] = e -> m_agb / e -> m_tot;

	e -> m_tot += mdot_ccsne(run, index) * run.dt;
	e -> m_tot += mdot_ia(run, m, index) * run.dt;
	e -> m_tot += m_AGB(run, m, index);
	e -> m_tot += m_returned(run, m, index);
	e -> m_tot -= run.SFR * run.dt * (*e).m_tot / run.MG;
	e -> m_tot -= (m.zeta[run.timestep] / m.eta[run.timestep] * 
		get_outflow_rate(run, m) * run.dt / run.MG * (*e).m_tot);
	// e -> m_tot -= ((get_outflow_rate(run, m) + run.SFR) * run.dt * 
	// 	(*e).m_tot / run.MG); 
	// if (!strcmp((*e).symbol, "Sr")) {
	// 	printf("AGB Strontium added: %e\n", m_AGB(run, m, index));
	// } else {}

}

extern double get_mstar(INTEGRATION run, MODEL m) {

	double mstar = 0;
	long i;
	for (i = 0l; i < run.timestep; i++) {
		// mstar += run.mdotstar[run.timestep - i] * run.dt * m.H[i];
		mstar += run.mdotstar[run.timestep - i] * run.dt * (1 - m.R[i]);
	}
	return mstar;

}

extern double get_outflow_rate(INTEGRATION run, MODEL m) {

	if (m.smoothing_time < run.dt) {
		return m.eta[run.timestep] * run.SFR;
	} else {
		long num_steps = (long) (m.smoothing_time / run.dt);
		long i;
		double avg = 0;
		if (num_steps > run.timestep) {
			for (i = 0l; i < run.timestep + 1; i++) {
				avg += run.mdotstar[run.timestep - i];
			}
			avg /= run.timestep + 1;
		} else {
			for (i = 0l; i < num_steps; i++) {
				avg += run.mdotstar[run.timestep - i];
			}
			avg /= num_steps;
		}
		return m.eta[run.timestep] * avg;
	}

}




