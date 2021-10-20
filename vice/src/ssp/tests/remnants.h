
#ifndef TESTS_SSP_REMNANTS_H
#define TESTS_SSP_REMNANTS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Test the implementation of the Kalirai et al. (2008) initial-final
 * remnant mass relationship at vice/src/ssp/remnants.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: remnants.c
 */
extern unsigned short test_Kalirai08_remnant_mass(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_SSP_REMNANTS_H */
