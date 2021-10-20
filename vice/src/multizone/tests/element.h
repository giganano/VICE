
#ifndef MULTIZONE_TESTS_ELEMENT_H
#define MULTIZONE_TESTS_ELEMENT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the separation test on the update_elements function the parent
 * directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short separation_test_update_elements(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_ELEMENT_H */
