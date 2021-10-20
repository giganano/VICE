
#ifndef TESTS_OBJECTS_CHANNEL_H
#define TESTS_OBJECTS_CHANNEL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a channel object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: channel.c
 */
extern unsigned short test_channel_initialize(void);

/*
 * Test the function which frees the memory stored by a channel object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: channel.c
 */
extern unsigned short test_channel_free(void);

/*
 * Obtain a pointer to a test instance of the CHANNEL object.
 *
 * source: channel.c
 */
extern CHANNEL *channel_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_CHANNEL_H */
