/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#ifndef ENRICHMENT_H
#define ENRICHMENT_H

extern int enrich(INTEGRATION *run, MODEL *m, char *name, double *times, 
	long num_times, double *outtimes);
extern double get_outflow_rate(INTEGRATION run, MODEL m);

/* SNe Ia enrichment functions */
extern double mdot_ia(INTEGRATION run, MODEL m, int index);
// extern int setup_RIA(MODEL *m, double *times, long num_times);
extern int setup_RIA(MODEL *m, double dt);
extern int set_sneia_yield(INTEGRATION *run, int index, double value);

/* CCSNe enrichment functions. */
extern double mdot_ccsne(INTEGRATION run, int index);
extern int set_ccsne_yield(INTEGRATION *run, int index, double value);

/* AGB enrichment functions. */
extern double m_AGB(INTEGRATION run, MODEL m, int index);
extern void setup_single_AGB_grid(ELEMENT *e, double **grid, double *times, 
	long num_times);
// extern int setup_AGB_grids(INTEGRATION *run, double ***grids, double *times, 
// 	long num_times);


#endif /* ENRICHMENT_H */

