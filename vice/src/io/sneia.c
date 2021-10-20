/*
 * This file implements file I/O for type Ia supernova yield functionality.
 */

#include <stdlib.h>
#include "../io.h"
#include "utils.h"
#include "sneia.h"

/*
 * Lookup the mass yield of a given element from type Ia supernovae
 *
 * Parameters
 * ==========
 * file: 		The name of the yield file, passed from python
 *
 * Returns
 * =======
 * The total mass yield in Msun of the given element reported by the built-in
 * study's data. -1 on failure to read from the data file
 *
 * header: sneia.h
 */
extern double single_ia_mass_yield_lookup(char *file) {

	int h_length = header_length(file);
	if (h_length == -1) return -1; 				/* error handling */
	/* -1 because these files have a blank line on the end */
	int n_isotopes = line_count(file) - h_length - 1;
	FILE *in = fopen(file, "r");
	if (in == NULL) return -1;

	int i;
	char *line = (char *) malloc (LINESIZE * sizeof(char));
	for (i = 0; i < h_length; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in);
			free(line);
			return -1;
		} else {
			continue;
		}
	}

	double yield = 0;
	for (i = 0; i < n_isotopes; i++) {
		double x;
		if (fscanf(in, "%s %le", line, &x)) {
			yield += x;
		} else {
			fclose(in);
			free(line);
			return -1;
		}
	}

	fclose(in);
	free(line);
	return yield;

}

