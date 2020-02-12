/* 
 * This file implements testing of the MDF object's memory management. 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "mdf.h" 


/* 
 * Test the function which constructs an mdf object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: mdf.h 
 */ 
extern unsigned short test_mdf_initialize(void) {

	MDF *test = mdf_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).abundance_distributions == NULL && 
		(*test).ratio_distributions == NULL && 
		(*test).bins == NULL 
	); 
	mdf_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored in an mdf object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: mdf.h 
 */ 
extern unsigned short test_mdf_free(void) { 

	/* The destructor function should not modify the address */ 
	MDF *test = mdf_initialize(); 
	void *initial_address = (void *) test; 
	mdf_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

