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

	/* +2l takes into account injection before and after evolution */ 
	return (*(*mz).mig).tracer_count == (
		((*(*mz).zones[0]).timestep + 2l) * 
		(*(*mz).mig).n_zones * 
		(*(*mz).mig).n_tracers 
	); 

} 

