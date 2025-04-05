
#include <stdlib.h>
#include "callback_current_state.h"


/*
 * Allocate memory for and return a pointer to a CALLBACK_CURRENT_STATE object,
 * initializing the user_func attribute to NULL.
 *
 * header: callback_current_state.h
 */
extern CALLBACK_CURRENT_STATE *callback_current_state_initialize(void) {

	CALLBACK_CURRENT_STATE *cbcs = (CALLBACK_CURRENT_STATE *) malloc (
		sizeof(CALLBACK_CURRENT_STATE));
	cbcs -> user_func = NULL;
	return cbcs;

}


/*
 * Free up the memory stored by a CALLBACK_CURRENT_STATE object.
 *
 * header: callback_current_state.h
 */
extern void callback_current_state_free(CALLBACK_CURRENT_STATE *cbcs) {

	if (cbcs != NULL) {
		free(cbcs);
		cbcs = NULL;
	} else {}

}

