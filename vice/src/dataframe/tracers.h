
#ifndef DATAFRAME_TRACERS_H
#define DATAFRAME_TRACERS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"
#include "calclookback.h"
#include "calclogz.h"
#include "calcz.h"

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
 * source: tracers.c
 */
extern double *tracers_row(FROMFILE *ff, unsigned long row, char **elements,
	unsigned int n_elements, double *solar, double Z_solar);

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
 * source: tracers.c
 */
extern unsigned int tracers_row_length(FROMFILE *ff, unsigned int n_elements,
	char **elements);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* DATAFRAME_TRACERS_H */
