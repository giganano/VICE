/*
 * This file implements multithreading in VICE using openMP. In order to enable
 * these features, VICE must be compiled with the '-fopenmp' compiler flag. On
 * Mac OS, users must install libomp prior to compiling from source and
 * comppile with the flags '-Xpreprocessor -fopenmp -lomp'.
 */

#include "multithread.h"
#include "debug.h"


/*
 * Set the number of threads to be used with openMP.
 *
 * Parameters
 * ==========
 * n: 		The number of threads to use.
 *
 * Returns
 * =======
 * 0 if openMP was linked at compile time or if only 1 thread is being used
 * if it wasn't linked at compile time. If the user is requesting multiple
 * threads but openMP wasn't linked at compile time, a value of 1 is
 * returned, in which case a RuntimeError will be raised in Python to alert
 * the user that they need to reinstall VICE from source and follow the
 * steps required to enable multithreading.
 * 
 * header: multithread.h
 */
extern unsigned short openmp_set_nthreads(unsigned short n) {

	trace_print();
	#if defined(_OPENMP)
		if (n) {
			omp_set_num_threads(n);
			debug_print("openMP enabled. NTHREADS = %u\n",
			// 	omp_get_max_threads());
			return 0u;
		} else {
			error_print("%s\n", "Cannot assign 0 threads to process.");
		}
	#else
		debug_print("%s\n", "openMP not enabled.");
		return n != 1u;
	#endif

}


/*
 * Determine the number of threads to be used with openMP.
 *
 * Returns
 * =======
 * The positive definite number of threads to be used. If openMP was not
 * linked with VICE at compile time, then this function will always return
 * a value of 1.
 *
 * header: multithread.h
 */
extern unsigned short openmp_get_nthreads(void) {

	trace_print();
	#if defined(_OPENMP)
		debug_print("openMP enabled. NTHREADS = %u\n", omp_get_max_threads());
		return omp_get_max_threads();
	#else
		debug_print("%s\n", "openMP not enabled.");
		return 1u;
	#endif

}


