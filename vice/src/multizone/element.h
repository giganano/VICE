
#ifndef MULTIZONE_ELEMENT_H
#define MULTIZONE_ELEMENT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Updates the mass of each element in each zone to the proper value at the
 * next timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * source: element.c
 */
extern void update_elements(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_ELEMENT_H */



