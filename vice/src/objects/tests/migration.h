
#ifndef TESTS_OBJECTS_MIGRATION_H
#define TESTS_OBJECTS_MIGRATION_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a migration object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: migration.c
 */
extern unsigned short test_migration_initialize(void);

/*
 * Test the function which frees the memory stored in a migration object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: migration.c
 */
extern unsigned short test_migration_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_MIGRATION_H */
