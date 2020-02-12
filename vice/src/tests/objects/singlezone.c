/* 
 * This file implements testing of the singlezone object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "singlezone.h" 


/* 
 * Test the function which constructs a singlezone object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: singlezone.h 
 */ 
extern unsigned short test_singlezone_initialize(void) {

	SINGLEZONE *test = singlezone_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).name != NULL && 
		(*test).history_writer == NULL && 
		(*test).mdf_writer == NULL && 
		(*test).output_times == NULL && 
		(*test).elements == NULL && 
		(*test).ism != NULL && 
		(*test).mdf != NULL && 
		(*test).ssp != NULL
	); 
	singlezone_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored by a singlezone object. 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: singlezone.h 
 */ 
extern unsigned short test_singlezone_free(void) {

	/* The destructor function should not modify the address */ 
	SINGLEZONE *test = singlezone_initialize(); 
	void *initial_address = (void *) test; 
	singlezone_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

