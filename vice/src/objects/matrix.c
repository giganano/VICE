/*
 * This file implements memory management for the matrix object.
 */

#include <stdlib.h>
#include "objects.h"
#include "matrix.h"


/*
 * Allocate memory for and return a pointer to a MATRIX object.
 * Automatically initializes all matrix elements to zero.
 *
 * Parameters
 * ==========
 * n_rows: 		The number of rows in the desired matrix.
 * n_cols: 		The number of columns in the desired matrix.
 *
 * header: matrix.h
 */
extern MATRIX *matrix_initialize(unsigned short n_rows, unsigned short n_cols) {

	unsigned short i, j;
	MATRIX *m = (MATRIX *) malloc (sizeof(MATRIX));
	m -> matrix = (double **) malloc (n_rows * sizeof(double *));
	for (i = 0u; i < n_rows; i++) {
		m -> matrix[i] = (double *) malloc (n_cols * sizeof(double));
		for (j = 0u; j < n_cols; j++) m -> matrix[i][j] = 0.0;
	}
	m -> n_rows = n_rows;
	m -> n_cols = n_cols;
	return m;

}


/*
 * Free up the memory associated with a matrix object.
 *
 * header: matrix.h
 */
extern void matrix_free(MATRIX *m) {

	if (m != NULL) {

		if ((*m).matrix != NULL) {

			unsigned int i;
			for (i = 0u; i < (*m).n_rows; i++) {
				if ((*m).matrix[i] != NULL) {
					free(m -> matrix[i]);
					m -> matrix[i] = NULL;
				} else {}
			}

			free(m -> matrix);
			m -> matrix = NULL;

		} else {}

		free(m);
		m = NULL;

	} else {}

}

