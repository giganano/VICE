/*
 * This is the main header file associated with the singlezone object
 */

#ifndef SINGLEZONE_H
#define SINGLEZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* Maximum amount of time in Gyr that VICE supports singlezone simulations */
#ifndef SINGLEZONE_MAX_EVAL_TIME
#define SINGLEZONE_MAX_EVAL_TIME 15
#endif /* SINGLEZONE_MAX_EVAL_TIME */

/*
 * The number of timesteps beyond the final evaluation time that memory is
 * allocated for as a safeguard against memory errors
 */
#ifndef BUFFER
#define BUFFER 10l
#endif /* BUFFER */

#include "objects.h"
#include "objects/singlezone.h"
#include "singlezone/agb.h"
#include "singlezone/ccsne.h"
#include "singlezone/channel.h"
#include "singlezone/element.h"
#include "singlezone/ism.h"
#include "singlezone/mdf.h"
#include "singlezone/recycling.h"
#include "singlezone/singlezone.h"
#include "singlezone/sneia.h"

#ifdef __cplusplus
}
#endif

#endif /* SINGLEZONE_H */


