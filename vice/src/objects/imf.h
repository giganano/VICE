
#ifndef OBJECTS_IMF_H
#define OBJECTS_IMF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

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
 * The IMF object; NULL if user_spec is not "salpter", "kroupa", or "custom"
 *
 * source: imf.c
 */
extern IMF_ *imf_initialize(double m_lower, double m_upper);

/*
 * Free up the memory stored in an IMF object.
 *
 * Parameters
 * ==========
 * imf: 		The IMF object to free up
 *
 * source: imf.c
 */
extern void imf_free(IMF_ *imf);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_IMF_H */

