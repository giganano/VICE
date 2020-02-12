/* 
 * This file implements testing of the ssp object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "ssp.h" 


/*
 * Test the function which constructs an ssp object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: ssp.h 
 */ 
extern unsigned short test_ssp_initialize(void) {

	SSP *test = ssp_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).imf != NULL && 
		(*test).crf == NULL && 
		(*test).msmf == NULL
	); 
	ssp_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored in an ssp object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: ssp.h 
 */ 
extern unsigned short test_ssp_free(void) {

	/* The destructor function should not modify the address */ 
	SSP *test = ssp_initialize(); 
	void *initial_address = (void *) test; 
	ssp_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

