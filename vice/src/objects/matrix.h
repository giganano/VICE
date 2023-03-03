
#ifndef OBJECTS_MATRIX_H
#define OBJECTS_MATRIX_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Allocate memory for and return a pointer to a MATRIX object.
 * Automatically initializes all matrix elements to zero.
 *
 * Parameters
 * ==========
 * n_rows: 		The number of rows in the desired matrix.
 * n_cols: 		The number of columns in the desired matrix.
 *
 * header: matrix.h
 */
extern MATRIX *matrix_initialize(unsigned short n_rows, unsigned short n_cols);

/*
 * Free up the memory associated with a matrix object.
 *
 * source: matrix.c
 */
extern void matrix_free(MATRIX *m);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_MATRIX_H */
