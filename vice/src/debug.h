/*
 * This file handles logging within VICE for development and debugging
 * purposes. VICE subscribes to a conventional format, where there are six
 * different types of verbosity for logging:
 * 
 * 1. info: General information regarding the process executed by the program.
 * 2. trace: Individual function calls and the files in which they're
 *    implemented.
 * 3. debug: Print the names of functions being called, the files in which
 *    they're implemented, the line numbers calling the logging print statement,
 *    and variable states.
 * 4. warning: Prints regardless of the user's logging level and whether or not
 *    they've ignored warnings in Python. Does not stop the program.
 * 5. error: A state is reached in which VICE cannot continue the calculation.
 *    This exits the python interpreter always.
 * 6. fatal: A state is reached in which VICE cannot *safely* continue the
 *    calculation. This exits the python interpreter always.
 */

#ifndef DEBUG_H
#define DEBUG_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "multithread.h"

/*
 * Failsafe: define the __func__ identifier if it isn't already for maximum
 * portability.
 */
#if __STDC_VERSION__ < 199901L
	#if __GNUC__ >= 2
		#define __func__ __FUNCTION__
	#else
		#define __func__ "<unknown>"
	#endif /* __GNUC__ */
#endif /* __STDC_VERSION__ */

/* Different level of verbosity within logging */
#define INFO 1u
#define TRACE 2u
#define DEBUG 3u

/*
 * Determine the depth of VICE's verbose logging output by obtaining the
 * integer value of the environment variable "VICE_LOG_LEVEL" - 1 for info,
 * 2 for trace, and 3 for debug.
 */
#define logging_level() ({ \
	char *_loglevel = getenv("VICE_LOGGING_LEVEL"); \
	_loglevel != NULL ? atoi(_loglevel) : 0; \
})

/*
 * Prints a statement to stderr if and only if the loglevel is equal to 1
 * (INFO).
 */
#define info_print(fmt, ...) \
	do { \
		if (logging_level() == INFO) { \
			fprintf(stderr, fmt, __VA_ARGS__); \
		} else {} \
	} while (0)

/*
 * Prints the name of the file and function that is being executed to stderr 
 * if and only if the loglevel is equal to 2 (INFO).
 */
#define trace_print() \
	do { \
		if (logging_level() == TRACE) { \
			fprintf(stderr, "%s:%s()\n", __FILE__, __func__); \
		} else {} \
	} while (0)

/*
 * Print the value of variables to the console to stderr if and only if the
 * loglevel is equal to 3 (DEBUG).
 */
#if defined(_OPENMP)
	#define debug_print(fmt, ...) \
		do { \
			if (!omp_get_thread_num() && logging_level() == DEBUG) { \
				fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, __LINE__, \
					__func__, __VA_ARGS__); \
			} else {} \
		} while (0)
#else
	#define debug_print(fmt, ...) \
		do { \
			if (logging_level() == DEBUG) { \
				fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, __LINE__, \
					__func__, __VA_ARGS__); \
			} else {} \
		} while (0)
#endif

/* For printing errors and warning messages in red. */
#define RESET "\033[0m"
#define RED "\033[31m"
#define BOLDRED "\033[1m\033[31m"

/*
 * Print a warning message to the console. This runs regardless of the logging
 * level and whether or not the user has turned off Python warnings. This
 * message is however intended for developers, so if this warning is raised in
 * an end user's system where they haven't modified source code, it should be
 * interpreted as an issue within VICE.
 */
#define warning_print(fmt, ...) \
	do { \
		fprintf(stderr, RED"Warning: "RESET fmt, __VA_ARGS__); \
	} while (0)

/*
 * Raise an error message to the console and exit the current process; this
 * will quit the Python interpreter. This runs regardless of the logging
 * level and whether or not the user has turned off Python warnings. This
 * message is however intended for developers, so if this warning is raised in
 * an end user's system where they haven't modified source code, it should be
 * interpreted as an issue within VICE.
 */
#define error_print(fmt, ...) \
	do { \
		fprintf(stderr, BOLDRED"Error!"RESET" %s:%d:%s(): " fmt, \
			__FILE__, __LINE__, __func__, __VA_ARGS__); \
		exit(1); \
	} while (0)

/*
 * Raise a fatal message to the console and exit the current process; this
 * will quit the Python interpreter. This runs regardless of the logging
 * level and whether or not the user has turned off Python warnings. This
 * message is however intended for developers, so if this warning is raised in
 * an end user's system where they haven't modified source code, it should be
 * interpreted as an issue within VICE.
 */
#define fatal_print(fmt, ...) \
	do { \
		fprintf(stderr, BOLDRED"Fatal!"RESET" %s:%d:%s(): " fmt, \
			__FILE__, __LINE__, __func__, __VA_ARGS__); \
		exit(1); \
	} while (0)

#endif /* DEBUG_H */

