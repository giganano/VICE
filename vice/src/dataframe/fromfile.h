
#ifndef DATAFRAME_FROMFILE_H
#define DATAFRAME_FROMFILE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Read in the data in a file into the fromfile object
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 *
 * Returns
 * =======
 * 0 on success from reading the file; 1 on failure
 *
 * source: fromfile.c
 */
extern unsigned short fromfile_read(FROMFILE *ff);

/*
 * Pull a column from the fromfile object based on its label.
 *
 * Parameters
 * ==========
 * ff: 		The fromfile object itself
 * label: 	The label of the column to pull
 *
 * Returns
 * =======
 * A double pointer to that column of the data; NULL if the label is not found.
 *
 * source: fromfile.c
 */
extern double *fromfile_column(FROMFILE *ff, char *label);

/*
 * Modify a column of the data in a fromfile object
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 * label: 	The label of the column to modify
 * arr: 	The new array to put in place of the old column. Assumed to be of
 * 			length (*ff).n_rows.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: fromfile.c
 */
extern unsigned short fromfile_modify_column(FROMFILE *ff, char *label,
	double *arr);

/*
 * Add a column to the data in a fromfile object.
 *
 * Parameters
 * ==========
 * ff: 		A pointer to the fromfile object
 * label: 	The label to let the new column have
 * arr: 	The new column itself
 *
 * Returns
 * =======
 * 0 on success; 1 on failure
 *
 * source: fromfile.c
 */
extern unsigned short fromfile_new_column(FROMFILE *ff, char *label,
	double *arr);

/*
 * Pull a row from the fromfile object based on its row number
 *
 * Parameters
 * ==========
 * ff: 		The fromfile object itself
 * row: 	The row number of the data to pull
 *
 * Returns
 * =======
 * A double pointer to that row of the data; NULL if the row number is outside
 * the allowed range.
 *
 * source: fromfile.c
 */
extern double *fromfile_row(FROMFILE *ff, unsigned long row);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* DATAFRAME_FROMFILE_H */

