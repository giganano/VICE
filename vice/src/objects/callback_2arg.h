
#ifndef OBJECTS_CALLBACK_2ARG_H
#define OBJECTS_CALLBACK_2ARG_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a CALLBACK_2ARG object,
 * initializing the user_func = NULL
 *
 * source: callback_2arg.c
 */
extern CALLBACK_2ARG *callback_2arg_initialize(void);

/*
 * Free up the memory stored in a CALLBACK_2ARG object
 *
 * source: callback_2arg.c
 */
extern void callback_2arg_free(CALLBACK_2ARG *cb2);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_CALLBACK_2ARG_H */
