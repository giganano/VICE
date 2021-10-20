
#ifndef DATAFRAME_CALCLOOKBACK_H
#define DATAFRAME_CALCLOOKBACK_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the lookback time to each output in history data by subtracting
 * the time from the maximum time found in the file.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the history data.
 *
 * Returns
 * =======
 * The lookback time to each line of output in the simulation
 *
 * source: calclookback.c
 */
extern double *history_lookback(FROMFILE *ff);

/*
 * Determine the age of each tracer star particle by subtracting its formation
 * time from the maximum formation time found in the output data.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the tracer particle data.
 *
 * Returns
 * =======
 * The age of each star
 *
 * source: calclookback.c
 */
extern double *tracers_age(FROMFILE *ff);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* DATAFRAME_CALCLOOKBACK_H */

