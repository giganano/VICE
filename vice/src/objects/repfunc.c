/* 
 * This file implements memory management for the repfunc object. 
 */ 

#include <stdlib.h> 
#include "repfunc.h" 


/* 
 * Allocate memory for and return a pointer to a repfunc object. The number of 
 * points is automatically set to 0 and the coordinates to NULL. 
 * 
 * header: repfunc.h 
 */ 
extern REPFUNC *repfunc_initialize(void) {

	REPFUNC *rpf = (REPFUNC *) malloc (sizeof(REPFUNC)); 
	rpf -> n_points = 0ul; 
	rpf -> xcoords = NULL; 
	rpf -> ycoords = NULL; 
	return rpf; 

}


/* 
 * Free up the memory stored in a repfunc object. 
 * 
 * header: repfunc.h 
 */ 
extern void repfunc_free(REPFUNC *rpf) {

	if (rpf != NULL) {

		if ((*rpf).xcoords != NULL) {
			free(rpf -> xcoords); 
			rpf -> xcoords = NULL; 
		} else {} 

		if ((*rpf).ycoords != NULL) {
			free(rpf -> ycoords); 
			rpf -> ycoords = NULL; 
		} else {} 

		free(rpf); 
		rpf = NULL; 

	} else {} 

}

