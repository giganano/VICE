
#ifndef TESTS_IO_SNEIA_H
#define TESTS_IO_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Test the function which looks up the mass yield from a single SN Ia
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: sneia.c
 */
extern unsigned short test_single_ia_mass_yield_lookup(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_IO_SNEIA_H */
