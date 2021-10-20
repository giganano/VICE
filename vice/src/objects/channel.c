/*
 * This file implements the memory management for the CHANNEL object.
 */

#include <stdlib.h>
#include "../channel.h"
#include "callback_1arg.h"
#include "objects.h"
#include "channel.h"


/*
 * Allocate memory for and return a pointer to a CHANNEL object.
 * Automatically initializes yield_ and rate to NULL. Allocates memory for and
 * fills the grid_.
 *
 * header: channel.h
 */
extern CHANNEL *channel_initialize(void) {

	CHANNEL *ch = (CHANNEL *) malloc (sizeof(CHANNEL));
	ch -> yield_ = callback_1arg_initialize();
	ch -> rate = NULL;
	ch -> entrainment = 1;

	return ch;

}


/*
 * Free up the memory in a CHANNEL object.
 *
 * header: channel.h
 */
extern void channel_free(CHANNEL *ch) {

	if (ch != NULL) {

		if ((*ch).yield_ != NULL) {
			callback_1arg_free(ch -> yield_);
			ch -> yield_ = NULL;
		} else {}

		if ((*ch).rate != NULL) {
			free(ch -> rate);
			ch -> rate = NULL;
		} else {}

		free(ch);
		ch = NULL;

	} else {}

}

