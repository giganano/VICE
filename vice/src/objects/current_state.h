
#ifndef OBJECTS_CURRENT_STATE_H
#define OBJECTS_CURRENT_STATE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a CURRENT_STATE object.
 * Automatically sets the abundance by mass for each element to 0.0.
 *
 * Parameters
 * ==========
 * n_elements: The number of elements tracked by the model.
 *
 * source: current_state.c
 */
extern CURRENT_STATE *current_state_initialize(unsigned short n_elements);

/*
 * Free up the memory stored by a CURRENT_STATE object.
 *
 * source: current_state.c
 */
extern void current_state_free(CURRENT_STATE *cs);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_CURRENT_STATE_H */
