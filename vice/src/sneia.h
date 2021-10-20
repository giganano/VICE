
#ifndef SNEIA_H
#define SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* power-law index of built-in SNe Ia DTD */
#ifndef PLAW_DTD_INDEX
#define PLAW_DTD_INDEX 1.1
#endif /* PLAW_DTD_INDEX */

/* The time up to which the RIa DTD is evaluated */
#ifndef RIA_MAX_EVAL_TIME
#define RIA_MAX_EVAL_TIME 15.0
#endif /* RIA_MAX_EVAL_TIME */

/* hash-code for exp-mode */
#ifndef EXP
#define EXP 333
#endif /* EXP */

/* hash-code for plaw-mode */
#ifndef PLAW
#define PLAW 436
#endif /* PLAW */

/* hash-code for custom DTD */
#ifndef CUSTOM
#define CUSTOM 667
#endif /* CUSTOM */

#include "objects.h"
#include "singlezone/sneia.h"
#include "multizone/sneia.h"
#include "objects/sneia.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SNEIA_H */


