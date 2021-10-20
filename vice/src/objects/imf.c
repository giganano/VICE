/*
 * This file implements the memory management for the IMF_ object.
 */

#include <stdlib.h>
#include "../imf.h"
#include "objects.h"
#include "callback_1arg.h"
#include "imf.h"


/*
 * Allocate memory for and return a pointer to an IMF object.
 *
 * Parameters
 * ==========
 * m_lower: 	The lower mass limit on star formation
 * m_upper: 	The upper mass limit on star formation
 *
 * Returns
 * =======
 * The IMF object; NULL if user_spec is not "salpeter", "kroupa", or "custom"
 *
 * header: imf.h
 */
extern IMF_ *imf_initialize(double m_lower, double m_upper) {

	IMF_ *imf = (IMF_ *) malloc (sizeof(IMF_));
	imf -> spec = (char *) malloc (SPEC_CHARP_SIZE * sizeof(char));
	imf -> m_lower = m_lower;
	imf -> m_upper = m_upper;
	imf -> custom_imf = callback_1arg_initialize();
	return imf;

}


/*
 * Free up the memory stored in an IMF object.
 *
 * Parameters
 * ==========
 * imf: 		The IMF object to deallocate
 *
 * header: imf.h
 */
extern void imf_free(IMF_ *imf) {

	if (imf != NULL) {

		if ((*imf).spec != NULL) {
			free(imf -> spec);
			imf -> spec = NULL;
		} else {}
		
		if ((*imf).custom_imf != NULL) {
			callback_1arg_free(imf -> custom_imf);
			imf -> custom_imf = NULL;
		} else {}

		free(imf);
		imf = NULL;

	} else {}

}

