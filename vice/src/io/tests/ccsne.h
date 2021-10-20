
#ifndef TESTS_IO_CCSNE_H
#define TESTS_IO_CCSNE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Test the CCSN yield grid reader at vice/src/io/ccsne.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ccsne.c
 */
extern unsigned short test_cc_yield_grid(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_IO_CCSNE_H */
