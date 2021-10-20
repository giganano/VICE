/*
 * This file handles memory management for the callback_1arg object
 */

#include <stdlib.h>
#include "callback_1arg.h"


/*
 * Allocate memory for and return a pointer to a CALLBACK_1ARG object,
 * initializing the user_func = NULL
 *
 * header: callback_1arg.h
 */
extern CALLBACK_1ARG *callback_1arg_initialize(void) {

	CALLBACK_1ARG *cb1 = (CALLBACK_1ARG *) malloc (sizeof(CALLBACK_1ARG));
	cb1 -> assumed_constant = 0;
	cb1 -> user_func = NULL;
	return cb1;

}


/*
 * Free up the memory stored in a CALLBACK_1ARG object
 *
 * header: callback_1arg.h
 */
extern void callback_1arg_free(CALLBACK_1ARG *cb1) {

	if (cb1 != NULL) {
		free(cb1);
		cb1 = NULL;
	} else {}

}

