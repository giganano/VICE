/*
 * This file is part of the VICE package.
 * Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
 * License: MIT License. See LICENSE in top-level directory
 * at: https://github.com/giganano/VICE.git.
 */

#ifndef MULTITHREAD_H
#define MULTITHREAD_H

#if defined(_OPENMP)
	#include <omp.h>
#endif

/*
 * Determined if the current installation supports multithreading with OpenMP.
 *
 * Returns
 * =======
 * 1 if OpenMP has been linked, 0 if not.
 *
 * source: multithread.c
 */
extern unsigned short openmp_linked(void);

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
 * source: multithread.c
 */
extern unsigned short openmp_set_nthreads(unsigned short n);

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
extern unsigned short openmp_get_nthreads(void);

#endif /* MULTITHREAD_H */

