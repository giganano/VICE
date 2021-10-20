/*
 * This file implements calculations of logarithmic metallicities [X/Y] for both
 * history and tracer particle output files. The functions are largely the
 * same, and for that reason are combined to not repeat code.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../dataframe.h"
#include "fromfile.h"
#include "calclogz.h"
#include "calcz.h"
#include "utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double *logarithmic_abundance(FROMFILE *ff, char *element,
	char **elements, unsigned int n_elements, double *solar,
	double *(*Z_element) (FROMFILE *, char *));
static double *logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar,
	double *(*Z_element) (FROMFILE *, char *));
static double *logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar,
	double *(*Z_total_by_element) (FROMFILE *, unsigned int, char **));


/*
 * Calculate the logarithmic abundance ratio of two elements [X/Y] relative
 * to the sun from a history object
 *
 * Parameters
 * ==========
 * ff: 				A pointer to the fromfile object
 * element1: 		The symbol of element X
 * element2: 		The symbol of element Y
 * elements: 		The symbols of all of the elements in the simulation
 * n_elements: 		The number of elements in the simulation
 * solar: 			Each element's solar abundance
 *
 * Returns
 * =======
 * A double pointer to [X/Y] at all output times; NULL if either element was
 * not found in the output.
 *
 * Notes
 * =====
 * This function responds properly when element2 == 'h' (i.e. when asked to
 * calculate [X/H])
 *
 * header: calclogz.h
 */
extern double *history_logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar) {

	return logarithmic_abundance_ratio(ff, element1, element2, elements,
		n_elements, solar, history_Z_element);

}


/*
 * Calculate the logarithmic abundance ratio of two elements [X/Y] relative
 * to the sun from star particle data
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the tracer particle data
 * element1: 	The symbol of the element X
 * element2: 	The symbol of the element Y
 * elements: 	The symbols of all of the elements in the simulation
 * n_elements: 	The number of elements in the simulation
 * solar: 		Each element's solar abundance
 *
 * Returns
 * =======
 * A double pointer to [X/Y] for all tracer particles. NULL if either element
 * was not found in the data.
 *
 * Notes
 * =====
 * This function responds properly when element2 == 'h' (i.e. when asked to
 * calculate [X/H])
 *
 * header: calclogz.h
 */
extern double *tracers_logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar) {

	return logarithmic_abundance_ratio(ff, element1, element2, elements,
		n_elements, solar, tracers_Z_element);

}


/*
 * Calculate the logarithmic abundance ratio relative to solar of two elements
 * (i.e. [X/Y]) for history or tracer particle data.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object containing the abundance data
 * element1: 	The (lower-case) symbol of element X
 * element2: 	The (lower-case) symbol of element Y
 * elements: 	The (lower-case) symbols of all of the elements
 * n_elements: 	The number of elements with data in the file
 * solar: 		The solar abundance of each element
 * Z_element: 	The function to use to lookup the metallicity by mass Z of the
 * 				element X in the fromfile object. For tracer particle data,
 * 				this should be tracers_Z_element, and history_Z_element for
 * 				history data.
 *
 * Returns
 * =======
 * [X/H] at all output times or for all tracer particles.
 *
 * Notes
 * =====
 * This function responds properly when element2 == 'h' (i.e. when asked to
 * calculate [X/H] rather than [X/Y]).
 */
static double *logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar,
	double *(*Z_element) (FROMFILE *, char *)) {

	if (!strcmp(element2, "h")) {
		/* return simply [X/H] */
		return logarithmic_abundance(ff, element1, elements, n_elements, solar,
			Z_element);
	} else {
		/* Determine the abundances of [X/H] and [Y/H] independently */
		double *XonH = logarithmic_abundance(ff, element1, elements, n_elements,
			solar, Z_element);
		double *YonH = logarithmic_abundance(ff, element2, elements, n_elements,
			solar, Z_element);
		if (XonH != NULL && YonH != NULL) {
			/* If both elements were found in the output */
			unsigned long i;
			double *ratio = (double *) malloc ((*ff).n_rows * sizeof(double));
			for (i = 0ul; i < (*ff).n_rows; i++) {
				/* [X/Y] = [X/H] - [Y/H] */
				ratio[i] = XonH[i] - YonH[i];
			}
			free(XonH);
			free(YonH);
			return ratio;
		} else {
			/* One of the elements was not found -> return NULL */
			if (XonH != NULL) free(XonH);
			if (YonH != NULL) free(YonH);
			return NULL;
		}
	}

}


/*
 * Calculate the logarithmic abundance relative to solar of a given element
 * (i.e. [X/H]) for history or tracer particle data.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object containing the abundance data
 * element: 	The element to calculate the log abundance for
 * elements: 	The (lower-case) symbols of all of the elements
 * n_elements: 	The number of elements with data in the file
 * solar: 		The solar abundance of each element
 * Z_element: 	The function to use to lookup the metallicity by mass Z of the
 * 				element X in the fromfile object. For tracer particle data,
 * 				this should be tracers_Z_element, and history_Z_element for
 * 				history data.
 *
 * Returns
 * =======
 * [X/H] at all output times or for all tracer particles.
 */
static double *logarithmic_abundance(FROMFILE *ff, char *element,
	char **elements, unsigned int n_elements, double *solar,
	double *(*Z_element) (FROMFILE *, char *)) {

	/* Start with the metallicity by mass of the element */
	double *onH = Z_element(ff, element);
	if (onH != NULL) {
		unsigned long i;
		int index = get_element_index(elements, element, n_elements);

		switch (index) {

			case -1:
				free(onH);
				return NULL;

			default:
				for (i = 0ul; i < (*ff).n_rows; i++) {
					onH[i] = log10(onH[i] / solar[index]);
				}
				return onH;

		}

	} else {
		return NULL;
	}

}


/*
 * Determine the scaled logarithmic total metallicity relative to solar [M/H]
 * at all output times from a history object.
 *
 * Parameters
 * ==========
 * ff: 				A pointer to the fromfile object
 * n_elements: 		The number of elements in the simulation
 * elements: 		The symbols of each element
 * solar: 			Each element's solar abundance
 *
 * Returns
 * =======
 * A double pointer to [M/H] at all output times
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * header: calclogz.h
 */
extern double *history_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar) {

	return logarithmic_scaled(ff, n_elements, elements, solar,
		history_Ztotal_by_element);

}


/*
 * Determine the scaled logarithmic total metallicity relative to solar [M/H]
 * for all star particles.
 *
 * Parameters
 * ==========
 * ff: 				A pointer to the fromfile object
 * n_elements: 		The number of elements in the simulation
 * elements: 		The symbols of each element
 * solar: 			Each element's solar abundance
 *
 * Returns
 * =======
 * A double pointer to [M/H] for all stars. NULL on failure.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * header: calclogz.h
 */
extern double *tracers_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar) {

	return logarithmic_scaled(ff, n_elements, elements, solar,
		tracers_Ztotal_by_element);

}


/*
 * Determine the scaled logarithmic total metallicity relative to solar [M/H]
 * for all output times in history data or all stars in tracer particle data.
 *
 * Parameters
 * ==========
 * ff: 					A pointer to the fromfile object
 * n_elements: 			The number of elements in the simulation
 * elements: 			The symbols of each element
 * solar: 				Each element's solar abundance
 * Z_total_by_element: 	The function to use to calculate the total metallicity
 * 						of the elements with recorded data in the file. For
 * 						tracer particle data, this should be
 * 						tracers_Ztotal_by_element, and history_Ztotal_by_element
 * 						for history data.
 *
 * Returns
 * =======
 * A double pointer to [M/H] for all stars or all lookback times.
 * NULL on failure.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 */
static double *logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar,
	double *(*Z_total_by_element) (FROMFILE *, unsigned int, char **)) {

	double solar_by_element = Zsolar_by_element(solar, n_elements, elements);
	double *total_by_element = Z_total_by_element(ff, n_elements, elements);
	if (total_by_element != NULL) {
		unsigned long i;
		double *scaled = (double *) malloc ((*ff).n_rows * sizeof(double));
		for (i = 0ul; i < (*ff).n_rows; i++) {
			scaled[i] = log10(total_by_element[i] / solar_by_element);
		}
		free(total_by_element);
		return scaled;
	} else {
		return NULL;
	}

}

