/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"
#include "stars.h"
#include "io.h"

/* 
 * Opens the output files for writing throughout the execution 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for the current execution
 * file1:			The name of the file holding the history output
 * file2:			The name of the file holding the mdf output
 * file3:			The name of the file holding the breakdown output 
 * 
 * header: io.h 
 */
extern int open_files(INTEGRATION *run, char *name) {

	/* Piece together the names of the files */
	char file1[10000], file2[10000];
	strcpy(file1, name);
	strcpy(file2, name);
	strcat(file1, "/history.out");
	strcat(file2, "/mdf.out");

	/* Open the files */
	run -> out1 = fopen(file1, "w");
	run -> out2 = fopen(file2, "w");

	/* Check for errors opening files */
	if ((*run).out1 == NULL) {
		return 1;
	} else if ((*run).out2 == NULL) {
		return 1;
	} else {
		return 0;
	}

}

/*
 * Closes all of the output files at the end of the INTEGRATION 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution. 
 * 
 * header: io.h 
 */
extern void close_files(INTEGRATION *run) {

	fclose(run -> out1);
	fclose(run -> out2);

}

/*
 * Writes the header to the history file 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current execution. 
 * 
 * header: io.h
 */
extern void write_history_header(INTEGRATION run, MODEL m) {

	fprintf(run.out1, "# MODE: %s\n", run.mode);
	fprintf(run.out1, "# TIME DIFFERENCE: %e Gyr\n", run.dt);
	fprintf(run.out1, "# SMOOTHING TIME: %e Gyr\n", m.smoothing_time);
	if (m.schmidt) {
		fprintf(run.out1, "# SCHMIDT-LAW SFE: True\n");
		fprintf(run.out1, "# SCHMIDT-LAW POWER-LAW INDEX: ");
		fprintf(run.out1, "SFE \\alpha %g\n", m.schmidt_index);
	} else {
		fprintf(run.out1, "# SCHMIDT-LAW SFE: False\n");
	}

	int i, j;
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "# %s SNE IA YIELD: %e\n", 
			run.elements[i].symbol, run.elements[i].sneia_yield);
	}

	fprintf(run.out1, "# SNE IA DTD MODEL: %s\n", m.dtd);
	fprintf(run.out1, "# SNE IA MINIMUM DELAY TIME: %e Gyr\n", m.t_d);
	if (!strcmp(m.dtd, "exp")) fprintf(run.out1, 
		"# SNE IA E-FOLDING TIMESCALE: %e\n", m.tau_ia);
	fprintf(run.out1, "# COLUMN NUMBERS: \n");
	fprintf(run.out1, "#\t0: Time (Gyr)\n");
	fprintf(run.out1, "#\t1: Mgas (Msun)\t\t\tGas mass\n");
	fprintf(run.out1, "#\t2: Mstar (Msun)\t\t\tStellar mass\n");
	fprintf(run.out1, "#\t3: SFR (Msun/yr)\t\tStar formation rate\n");
	fprintf(run.out1, "#\t4: IFR (Msun/yr)\t\tInfall rate\n");
	fprintf(run.out1, "#\t5: OFR (Msun/yr)\t\tOutflow rate\n");
	int n = 6;
	for (i = 0; i < run.num_elements; i++) {
		/* The inflow metallicity for each element */ 
		fprintf(run.out1, "#\t%d: Z_in(%s)\t\tInflow %s metallicity\n", 
			n, run.elements[i].symbol, run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		/* The outflow metallicity of each element */ 
		fprintf(run.out1, "#\t%d: Z_out(%s)\t\tOutflow %s metallicity\n", 
			n, run.elements[i].symbol, run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		/* The ISM mass of each element */ 
		fprintf(run.out1, "#\t%d: Mass(%s) (Msun)\n", n, 
			run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		/* The mass abundance Z = Mx/Mg of each element */ 
		fprintf(run.out1, "#\t%d: Z(%s)\n", n, run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		/* The logarithmic mass abundance [X/H] of each element */ 
		fprintf(run.out1, "#\t%d: [%s/H]\n", n, run.elements[i].symbol);
		n++;
	}
	for (i = 1; i < run.num_elements; i++) {
		/* 
		 * Write the logarithmic abundance ratio [X/Y] for all pairs of 
		 * elements 
		 */ 
		for (j = 0; j < i; j++) {
			fprintf(run.out1, "#\t%d: [%s/%s]\n", n, run.elements[i].symbol, 
				run.elements[j].symbol);
			n++;
		}
	}
	fprintf(run.out1, "#\t%d: Eta_0\n", n);
	fprintf(run.out1, "#\t%d: R_eff\n", n + 1);

}

/*
 * Writes output to the history file at the current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution.
 * m:			The MODEL struct for the current execution.  
 * 
 * header: io.h
 */ 
extern void write_history_output(INTEGRATION run, MODEL m) {

	/* 
	 * Allocate memory to determine the mass abundance Z = Mx/Mg and the 
	 * logarithmic abundance [X/H] of each element. These values are not 
	 * tracked by VICE at each timestep, but are determined at each output. 
	 */ 
	double *Z = (double *) malloc (run.num_elements * sizeof(double));
	double *onH = (double *) malloc (run.num_elements * sizeof(double));
	int i, j;
	for (i = 0; i < run.num_elements; i++) {
		Z[i] = run.elements[i].m_tot / run.MG;
		onH[i] = log10(Z[i] / run.elements[i].solar);
	}
	/* Write the evolutionary parameters */ 
	fprintf(run.out1, "%e\t", run.current_time);
	fprintf(run.out1, "%e\t", run.MG);
	fprintf(run.out1, "%e\t", get_mstar(run, m));
	fprintf(run.out1, "%e\t", run.SFR / 1e9);
	fprintf(run.out1, "%e\t", run.IFR / 1e9);
	double outrate = get_outflow_rate(run, m) / 1e9;
	fprintf(run.out1, "%e\t", outrate);
	for (i = 0; i < run.num_elements; i++) {
		/* Write the inflow metallicity of each timestep */ 
		fprintf(run.out1, "%e\t", m.Zin[i][run.timestep]);
	}
	for (i = 0; i < run.num_elements; i++) {
		/* Write the outflow metallicity at each timestep */ 
		fprintf(run.out1, "%e\t", m.enh[run.timestep] * Z[i]);
	}
	for (i = 0; i < run.num_elements; i++) { 
		/* Write the total ISM mass of each element at each timestep */ 
		fprintf(run.out1, "%e\t", run.elements[i].m_tot);
	}
	for (i = 0; i < run.num_elements; i++) {
		/* Write the ISM metallicity Z = Mx/Mg */ 
		fprintf(run.out1, "%e\t", Z[i]);
	}
	for (i = 0; i < run.num_elements; i++) {
		/* Write the [X/H] logarithmic abundance */ 
		fprintf(run.out1, "%e\t", onH[i]);
	}
	for (i = 1; i < run.num_elements; i++) {
		/* Write the logarithmic abundance ratio [X/Y] */ 
		for (j = 0; j < i; j++) {
			fprintf(run.out1, "%e\t", onH[i] - onH[j]);
		}
	}
	/* Write the mass loading factor */ 
	fprintf(run.out1, "%e\t", m.eta[run.timestep]);
	/* Write the effective return fraction */ 
	if (m.continuous) {
		fprintf(run.out1, "%e\n", m_returned(run, m, -1) / (run.SFR * run.dt));
	} else {
		fprintf(run.out1, "%e\n", m.R0);
	}
	/* Free the Z and onH pointers */ 
	free(Z);
	free(onH);

}

/*
 * Writes the header to the mdf output file. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution. 
 * 
 * header: io.h
 */
extern void write_mdf_header(INTEGRATION run) {

	/* 
	 * The first two columns are the bin edges. Subsequent columns are the 
	 * probability densities of stars in that [X/H] logarithmic absolute 
	 * abundance bin for each element. Subsequent columns thereafter are the 
	 * probability densities of stars in that [X/Y] logarithmic abundance 
	 * ratio for each combination of elements 
	 */ 
	int i, j;
	fprintf(run.out2, "# bin_edge_left\tbin_edge_right\t");
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out2, "dN/d[%s/H]\t", run.elements[i].symbol);
	}
	for (i = 1; i < run.num_elements; i++) {
		for (j = 0; j < i; j++) {
			fprintf(run.out2, "dN/d[%s/%s]\t", run.elements[i].symbol, 
				run.elements[j].symbol);
		}
	}
	fprintf(run.out2, "\n");

}

#if 0
/*
Writes the header to the mdf output file.

Args:
=====
run:		The INTEGRATION struct for the current execution.

header: io.h
*/
extern void write_mdf_header(INTEGRATION run) {

	fprintf(run.out2, "# bin_edge_left\t");
	fprintf(run.out2, "bin_edge_right\t");
	int i;
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out2, "dN/d[%s/H]\t", run.elements[i].symbol);
	}
	for (i = 1; i < run.num_elements; i++) {
		fprintf(run.out2, "dN/d[%s/%s]\t", run.elements[i].symbol, 
			run.elements[0].symbol);
	}
	fprintf(run.out2, "\n");

}
#endif

/*
 * Writes output to the mdf output file at the final timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution.
 * m:			The MODEL struct for the current execution. 
 * 
 * header: io.h
 */
extern void write_mdf_output(INTEGRATION run, MODEL m) {

	long i; 
	int j;
	/* The number of MDFs */ 
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	for (i = 0l; i < m.num_bins; i++) {
		/* Write the bin edges */ 
		fprintf(run.out2, "%e\t%e\t", m.bins[i], m.bins[i + 1l]);
		for (j = 0; j < num_mdfs; j++) {
			/* Write the value of each MDF in that bin */ 
			fprintf(run.out2, "%e\t", m.mdf[j][i]);
		}
		fprintf(run.out2, "\n");
	}

}

#if 0
/*
Writes output to the mdf output file at the final timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution.
m:			The MODEL struct for the current execution.

header: io.h
*/
extern void write_mdf_output(INTEGRATION run, MODEL m) {

	long i;
	int j;
	for (i = 0l; i < m.num_bins; i++) {
		fprintf(run.out2, "%e\t%e\t", m.bins[i], m.bins[i + 1]);
		for (j = 0; j < 2 * run.num_elements - 1; j++) {
			fprintf(run.out2, "%e\t", m.mdf[j][i]);
		}
		fprintf(run.out2, "\n");
	}

}


/*
Writes the header to the breakdown output file. 

Args:
=====
run:		The INTEGRATION struct for the current execution.
*/
extern void write_breakdown_header(INTEGRATION run) {

	fprintf(run.out3, "# Time\t");
	int i;
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out3, "f_CCSNe(%s)\t", run.elements[i].symbol);
		fprintf(run.out3, "f_SNeIa(%s)\t", run.elements[i].symbol);
		fprintf(run.out3, "f_AGB(%s)\t", run.elements[i].symbol);
	}
	fprintf(run.out3, "\n");

}

/*
Writes to the breakdown output file at the current timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution.
*/
extern void write_breakdown_output(INTEGRATION run) {

	int i;
	fprintf(run.out3, "%e\t", run.current_time);
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out3, "%e\t", run.elements[i].breakdown[run.timestep][0]);
		fprintf(run.out3, "%e\t", run.elements[i].breakdown[run.timestep][1]);
		fprintf(run.out3, "%e\t", run.elements[i].breakdown[run.timestep][2]);
	}
	fprintf(run.out3, "\n");

}
#endif





