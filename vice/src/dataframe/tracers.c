/*
 * This file implements the functionality of the tracers subclass of the VICE
 * dataframe.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../dataframe.h"
#include "../utils.h"
#include "fromfile.h"
#include "tracers.h"
#include "calcz.h"
#include "calclogz.h"
#include "utils.h"


/*
 * PUll a row of data from a tracers object. This will automatically calculate
 * the logarithmic abundances, and all ratios for that star particle.
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
 * header: tracers.h
 */
extern double *tracers_row(FROMFILE *ff, unsigned long row, char **elements,
	unsigned int n_elements, double *solar, double Z_solar) {

	/* Allowed range of row number */
	if (row >= (*ff).n_rows) return NULL;
	unsigned int length = tracers_row_length(ff, n_elements, elements);

	/* Pull the columns already there and resize */
	double *data = fromfile_row(ff, row);
	if (data != NULL) {
		data = (double *) realloc (data, length * sizeof(double));
	} else {
		return NULL;
	}

	/* Append the logarithmic abundance relative to solar of each element */
	unsigned int i, n = (*ff).n_cols;
	for (i = 0u; i < n_elements; i++) {
		double *onH = tracers_logarithmic_abundance_ratio(ff, elements[i], "h",
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
	for (i = 1u; i < n_elements; i++) {
		unsigned int j;
		for (j = 0u; j < i; j++) {
			double *XonY = tracers_logarithmic_abundance_ratio(ff, elements[i],
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

	double *scaled = tracers_Zscaled(ff, n_elements, elements, solar, Z_solar);
	if (scaled != NULL) {
		data[n] = scaled[row];
		free(scaled);
		n++;
	} else {
		free(data);
		return NULL;
	}

	double *MonH = tracers_logarithmic_scaled(ff, n_elements, elements, solar);
	if (MonH != NULL) {
		data[n] = MonH[row];
		free(MonH);
		n++;
	} else {
		free(data);
		return NULL;
	}

	double *age = tracers_age(ff);
	if (age != NULL) {
		data[n] = age[row];
		free(age);
		n++;
	} else {
		free(data);
		return NULL;
	}

	for (i = 0u; i < n_elements; i++) {
		if (!strcmp(elements[i], "he")) {
			int idx = column_number(ff, "z(he)");
			if (idx >= 0) {
				data[n] = data[idx];
				n++;
				break;
			} else {
				free(data);
				return NULL;
			}
		} else {}
	}

	return data;

}


/*
 * Determine the number of elements in one row of tracers output
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the tracers data
 * n_elements: 	The number of elements with recorded data
 * elements: 	The symbols of the chemical elements in the output
 *
 * Returns
 * =======
 * The total number of elements in the line of output
 *
 * header: tracers,h
 */
extern unsigned int tracers_row_length(FROMFILE *ff, unsigned int n_elements,
	char **elements) {

	/*
	 * One for each column already there, another one for each [X/H]
	 * measurement, and then n choose 2 cross combinations of [X/Y]
	 * abundance ratios, one each for Z, [M/H], and age, and potentially one
	 * for Y.
	 */
	unsigned short i, has_helium = 0u;
	for (i = 0ul; i < n_elements; i++) {
		if (!strcmp(elements[i], "he")) {
			has_helium = 1u;
			break;
		} else {}
	}

	return has_helium + 3u + (*ff).n_cols + n_elements + choose(
		n_elements, 2ul);

}

