
#ifndef DATAFRAME_CALCZ_H
#define DATAFRAME_CALCZ_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Calculate the metallicity by mass Z of a given element in a history
 * object.
 *
 * Parameters
 * ==========
 * ff:			A pointer to the fromfile object
 * element: 	The element to calculate the metallicity by mass of
 *
 * Returns
 * =======
 * A double pointer to Z(element) at all output times; NULL if the element is
 * not found in the output
 *
 * source: calcz.c
 */
extern double *history_Z_element(FROMFILE *ff, char *element);

/*
 * Calculate the metallicity by mass Z of a given element for all stars in a
 * tracer particle output file.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the stellar data
 * element: 	The element to lookup the metallicity by mass for
 *
 * Returns
 * =======
 * Z(x) for each star in the output data
 *
 * source: calcz.c
 */
extern double *tracers_Z_element(FROMFILE *ff, char *element);

/*
 * Calculate the sum total metallicity of each element from output stored in a
 * fromfile object with history data.
 *
 * Parameters
 * ==========
 * ff: 				The fromfile object
 * n_elements: 		The number of elements with data in the file
 * elements: 		The (lower-case) symbols of the elements
 *
 * Returns
 * =======
 * The sum total metallicity of the ISM at each considering only simulated
 * elements.
 *
 * source: calcz.c
 */
extern double *history_Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements);

/*
 * Calculate the sum total metallicity of each element from output stored in a
 * fromfile object with tracer particle data.
 *
 * Parameters
 * ==========
 * ff: 				The fromfile object
 * n_elements: 		The number of elements with data in the file
 * elements: 		The (lower-case) symbols of the elements
 *
 * Returns
 * =======
 * The sum total metallicity of each star considering only simulated elements.
 *
 * source: calcz.c
 */
extern double *tracers_Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements);

/*
 * Determine the scaled metallicity by mass at all output times according to:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements with data in the file
 * elements: 			The (lower-case) symbols of each element
 * solar: 				The solar abundance of each element
 * Z_solar: 			The adopted solar abundance from the simulation
 *
 * Returns
 * =======
 * The scaled metallicity of the ISM at all output times.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * source: calcz.c
 */
extern double *history_Zscaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar, double Z_solar);

/*
 * Determine the scaled metallicity by mass for all tracer particles according
 * to:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements with data in the file
 * elements: 			The (lower-case) symbols of each element
 * solar: 				The solar abundance of each element
 * Z_solar: 			The adopted solar abundance from the simulation
 *
 * Returns
 * =======
 * The scaled metallicity of each tracer particle.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * source: calcz.c
 */
extern double *tracers_Zscaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar, double Z_solar);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* DATAFRAME_CALCZ_H */

