/*
 * This file implements the memory management for the fromfile object.
 */

#include <stdlib.h>
#include "../dataframe.h"
#include "../io.h"
#include "objects.h"
#include "fromfile.h"


/*
 * Allocate memory and return a pointer to a fromfile object. Automatically
 * allocates memory for the name of the file.
 *
 * header: fromfile.h
 */
extern FROMFILE *fromfile_initialize(void) {

	FROMFILE *ff = (FROMFILE *) malloc (sizeof(FROMFILE));
	ff -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char));
	ff -> n_rows = 0ul;
	ff -> n_cols = 0u;
	ff -> labels = NULL;
	ff -> data = NULL;
	return ff;

}


/*
 * Free up the memory stored in a fromfile object.
 *
 * header: fromfile.h
 */
extern void fromfile_free(FROMFILE *ff) {

	if (ff != NULL) {

		if ((*ff).name != NULL) {
			free(ff -> name);
			ff -> name = NULL;
		} else {}

		if ((*ff).labels != NULL) {
			/* Each label has memory that likely needs freed */
			unsigned int i;
			for (i = 0; i < (*ff).n_cols; i++) {
				if ((*ff).labels[i] != NULL) {
					free(ff -> labels[i]);
					ff -> labels[i] = NULL;
				} else {
					continue;
				}
			}
			free(ff -> labels);
			ff -> labels = NULL;
		} else {}

		if ((*ff).data != NULL) {
			free(ff -> data);
			ff -> data = NULL;
		} else {}

		free(ff);
		ff = NULL;

	} else {}

}

