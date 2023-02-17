/*
 * This file implements matrix algebra routines.
 */

#include <stdlib.h>
#include <math.h>
#include "../objects.h"
#include "../debug.h"
#include "matrix.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static MATRIX *matrix_minor(MATRIX m, unsigned short axis[2]);
static MATRIX *matrix_adjoint(MATRIX m);
static MATRIX *matrix_cofactors(MATRIX m);
static MATRIX *matrix_transpose(MATRIX m);


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
 * header: matrix.h
 */
extern MATRIX *matrix_invert(MATRIX m) {

	double det = matrix_determinant(m);
	if (det) {
		MATRIX *adjoint = matrix_adjoint(m);
		unsigned short i, j;
		for (i = 0u; i < m.n_rows; i++) {
			for (j = 0u; j < m.n_cols; j++) {
				adjoint -> matrix[i][j] /= det;
			}
		}
		return adjoint;
	} else {
		return NULL;
	}

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

	if (m.n_rows != m.n_cols) {
		fatal_print("%s\n",
			"Cannot compute the determinant of a non-square matrix.");
	} else {
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
				MATRIX *minor = matrix_minor(m, axis);
				result += pow(-1, i) * m.matrix[0][i] * matrix_determinant(
					*minor);
				matrix_free(minor);
			}
			return result;
		}
	}

}


/*
 * Compute the adjoint of a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 *
 * Returns
 * =======
 * The adjoint, defined as the transpose of the matrix of cofactors.
 *
 * Notes
 * =====
 * Some textbooks and authors use the term adjugate instead of adjoint. Though
 * we use the term adjoint here, they refer to the same thing. NULL if the
 * determinant of the input matrix is zero.
 */
static MATRIX *matrix_adjoint(MATRIX m) {

	MATRIX *cofactors = matrix_cofactors(m);
	if (cofactors == NULL) {
		return NULL;
	} else {
		MATRIX *adjoint = matrix_transpose(*cofactors);
		matrix_free(cofactors);
		return adjoint;
	}

}



/*
 * Compute the matrix of cofactors for a square matrix.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 *
 * Returns
 * =======
 * The matrix of cofactors, defined as A_ij = (-1)^(i + j) det(m_ij) where m_ij
 * is the ij'th minor of m. NULL if the determinant of the input matrix is
 * zero.
 */
static MATRIX *matrix_cofactors(MATRIX m) {

	double det = matrix_determinant(m);
	if (det) {
		MATRIX *adjoint = matrix_initialize(m.n_rows, m.n_rows);
		unsigned short i, j;
		for (i = 0u; i < m.n_rows; i++) {
			for (j = 0u; j < m.n_cols; j++) {
				unsigned short axis[2] = {i, j};
				MATRIX *minor = matrix_minor(m, axis);
				adjoint -> matrix[i][j] = pow(-1, 
					i + j) * matrix_determinant(*minor);
				matrix_free(minor);
			}
		}
		return adjoint;
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
 *
 * Returns
 * =======
 * The transpose, defined as M_ij^T = M_ji.
 */
static MATRIX *matrix_transpose(MATRIX m) {

	MATRIX *transpose = matrix_initialize(m.n_cols, m.n_rows);
	unsigned short i, j;
	for (i = 0u; i < m.n_rows; i++) {
		for (j = 0u; j < m.n_cols; j++) {
			transpose -> matrix[j][i] = m.matrix[i][j];
		}
	}
	return transpose;

}


/*
 * Obtain one of a matrix's minors.
 *
 * Parameters
 * ==========
 * m: 		The input matrix itself.
 * axis: 	Which minor to obtain. axis[0] refers to the row and axis[1] to the
 * 			column to omit from the minor.
 *
 * Returns
 * =======
 * If m is an NxN matrix, the returned matrix is the corresponding (N-1)x(N-1)
 * minor with the specified row and column omitted from the original.
 */
static MATRIX *matrix_minor(MATRIX m, unsigned short axis[2]) {

	MATRIX *minor = matrix_initialize(m.n_rows - 1u, m.n_rows - 1u);
	unsigned short i, n1 = 0u;
	for (i = 0u; i < m.n_rows; i++) {
		if (i != axis[0]) {
			unsigned short j, n2 = 0;
			for (j = 0u; j < m.n_cols; j++) {
				if (j != axis[1]) {
					minor -> matrix[n1][n2] = m.matrix[i][j];
					n2++;
				} else {}
			}
			n1++;
		} else {}
	}

	return minor;

}


