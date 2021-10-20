
#ifndef TESTS_SSP_MSMF_H
#define TESTS_SSP_MSMF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the MSMF function at vice/src/ssp/msmf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: msmf.c
 */
extern unsigned short test_MSMF(void);

/*
 * Test the setup_MSMF function at vice/src/ssp/msmf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: msmf.c
 */
extern unsigned short test_setup_MSMF(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_SSP_MSMF_H */
