
#ifndef DATAFRAME_HISTORY_H
#define DATAFRAME_HISTORY_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"
#include "calclookback.h"
#include "calclogz.h"
#include "calcz.h"

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
 * source: history.c
 */
extern double *history_row(FROMFILE *ff, unsigned long row, char **elements,
	unsigned int n_elements, double *solar, double Z_solar);

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
 * source: history.c
 */
extern unsigned int history_row_length(FROMFILE *ff, unsigned int n_elements,
	char **elements);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* DATAFRAME_HISTORY_H */


