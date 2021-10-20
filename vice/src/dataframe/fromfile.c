/*
 * This file implements the functionality of the fromfile objects, a
 * subclass of the VICE dataframe.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../dataframe.h"
#include "../io.h"
#include "fromfile.h"
#include "utils.h"


/*
 * Read in the data in a file into the fromfile object
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 *
 * Returns
 * =======
 * 0 on success from reading the file; 1 on failure
 *
 * header: fromfile.h
 */
extern unsigned short fromfile_read(FROMFILE *ff) {

	/* Use file I/O subroutines in io.h to error check the file */
	int dimension = file_dimension((*ff).name);

	switch (dimension) {

		case -1:
			return 1;

		default:
			ff -> n_cols = (unsigned) dimension;
			ff -> n_rows = (unsigned long) (
				line_count((*ff).name) - header_length((*ff).name)
			);

			switch ((*ff).n_rows) {
				case 0:
					ff -> n_cols = 0;
					return 1;
				default:
					ff -> data = read_square_ascii_file((*ff).name);
					return 0;
			}

	}

}


/*
 * Pull a column from the fromfile object based on its label.
 *
 * Parameters
 * ==========
 * ff: 		The fromfile object itself
 * label: 	The label of the column to pull
 *
 * Returns
 * =======
 * A double pointer to that column of the data; NULL if the label is not found.
 *
 * header: fromfile.h
 */
extern double *fromfile_column(FROMFILE *ff, char *label) {

	int col = column_number(ff, label);
	unsigned long i;
	double *column;

	switch (col) {

		case -1:
			return NULL;

		default:
			column = (double *) malloc ((*ff).n_rows * sizeof(double));
			for (i = 0l; i < (*ff).n_rows; i++) {
				column[i] = (*ff).data[i][col];
			}
			return column;

	}

}


/*
 * Modify a column of the data in a fromfile object
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 * label: 	The label of the column to modify
 * arr: 	The new array to put in place of the old column. Assumed to be of
 * 			length (*ff).n_rows.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * header: fromfile.h
 */
extern unsigned short fromfile_modify_column(FROMFILE *ff, char *label,
	double *arr) {

	int column = column_number(ff, label);
	unsigned long i;

	switch (column) {

		case -1:
			/* automatically make a new column */
			return fromfile_new_column(ff, label, arr);

		default:
			for (i = 0l; i < (*ff).n_rows; i++) {
				ff -> data[i][column] = arr[i];
			}
			return 0;

	}

}


/*
 * Add a column to the data in a fromfile object.
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 * label: 	The label to let the new column have
 * arr: 	The new column itself
 *
 * Returns
 * =======
 * 0 on success; 1 on failure
 *
 * header: fromfile.h
 */
extern unsigned short fromfile_new_column(FROMFILE *ff, char *label,
	double *arr) {

	unsigned long i;
	switch (column_number(ff, label)) {

		case -1:
			/* Only assigned the new column if the label isn't recognized */
			ff -> labels = (char **) realloc (ff -> labels,
				((*ff).n_cols + 1) * sizeof(char *));
			ff -> labels[(*ff).n_cols] = (char *) malloc ((strlen(label) + 1) *
				sizeof(char));
			strcpy(ff -> labels[(*ff).n_cols], label);
			for (i = 0l; i < (*ff).n_rows; i++) {
				ff -> data[i] = (double *) realloc (ff -> data[i],
					((*ff).n_cols + 1) * sizeof(double));
				ff -> data[i][(*ff).n_cols] = arr[i];
			}
			ff -> n_cols++;
			return 0;

		default:
			return 1;

	}

}


/*
 * Pull a row from the fromfile object based on its row number
 *
 * Parameters
 * ==========
 * ff: 		The fromfile object itself
 * row: 	The row number of the data to pull
 *
 * Returns
 * =======
 * A double pointer to that row of the data; NULL if the row number is outside
 * the allowed range.
 *
 * header: fromfile.h
 */
extern double *fromfile_row(FROMFILE *ff, unsigned long row) {

	if (row < (*ff).n_rows) {
		unsigned int i;
		double *data = (double *) malloc ((*ff).n_cols * sizeof(double));
		for (i = 0; i < (*ff).n_cols; i++) {
			data[i] = (*ff).data[row][i];
		}
		return data;
	} else {
		return NULL;
	}

}

