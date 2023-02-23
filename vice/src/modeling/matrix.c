/*
 * This file implements matrix algebra routines.
 */

#include <stdlib.h>
#include <math.h>
#include "../objects.h"
#include "../debug.h"
#include "matrix.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static MATRIX *matrix_minor(MATRIX m, unsigned short axis[2], MATRIX *result);
static MATRIX *matrix_adjoint(MATRIX m, MATRIX *result);
static MATRIX *matrix_cofactors(MATRIX m, MATRIX *result);
static void matrix_reset(MATRIX *m);


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
 * header: matrix.h
 */
extern MATRIX *matrix_multiply(MATRIX m1, MATRIX m2, MATRIX *result) {

	if (m1.n_cols == m2.n_rows) {
		if (result == NULL) {
			result = matrix_initialize(m1.n_rows, m2.n_cols);
		} else {
			result -> n_rows = m1.n_rows;
			result -> n_cols = m2.n_cols;
			matrix_reset(result);
		}
		unsigned short i, j, k;
		for (i = 0u; i < (*result).n_rows; i++) {
			for (j = 0u; j < (*result).n_cols; j++) {
				for (k = 0u; k < m1.n_cols; k++) {
					result -> matrix[i][j] += m1.matrix[i][k] * m2.matrix[k][j];
				}
			}
		}
		return result;
	} else {
		fatal_print("%s\n",
			"Matrix dimensions incompatible for multiplication.");
	}

}


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
 * header: matrix.h
 */
extern MATRIX *matrix_invert(MATRIX m, MATRIX *result) {

	double det = matrix_determinant(m);
	if (det) {
		result = matrix_adjoint(m, result);
		unsigned short i, j;
		for (i = 0u; i < m.n_rows; i++) {
			for (j = 0u; j < m.n_cols; j++) result -> matrix[i][j] /= det;
		}
		return result;
	} else {
		return NULL;
	}

}


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
 * header: matrix.h
 */
extern MATRIX *matrix_transpose(MATRIX m, MATRIX *result) {

	if (result == NULL) {
		result = matrix_initialize(m.n_rows, m.n_cols);
	} else {
		result -> n_rows = m.n_cols;
		result -> n_cols = m.n_rows;
		matrix_reset(result);
	}
	unsigned short i, j;
	for (i = 0u; i < m.n_rows; i++) {
		for (j = 0u; j < m.n_cols; j++) result -> matrix[j][i] = m.matrix[i][j];
	}

	return result;

}


/*
 * Compute the determinant of a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The matrix itself.
 *
 * Returns
 * =======
 * det(M), computed via expansion by minors in the first row of the matrix.
 * The expansion by minors is handled recursively within an iterative sum.
 * The solution for a 2x2 matrix is implemented as the base case. As a failsafe,
 * the obvious solution for a 1x1 matrix is implemented as an additional base
 * case.
 *
 * header: matrix.h
 */
extern double matrix_determinant(MATRIX m) {

	if (m.n_rows == m.n_cols) {
		if (m.n_rows == 1u) {
			/* Additional failsafe base case -- a 1x1 matrix */
			return m.matrix[0][0];
		} else if (m.n_rows == 2u) {
			/* The base case -- a 2x2 matrix */
			return (
				m.matrix[0][0] * m.matrix[1][1] -
				m.matrix[0][1] * m.matrix[1][0]
			);
		} else {
			/* The recursive case -- an NxN matrix where N > 2 */
			double result = 0;
			unsigned short i;
			for (i = 0u; i < m.n_cols; i++) {
				unsigned short axis[2] = {0, i};
				MATRIX *minor = matrix_minor(m, axis, NULL);
				result += pow(-1, i) * m.matrix[0][i] * matrix_determinant(
					*minor);
				matrix_free(minor);
			}
			return result;
		}

	} else {
		fatal_print("%s\n",
			"Cannot compute the determinant of a non-square matrix.");
	}

}


/*
 * Compute the adjoint of a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			adjoint matrix, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * The adjoint, defined as the transpose of the matrix of cofactors. NULL if
 * the determinant of the input matrix is zero.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input, unless the determinant is zero.
 *
 * Notes
 * =====
 * Some textbooks and authors use the term adjugate instead of adjoint. Though
 * we use the term adjoint here, they refer to the same thing. 
 */
static MATRIX *matrix_adjoint(MATRIX m, MATRIX *result) {

	MATRIX *cofactors = matrix_cofactors(m, NULL);
	if (cofactors == NULL) {
		return NULL;
	} else {
		result = matrix_transpose(*cofactors, result);
		matrix_free(cofactors);
		return result;
	}

}


/*
 * Compute the matrix of cofactors for a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			cofactors matrix, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * The matrix of cofactors, defined as A_ij = (-1)^(i + j) det(m_ij) where m_ij
 * is the ij'th minor of m. NULL if the determinant of the input matrix is
 * zero.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input.
 */
static MATRIX *matrix_cofactors(MATRIX m, MATRIX *result) {

	double det = matrix_determinant(m);
	if (det) {
		if (result == NULL) {
			result = matrix_initialize(m.n_rows, m.n_cols);
		} else {
			result -> n_rows = m.n_rows;
			result -> n_cols = m.n_cols;
			matrix_reset(result);
		}
		unsigned short i, j;
		for (i = 0u; i < m.n_rows; i++) {
			for (j = 0u; j < m.n_cols; j++) {
				unsigned short axis[2] = {i, j};
				MATRIX *minor = matrix_minor(m, axis, NULL);
				result -> matrix[i][j] = pow(-1,
					i + j) * matrix_determinant(*minor);
				matrix_free(minor);
			}
		}
		return result;
	} else {
		return NULL;
	}

}


/*
 * Obtain one of a matrix's minors.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 * axis: 	Which minor to obtain. axis[0] refers to the row and axis[1] to the
 * 			column to omit from the minor.
 * result:	A pointer to an already-initialized MATRIX object to store the
 * 			minor, if applicable. If NULL, memory will be allocated
 * 			automatically.
 *
 * Returns
 * =======
 * If m is an NxN matrix, the returned matrix is the corresponding (N-1)x(N-1)
 * minor with the specified row and column omitted from the original.
 *
 * If a pointer is provided for the resultant matrix, this will be the same
 * memory address as the input.
 */
static MATRIX *matrix_minor(MATRIX m, unsigned short axis[2], MATRIX *result) {

	if (result == NULL) {
		result = matrix_initialize(m.n_rows - 1u, m.n_rows - 1u);
	} else {
		result -> n_rows = m.n_rows - 1u;
		result -> n_cols = m.n_cols - 1u;
		matrix_reset(result);
	}
	unsigned short i, n1 = 0u;
	for (i = 0u; i < m.n_rows; i++) {
		if (i != axis[0]) {
			unsigned short j, n2 = 0u;
			for (j = 0u; j < m.n_cols; j++) {
				if (j != axis[1]) {
					result -> matrix[n1][n2] = m.matrix[i][j];
					n2++;
				} else {}
			}
			n1++;
		} else {}
	}

	return result;

}


/*
 * Set all elements of a matrix equal to zero. Reallocates memory for the
 * matrix pointer to safeguard against segmentation faults.
 */
static void matrix_reset(MATRIX *m) {

	unsigned short i;
	m -> matrix = (double **) realloc (m -> matrix,
		(*m).n_rows * sizeof(double *));
	for (i = 0u; i < (*m).n_rows; i++) {
		unsigned short j;
		m -> matrix[i] = (double *) realloc (m -> matrix[i],
			(*m).n_cols * sizeof(double));
		for (j = 0u; j < (*m).n_cols; j++) m -> matrix[i][j] = 0.0;
	}

}


