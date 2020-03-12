/* 
 * This file implements testing of the channel object's memory management 
 */ 

#include <stdlib.h> 
#include "../../objects.h" 
#include "channel.h" 


/* 
 * Test the function which constructs a channel object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: channel.h 
 */ 
extern unsigned short test_channel_initialize(void) { 

	CHANNEL *test = channel_initialize(); 
	unsigned short result = (test != NULL && 
		(*test).yield_ == NULL && 
		(*test).rate == NULL && 
		(*test).entrainment == 1
	); 
	channel_free(test); 
	return result; 

} 


/* 
 * Test the function which frees the memory stored by a channel object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: channel.h 
 */ 
extern unsigned short test_channel_free(void) { 

	/* The destructor function should not modify the address */ 
	CHANNEL *test = channel_initialize(); 
	void *initial_address = (void *) test; 
	channel_free(test); 
	void *final_address = (void *) test; 
	return initial_address == final_address; 

}

