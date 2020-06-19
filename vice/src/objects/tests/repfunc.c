/* 
 * This file implements testing of the repfunc object's memory management. 
 */ 

#include "../repfunc.h" 


/* 
 * Tests the memory allocation routine for the repfunc object. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: repfunc.h 
 */ 
extern unsigned short test_repfunc_initialize(void) {

	REPFUNC *test = repfunc_initialize(); 
	unsigned short status = test != NULL; 
	if (status) {
		status &= (*test).n_points == 0ul; 
		status &= (*test).xcoords == NULL; 
		status &= (*test).ycoords == NULL; 
		repfunc_free(test); 
		return status; 
	} else {
		return 0u; 
	}

}


/* 
 * Test the function which frees the memory stored by a repfunc object. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: repfunc.h 
 */ 
extern unsigned short test_repfunc_free(void) {

	/* The destructor function should not modify the address */ 
	REPFUNC *test = repfunc_initialize(); 
	void *initial_address = (void *) test; 
	repfunc_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

