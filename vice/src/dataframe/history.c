/*
 * This file implements the core routines of the history subclass of the
 * VICE dataframe.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../dataframe.h"
#include "../utils.h"
#include "../io.h"
#include "fromfile.h"
#include "history.h"
#include "calclogz.h"
#include "calcz.h"
#include "utils.h"


/*
 * Pull a row of data from a history object. This will automatically calculate
 * the abundances by mass, their logarithmic counterparts, and all ratios for
 * that output time.
 *
 * Parameters
 * ==========
 * ff: 				A pointer to the fromfile object
 * row: 			The row number to pull
 * elements: 		The symbols of the elements to pull
 * n_elements: 		The number of elements in the simulation
 * solar: 			The solar abundance of each element
 * Z_solar: 		The adopted solar metallicity by mass
 *
 * Returns
 * =======
 * The corresponding row of the data; NULL on failure.
 *
 * header: history.h
 */
extern double *history_row(FROMFILE *ff, unsigned long row, char **elements,
	unsigned int n_elements, double *solar, double Z_solar) {

	/* Allowed range of row number */
	if (row >= (*ff).n_rows) return NULL;
	unsigned int length = history_row_length(ff, n_elements, elements);

	/* Pull the columns already there and resize */
	double *data = fromfile_row(ff, row);
	if (data != NULL) {
		data = (double *) realloc (data, length * sizeof(double));
	} else {
		return NULL;
	}

	/* Append the metallicity by mass of each element */
	unsigned int i, n = (*ff).n_cols;
	for (i = 0; i < n_elements; i++) {
		double *Z = history_Z_element(ff, elements[i]);
		if (Z != NULL) {
			data[n] = Z[row];
			if (!strcmp(elements[i], "he")) data[length - 1u] = Z[row];
			free(Z);
			n++;
		} else {
			free(data);
			return NULL;
		}
	}

	/* Append the logarithmic abundance relative to solar of each element */
	for (i = 0; i < n_elements; i++) {
		double *onH = history_logarithmic_abundance_ratio(ff, elements[i], "h",
			elements, n_elements, solar);
		if (onH != NULL) {
			data[n] = onH[row];
			free(onH);
			n++;
		} else {
			free(data);
			return NULL;
		}
	}

	/*
	 * Append the logarithmic abundance ratios relative to solar for each
	 * combination of elements
	 */
	for (i = 1; i < n_elements; i++) {
		unsigned int j;
		for (j = 0; j < i; j++) {
			double *XonY = history_logarithmic_abundance_ratio(ff, elements[i],
				elements[j], elements, n_elements, solar);
			if (XonY != NULL) {
				data[n] = XonY[row];
				free(XonY);
				n++;
			} else {
				free(data);
				return NULL;
			}
		}
	}

	double *scaled = history_Zscaled(ff, n_elements, elements, solar, Z_solar);
	if (scaled != NULL) {
		data[n] = scaled[row];
		free(scaled);
		n++;
	} else {
		free(data);
		return NULL;
	}

	double *MonH = history_logarithmic_scaled(ff, n_elements, elements, solar);
	if (MonH != NULL) {
		data[n] = MonH[row];
		free(MonH);
		n++;
	} else {
		free(data);
		return NULL;
	}

	double *lookback = history_lookback(ff);
	if (lookback != NULL) {
		data[n] = lookback[row];
		free(lookback);
		n++;
	} else {
		free(data);
		return NULL;
	}

	return data;

}


/*
 * Determine the number of elements in one row of history output
 *
 * Parameters
 * ==========
 * ff: 				A pointer to the fromfile object
 * n_elements: 		The number of elements in the output
 * elements: 		The symbols of the chemical elements in the output
 *
 * Returns
 * =======
 * The total number of elements in the line of output
 *
 * header: history.h
 */
extern unsigned int history_row_length(FROMFILE *ff, unsigned int n_elements,
	char **elements) {

	/*
	 * One for each column already there, another two for each z(x) and [x/h]
	 * measurement, then n choose 2 cross combinations of [X/Y] abundance
	 * ratios, one each for Z and [M/H], and potentially one for Y.
	 */

	unsigned short i, has_helium = 0u;
	for (i = 0ul; i < n_elements; i++) {
		if (!strcmp(elements[i], "he")) {
			has_helium = 1u;
			break;
		} else {}
	}

	return has_helium + 3u + (*ff).n_cols + (2u * n_elements) + choose(
		n_elements, 2ul);

}


