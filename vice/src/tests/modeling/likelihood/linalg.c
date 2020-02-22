/* 
 * This file implements tests of the linear algebra routines at 
 * vice/src/modeling/likelihood/linalg.h 
 */ 

#include <stdlib.h> 
#include <stdio.h> 
#include <time.h> 
#include <math.h> 
#include "../../../modeling/likelihood/linalg.h" 
#include "../../../utils.h" 
#include "linalg.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double **test_dummy(void); 
static void modify_test_dummy(double **test); 


/* 
 * Test the function which adds two matrices of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure. 
 * 
 * header: linalg.h 
 */ 
extern unsigned short test_add_matrices(void) { 

	/* 
	 * Test the function by adding two test dummies, the result of which is 
	 * known. 
	 */ 

	unsigned short i, j; 
	double **mat1 = test_dummy(); 
	double **mat2 = test_dummy(); 
	double **result = add_matrices(mat1, mat2, TEST_MATRIX_SIZE, 
		TEST_MATRIX_SIZE); 
	free(mat1); 
	free(mat2); 
	for (i = 0u; i < TEST_MATRIX_SIZE; i++) { 
		for (j = 0u; j < TEST_MATRIX_SIZE; j++) { 
			if (result[i][j] != 2 * (i + 1) * (j + 1)) { 
				free(result); 
				return 0u; 
			} else {} 
		} 
	} 
	free(result); 
	return 1u; 

} 


/* 
 * Test the function which subtracts two matrices of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: linalg.h 
 */ 
extern unsigned short test_subtract_matrices(void) {

	/* 
	 * Test the function by subtracting a test dummy from a test dummy, the 
	 * result of which is a matrix of zeroes. 
	 */ 

	unsigned short i, j; 
	double **mat1 = test_dummy(); 
	double **mat2 = test_dummy(); 
	double **result = subtract_matrices(mat1, mat2, TEST_MATRIX_SIZE, 
		TEST_MATRIX_SIZE); 
	free(mat1); 
	free(mat2); 
	for (i = 0u; i < TEST_MATRIX_SIZE; i++) {
		for (j = 0u; j < TEST_MATRIX_SIZE; j++) {
			if (result[i][j]) {
				free(result); 
				return 0u; 
			} else {} 
		} 
	} 
	free(result); 
	return 1u; 

} 


/* 
 * Test the function which transposes a matrix of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: linalg.h 
 */ 
extern unsigned short test_transpose(void) { 

	/* 
	 * Test the function by transposing a test dummy, which will be equal to 
	 * the test dummy since that is a symmetric matrix 
	 */ 

	unsigned short i, j; 
	double **mat = test_dummy(); 
	double **result = transpose(mat, TEST_MATRIX_SIZE, TEST_MATRIX_SIZE); 
	for (i = 0u; i < TEST_MATRIX_SIZE; i++) {
		for (j = 0u; j < TEST_MATRIX_SIZE; j++) {
			if (mat[i][j] != result[i][j]) {
				free(mat); 
				free(result); 
				return 0u; 
			} else {} 
		} 
	} 
	free(mat); 
	free(result); 
	return 1u; 

} 


/* 
 * Test the function which calculates the determinant of a matrix of given size 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: linalg.h 
 */ 
extern unsigned short test_determinant(void) { 

	/* 
	 * Test the function by calculating the determinant of a test dummy, which 
	 * has a known determinant of zero. 
	 */ 

	double **mat = test_dummy(); 
	double result = determinant(mat, TEST_MATRIX_SIZE); 
	free(mat); 
	return (result == 0); 

} 


/* 
 * Test the function which inverts a matrix of given size 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: linalg.h 
 */ 
extern unsigned short test_inversion(void) {

	/* 
	 * Having a known determinant of zero, the test dummy is first modified 
	 * with randomly generated numbers between 0 and 1 to give it a nonzero 
	 * determinant. This ensures that it will be invertible. 
	 * 
	 * It can then be checked that the product of the inverted and original 
	 * matrix is within double precision of the identity matrix. 
	 */ 

	double **mat = test_dummy(); 
	double **test = invert(mat, TEST_MATRIX_SIZE); 
	if (test != NULL) { 
		free(mat); 
		free(test); 
		return 0u; 
	} else { 

		do { 
			/* 
			 * do-while loop in case modification produces another 
			 * non-invertible matrix 
			 */ 
			modify_test_dummy(mat); 
		} while (determinant(mat, TEST_MATRIX_SIZE) == 0); 

		double **inv = invert(mat, TEST_MATRIX_SIZE); 
		double **result = multiply_matrices(mat, inv, TEST_MATRIX_SIZE, 
			TEST_MATRIX_SIZE, TEST_MATRIX_SIZE); 
		free(mat); 
		free(inv); 

		unsigned short i, j; 
		for (i = 0u; i < TEST_MATRIX_SIZE; i++) {
			for (j = 0u; j < TEST_MATRIX_SIZE; j++) { 
				if (absval(result[i][j] - (i == j)) > 1e-10) { 
					free(result); 
					return 0u; 
				} else {} 
			} 
		} 
		free(result); 
		return 1u; 

	} 

}


/* 
 * Returns a SIZE x SIZE matrix whose ij'th element = (i + 1) * (j + 1) 
 */ 
static double **test_dummy(void) {

	unsigned short i, j; 
	double **mat = (double **) malloc (TEST_MATRIX_SIZE * sizeof(double *)); 
	for (i = 0u; i < TEST_MATRIX_SIZE; i++) {
		mat[i] = (double *) malloc (TEST_MATRIX_SIZE * sizeof(double *)); 
		for (j = 0u; j < TEST_MATRIX_SIZE; j++) {
			mat[i][j] = (i + 1) * (j + 1); 
		} 
	} 
	return mat; 

} 


/* 
 * Modifies a test dummy matrix by adding pseudorandom numbers between 0 and 1 
 * to each element of the test dummy 
 */ 
static void modify_test_dummy(double **test) {

	srand(time(0)); 
	unsigned short i, j; 
	for (i = 0u; i < TEST_MATRIX_SIZE; i++) {
		for (j = 0u; j < TEST_MATRIX_SIZE; j++) {
			test[i][j] += (double) rand() / (double) RAND_MAX; 
		} 
	} 

}

