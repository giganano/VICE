
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"
#include "stars.h"
#include "io.h"

/* 
Opens the output files for writing throughout the execution 

Args:
=====
run:		The INTEGRATION struct for the current execution
file1:		The name of the file holding the history output
file2:		The name of the file holding the mdf output
file3:		The name of the file holding the breakdown output
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
	// run -> out3 = fopen(file3, "w");

	// free(file1);
	// free(file2);
	// free(file3);

	/* Check for errors opening files */
	if ((*run).out1 == NULL) {
		printf("a\n");
		return 1;
	} else if ((*run).out2 == NULL) {
		printf("b\n");
		return 1;
	} else {
	// } else if ((*run).out3 == NULL) {
	// 	return 1;
	// } else {
		return 0;
	}

}

/*
Closes all of the output files at the end of the INTEGRATION

Args:
=====
run:		The INTEGRATION struct for the current execution.
*/
extern void close_files(INTEGRATION run) {

	fclose(run.out1);
	fclose(run.out2);
	// fclose(run.out3);

}

/*
Writes the header to the history file

Args:
=====
run:		The INTEGRATION struct for the current execution
m:			The MODEL struct for the current execution.
*/
extern void write_history_header(INTEGRATION run, MODEL m) {

	fprintf(run.out1, "# MODE: %s\n", run.mode);
	fprintf(run.out1, "# TIME DIFFERENCE: %e Gyr\n", run.dt);
	fprintf(run.out1, "# SMOOTHING TIME: %e Gyr\n", m.smoothing_time);
	// fprintf(run.out1, "# SCHMIDT-LAW SFE BEHAVIOR: ")
	if (m.schmidt) {
		fprintf(run.out1, "# SCHMIDT-LAW SFE: True\n");
		fprintf(run.out1, "# SCHMIDT-LAW POWER-LAW INDEX: ");
		fprintf(run.out1, "SFE \\alpha %g\n", m.schmidt_index);
	} else {
		fprintf(run.out1, "# SCHMIDT-LAW SFE: False\n");
	}

	int i, j;
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "# IMF INTEGRATED %s CCSN YIELD: %e\n", 
			run.elements[i].symbol, run.elements[i].ccsne_yield);
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
	// fprintf(run.out1, "#\t6: Zout\t\t\tOutflow metallicity\n");
	int n = 6;
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "#\t%d: Mass(%s) (Msun)\n", n, 
			run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "#\t%d: Z(%s)\n", n, run.elements[i].symbol);
		n++;
	}
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "#\t%d: [%s/H]\n", n, run.elements[i].symbol);
		n++;
	}
	for (i = 1; i < run.num_elements; i++) {
		// fprintf(run.out1, "#\t%d: [%s/%s]\n", n, run.elements[i].symbol, 
		// 	run.elements[0].symbol);
		// n++;
		for (j = 0; j < i; j++) {
			fprintf(run.out1, "#\t%d: [%s/%s]\n", n, run.elements[i].symbol, 
				run.elements[j].symbol);
			n++;
		}
	}
	fprintf(run.out1, "#\t%d: Eta_0\n", n);
	fprintf(run.out1, "#\t%d: R\n", n + 1);
	fprintf(run.out1, "#\t%d: Zeta\n", n + 2);

}

/*
Writes output to the history file at the current timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution.
m:			The MODEL struct for the current execution.
*/
extern void write_history_output(INTEGRATION run, MODEL m) {

	double *Z = (double *) malloc (run.num_elements * sizeof(double));
	double *onH = (double *) malloc (run.num_elements * sizeof(double));
	double Ztot = 0;
	int i, j;
	for (i = 0; i < run.num_elements; i++) {
		Z[i] = run.elements[i].m_tot / run.MG;
		onH[i] = log10(Z[i] / run.elements[i].solar);
		Ztot += Z[i];
	}
	fprintf(run.out1, "%e\t", run.current_time);
	fprintf(run.out1, "%e\t", run.MG);
	fprintf(run.out1, "%e\t", get_mstar(run, m));
	fprintf(run.out1, "%e\t", run.SFR / 1e9);
	fprintf(run.out1, "%e\t", run.IFR / 1e9);
	double outrate = get_outflow_rate(run, m) / 1e9;
	fprintf(run.out1, "%e\t", outrate);
	// fprintf(run.out1, "%e\t", m.zeta[run.timestep]/m.eta[run.timestep]*Ztot);
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "%e\t", run.elements[i].m_tot);
	}
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "%e\t", Z[i]);
	}
	for (i = 0; i < run.num_elements; i++) {
		fprintf(run.out1, "%e\t", onH[i]);
	}
	for (i = 1; i < run.num_elements; i++) {
		// fprintf(run.out1, "%e\t", onH[i] - onH[0]);
		for (j = 0; j < i; j++) {
			fprintf(run.out1, "%e\t", onH[i] - onH[j]);
		}
	}
	fprintf(run.out1, "%e\t", m.eta[run.timestep]);
	if (m.continuous) {
		fprintf(run.out1, "%e\t", m_returned(run, m, -1) / (run.SFR * run.dt));
	} else {
		fprintf(run.out1, "%e\t", m.R0);
	}
	fprintf(run.out1, "%e\n", m.zeta[run.timestep]);
	free(Z);
	free(onH);

}

/*
Writes the header to the mdf output file.

Args:
=====
run:		The INTEGRATION struct for the current execution.
*/
extern void write_mdf_header(INTEGRATION run) {

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

/*
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
*/

/*
Writes output to the mdf output file at the final timestep.

Args:
=====
run:		The INTEGRATION struct for the current execution.
m:			The MODEL struct for the current execution.
*/
extern void write_mdf_output(INTEGRATION run, MODEL m) {

	long i; 
	int j;
	int num_mdfs = run.num_elements + (run.num_elements * (run.num_elements - 
		1))/2;
	for (i = 0l; i < m.num_bins; i++) {
		fprintf(run.out2, "%e\t%e\t", m.bins[i], m.bins[i + 1l]);
		for (j = 0; j < num_mdfs; j++) {
			fprintf(run.out2, "%e\t", m.mdf[j][i]);
		}
		fprintf(run.out2, "\n");
	}

}

/*
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
*/

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





