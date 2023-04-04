
#ifndef MODELING_MATRIX_H
#define MODELING_MATRIX_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Add two matrices.
 *
 * Parameters
 * ==========
 * m1: 			The first of the two input matrices
 * m2: 			The second of the two input matrices
 * result: 		A pointer to an already-initialized MATRIX object to store the
 * 				resultant matrix, if applicable. If NULL, memory will be
 * 				allocated automatically.
 *
 * Returns
 * =======
 * A matrix M such that M_ij = m1_ij + m2_ij.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input.
 *
 * source: matric.c
 */
extern MATRIX *matrix_add(MATRIX m1, MATRIX m2, MATRIX *result);

/*
 * Subtract two matrices.
 *
 * Parameters
 * ==========
 * m1: 			The first of the two input matrices
 * m2: 			The second of the two input matrices
 * result: 		A pointer to an already-initialized MATRIX object to store the
 * 				resultant matrix, if applicable. If NULL, memory will be
 * 				allocated automatically.
 *
 * Returns
 * =======
 * A matrix M such that M_ij = m1_ij - m2_ij.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input.
 *
 * source: matrix.c
 */
extern MATRIX *matrix_subtract(MATRIX m1, MATRIX m2, MATRIX *result);

/*
 * Multiply two matrices.
 *
 * Parameters
 * ==========
 * m1: 		The first matrix in the multiplication.
 * m2:		The second matrix in the multiplication.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			resultant matrix, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * A pointer to the resultant matrix c, defined as c_ij = \sum_k m1_ik * m2_kj
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input, unless the determinant is zero.
 *
 * source: matrix.c
 */
extern MATRIX *matrix_multiply(MATRIX m1, MATRIX m2, MATRIX *result);

/*
 * Invert a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			inverse matrix, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * The inverse m^-1 of the input matrix defined such that (m^-1)m = m(m^-1) = I
 * where I is the identity matrix. NULL if the determinant of the input matrix
 * is zero.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input, unless the determinant is zero.
 *
 * source: matrix.c
 */
extern MATRIX *matrix_invert(MATRIX m, MATRIX *result);

/*
 * Transpose a matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			transpose, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * The transpose, defined as M_ij^T = M_ji.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input.
 *
 * source: matrix.c
 */
extern MATRIX *matrix_transpose(MATRIX m, MATRIX *result);

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