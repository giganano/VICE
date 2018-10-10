/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#ifndef SPECS_H
#define SPECS_H

#include <stdio.h>


typedef struct model {

	char *imf;
	char *dtd;
	double **mdf;
	double *bins;
	long num_bins;
	double *eta;
	double *enh;
	double **Zin;
	double *R;
	double *H;
	double *tau_star;
	double schmidt_index;
	double mgschmidt;
	double t_d;
	double tau_ia;
	double *ria;
	double smoothing_time;
	double m_upper;
	double m_lower;
	double R0;
	int continuous;
	int schmidt;
	double Z_solar;

} MODEL;


typedef struct element {

	char *symbol;
	double ccsne_yield;
	double sneia_yield;
	double **agb_grid;
	double *agb_m;
	double *agb_z;
	long num_agb_m;
	long num_agb_z;
	double m_ccsne;
	double m_sneia;
	double m_agb;
	double m_tot;
	double **breakdown;
	double solar;

} ELEMENT;


typedef struct integration {

	FILE *out1;
	FILE *out2;
	FILE *out3;
	char *mode;
	double *spec;
	double MG;
	double SFR;
	double IFR;
	int num_elements;
	double *mdotstar;
	double **Zall;
	double dt;
	double current_time;
	long timestep;
	ELEMENT *elements;

} INTEGRATION;



#endif /* SPECS_H */

