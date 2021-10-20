/*
 * This file implements file I/O for core-collapse supernovae yield
 * functionality.
 */

#include <stdlib.h>
#include "../io.h"
#include "utils.h"
#include "ccsne.h"

/*
 * Read a yield table for CCSNe.
 *
 * Parameters
 * ==========
 * file: 		The name of the file, passed from python.
 *
 * Returns
 * =======
 * Type **double:
 * 		returned[i][0]: initial stellar mass
 * 		returned[i][1]: total mass yield of the element
 * NULL on failure to read from the file
 *
 * header: ccsne.h
 */
extern double **cc_yield_grid(char *file) {

	/*
	 * The number of masses and isotopes on the grid can be determined from
	 * the length and dimensionality of the data file
	 */
	int n_masses = line_count(file) - header_length(file);
	if (n_masses == 0) return NULL;
	int dimension = file_dimension(file);
	if (dimension == -1) return NULL; 			/* error handling */

	int i, j;
	double **raw = read_square_ascii_file(file);
	double **grid = (double **) malloc ( (unsigned) n_masses *
		sizeof(double *));
	for (i = 0; i < n_masses; i++) {
		/* Convert to a stellar mass - total isotope mass yield grid */
		grid[i] = (double *) malloc (2 * sizeof(double));
		grid[i][0] = raw[i][0];
		grid[i][1] = 0;
		for (j = 1; j < dimension; j++) {
			grid[i][1] += raw[i][j];
		}
	}
	free(raw);
	return grid;

}

