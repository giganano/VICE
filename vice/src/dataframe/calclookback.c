/*
 * This file implements calculations of ages and lookback times for history and
 * tracer particle data. The functions are largely the same, and for that
 * reason are combined to not repeat code.
 */


#include <stdlib.h>
#include "../dataframe.h"
#include "../utils.h"
#include "calclookback.h"
#include "fromfile.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double *age_lookback(FROMFILE *ff, char *time_label);


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
 * header: calclookback.h
 */
extern double *history_lookback(FROMFILE *ff) {

	return age_lookback(ff, "time");

}


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
 * header: calclookback.h
 */
extern double *tracers_age(FROMFILE *ff) {

	return age_lookback(ff, "formation_time");

}


/*
 * Determine either the ages of stars in tracer particle data or the lookback
 * time for history data.
 *
 * Parameters
 * ==========
 * ff: 			The fromfile object holding the data
 * time_label: 	The column label for time
 *
 * Returns
 * =======
 * The difference between the maximum time and the recorded time for each row
 * of the data file.
 */
static double *age_lookback(FROMFILE *ff, char *time_label) {

	unsigned long i;
	double *time_ = fromfile_column(ff, time_label);
	double max_time = max(time_, (*ff).n_rows);
	double *ages_lookbacks = (double *) malloc ((*ff).n_rows * sizeof(double));
	for (i = 0ul; i < (*ff).n_rows; i++) {
		ages_lookbacks[i] = max_time - time_[i];
	}
	free(time_);
	return ages_lookbacks;

}

