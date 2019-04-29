/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script implements all file reading routines in VICE. 
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "specs.h"
#include "io.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double **read_grid(char *file);

/* 
 * Some large number to denote the length of the line. The files that VICE 
 * interacts with will not have lines this long - the history.out file 
 * associated with each integration only reaches several thousand characters 
 * per line. 
 */ 
static long LINESIZE = 100000l; 

/*
 * Reads the AGB grid for further expansion based on timestepping in the 
 * subroutines in agb.c
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for this iteration of the code
 * file:			The name of the file holding the grid
 * index:			The index of the element 
 * 
 * header: io.h
 */
extern int read_agb_grid(INTEGRATION *run, char *file, int index) {

	long length = num_lines(file);		// number of lines in the file 
	if (length == -1l) return 1;		// if an error occurred 
	ELEMENT *e = &((*run).elements[index]);

	FILE *in = fopen(file, "r");
	/* first keeps track of the first occurrence of a given mass in the table */
	double *first = (double *) malloc (3 * sizeof(double));
	/* line keeps track of the line that was just read in */
	double *line = (double *) malloc (3 * sizeof(double));
	if (fscanf(in, "%lf %lf %lf", &first[0], &first[1], &first[2]) == 0) {
		printf("ERROR reading file: %s\n", file); 
		exit(0); 
	} else {} 
	e -> num_agb_z = 0l; // start counting metallicities 
	do {
		if (fscanf(in, "%lf %lf %lf", &line[0], &line[1], &line[2]) == 0) {
			printf("ERROR reading file: %s\n", file);
			exit(0);
		} else {} 
		e -> num_agb_z++;
		/* Count metallicities while the mass stays the same */ 
	} while (line[0] == first[0]);
	free(first);
	free(line);
	fclose(in); // close the file and free the arrays 

	int i, j;
	/* 
	 * The length of the file must be divisible by the number of sampled 
	 * masses and metallicities. Otherwise assume that the file is formatted 
	 * correctly, with mass and metallicity increasing line by line. 
	 * Current supported versions of VICE do not support user constructed AGB 
	 * tables, so this it not a source of error. 
	 */
	if (length % (*e).num_agb_z != 0) {
		return 2;
	} else {
		e -> num_agb_m = length / (*e).num_agb_z;
		in = fopen(file, "r"); // reopen the file 
		/* Store the masses, metallicities, and yields in 1D/2D arrays */ 
		e -> agb_m = (double *) malloc ((*e).num_agb_m * sizeof(double));
		e -> agb_z = (double *) malloc ((*e).num_agb_z * sizeof(double));
		e -> agb_grid = (double **) malloc ((*e).num_agb_m * sizeof(double *));
		for (i = 0; i < (*e).num_agb_m; i++) {
			e -> agb_grid[i] = (double *) malloc ((*e).num_agb_z * 
				sizeof(double)); 
			for (j = 0; j < (*e).num_agb_z; j++) {
				/* Fill the grid element corresponding to the line */
				if (fscanf(in, "%lf %lf %lf", &((*e).agb_m[i]), &((*e).agb_z[j]), 
					&((*e).agb_grid[i][j])) == 0) {
					printf("ERROR reading file: %s\n", file);
					exit(0); 
				} else {} 
			}
		}
		fclose(in);
		return 0;		
	}

}

/*
 * Reads in a square output file given the destination pointer to store it at in 
 * the memory, the file name, the dimensionality of the output, and the 
 * number of lines in the header. All of these parameters will be determined in 
 * python and the user will only need to specify the name of the previous 
 * INTEGRATION. 
 * 
 * Args:
 * =====
 * file:			The file holding the history output 
 * 
 * header: io.h 
 */
extern double **read_output(char *file) {

	long length = num_lines(file);  			// number of lines in the file 
	if (length == -1l) return NULL;				// if an error occurred 
	int h_length = header_length(file);			// the length of the header 
	int dim = file_dimension(file, h_length); 	// dimensionality of the data 

	long i;
	int j;
	FILE *in = fopen(file, "r");
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	double **data = (double **) malloc ((length - h_length) * sizeof(double *));
	for (i = 0l; i < h_length; i++) {
		/* Read passed the header of the file  */ 
		if (fgets(line, LINESIZE, in) == NULL) {
			printf("ERROR reading file: %s\n", file); 
			exit(0);
		} else {} 
	}
	for (i = 0l; i < length - h_length; i++) {
		/* Allocate memory for this line */ 
		data[i] = (double *) malloc (dim * sizeof(double)); 
		for (j = 0; j < dim; j++) {
			/* Fill it knowing the dimensionality */ 
			if (fscanf(in, "%lf", &data[i][j]) == 0) {
				printf("ERROR reading file: %s\n", file);
				exit(0); 
			} else {} 
		}
	}
	free(line);
	fclose(in);
	return data;

}

/* 
 * Determines the length of the header of an output file assuming the commenting 
 * character is '#' 
 * 
 * Args:
 * =====
 * file:		A character pointer to the name of the output file. 
 * 
 * header: io.h 
 */
extern int header_length(char *file) {

	FILE *in; 
	in = fopen(file, "r");					// open the file 
	if (in == NULL) return -1; 

	int n = 0;
	/* Store a line in memory */ 
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	if (fgets(line, LINESIZE, in) == NULL) {
		printf("ERROR reading file: %s\n", file);
		exit(0); 
	} else {}
	while(line[0] == '#') {
		n++;		// count up while '#' is the first character on the line 
		if (fgets(line, LINESIZE, in) == NULL) {
			printf("ERROR reading file: %s\n", file);
			exit(0); 
		}
	}
	fclose(in);
	free(line);
	return n;

}

/*
 * Determines the dimensionality of the file off of the first line passed the 
 * header. 
 * 
 * Args:
 * =====
 * file:					The name of the file
 * header_length:			The number of lines in the header* 
 * 
 * header: io.h 
 */
extern int file_dimension(char *file, int hlength) {

	FILE *in;
	in = fopen(file, "r"); 					// open the file 
	if (in == NULL) return -1;

	int i;
	int dim = 0;
	/* Store a line in memory and read passed the header */ 
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	for (i = 0; i <= hlength; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			printf("ERROR reading file: %s\n", file); 
			exit(0); 
		}
	}
	/* 
	 * For any character in the line that is not whitespace, if the following 
	 * character is whitespace, increment the dimensionality. 
	 */
	unsigned int j;
	for (j = 0; j < strlen(line) - 1; j++) {
		if (isspace(line[j + 1]) && !isspace(line[j])) {
			dim++;
		} else {
			continue;
		}
	}
	return dim;

}

/*
 * Returns the number of lines in an ascii text file. 
 * 
 * Args:
 * =====
 * file:		The name of the file 
 * 
 * header: io.h 
 */
extern long num_lines(char *file) {

	FILE *in = fopen(file, "r");				// open the file 
	if (in == NULL) return -1l;

	/* 
	 * Store a line in memory and start reading in lines. Don't stop until 
	 * there aren't any more lines to read in, and just count them. 
	 */ 
	long n = 0l; 
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	while (fgets(line, LINESIZE, in) != NULL) {
		n++;
	}
	fclose(in);
	free(line);
	return n;

}

/*
 * Pulls the total yields off of the data file and returns them as a 2-D array 
 * where the zeroth column is the masses and the first column is the total 
 * yields of all isotopes at that stellar mass. 
 * 
 * Args:
 * =====
 * file: 		The name of the file containing the yield grid 
 * 
 * header: io.h 
 */
extern double **yields(char *file) {

	double **raw = read_grid(file); 	// The data as is 
	int size = gridsize(file);			// The number of masses on the grid 
	double **grid = (double **) malloc (size * sizeof(double *));
	/* File dimensionality */ 
	int i, j, dim = file_dimension(file, header_length(file)); 
	for (i = 0; i < size; i++) {
		/* 
		 * At each element on the grid, store the stellar mass as the 0th element
		 * and the total yield of all isotopes of a given element as the 1st
		 */
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
 * Determines the gridsize of a core-collapse supernova yield grid. It does 
 * this by simply seeing how many lines there are, since this is how these 
 * files are formatted. 
 * 
 * Args: 
 * =====
 * file: 				The name of the file 
 * 
 * header: io.h 
 */ 
extern int gridsize(char *file) { 

	FILE *in = fopen(file, "r"); 
	if (in == NULL) return -1; 

	printf("a\n"); 
	int i, n = 1, hlen = header_length(file); 
	printf("b, hlen = %d\n", hlen); 
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	if (fgets(line, LINESIZE, in) == NULL) {
		printf("ERROR reading file: %s\n", file); 
		exit(0); 
	} else {} 
	printf("c\n"); 

	/* Read passed the header */ 
	for (i = 0; i < hlen; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			printf("ERROR reading file: %s\n", file); 
			exit(0); 
		} else {} 
	}
	printf("d\n"); 

	/* 
	 * Increment the number of elements on the grid based on the number of 
	 * lines 
	 */ 
	while (fgets(line, LINESIZE, in) != NULL) {
		n++; 
	}
	printf("e\n"); 
	fclose(in);
	printf("f\n"); 
	free(line);
	printf("g\n"); 
	return n;

}

/*
 * Reads in the grid from the data file and returns it as a 2-D array 
 * 
 * Args:
 * =====
 * file:		The name of the data file
 */
static double **read_grid(char *file) {

	FILE *in = fopen(file, "r");
	int size = gridsize(file);

	/* Allocate memory for the data */
	double **data = (double **) malloc (size * sizeof(double *));
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	int i, j, hlen = header_length(file), dim = file_dimension(file, hlen);

	/* Read passed the header */ 
	for (i = 0; i < hlen; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			printf("ERROR reading file: %s\n", file); 
			exit(0); 
		} else {} 
	}

	/* Scan in the data given the dimensionality of the file */ 
	for (i = 0; i < size; i++) {
		data[i] = (double *) malloc (dim * sizeof(double));
		for (j = 0; j < dim; j++) {
			if (fscanf(in, "%lf", &data[i][j]) == 0) {
				printf("ERROR reading file: %s\n", file); 
				exit(0); 
			} else {} 
		}
	}
	fclose(in);
	free(line);
	return data;

}


