/*
 * This file implements utility functions for VICE's file I/O.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include "../io.h"
#include "utils.h"


/*
 * Reads in a square ascii file given the name of the file.
 *
 * Parameters
 * ==========
 * file: 		The name of the file
 *
 * Returns
 * =======
 * Type double**. The data stored in the file as a 2D array indexed via
 * data[row_number][column_number]. NULL upon failure to read the input file.
 *
 * header: utils.h
 */
extern double **read_square_ascii_file(char *file) {

	/*
	 * Initialize important variables for reading the file. See docstrings of
	 * called functions for details on these quantities
	 */
	long length = line_count(file);
	if (length == -1l) return NULL; 		/* error handling */
	int h_length = header_length(file);
	if (h_length == -1) return NULL;
	int dimension = file_dimension(file);
	if (dimension == -1) return NULL;
	FILE *in = fopen(file, "r");
	if (in == NULL) return NULL;

	/* Read passed the header */
	int i;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	for (i = 0; i < h_length; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in);
			free(line);
			return NULL;
		} else {}
	}
	free(line);

	/*
	 * Assume that all lines beneath the header have data, then read the
	 * data in as a 2D array
	 */
	long j;
	double **data = (double **) malloc ( (unsigned) (length - h_length) *
		sizeof(double *));
	for (j = 0l; j < length - h_length; j++) {
		data[j] = (double *) malloc ( (unsigned) dimension * sizeof(double));
		for (i = 0; i < dimension; i++) {
			if (fscanf(in, "%lf", &data[j][i])) {
				continue;
			} else {
				fclose(in);
				free(data);
				return NULL;
			}
		}
	}
	fclose(in);
	return data;

}


/*
 * Determine the length of the header at the top of a data file assuming all
 * header lines begin with #.
 *
 * Parameters
 * ==========
 * file: 	The name of the file
 *
 * Returns
 * =======
 * The length of the header; -1 on failure to read from the file.
 *
 * header: utils.h
 */
extern int header_length(char *file) {

	/* Open the file and check for error opening the file */
	FILE *in = fopen(file, "r");
	if (in == NULL) {
		return -1;
	}

	/* Store a line in memory, check for error reading the first line */
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	if (fgets(line, LINESIZE, in) == NULL) {
		fclose(in);
		free(line);
		return -1;
	} else {}

	/* Add up the number of lines at the beginning of file that start with # */
	int n = 0;
	while (line[0] == '#') {
		n++;
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in);
			free(line);
			return -1;
		} else {
			continue;
		}
	}

	fclose(in);
	free(line);
	return n;

}


/*
 * Determine the dimensionality of a data file off of the first line passed the
 * header, assuming the header is commented out with '#'.
 *
 * Parameters
 * ==========
 * file: 		The file to determine the dimensionality of
 *
 * Returns
 * =======
 * The number of quantities on one line of the file. -1 on failure to read
 * from the file
 *
 * header: utils.h
 */
extern int file_dimension(char *file) {

	/* Need to read past header first, find out how many lines that is */
	int hlen = header_length(file);
	if (hlen == -1) return -1; 		/* error checking */

	FILE *in = fopen(file, "r");
	if (in == NULL) return -1; 		/* error checking */

	/* Store a line in memory, read passed the header */
	int i;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	for (i = 0; i <= hlen; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in);
			free(line);
			return -1; 				/* error checking */
		} else {
			continue;
		}
	}

	/*
	 * For any character in the line that is not whitespace, if the following
	 * character is whitespace, increment the dimensionality.
	 */
	int dimension = 0;
	unsigned int j;
	for (j = 0; j < strlen(line) - 1; j++) {
		if (isspace(line[j + 1]) && !isspace(line[j])) {
			dimension++;
		} else {
			continue;
		}
	}
	fclose(in);
	free(line);
	return dimension;

}


/*
 * Determine the number of lines in an text file
 *
 * Parameters
 * ==========
 * file: 		The name of the file
 *
 * Returns
 * =======
 * The number of total lines, counting comment headers and blank lines. -1l on
 * failure to read from the file
 *
 * header: utils.h
 */
extern long line_count(char *file) {

	FILE *in = fopen(file, "r");
	if (in == NULL) return -1l; 		/* error checking */

	/*
	 * Start reading in lines, count them, and don't stop until fgets returns
	 * NULL.
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

