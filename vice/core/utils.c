
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "specs.h"
#include "utils.h"


extern int setup_Zin(INTEGRATION run, MODEL *m, double *arr, long num_times) {

	int i;
	long j;
	m -> Zin = (double **) malloc (run.num_elements * sizeof(double *));
	for (i = 0; i < run.num_elements; i++) {
		m -> Zin[i] = (double *) malloc (num_times * sizeof(double));
		for (j = 0l; j < num_times; j++) {
			m -> Zin[i][j] = arr[i * num_times + j];
		}
	}
	return 1;

}

extern int setup_elements(INTEGRATION *run, char **symbols, double *solars) {

	int i;
	run -> elements = (ELEMENT *) malloc ((*run).num_elements * sizeof(
		ELEMENT));
	for (i = 0; i < (*run).num_elements; i++) {
		ELEMENT *e = &((*run).elements[i]);
		e -> symbol = symbols[i];
		e -> solar = solars[i];
	}
	return 0;

}

extern void clean_structs(INTEGRATION *run, MODEL *m) {

	/* Free the model parameters setup during integration */
	free(m -> mdf);
	free(m -> R);
	free(m -> H);
	if (strcmp((*m).dtd, "custom")) {
		free(m -> ria);
	} else {}

	/* Free the integration parameters setup during integration. */
	free(run -> Zall);

	/* Free individual element parameters setup during integration. */
	int i;
	for (i = 0; i < (*run).num_elements; i++) {
		ELEMENT *e = &((*run).elements[i]);
		free(e -> agb_grid);
		free(e -> agb_m);
		free(e -> agb_z);
	}

}


