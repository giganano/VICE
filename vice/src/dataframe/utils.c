/*
 * This file implements utility functions for the dataframe subroutines written
 * in C.
 */

#include <stdlib.h>
#include <string.h>
#include "../dataframe.h"
#include "utils.h"


/*
 * Determine the index of an element in a history object.
 *
 * Parameters
 * ==========
 * elements: 	The element symbols themselves
 * element: 	The symbol of the element to get the index for
 * n_elements: 	The number of elements tracked by the simulation
 *
 * Returns
 * =======
 * The element's index: the integer such that hist.elements[index] is the
 * same symbol as char *element. -1 if the element is not found in the history
 * object.
 *
 * header: utils.h
 */
extern int get_element_index(char **elements, char *element,
	unsigned int n_elements) {

	unsigned int i;
	for (i = 0; i < n_elements; i++) {
		if (!strcmp(elements[i], element)) return (signed) i;
	}
	return -1;

}


/*
 * Determine the total solar abundance by summing the solar abundances of each
 * element in the history object.
 *
 * Parameters
 * ==========
 * solar: 		The solar abundance of each element
 * n_elements; 	The number of elements in the simulation
 * elements: 	The (lower-case) symbol of each element
 *
 * Returns
 * =======
 * The metallicity of the sun considering only simulated elements
 *
 * header: utils.h
 */
extern double Zsolar_by_element(double *solar, unsigned int n_elements,
	char **elements) {

	double Zsolar = 0;
	unsigned int i;
	for (i = 0u; i < n_elements; i++) {
		if (strcmp(elements[i], "he")) Zsolar += solar[i];
	}
	return Zsolar;

}


/*
 * Obtain the column number of a given label in the data. Used for keying the
 * data from a VICE dataframe wrapper.
 *
 * Parameters
 * ==========
 * ff: 		The fromfile object itself
 * label: 	The label to key on
 *
 * Returns
 * =======
 * The column number corresponding to the label. -1 if not found in the
 * dataframe.
 *
 * header: utils.h
 */
extern int column_number(FROMFILE *ff, char *label) {

	unsigned int i;
	for (i = 0u; i < (*ff).n_cols; i++) {
		if (!strcmp((*ff).labels[i], label)) return (signed) i;
	}
	return -1;

}


