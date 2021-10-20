
#ifndef TESTS_SSP_CRF_H
#define TESTS_SSP_CRF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the CRF function at vice/src/ssp/crf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: crf.c
 */
extern unsigned short test_CRF(void);

/*
 * Test the setup_CRF function at vice/src/ssp/crf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: crf.c
 */
extern unsigned short test_setup_CRF(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_SSP_CRF_H */

