
#ifndef DATAFRAME_UTILS_H
#define DATAFRAME_UTILS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: utils.c
 */
extern int get_element_index(char **elements, char *element,
	unsigned int n_elements);

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
 * source: utils.c
 */
extern double Zsolar_by_element(double *solar, unsigned int n_elements,
	char **elements);

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
 * source: utils.c
 */
extern int column_number(FROMFILE *ff, char *label);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* DATAFRAME_UTILS_H */

