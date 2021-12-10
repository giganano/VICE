
#ifndef MULTITHREAD_H
#define MULTITHREAD_H

#if defined(_OPENMP)
	#include <omp.h>
#endif /* _OPENMP */

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
 * source: multithread.c
 */
extern unsigned short openmp_set_nthreads(unsigned short n);

/*
 * Determine the number of threads to be used with openMP.
 *
 * Returns
 * =======
 * The positive definite number of threads to be used. If openMP was not
 * linked with VICE at compile time, then this function will always return
 * a value of 1.
 *
 * source: multithread.c
 */
extern unsigned short openmp_get_nthreads(void);

#endif /* MULTITHREAD_H */
