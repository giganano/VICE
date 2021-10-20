
#ifndef TESTS_CALLBACK_H
#define TESTS_CALLBACK_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Test the callback_1arg_evaluate function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: callback.c
 */
extern unsigned short test_callback_1arg_evaluate(void);

/*
 * Test the callback_2arg evaluate function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: callback.c
 */
extern unsigned short test_callback_2arg_evaluate(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_CALLBACK_H */
