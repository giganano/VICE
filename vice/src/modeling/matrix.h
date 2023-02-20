
#ifndef MODELING_MATRIX_H
#define MODELING_MATRIX_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Multiply two matrices.
 *
 * Parameters
 * ==========
 * m1: 		The first matrix in the multiplication.
 * m2:		The second matrix in the multiplication.
 *
 * Returns
 * =======
 * A pointer to the resultant matrix c, defined as c_ij = \sum_k m1_ik * m2_kj
 *
 * source: matrix.c
 */
extern MATRIX *matrix_multiply(MATRIX m1, MATRIX m2);

/*
 * Invert a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix.
 *
 * Returns
 * =======
 * The inverse m^-1 of the input matrix defined such that (m^-1)m = m(m^-1) = I
 * where I is the identity matrix. NULL if the determinant of the input matrix
 * is zero.
 *
 * source: matrix.c
 */
extern MATRIX *matrix_invert(MATRIX m);

/*
 * Compute the determinant of a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The MATRIX object containing the matrix itself.
 *
 * Returns
 * =======
 * det(M), computed via expansion by minors in the first row of the matrix.
 * The expansion by minors is handled recursively within an iterative sum.
 * The solution for a 2x2 matrix is implemented as the base case. As a failsafe,
 * the obvious solution for a 1x1 matrix is implemented as an additional base
 * case.
 *
 * source: matrix.c
 */
extern double matrix_determinant(MATRIX m);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MODELING_MATRIX_H */
