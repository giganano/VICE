/*
 * This file handles memory management for the callback_2arg object
 */

#include <stdlib.h>
#include "callback_2arg.h"


/*
 * Allocate memory for and return a pointer to a CALLBACK_2ARG object,
 * initializing the user_func = NULL
 *
 * header: callback_2arg.h
 */
extern CALLBACK_2ARG *callback_2arg_initialize(void) {

	CALLBACK_2ARG *cb2 = (CALLBACK_2ARG *) malloc (sizeof(CALLBACK_2ARG));
	cb2 -> assumed_constant = 0;
	cb2 -> user_func = NULL;
	return cb2;

}


/*
 * Free up the memory stored in a CALLBACK_2ARG object
 *
 * header: callback_2arg.h
 */
extern void callback_2arg_free(CALLBACK_2ARG *cb2) {

	if (cb2 != NULL) {
		free(cb2);
		cb2 = NULL;
	} else {}

}

