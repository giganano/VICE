/*
 * This file implements memory management for the INTEGRAL object.
 */

#include <stdlib.h>
#include "../yields.h"
#include "objects.h"
#include "integral.h"


/*
 * Allocate memory for and return a pointer to an integral object.
 *
 * header: integral.h
 */
extern INTEGRAL *integral_initialize(void) {

	return (INTEGRAL *) malloc (sizeof(INTEGRAL));

}


/*
 * Free up the memory stored in the integral object.
 *
 * header: integral.h
 */
extern void integral_free(INTEGRAL *intgrl) {

	if (intgrl != NULL) {

		free(intgrl);
		intgrl = NULL;

	} else {}

}

