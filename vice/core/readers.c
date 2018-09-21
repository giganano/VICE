
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "specs.h"
#include "io.h"

static long LINESIZE = 10000;


/*
Reads the AGB grid for further expansion based on timestepping in the subroutines 
in agb.c

Args:
=====
run:			The INTEGRATION struct for this iteration of the code
file:			The name of the file holding the grid
index:			The index of the element
*/
extern int read_agb_grid(INTEGRATION *run, char *file, int index) {

	long length = num_lines(file);
	if (length == -1l) return 1;
	ELEMENT *e = &((*run).elements[index]);

	FILE *in = fopen(file, "r");
	double *first = (double *) malloc (3 * sizeof(double));
	double *line = (double *) malloc (3 * sizeof(double));
	fscanf(in, "%lf %lf %lf", &first[0], &first[1], &first[2]);
	e -> num_agb_z = 0l;
	// printf("%s\n", (*e).symbol);
	do {
		fscanf(in, "%lf %lf %lf", &line[0], &line[1], &line[2]);
		e -> num_agb_z++;
		// printf("%lf %lf %lf\n", line[0], line[1], line[2]);
	} while (line[0] == first[0]);
	free(first);
	free(line);
	fclose(in);

	int i, j;
	if (length % (*e).num_agb_z != 0) return 2;
	e -> num_agb_m = length / (*e).num_agb_z;
	in = fopen(file, "r");
	e -> agb_m = (double *) malloc ((*e).num_agb_m * sizeof(double));
	e -> agb_z = (double *) malloc ((*e).num_agb_z * sizeof(double));
	e -> agb_grid = (double **) malloc ((*e).num_agb_m * sizeof(double *));
	for (i = 0; i < (*e).num_agb_m; i++) {
		e -> agb_grid[i] = (double *) malloc ((*e).num_agb_z * sizeof(double));
		for (j = 0; j < (*e).num_agb_z; j++) {
			fscanf(in, "%lf %lf %lf", &((*e).agb_m[i]), &((*e).agb_z[j]), 
				&((*e).agb_grid[i][j]));
		}
	}
	fclose(in);
	return 0;

}

/*
extern int test_agb_reader(INTEGRATION *run) {

	int i, j;
	for (i = 0; i < (*run).elements[0].num_agb_m; i++) {
		for (j = 0; j < (*run).elements[0].num_agb_z; j++) {
			printf("%lf %lf %e\n", (*run).elements[0].agb_m[i], 
				(*run).elements[0].agb_z[j], 
				(*run).elements[0].agb_grid[i][j]);
		}
	}
	return 0;
}
*/




/*
Reads in a square output file given the destination pointer to store it at in 
the memory, the file name, the dimensionality of the output, and the 
number of lines in the header. All of these parameters will be determined in 
python and the user will only need to specify the name of the previous 
INTEGRATION. 

Args:
=====
file:				The file holding the history output
*/
extern double **read_output(char *file) {

	long length = num_lines(file);
	if (length == -1l) return NULL;
	int h_length = header_length(file);
	int dim = dimension(file, h_length);

	long i;
	int j;
	FILE *in = fopen(file, "r");
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	double **data = (double **) malloc ((length - h_length) * sizeof(double *));
	for (i = 0l; i < h_length; i++) {
		fgets(line, LINESIZE, in);
	}
	for (i = 0l; i < length - h_length; i++) {
		data[i] = (double *) malloc (dim * sizeof(double));
		for (j = 0; j < dim; j++) {
			fscanf(in, "%lf", &data[i][j]);
		}
	}
	free(line);
	fclose(in);
	return data;

}

/* 
Determines the length of the header of an output file assuming the commenting 
character is '#'

Args:
=====
file:		A character pointer to the name of the output file.
*/
extern int header_length(char *file) {

	FILE *in; 
	in = fopen(file, "r");
	if (in == NULL) return -1;

	int n = 0;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	fgets(line, LINESIZE, in);
	while(line[0] == '#') {
		n++;
		fgets(line, LINESIZE, in);
		// if (line == NULL) {
		// 	fclose(in);
		// 	free(line);
		// 	return -2;
		// } else {
		// 	continue;
		// }
	}
	fclose(in);
	free(line);
	return n;

}

/*
Determines the dimensionality of the file off of the first line passed the header.

Args:
=====
file:					The name of the file
header_length:			The number of lines in the header
*/
extern int dimension(char *file, int hlength) {

	FILE *in;
	in = fopen(file, "r");
	if (in == NULL) return -1;

	int i, dim = 0;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	for (i = 0; i <= hlength; i++) {
		fgets(line, LINESIZE, in);
	}
	for (i = 0; i < strlen(line) - 1; i++) {
		if (isspace(line[i + 1]) && !isspace(line[i])) {
			dim++;
		} else {
			continue;
		}
	}
	return dim;

}

/*
Returns the number of lines in an ascii text file.

Args:
=====
file:		The name of the file
*/
extern long num_lines(char *file) {

	FILE *in = fopen(file, "r");
	if (in == NULL) return -1l;

	long n = 0l;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	while (fgets(line, LINESIZE, in) != NULL) {
		n++;
	}
	fclose(in);
	free(line);
	return n;

}

