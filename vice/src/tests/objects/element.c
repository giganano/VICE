/* 
 * This file implements testing of the element object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "element.h" 


/* 
 * Test the function which constructs an element object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: element.h 
 */ 
extern unsigned short test_element_initialize(void) {

	ELEMENT *test = element_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).symbol != NULL && 
		(*test).agb_grid != NULL && 
		(*test).ccsne_yields != NULL && 
		(*test).sneia_yields != NULL && 
		(*test).channels == NULL && 
		(*test).n_channels == 0u 
	); 
	element_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored by an element object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: element.h 
 */ 
extern unsigned short test_element_free(void) {

	/* The destructor function should not modify the address */ 
	ELEMENT *test = element_initialize(); 
	void *initial_address = (void *) test; 
	element_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

