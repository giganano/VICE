/*
 * This file implements the memory management for the datum object.
 */

#include <stdlib.h>
#include <stdint.h>
#include "../debug.h"
#include "objects.h"
#include "datum.h"
#include "matrix.h"


/*
 * Allocate memory for and return a pointer to a DATUM object.
 * Sets up the datum as a row vector rather than a column vector and
 * initializes each of the values to zero.
 *
 * Parameters
 * ==========
 * dim: 		The dimensionality of the datum.
 *
 * header: datum.h
 */
extern DATUM *datum_initialize(unsigned short dim) {

	DATUM *d = (DATUM *) matrix_initialize(1u, dim);
	d = (DATUM *) realloc (d, sizeof(DATUM));
	d -> labels = (char **) malloc (dim * sizeof(char *));
	unsigned short i;
	for (i = 0u; i < dim; i++) d -> labels[i] = NULL;
	d -> cov = NULL; /* to be assigned in python */
	return d;

}


/*
 * Free up the memory stored in a datum object.
 *
 * header: datum.h
 */
extern void datum_free(DATUM *d) {

	if (d != NULL) {

		unsigned short i, dim;
		if ((*d).n_rows == 1u) {
			dim = (*d).n_cols;
		} else if ((*d).n_cols == 1u) {
			dim = (*d).n_rows;
		} else {
			fatal_print("%s\n",
				"Could not determine datum dimensionality.");
		}
		for (i = 0u; i < dim; i++) {
			if (d -> labels[i] != NULL) {
				free(d -> labels[i]);
				d -> labels[i] = NULL;
			} else {}
		}
		free(d -> labels);
		d -> labels = NULL;
		// if (d -> cov != NULL) matrix_free(d -> cov); // abort trap on exit
		matrix_free( (MATRIX *) d);

	} else {}

}


/*
 * Link the covariance matrix object to the datum at initialization time in
 * python.
 *
 * Parameters
 * ==========
 * d: 			The datum pointer to link to
 * address: 	The address of the matrix pointer to link to, expressed as a
 * 				string
 *
 * header: datum.h
 */
extern void link_cov_matrix(DATUM *d, char *address) {

	unsigned long ul;
	sscanf(address, "%lx", &ul);
	d -> cov = (COVARIANCE_MATRIX *) (uintptr_t) ul;

}

