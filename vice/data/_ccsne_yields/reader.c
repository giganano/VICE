
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "cc_yields.h"

static double **read_grid(char *file);
static int dimension(char *file);
static int header_length(char *file);
static long LINESIZE = 10000l;

/*
Pulls the total yields off of the data file and returns them as a 2-D array 
where the zeroth column is the masses and the first column is the total 
yields of all isotopes at that stellar mass. 

Args:
=====
The name of the file
*/
extern double **yields(char *file) {

	double **raw = read_grid(file);
	double **grid = (double **) malloc (10 * sizeof(double *));
	int i, j, dim = dimension(file);
	for (i = 0; i < 10; i++) {
		grid[i] = (double *) malloc (2 * sizeof(double));
		grid[i][0] = raw[i][0];
		grid[i][1] = 0;
		for (j = 1; j < dim; j++) {
			grid[i][1] += raw[i][j];
		}
	}
	free(raw);
	return grid;

}

/*
Reads in the grid from the data file and returns it as a 2-D array

Args:
=====
file:		The name of the data file
*/
static double **read_grid(char *file) {

	FILE *in = fopen(file, "r");
	// All yields are sampled at 10 different stellar masses
	double **data = (double **) malloc (10 * sizeof(double *));
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	int i, j, hlen = header_length(file), dim = dimension(file);
	for (i = 0; i < hlen; i++) {
		fgets(line, LINESIZE, in);
	}
	for (i = 0; i < 10; i++) {
		data[i] = (double *) malloc (dim * sizeof(double));
		for (j = 0; j < dim; j++) {
			fscanf(in, "%lf", &data[i][j]);
		}
	}
	fclose(in);
	free(line);
	return data;

}

/*
Determines the dimensionality of a data file assuming that the comment header 
is marked by a '#' as the first character.

Args:
=====
file:		The name of the data file
*/
static int dimension(char *file) {

	FILE *in = fopen(file, "r");
	if (in == NULL) return -1;

	unsigned int i;
	int dim = 0;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	do {
		fgets(line, LINESIZE, in);
	} while (line[0] == '#');
	for (i = 0; i < strlen(line) - 1; i++) {
		if (isspace(line[i + 1]) && !isspace(line[i])) {
			dim++;
		} else {
			continue;
		}
	}
	free(line);
	fclose(in);
	return dim;

}

/*
Returns the number of lines in the header block at the top of a data file 
assuming that '#' is the first character of each line in the header block

Args:
=====
file:		The name of the data file
*/
static int header_length(char *file) {

	FILE *in = fopen(file, "r");
	if (in == NULL) return -1;
	
	int n = 0;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	fgets(line, LINESIZE, in);
	while (line[0] == '#') {
		n++;
		fgets(line, LINESIZE, in);
	}
	fclose(in);
	free(line);
	return n;

}


