/* 
 * This file implements testing of the sneia_yield_specs object's memory 
 * management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "sneia.h" 


/* 
 * Test the function which constructs a sneia_yield_specs object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: sneia.h 
 */ 
extern unsigned short test_sneia_yield_initialize(void) { 

	SNEIA_YIELD_SPECS *test = sneia_yield_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).functional_yield == NULL && 
		(*test).constant_yield == 0 && 
		(*test).RIa == NULL && 
		(*test).dtd != NULL && 
		(*test).tau_ia == 1.5 && 
		(*test).t_d == 0.15 && 
		(*test).entrainment == 1 
	); 
	sneia_yield_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored in a sneia_yield_specs object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: sneia.h 
 */ 
extern unsigned short test_sneia_yield_free(void) {

	/* The destructor function should not modify the address */ 
	SNEIA_YIELD_SPECS *test = sneia_yield_initialize(); 
	void *initial_address = (void *) test; 
	sneia_yield_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

