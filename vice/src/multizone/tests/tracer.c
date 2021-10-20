/*
 * This file implements testing of the tracer routines in the parent directory.
 */

#include "../tracer.h"


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
 * header: tracer.h
 */
extern unsigned short generic_test_inject_tracers(MULTIZONE *mz) {

	/*
	 * There will always be two timesteps worth of tracer particles beyond the
	 * final timestep - the first comes from the call to inject_tracers at
	 * the beginning of each model, and the second comes from the fact that
	 * inject_tracers at each timestep is called before the current time is
	 * modified (the current time is the criterion for deciding whether or not
	 * they should be injected).
	 */
	unsigned long n_timesteps = 2ul + (unsigned long) (
		(*(*mz).zones[0]).output_times[(*(*mz).zones[0]).n_outputs - 1l] /
		(*(*mz).zones[0]).dt
	);
	unsigned long correct = (n_timesteps * (*(*mz).mig).n_zones *
		(*(*mz).mig).n_tracers);
	return (*(*mz).mig).tracer_count == correct;

}

