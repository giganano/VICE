/*
 * This file implements tests of VICE's utiltiy functions at vice/src/utils.h
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "../utils.h"
#include "../yields.h"
#include "../ism.h"
#include "utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned long factorial(unsigned short n);

static double TEST_RANDOM_RANGE_MIN = 0;
static double TEST_RANDOM_RANGE_MAX = 100;
static unsigned short TEST_BINSPACE_N_BINS = 1000u;


/*
 * Test the choose operation (a b) implemented at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_choose(void) {

	/*
	 * Test the function by looking at all (n k) operations where n ranges
	 * from 0 to 20 (inclusive) and ensuring it is equal to the mathematical
	 * definition from factorials
	 */
	unsigned short i, j;
	for (i = 0u; i <= 20u; i++) {
		for (j = 0u; j <= i; j++) {
			if (choose(i, j) != factorial(i) /
				(factorial(j) * factorial(i - j))) {
				return 0u;
			}
		}
	}
	return 1u;

}


/*
 * Compute the value of n!
 *
 * Parameters
 * ==========
 * n: 		The value to compute the factorial for
 *
 * Returns
 * =======
 * n * (n - 1) * (n - 2) * ... * 3 * 2 * 1
 */
static unsigned long factorial(unsigned short n) {

	/*
	 * The classic recursive implementation of n!
	 *
	 * Notes
	 * =====
	 * Due to this adopted implementation, this function will only behaver
	 * property for values of n up to 20
	 */
	if (n) {
		return (unsigned long) n * factorial(n - 1ul);
	} else {
		return 1ul;
	}

}


/*
 * Test the absolute value function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_absval(void) {

	return absval(-1) > 0 && absval(1) > 0;

}


/*
 * Tests the sign function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_sign(void) {

	return sign(-1) < 0 && sign(1) > 0;

}


/*
 * Test the simple hash function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_simple_hash(void) {

	/* Test by comparing to several internal hash codes */
	return (
		simple_hash("euler") == EULER &&
		simple_hash("midpoint") == MIDPOINT &&
		simple_hash("trapezoid") == TRAPEZOID &&
		simple_hash("simpson") == SIMPSON &&
		simple_hash("gas") == GAS &&
		simple_hash("ifr") == IFR &&
		simple_hash("sfr") == SFR
	);

}


/*
 * Test the psuedorandom number generator at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_rand_range(void) {

	/*
	 * Draw a random number in a specified range 10000 times and ensure that
	 * its always in that range.
	 */
	unsigned short i;
	for (i = 0u; i < 10000u; i++) {
		double test = rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX);
		if (test < TEST_RANDOM_RANGE_MIN || test > TEST_RANDOM_RANGE_MAX) {
			return 0u;
		} else {}
	}
	return 1u;

}


/*
 * Test the 1-D interpolation function vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_interpolate(void) {

	/*
	 * Tests the interpolation function by ensuring that two psuedorandomly
	 * generated points interpolate at the arithmetic mean of the x-values to
	 * to the arithmetic mean of the y-values. Repeat this test 10,000 times.
	 */
	unsigned short i;
	for (i = 0u; i < 10000u; i++) {
		double pt1[2] = {
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
		};
		double pt2[2] = {
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
		};
		double test = interpolate(pt1[0], pt2[0], pt1[1], pt2[1],
			(pt1[0] + pt2[0]) / 2);
		if (absval((pt1[1] + pt2[1]) / (2 * test) - 1) > 1e-5) {
			return 0u;
		} else {}
	}
	return 1u;

}


/*
 * Test the 2D interpolation function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_interpolate2D(void) {

	/*
	 * Tests the interpolation function by ensuring that four pseudorandomly
	 * generated points interpolate at the arithmetic mean of the x- and
	 * y-values to arithmetic mean of the z-values
	 */
	unsigned short i;
	for (i = 0u; i < 10000u; i++) {

		double x[2] = {
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
		};
		double y[2] = {
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
			rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
		};
		double f[2][2] = {
			{
				rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
				rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
			},
			{
				rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX),
				rand_range(TEST_RANDOM_RANGE_MIN, TEST_RANDOM_RANGE_MAX)
			}
		};

		double test = interpolate2D(x, y, f,
			(x[0] + x[1]) / 2, (y[0] + y[1]) / 2);

		if (absval((f[0][0] + f[0][1] + f[1][0] + f[1][1]) / (4 * test) - 1)
			> 1e-5) {
			return 0u;
		} else {}

	}
	return 1u;

}


/*
 * Test the sqrt(x) interpolation function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_interpolate_sqrt(void) {

	/*
	 * Test this interpolation function by ensuring that something adequately
	 * close to sqrt(x) is returned when the points (0, 0) and (1, 1) are
	 * extrapolated from.
	 */

	unsigned short i, status = 1u;
	for (i = 0u; i < 10000u; i++) {

		double test_value = rand_range(TEST_RANDOM_RANGE_MIN,
			TEST_RANDOM_RANGE_MAX);
		status &= (
			absval(interpolate_sqrt(0, 1, 0, 1, test_value) - sqrt(test_value))
			< 1e-5
		);
		if (!status) break;

	}

	return status;

}


/*
 * Tests the bin number lookup function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_get_bin_number(void) {

	/*
	 * Tests the function by making sure a test binspace's bin centers evalute
	 * to their index
	 */
	unsigned short i;
	double *test_bins = binspace(
		TEST_RANDOM_RANGE_MIN,
		TEST_RANDOM_RANGE_MAX,
		TEST_BINSPACE_N_BINS
	);
	double *centers = bin_centers(test_bins, TEST_BINSPACE_N_BINS);
	for (i = 0u; i < TEST_BINSPACE_N_BINS; i++) {
		if (get_bin_number(test_bins, TEST_BINSPACE_N_BINS, centers[i]) != i) {
			return 0u;
		} else {}
	}
	return 1u;

}


/*
 * Test the binspace function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_binspace(void) {

	/*
	 * Generate a test binspace with knwon bounds and width, then make sure
	 * each element is separated by the bin width
	 */
	unsigned short i;
	double *test = binspace(
		TEST_RANDOM_RANGE_MIN,
		TEST_RANDOM_RANGE_MAX,
		TEST_BINSPACE_N_BINS
	);
	for (i = 0u; i < TEST_BINSPACE_N_BINS; i++) {
		if (
			absval((test[i + 1u] - test[i]) / ((TEST_RANDOM_RANGE_MAX -
				TEST_RANDOM_RANGE_MIN) / TEST_BINSPACE_N_BINS) - 1) > 1e-5) {
			return 0u;
		} else {}
	}
	return 1u;

}


/*
 * Test the bin_centers function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_bin_centers(void) {

	unsigned short i;
	double *bins = binspace(
		TEST_RANDOM_RANGE_MIN,
		TEST_RANDOM_RANGE_MAX,
		TEST_BINSPACE_N_BINS
	);
	/* brute-force test by simply calculating the mean value */
	double *test = bin_centers(bins, TEST_BINSPACE_N_BINS);
	for (i = 0u; i < TEST_BINSPACE_N_BINS; i++) {
		if (test[i] != (bins[i] + bins[i + 1u]) / 2) {
			free(bins);
			free(test);
			return 0u;
		} else {}
	}
	free(bins);
	free(test);
	return 1u;

}


/*
 * Test the sum function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_sum(void) {

	/*
	 * test-by adding up integers and comparing with the results of the
	 * sum function (i.e. the triangle numbers)
	 */

	unsigned short i;
	double *test = (double *) malloc (100u * sizeof(double));
	for (i = 0u; i < 100u; i++) {
		test[i] = i;
	}
	double s = 0;
	for (i = 0u; i < 100u; i++) {
		s += test[i];
		if (sum(test, (unsigned long) (i + 1l)) != s) {
			free(test);
			return 0u;
		} else {}
	}
	free(test);
	return 1u;

}


/*
 * Test the function which sets char pointer values from ordinal numbers
 * sent from Python at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_set_char_p_value(void) {

	unsigned short i;
	char *test = (char *) malloc (11u * sizeof(char));
	int *ords = (int *) malloc (10u * sizeof(int));
	for (i = 0u; i < 10u; i++) {
		ords[i] = 97 + i;
	}
	set_char_p_value(test, ords, 10u);
	unsigned short result = !strcmp(test, "abcdefghij");
	free(test);
	free(ords);
	return result;

}


/*
 * Test the max function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_max(void) {

	/*
	 * Test by ensuring it returns the final element from an array of
	 * least-to-greatest sorted values
	 */
	unsigned short i;
	double *test = (double *) malloc (100u * sizeof(double));
	for (i = 0u; i < 100u; i++) {
		test[i] = i;
	}
	unsigned short result = max(test, 100u) == test[99];
	free(test);
	return result;

}

