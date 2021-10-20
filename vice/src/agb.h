
#ifndef AGB_H
#define AGB_H

#ifdef __cplusplus
extern "C" {
#endif

/* The maximum mass of a star in Msun that undergoes an AGB phase in VICE */
#ifndef MAX_AGB_MASS
#define MAX_AGB_MASS 8
#endif /* MAX_AGB_MASS */

/* The minimum mass of a star in Msun that undergoes an AGB phase in VICE */
#ifndef MIN_AGB_MASS
#define MIN_AGB_MASS 0
#endif /* MIN_AGB_MASS */

#include "objects.h"
#include "singlezone/agb.h"
#include "multizone/agb.h"
#include "objects/agb.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* AGB_H */

