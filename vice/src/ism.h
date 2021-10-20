
#ifndef ISM_H
#define ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* hash-code for gas-mode */
#ifndef GAS
#define GAS 315
#endif /* GAS */

/* hash-code for infall-mode */
#ifndef IFR
#define IFR 321
#endif /* IFR */

/* hash-code for star formation-mode */
#ifndef SFR
#define SFR 331
#endif /* SFR */

#include "objects.h"
#include "singlezone/ism.h"
#include "multizone/ism.h"
#include "objects/ism.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* ISM_H */

