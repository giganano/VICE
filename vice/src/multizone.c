/* 
 * This file implements the multizone object and the simulations thereof 
 */ 

#include <stdlib.h> 
#include "multizone.h" 
#include "singlezone.h" 
#include "element.h" 
#include "tracer.h" 
#include "io.h" 

/* 
 * Allocates memory for and returns a pointer to a multizone object 
 * 
 * header: multizone.h 
 */ 
extern MULTIZONE *multizone_initialize(void) {

	MULTIZONE *mz = (MULTIZONE *) malloc (sizeof(MULTIZONE)); 
	mz -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	mz -> zones = NULL; 
	mz -> migration_matrix = NULL; 
	return mz; 

}

/*
 * Frees the memory stored in a multizone object 
 * 
 * header: multizone.h 
 */ 
extern void multizone_free(MULTIZONE *mz) {

	free(mz -> name); 
	if ((*mz).zones != NULL) {
		unsigned int i; 
		for (i = 0; i < (*mz).n_zones; i++) {
			singlezone_free(mz -> zones[i]); 
		} 
	} else {} 
	if ((*mz).migration_matrix != NULL) free(mz -> migration_matrix); 

} 



