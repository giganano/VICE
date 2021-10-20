
#ifndef TESTS_IO_AGB_H
#define TESTS_IO_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the import_agb_grid function at vice/src/io/agb.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short test_import_agb_grid(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_IO_AGB_H */
