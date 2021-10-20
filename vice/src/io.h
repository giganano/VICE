
#ifndef IO_H
#define IO_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef LINESIZE
#define LINESIZE 100000l
#endif /* LINESIZE */

/* The maximum number of characters in the names of files */
#ifndef MAX_FILENAME_SIZE
#define MAX_FILENAME_SIZE 10000l
#endif /* MAX_FILENAME_SIZE */

#include "objects.h"
#include "io/agb.h"
#include "io/ccsne.h"
#include "io/multizone.h"
#include "io/progressbar.h"
#include "io/sneia.h"
#include "io/singlezone.h"
#include "io/utils.h"

#ifdef __cplusplus
}
#endif

#endif /* IO_H */

