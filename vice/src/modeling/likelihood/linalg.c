/* 
 * This file implements linear algebra routines for handling matrices. 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../likelihood.h" 
#include "linalg.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double **get_minor(double **mat, unsigned long n, unsigned long i, 
	unsigned long j); 
static double *get_minor_row(double **mat, unsigned long n, unsigned long i, 
	unsigned long j); 

/* 
 * Multiply two matrices 
 * 
 * Parameters 
 * ========== 
 * mat1: 			The first matrix, assumed to be l x m 
 * mat2: 			The second matrix, assumed to be m x n 
 * l: 				The number of rows in mat1 
 * m: 				The number of columns in mat1 and number of rows in mat2 
 * n: 				The number of columns in mat2 
 * 
 * Returns 
 * ======= 
 * A pointer to the resulting l x n matrix 
 * 
 * header: linalg.h 
 */ 
extern double **multiply_matrices(double **mat1, double **mat2, 
	unsigned long l, unsigned long m, unsigned long n) {

	/* 
	 * mat1 is lxm and mat2 is mxn. result is lxn 
	 */ 

	unsigned long i, j; 
	double **result = (double **) malloc (l * sizeof(double *)); 
	for (i = 0ul; i < l; i++) {
		result[i] = (double *) malloc (n * sizeof(double)); 
		for (j = 0ul; j < n; j++) {
			result[i][j] = 0; 
		} 
	} 

	for (i = 0ul; i < l; i++) {
		for (j = 0ul; j < n; j++) {
			/* 
			 * Matrix multiplication formula: 
			 * 
			 * result[i][j] = sum(mat1[i][k] * mat2[k][j]) 
			 * 
			 * where k runs from 1 to m (or 0 to m - 1 in zero-based indexing) 
			 */ 
			unsigned long k; 
			for (k = 0ul; k < m; k++) {
				result[i][j] += mat1[i][k] * mat2[k][j]; 
			}
		}
	} 
	return result; 

} 


/* 
 * Multiply a matrix by a scalar 
 * 
 * Parameters 
 * ========== 
 * mat: 			The matrix to multiply (size m x n) 
 * scalar: 			The scalar to propogate through mat 
 * m: 				The number of rows in mat 
 * n: 				The number of columns in mat 
 * 
 * Returns 
 * ======= 
 * The resultant a_ij = scalar * mat_ij matrix 
 * 
 * header: linalg.h 
 */ 
extern double **multiply_matrix_scalar(double **mat, double scalar, 
	unsigned long m, unsigned long n) {

	unsigned long i, j; 
	double **result = (double **) malloc (m * sizeof(double *)); 
	for (i = 0ul; i < m; i++) {
		result[i] = (double *) malloc (n * sizeof(double)); 
		for (j = 0ul; j < n; j++) {
			result[i][j] = scalar * mat[i][j]; 
		} 
	} 
	return result; 

} 


/* 
 * Add to same-size matrices 
 * 
 * Parameters 
 * ========== 
 * mat1: 		The first matrix (size m x n) 
 * mat2: 		The second matrix (size m x n) 
 * m: 			The number of rows in each matrix 
 * n: 			The number of columns in each matrix 
 * 
 * Returns 
 * =======
 * The matrix defined by a_ij = mat1_ij + mat2_ij 
 * 
 * header: linalg.h 
 */ 
extern double **add_matrices(double **mat1, double **mat2, 
	unsigned long m, unsigned long n) {

	unsigned long i, j; 
	double **result = (double **) malloc (m * sizeof(double *)); 
	for (i = 0ul; i < m; i++) {
		result[i] = (double *) malloc (n * sizeof(double)); 
		for (j = 0ul; j < n; j++) {
			result[i][j] = mat1[i][j] + mat2[i][j]; 
		} 
	} 
	return result; 

} 


/* 
 * Subtract one matrix from another of the same size 
 * 
 * Parameters 
 * ========== 
 * mat1: 			The matrix to subtract from (size m x n) 
 * mat2: 			The matrix to subtract (size m x n) 
 * m: 				The number of rows in each matrix 
 * n: 				The number of columns in each matrix 
 * 
 * Returns 
 * ======= 
 * The matrix defined by a_ij = mat1_ij - mat2_ij 
 * 
 * header: linalg.h 
 */ 
extern double **subtract_matrices(double **mat1, double **mat2, 
	unsigned long m, unsigned long n) {

	/* 
	 * In the interest of not duplicating code, treat subtraction as adding 
	 * negative mat2. 
	 */ 
	double **minus_mat2 = multiply_matrix_scalar(mat2, -1, m, n); 
	double **result = add_matrices(mat1, minus_mat2, m, n); 
	free(minus_mat2); 
	return result; 

} 


/* 
 * Transpose a matrix 
 * 
 * Parameters 
 * ========== 
 * mat: 			The matrix to transpose (size m x n) 
 * m: 				The number of rows in mat 
 * n: 				The number of columns in mat 
 * 
 * Returns 
 * ======= 
 * The matrix defined by a_ij = mat_ji 
 * 
 * header: linalg.h 
 */ 
extern double **transpose(double **mat, unsigned long m, unsigned long n) {

	unsigned long i, j; 
	double **result = (double **) malloc (n * sizeof(double *)); 
	for (i = 0ul; i < n; i++) {
		result[i] = (double *) malloc (m * sizeof(double)); 
		for (j = 0ul; j < m; j++) {
			result[i][j] = mat[j][i]; 
		} 
	} 
	return result; 

} 


extern double determinant(double **mat, unsigned long size) {

	if (size == 2) { 
		/* Determinant of a 2-D matrix */ 
		return (mat[0][0] * mat[1][1]) - (mat[0][1] * mat[1][0]); 
	} else {
		/* 
		 * Expand by minors in 0th column, calling this function 
		 * recursively using an iterative sum approach 
		 */ 
		double det = 0; 
		unsigned long i; 
		for (i = 0ul; i < size; i++) {
			double **minor_ = get_minor(mat, size, i, 0); 
			if (i % 1) { 
				/* expanding in column 0, (-1)^(i+j) = (-1)^i always */ 
				det -= mat[i][0] * determinant(minor_, size - 1ul); 
			} else {
				det += mat[i][0] * determinant(minor_, size - 1ul); 
			} 
			free(minor_); 
		} 
		return det; 
	} 

}


static double **get_minor(double **mat, unsigned long n, unsigned long i, 
	unsigned long j) {

	unsigned long i_, row = 0ul; 
	double **minor_ = (double **) malloc ((n - 1ul) * sizeof(double *)); 
	for (i_ = 0ul; i_ < n; i_++) {
		if (i_ != i) {
			minor_[row] = get_minor_row(mat, n, i_, j); 
			row++; 
		} else {} 
	} 
	return minor_; 

} 


/* 
 * Obtain the i'th row of the xj'th minor of matrix mat 
 * 
 * Parameters 
 * ========== 
 * mat: 		The matrix to obtain the row of the minor for 
 * n: 			The matrix is n x n in size (must be square) 
 * i: 			The row to pull from 
 * j: 			The column number to exclude from mat 
 * 
 * Returns 
 * ======= 
 * The i'th row of matrix mat with element j omitted 
 */ 
static double *get_minor_row(double **mat, unsigned long n, unsigned long i, 
	unsigned long j) {

	unsigned long j_, col = 0ul; 
	double *row = (double *) malloc ((n - 1ul) * sizeof(double)); 
	for (j_ = 0ul; j_ < n; j_++) {
		if (j_ != j) {
			row[col] = mat[i][j_]; 
			col++; 
		} else {} 
	} 
	return row; 

}

