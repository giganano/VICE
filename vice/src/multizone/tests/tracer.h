
#ifndef MULTIZONE_TESTS_TRACER_H
#define MULTIZONE_TESTS_TRACER_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs a generic test of the inject_tracers function in the parent
 * directory. This should always be equal to the timestep times the number of
 * zones times the number of tracer particles per zone per timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: tracer.c
 */
extern unsigned short generic_test_inject_tracers(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_TRACER_H */
