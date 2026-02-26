
#ifndef OBJECTS_CALLBACK_CURRENT_STATE_H
#define OBJECTS_CALLBACK_CURRENT_STATE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a CALLBACK_CURRENT_STATE object,
 * initializing the user_func attribute to NULL.
 *
 * source: callback_current_state.c
 */
extern CALLBACK_CURRENT_STATE *callback_current_state_initialize(void);

/*
 * Free up the memory stored by a CALLBACK_CURRENT_STATE object.
 *
 * source: callback_current_state.c
 */
extern void callback_current_state_free(CALLBACK_CURRENT_STATE *cbcs);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_CALLBACK_CURRENT_STATE_H */
