/* 
 * This file implements testing of the dataset object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "dataset.h" 


/* 
 * Test the function which constructs a dataset object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: dataset.h 
 */ 
extern unsigned short test_dataset_initialize(void) {

	DATASET *test = dataset_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).data == NULL && 
		(*test).errors == NULL && 
		(*test).inv_cov == NULL && 
		(*test).predictions == NULL && 
		(*test).labels == NULL && 
		(*test).n_quantities == 0u && 
		(*test).n_points == 0ul 
	); 
	dataset_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored by a dataset object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: dataset.h 
 */ 
extern unsigned short test_dataset_free(void) {

	/* The destructor function should not modify the address */ 
	DATASET *test = dataset_initialize(); 
	void *initial_address = (void *) test; 
	dataset_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

} 

