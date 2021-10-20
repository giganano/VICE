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
	hds -> ids = NULL;
	hds -> birth_times = NULL;
	hds -> birth_radii = NULL;
	hds -> final_radii = NULL;
	hds -> zform = NULL;
	hds -> zfinal = NULL;
	hds -> v_rad = NULL;
	hds -> v_phi = NULL;
	hds -> v_z = NULL;
	hds -> rad_bins = NULL;
	hds -> decomp = NULL;
	hds -> n_rad_bins = 0u;
	hds -> mode = NULL;
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

		if ((*hds).ids != NULL) {
			free(hds -> ids);
			hds -> ids = NULL;
		} else {}

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

		if ((*hds).zform != NULL) {
			free(hds -> zform);
			hds -> zform = NULL;
		} else {}

		if ((*hds).zfinal != NULL) {
			free(hds -> zfinal);
			hds -> zfinal = NULL;
		} else {}

		if ((*hds).v_rad != NULL) {
			free(hds -> v_rad);
			hds -> v_rad = NULL;
		} else {}

		if ((*hds).v_phi != NULL) {
			free(hds -> v_phi);
			hds -> v_phi = NULL;
		} else {}

		if ((*hds).v_z != NULL) {
			free(hds -> v_z);
			hds -> v_z = NULL;
		} else {}

		if ((*hds).rad_bins != NULL) {
			free(hds -> rad_bins);
			hds -> rad_bins = NULL;
		} else {}

		if ((*hds).mode != NULL) {
			free(hds -> mode);
			hds -> mode = NULL;
		} else {}

		free(hds);
		hds = NULL;

	} else {}

}

