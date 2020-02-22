
#ifndef TESTS_MODELING_LIKELIHOOD_LINALG_H 
#define TESTS_MODELING_LIKELIHOOD_LINALG_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cpluspus */ 

/* The number of rows and columns in a test matrix */ 
#ifndef TEST_MATRIX_SIZE 
#define TEST_MATRIX_SIZE 5u 
#endif /* TEST_MATRIX_SIZE */ 

/* 
 * Test the function which adds two matrices of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure. 
 * 
 * source: linalg.c 
 */ 
extern unsigned short test_add_matrices(void); 

/* 
 * Test the function which subtracts two matrices of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: linalg.c 
 */ 
extern unsigned short test_subtract_matrices(void); 

/* 
 * Test the function which transposes a matrix of size m x n 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: linalg.c 
 */ 
extern unsigned short test_transpose(void); 

/* 
 * Test the function which calculates the determinant of a matrix of given size 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: linalg.c 
 */ 
extern unsigned short test_determinant(void); 

/* 
 * Test the function which inverts a matrix of given size 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: linalg.c 
 */ 
extern unsigned short test_inversion(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_MODELING_LIKELIHOOD_LINALG_H */ 

