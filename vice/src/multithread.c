/*
 * This file is part of the VICE package.
 * Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
 * License: MIT License. See LICENSE in top-level directory
 * at: https://github.com/giganano/VICE.git.
 *
 * This file implements multithreading in VICE using OpenMP. In order to enable
 * these features, VICE must be compiled with the "-fopenmp" compiler flag.
 * On Mac OS, users must install libomp with Homebrew prior to compiling from
 * source and compiling with the flags "-Xpreprocessor -fopenmp -lomp".
 */

#include "multithread.h"
#include "debug.h"


/*
 * Determined if the current installation supports multithreading with OpenMP.
 *
 * Returns
 * =======
 * 1 if OpenMP has been linked, 0 if not.
 *
 * header: multithread.h
 */
extern unsigned short openmp_linked(void) {

	#if defined(_OPENMP)
		return 1u;
	#else
		return 0u;
	#endif

}


/*
 * Set the number of threads to be used with OpenMP.
 *
 * Parameters
 * ==========
 * n: 		The number of threads to use.
 *
 * Returns
 * =======
 * 0 if OpenMP was linked at compile time or if only 1 thread is being used if
 * it wasn't linked at compile time. If the user is requesting multiple threads
 * but OpenMP wasn't linked at compile time, a value of 1 is returned, in which
 * case Python will raise a RuntimeError to alert the user that they actually
 * need to reinstall VICE if they want to use multithreading.
 *
 * header: multithread.h
 */
extern unsigned short openmp_set_nthreads(unsigned short n) {

	trace_print();
	#if defined(_OPENMP)
		if (n) {
			omp_set_num_threads(n);
			debug_print("OpenMP enabled. MAXTHREADS = %u\n",
				omp_get_num_threads());
			return 0u;
		} else {
			error_print("%s\n", "Cannot assign 0 threads to process.");
		}
	#else
		debug_print("%s\n", "OpenMP not enabled.");
		return n != 1u;
	#endif

}


/*
 * Determine the number of threads to be used with OpenMP.
 *
 * Returns
 * =======
 * The positive definite number of threads to be used. If OpenMP was not
 * linked with VICE at compile time, then this function will alwasy return
 * a value of 1.
 *
 * source: multithread.c
 */
extern unsigned short openmp_get_nthreads(void) {

	trace_print();
	#if defined(_OPENMP)
		debug_print("OpenMP enabled. MAXTHREADS = %u\n", omp_get_num_threads());
		return omp_get_num_threads();
	#else
		debug_print("%s\n", "OpenMP not enabled.");
		return 1u;
	#endif

}

