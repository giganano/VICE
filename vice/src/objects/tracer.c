/*
 * This file implements memory manangement for the tracer object.
 */

#include <stdlib.h>
#include "../tracer.h"
#include "objects.h"
#include "tracer.h"


/*
 * Allocates memory for and returns a pointer to a TRACER particle.
 *
 * header: tracer.h
 */
extern TRACER *tracer_initialize(void) {

	TRACER *t = (TRACER *) malloc (sizeof(TRACER));
	t -> mass = 0;
	t -> zone_history = NULL;
	return t;

}


/*
 * Frees up the memory stored by the tracer particle.
 *
 * header: tracer.h
 */
extern void tracer_free(TRACER *t) {

	if (t != NULL) {

		if ((*t).zone_history != NULL) {
			free(t -> zone_history);
			t -> zone_history = NULL;
		}

		free(t);
		t = NULL;
		
	} else {}

}

