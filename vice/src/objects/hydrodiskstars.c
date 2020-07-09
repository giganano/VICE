/* 
 * This file implements memory management of the hydrodiskstars object, which 
 * is used under the hood in the VICE toolkit. 
 */ 

#include <stdlib.h> 
#include "hydrodiskstars.h" 


/* 
 * Allocate memory for and return a pointer to a hydrodiskstars object. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern HYDRODISKSTARS *hydrodiskstars_initialize(void) {

	HYDRODISKSTARS *hds = (HYDRODISKSTARS *) malloc (sizeof(HYDRODISKSTARS)); 
	hds -> n_stars = 0ul; 
	hds -> birth_times = NULL; 
	hds -> birth_radii = NULL; 
	hds -> final_radii = NULL; 
	hds -> rad_bins = NULL; 
	hds -> n_rad_bins = 0u; 
	return hds; 

} 


/* 
 * Free the memory stored by a hydrodiskstars object. 
 * 
 * header: hydrodiskstars.h 
 */ 
extern void hydrodiskstars_free(HYDRODISKSTARS *hds) {

	if (hds != NULL) {

		hds -> n_stars = 0ul; 
		hds -> n_rad_bins = 0u; 

		if ((*hds).birth_times != NULL) {
			free(hds -> birth_times); 
			hds -> birth_times = NULL; 
		} else {} 

		if ((*hds).birth_radii != NULL) {
			free(hds -> birth_radii); 
			hds -> birth_radii = NULL; 
		} else {} 

		if ((*hds).final_radii != NULL) {
			free(hds -> final_radii); 
			hds -> final_radii = NULL; 
		} else {} 

		if ((*hds).rad_bins != NULL) {
			free(hds -> rad_bins); 
			hds -> rad_bins = NULL; 
		} else {} 

		free(hds); 
		hds = NULL; 

	} else {} 

}

