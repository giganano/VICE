/*
 * This file implements testing of the core routine of the integral object - the
 * quad function at vice/src/yields/integral.h
 *
 * This test works by integrating sin(x) from 0 to pi / 2, the value of which is
 * known to be 1. It then ensures that the return value is within the
 * specified tolerance from 1.
 */


#include <stdlib.h>
#include <math.h>
#include "../../yields.h"
#include "../../utils.h"
#include "../../stats.h"
#include "integral.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short test_quad_common(unsigned long method);
static double test_function(double x);
static INTEGRAL *get_test_integral(void);
static unsigned short assess_test(INTEGRAL test);


/*
 * Test the numerical quadrature implementation of Euler's method
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_quad_euler(void) {

	return test_quad_common(EULER);

}


/*
 * Test the numerical quadrature implementation of trapezoid rule
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_quad_trapzd(void) {

	return test_quad_common(TRAPEZOID);

}


/*
 * Test the numerical quadrature implementation of midpoint rule
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_quad_midpt(void) {

	return test_quad_common(MIDPOINT);

}


/*
 * Test the numerical quadrature implementation of Simpson's method
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: integral.h
 */
extern unsigned short test_quad_simp(void) {

	return test_quad_common(SIMPSON);

}


/*
 * Common routine for testing the implementation of a given quadrature routine
 *
 * Parameters
 * ==========
 * method: 		The hash-code for the method to test (see vice/src/yields.h)
 *
 * Returns
 * =======
 * 1 on a successful test, 0 on a failed test
 */
static unsigned short test_quad_common(unsigned long method) {

	INTEGRAL *test = get_test_integral();
	test -> method = method;
	quad(test);
	unsigned short result = assess_test(*test);
	integral_free(test);
	return result;

}


/*
 * Determine whether or not the test integral passes
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short assess_test(INTEGRAL test) {

	return absval(test.result - 1) < (test.error * test.result);

}


/*
 * Obtain the integral object meant to test the quadrature function.
 */
static INTEGRAL *get_test_integral(void) {

	INTEGRAL *test = integral_initialize();
	test -> func = &test_function;
	test -> a = 0;
	test -> b = PI / 2;
	test -> tolerance = TEST_INTEGRAL_TOLERANCE;
	test -> Nmin = 64;
	test -> Nmax = 2e8;
	return test;

}


/*
 * The test function -> sin(x) from the math library. This test integrates
 * sin(x) from 0 to pi/2 and ensures that the return value is within the
 * specified tolerance of 1.
 */
static double test_function(double x) {

	return sin(x);

}

