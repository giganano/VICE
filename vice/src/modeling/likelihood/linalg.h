
#ifndef MODELING_LIKELIHOOD_LINALG_H 
#define MODELING_LIKELIHOOD_LINALG_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

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
 * source: linalg.c   
 */ 
extern double **multiply_matrices(double **mat1, double **mat2, 
	unsigned long l, unsigned long m, unsigned long n); 

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
 * source: linalg.c   
 */ 
extern double **multiply_matrix_scalar(double **mat, double scalar, 
	unsigned long m, unsigned long n); 

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
 * source: linalg.c   
 */ 
extern double **add_matrices(double **mat1, double **mat2, 
	unsigned long m, unsigned long n); 

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
 * source: linalg.c   
 */ 
extern double **subtract_matrices(double **mat1, double **mat2, 
	unsigned long m, unsigned long n); 

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
 * source: linalg.c   
 */ 
extern double **transpose(double **mat, unsigned long m, unsigned long n); 

extern double determinant(double **mat, unsigned long size); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_LINALG_H */ 

