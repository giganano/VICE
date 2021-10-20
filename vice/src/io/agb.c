/*
 * This file implements file I/O for asymptotic giant branch star yield
 * functionality.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "../io.h"
#include "utils.h"
#include "agb.h"

/*
 * Import a built-in AGB star yields grid.
 *
 * Parameters
 * ==========
 * e: 		A pointer to the element struct to import the grid into
 * file: 	The name of the file containing the AGB yield grid. These are
 * 			include in VICE's data directory, and direct user access to them
 * 			is strongly discouraged.
 *
 * Returns
 * =======
 * 0 on success; nonezero on failure
 *
 * header: io.h
 */
extern unsigned short import_agb_grid(ELEMENT *e, char *file) {

	/*
	 * Initialize important variables for reading the file. See docstrings of
	 * called functions for details on these quantities.
	 *
	 * Note: The change in error handing check to require that AGB yield grids
	 * be 3-dimensional. All AGB yield data files stored internally in VICE
	 * are of this format.
	 */
	long length = line_count(file);
	if (length == -1l) return 1; 		/* error handling */
	int h_length = header_length(file);
	if (h_length == -1) return 2;
	int dimension = file_dimension(file);
	if (dimension != 3) return 3;
	FILE *in = fopen(file, "r");
	if (in == NULL) return 4;

	/*
	 * first keeps track of the first occurrence of a given mass in the
	 * table
	 *
	 * line keeps track of the line that was just read in
	 */
	double *first = (double *) malloc (3 * sizeof(double));
	double *line = (double *) malloc (3 * sizeof(double));
	if (!fscanf(in, "%lf %lf %lf", &first[0], &first[1], &first[2])) {
		fclose(in);
		free(first);
		free(line);
		return 5;
	} else {}

	e -> agb_grid -> interpolator -> n_y_values = 0l; /* count metallicities */
	do {
		if (fscanf(in, "%lf %lf %lf", &line[0], &line[1], &line[2])) {
			/* Count metallicities while the mass stays the same */
			e -> agb_grid -> interpolator -> n_y_values++;
			continue;
		} else {
			fclose(in);
			free(first);
			free(line);
			return 6;
		}
	} while (line[0] == first[0]);

	/* Free up memory, start over, and read the whole thing in */
	free(first);
	free(line);
	fclose(in);

	/*
	 * The length of the file must be divisible by the number of sampled
	 * massed and metallicities. Otherwise assume that the file is formatted
	 * correctly, with mass and metallicity increasing line by line. Current
	 * supported versions of VICE do not support user constructed AGB tables,
	 * so this is not a source of error.
	 *
	 * The grid files are designed such that the metallicites go up at
	 * constant mass, then the mass increases, and both increase monotonically
	 * with the line number. These lines are explicitly designed to read in
	 * that format.
	 */
	switch( (unsigned) length % (*(*(*e).agb_grid).interpolator).n_y_values ) {
		unsigned long i, j;

		case 0:
			/*
			 * The switch must be equal to zero, or else the data file has
			 * been tampered with.
			 */
			e -> agb_grid -> interpolator -> n_x_values = (unsigned) (
				length) / (*(*(*e).agb_grid).interpolator).n_y_values;

			unsigned long n_x_values = (
				*(*(*e).agb_grid).interpolator).n_x_values;
			unsigned long n_y_values = (
				*(*(*e).agb_grid).interpolator).n_y_values;

			in = fopen(file, "r");
			if (in == NULL) return 1;
			e -> agb_grid -> interpolator -> xcoords = (double *) malloc (
				n_x_values * sizeof(double));
			e -> agb_grid -> interpolator -> ycoords = (double *) malloc (
				n_y_values * sizeof(double));
			e -> agb_grid -> interpolator -> zcoords = (double **) malloc (
				n_x_values * sizeof(double *));
			for (i = 0ul; i < n_x_values; i++) {
				e -> agb_grid -> interpolator -> zcoords[i] = (double *) malloc (
					n_y_values * sizeof(double));
				for (j = 0ul; j < n_y_values; j++) {
					if (fscanf(
						in, "%lf %lf %lf",
						&(e -> agb_grid -> interpolator -> xcoords[i]),
						&(e -> agb_grid -> interpolator -> ycoords[j]),
						&(e -> agb_grid -> interpolator -> zcoords[i][j])
					)) {
						continue;
					} else {
						free(e -> agb_grid -> interpolator -> xcoords);
						free(e -> agb_grid -> interpolator -> ycoords);
						free(e -> agb_grid -> interpolator -> zcoords);
						fclose(in);
						return 7;
					}
				}
			}
			fclose(in);
			return 0; 		/* error handling: success */

		default:
			return 8; 		/* error handling: failure */

	}

}

