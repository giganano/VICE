
#ifndef DEBUG_H
#define DEBUG_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

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
#define debug_print(fmt, ...) \
	do { \
		if (logging_level() == DEBUG) { \
			fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, __LINE__, __func__, \
				__VA_ARGS__); \
		} else {} \
	} while (0)

/* For printing errors and warning messages in red. */
#define RESET "\033[0m"
#define RED "\033[31m"
#define BOLDRED "\033[1m\033[31m"

/* Print a warning message to the console */
#define warning_print(fmt, ...) \
	do { \
		fprintf(stderr, RED"Warning: "RESET fmt, __VA_ARGS__); \
	} while (0)

/* Raise an error message to the console and exit the program */
#define error_print(fmt, ...) \
	do { \
		fprintf(stderr, BOLDRED"Error!"RESET" %s:%d:%s(): " fmt, \
			__FILE__, __LINE__, __func__, __VA_ARGS__); \
		exit(1); \
	} while (0)

/* Raise a fatal massage to the console and exit the program */
#define fatal_print(fmt, ...) \
	do { \
		fprintf(stderr, BOLDRED"Fatal!"RESET" %s:%d:%s(): " fmt, \
			__FILE__, __LINE__, __func__, __VA_ARGS__); \
		exit(1); \
	} while (0)

#endif /* DEBUG_H */

