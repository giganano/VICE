
#ifndef OBJECTS_DATUM_H
#define OBJECTS_DATUM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Allocate memory for and return a pointer to a DATUM object.
 * Sets up the datum as a row vector rather than a column vector and
 * initializes each of the values to zero.
 *
 * Parameters
 * ==========
 * dim: 		The dimensionality of the datum.
 *
 * source: datum.c
 */
extern DATUM *datum_initialize(unsigned short dim);

/*
 * Free up the memory stored in a datum object.
 *
 * source: datum.c
 */
extern void datum_free(DATUM *d);

/*
 * Link the covariance matrix object to the datum at initialization time in
 * python.
 *
 * Parameters
 * ==========
 * d: 			The datum pointer to link to
 * address: 	The address of the matrix pointer to link to, expressed as a
 * 				string
 *
 * source: datum.c
 */
extern void link_cov_matrix(DATUM *d, char *address);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_DATUM_H */
