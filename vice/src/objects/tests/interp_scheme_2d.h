
#ifndef OBJECTS_TESTS_INTERP_SCHEME_2D_H
#define OBJECTS_TESTS_INTERP_SCHEME_2D_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Tests the memory allocation routine for the interp_scheme_2d object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: interp_scheme_2d.c
 */
extern unsigned short test_interp_scheme_2d_initialize(void);


/*
 * Test the function which frees the memory stored by an interp_scheme_2d
 * object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure.
 *
 * source: interp_scheme_2d.c
 */
extern unsigned short test_interp_scheme_2d_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_TESTS_INTERP_SCHEME_2D_H */
