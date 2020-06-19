/* 
 * This file implements testing of the repfunc object core routines. 
 */ 

#include <stdlib.h> 
#include "../repfunc.h" 
#include "../../utils.h" 

/* The number of points to place in a test repfunc object */ 
static unsigned short REPFUNC_TEST_N_POINTS = 100u; 


/* 
 * Tests the repfunc_evaluate function in the parent directory. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: repfunc.h 
 */ 
extern unsigned short test_repfunc_evaluate(void) {

	/* 
	 * This tests the evaluate function by putting the function f(x) = x 
	 * into a repfunc object and then ensuring that all evaluations return the 
	 * original value of x. 
	 */ 

	REPFUNC *test = repfunc_initialize(); 

	if (test != NULL) {
		test -> n_points = REPFUNC_TEST_N_POINTS; 
		test -> xcoords = (double *) malloc (
			REPFUNC_TEST_N_POINTS * sizeof(double)); 
		test -> ycoords = (double *) malloc (
			REPFUNC_TEST_N_POINTS * sizeof(double)); 
		unsigned short i; 
		seed_random(); 
		for (i = 0u; i < REPFUNC_TEST_N_POINTS; i++) {
			test -> xcoords[i] = rand_range(i, i + 1u); 
			test -> ycoords[i] = (*test).xcoords[i]; 
		} 

		unsigned short status = 1u; 
		for (i = 0u; i < 1000u; i++) {
			double x = rand_range(-10000, 10000); 
			status &= repfunc_evaluate(*test, x) == x; 
			if (!status) break; 
		} 

		repfunc_free(test); 
		return status; 

	} else {
		return 0u; 
	}

}

