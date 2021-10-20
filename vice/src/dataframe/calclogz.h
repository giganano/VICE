
#ifndef DATAFRAME_CALCLOGZ_H
#define DATAFRAME_CALCLOGZ_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

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
 * source: calclogz.c
 */
extern double *history_logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar);

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
 * source: calclogz.c
 */
extern double *tracers_logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
	char *element2, char **elements, unsigned int n_elements, double *solar);

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
 * source: calclogz.c
 */
extern double *history_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar);

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
 * source: calclogz.c
 */
extern double *tracers_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* DATAFRAME_CALCLOGZ_H */

