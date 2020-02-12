/* 
 * This file implements testing of the ism object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "ism.h" 


/* 
 * Test the function which constructs an ism object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: ism.h 
 */ 
extern unsigned short test_ism_initialize(void) {

	ISM *test = ism_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).mode != NULL && 
		(*test).specified == NULL && 
		(*test).star_formation_history == NULL && 
		(*test).eta == NULL && 
		(*test).enh == NULL && 
		(*test).tau_star == NULL 
	); 
	ism_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored in an ism object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: ism.h 
 */ 
extern unsigned short test_ism_free(void) { 

	/* The destructor function should not modify the address */ 
	ISM *test = ism_initialize(); 
	void *initial_address = (void *) test; 
	ism_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

