/*
 * This file implements pure utility functions.
 */

#include <sys/time.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <time.h>
#include "utils.h"
#include "singlezone.h"

/* Define the checksum function adopted in this implementation */
unsigned long (*checksum)(char *) = &simple_hash;


/*
 * Performs the choose operations between two positive numbers
 *
 * Parameters
 * ==========
 * a: 		The larger of the two values
 * b: 		The smaller of the two values
 *
 * Returns
 * =======
 * The value of a choose b. 0 if b > a.
 *
 * Notes
 * =====
 * Sometimes the choose operation is referred to as 'take' (i.e. a 'take' b
 * rather than a 'choose' b)
 *
 * header: utils.h
 */
extern unsigned long choose(unsigned long a, unsigned long b) {

	if (a > b) {
		/*
		 * a choose b = (a(a - 1)(a - 2)...(a - b + 1)) / b!
		 */
		unsigned long x = a;
		unsigned long y = b;
		unsigned long numerator = 1;
		unsigned long denominator = 1;
		while (y) {
			numerator *= x;
			denominator *= y;
			x--;
			y--;
		}
		return numerator / denominator;
	} else {
		return (a == b);
	}

}


/*
 * Determine the absolute value of a double x. This function extends the
 * standard library function abs, which only excepts values of type int.
 *
 * Parameters
 * ==========
 * x: 		The number to determine the absolute value of
 *
 * Returns
 * =======
 * +x if x >= 0, -x if x < 0
 *
 * header: utils.h
 */
extern double absval(double x) {

	return sign(x) * x;

}


/*
 * Determine the sign of a double x
 *
 * Parameters
 * ==========
 * x: 		The value to determine the sign of
 *
 * Returns
 * =======
 * +1 if x >= 0, -1 if x < 0
 *
 * header: utils.h
 */
extern short sign(double x) {

	return (x >= 0) - (x < 0);

}


/*
 * Obtain a simple hash for a string
 *
 * Parameters
 * ==========
 * str: 		The string to hash
 *
 * Returns
 * =======
 * The sum of the ordinal numbers for each character in the string
 *
 * Notes
 * =====
 * If this routine is modified, the following header files contain #define'd
 * hashes that need to be modified the match the returned value.
 *
 * header: utils.h
 */
extern unsigned long simple_hash(char *str) {

	unsigned long h = 0l;
	unsigned long i;
	for (i = 0l; i < strlen(str); i++) {
		/* VICE only allows ascii strings, so cast to unsigned is fine */
		h += (unsigned) tolower(str[i]);
	}
	return h;

}


/*
 * Seeds the random number generator off of the current time.
 *
 * Notes
 * =====
 * This function uses the current time of day to seed the random number
 * generator. It can be reseeded every 25 microseconds. This is nearly the
 * fastest it can be reseeded if seeding based on time with srand. srand takes
 * an unsigned int as a parameter, the maximum values for which is 2^32 - 1.
 * Dividing up the amount of time in one day by this value yields 20.116568
 * microseconds. This function thus divides the time of day in microseconds
 * by 25, using an overestimate to be safe, and uses this as the RNG seed.
 *
 * header: utils.h
 */
extern void seed_random(void) {

	struct timeval tv;
	gettimeofday(&tv, NULL);
	unsigned long time_in_microseconds = 1e6 * tv.tv_sec + tv.tv_usec;
	unsigned int seed = (unsigned int) (time_in_microseconds / 25l);
	srand(seed);

}


/*
 * Generate a pseudorandom number in a specified range.
 *
 * Parameters
 * ==========
 * minimum: 		The minimum value
 * maximum: 		The maximum value
 *
 * Returns
 * =======
 * A pseudorandom number between minimum and maximum
 *
 * header: utils.h
 */
extern double rand_range(double minimum, double maximum) {

	return minimum + (maximum - minimum) * ((double) rand() / RAND_MAX);

}


/*
 * A standard interpolation function. For two points (x1, y1) and (x2, y2),
 * this function draws the line between them and finds the expected value of y
 * for a given value of x via linear extrapolation.
 *
 * Parameters
 * ==========
 * x1: 		The first x-value
 * x2: 		The second x-value
 * y1: 		The first y-value
 * y2: 		The second y-value
 * x: 		The x-value to extrapolate to
 *
 * Returns
 * =======
 * y: The expected value for y such that (x, y) lies on the same line
 * defined by (x1, y1) and (x2, y2).
 *
 * header: utils.h
 */
extern double interpolate(double x1, double x2, double y1, double y2,
	double x) {

	/* Can be derived from the point-slope form of a line */
	return (y2 - y1) / (x2 - x1) * (x - x1) + y1;

}


/*
 * Two dimensional interpolation. For four points (x1, y1), (x1, y2), (x2, y1),
 * and (x2, y2) defining a square in the xy-plane, where the value of a
 * function f is known at those four points, determine an estimate of the value
 * of f at a point of interest (x0, y0).
 *
 * Parameters
 * ==========
 * x: 		A pointer to the values [x1, x2]
 * y: 		A pointer to the values [y1, y2]
 * f: 		A pointer to the values [f(x1, y1), f(x1, y2), f(x2, y1),
 * 				f(x2, y2)]
 * x0: 		The x-coordinate of the point of interest
 * y0: 		The y-coordinate of the point of interest
 *
 * Returns
 * =======
 * An estimate of the value of f(x, y) via three 1-dimensional linear
 * interpolation operations, allowing for extrapolation to points of
 * interest (x0, y0) not bound by the square definfed by x1, x2, y1, and y2.
 *
 * header: utils.h
 */
extern double interpolate2D(double x[2], double y[2], double f[2][2],
	double x0, double y0) {

	/*
	 * By implementing this is a chain of two 1-D interpolations,
	 * extrapolation to elements off the grid is allowed. This is
	 * necessary in determining yields of AGB stars at metallicities
	 * that are above and below the grid.
	 *
	 * First interpolate in the y-direction.
	 */
	double f_of_x1y0 = interpolate(y[0], y[1], f[0][0], f[0][1], y0);
	double f_of_x2y0 = interpolate(y[0], y[1], f[1][0], f[1][1], y0);

	/* Then in the x-direction */
	return interpolate(x[0], x[1], f_of_x1y0, f_of_x2y0, x0);

}


/*
 * Interpolation with a sqrt(x) dependence.
 *
 * Parameters
 * ==========
 * x1: 		The x-coordinate of the first point
 * x2: 		The x-coordinate of the second point
 * y1: 		The y-coordinate of the first point
 * y2: 		The y-coordinate of the second point
 * x: 		The x-coordinate of the point whose y-value is to be interpolated
 *
 * Returns
 * =======
 * The value y defined such that (x, y) lies on a sqrt(x) curve defined by
 * (x1, y1) and (x2, y2)
 *
 * header: utils.h
 */
extern double interpolate_sqrt(double x1, double x2, double y1, double y2,
	double x) {

	return (y2 - y1) * sqrt( (x - x1) / (x2 - x1) ) + y1;

}


/*
 * Gets the bin number for a given value in a specified array of bin edges.
 *
 * Parameters
 * ==========
 * binspace: 		A pointer to the bin edges
 * num_bins: 		The number of bins in the binspace. This should always be
 * 					1 less than the number of elements in this array.
 * value: 			The value to find the bin number for
 *
 * Returns
 * =======
 * The index (zero-based) of the bin number corresponding to the given value.
 * -1l in the case that the value does not lie in the given binspace.
 *
 * Notes
 * =====
 * It's assumed that the binspace is sorted from least to greatest. This should
 * always be the case in VICE's backend unless the code base has been altered.
 *
 * header: utils.h
 */
extern long get_bin_number(double *binspace, unsigned long num_bins,
	double value) {

	/*
	 * Notes
	 * =====
	 * This function used to search based on an if statement which checked if
	 * the lower edge was less than the value and that the value was less than
	 * the upper edge. This was embedded in a for-loop which returned -1l if it
	 * reached the end of the loop. Allowing the comparison to be done based
	 * on the upper edge alone (as implemented below) resulted in a ~20%
	 * increase in speed for values known to be within a given binspace.
	 */

	if (value < binspace[0] || value > binspace[num_bins]) {
		/* If the value does not lie within the given binspace */
		return -1l;
	} else {
		/*
		 * Increment the index by 1 until the next element is larger than the
		 * value. When that's true, the index is the bin number.
		 */
		unsigned long idx = 0ul;
		while (binspace[idx + 1ul] < value) idx++;
		return (signed) idx;
	}

}


/*
 * Determine the metallicity by mass of the ISM. This is not simply the sum
 * of the total metallicities by mass of each individual element. VICE employs
 * the following scaling relation:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * in order to prevent simulations tracking only a few elements from behaving
 * as if they have intrinsically low metallicities at all times. See section
 * 5.4 of VICE's science documentation for further details.
 *
 * Parameters
 * ==========
 * sz: 			The singlezone object associated with the current simulation.
 * timestep: 	The timestep number to find the proper metallicity for
 *
 * Returns
 * =======
 * The metallicity by mass of the ISM scaled according to the above relation.
 *
 * header: utils.h
 */
extern double scale_metallicity(SINGLEZONE sz, unsigned long timestep) {

	unsigned int i;
	double solar_by_element = 0, z_by_element = 0;

	/*
	 * Add up the solar abundance by mass of each element and the abundance
	 * by mass in the ISM of each element for only those tracked by the
	 * current simulation.
	 */
	for (i = 0; i < sz.n_elements; i++) {
		/* Don't count helium as a metal */
		if (strcmp((*sz.elements[i]).symbol, "he")) {
			solar_by_element += (*sz.elements[i]).solar;
			z_by_element += (*sz.elements[i]).Z[timestep];
		} else {}
	}

	return sz.Z_solar * z_by_element / solar_by_element;

}


/*
 * Returns a pointer to an array of linearly spaced doubles between two
 * specified values. For a binspace with N bins, the resulting array is of
 * length N + 1 due to the final bin edge.
 *
 * Parameters
 * ==========
 * start: 		The left-most bin edge
 * stop: 		The right-most bin edge
 * N: 			The number of desired bins
 *
 * header: utils.h
 */
extern double *binspace(double start, double stop, unsigned long N) {

	double *arr = (double *) malloc ((N + 1l) * sizeof(double));
	double dx = (stop - start) / N;
	unsigned long i;
	for (i = 0l; i <= N; i++) {
		arr[i] = start + i * dx;
	}
	return arr;

}


/*
 * Determine the center of each bin in an array of bin edges by taking the
 * arithmetic mean of adjacent bin edges. For a binspace with n bins (i.e. of
 * length n + 1), the resultant array from this function will be of length n.
 *
 * Parameters
 * ==========
 * edges: 		The bin edges themselves
 * n_bins: 		The number of bins in the binspace. This is always 1 less than
 * 				the number of elements in the edges array.
 *
 * Returns
 * =======
 * An array containing the arithmetic mean of adjacent bin edges.
 *
 * header: utils.h
 */
extern double *bin_centers(double *edges, unsigned long n_bins) {

	double *centers = (double *) malloc (n_bins * sizeof(double));
	unsigned long i;
	for (i = 0l; i < n_bins; i++) {
		centers[i] = (edges[i] + edges[i + 1l]) / 2.0;
	}
	return centers;

}


/*
 * Determine the sum of an array of double with known length.
 *
 * Parameters
 * ==========
 * arr: 		The array to sum
 * len: 		The number of elements in the array
 *
 * Returns
 * =======
 * The sum of all array elements
 *
 * header: utils.h
 */
extern double sum(double *arr, unsigned long len) {

	unsigned long i;
	double s = 0;
	for (i = 0l; i < len; i++) {
		s += arr[i];
	}
	return s;

}


/*
 * Sets the value of a string according to the ordinals of its values. Assumes
 * that the destination char * has already had memory allocated.
 *
 * Parameters
 * ==========
 * dest: 		The destination char pointer
 * ords: 		The ordinals for the string
 * length: 		The length of the string
 *
 * header: utils.h
 */
extern void set_char_p_value(char *dest, int *ords, int length) {

	int i;
	for (i = 0; i < length; i++) {
		dest[i] = ords[i];
	}
	dest[length] = '\0'; 	/* null terminator */

}


/*
 * Determine the maximum value stored in an array of double precision values.
 *
 * Parameters
 * ==========
 * arr: 		A pointer to the array itself
 * length: 		The number of values stored in the array
 *
 * Returns
 * =======
 * max_: The maximum value of the array
 *
 * header: utils.h
 */
extern double max(double *arr, unsigned long length) {

	if (length >= 2) {
		unsigned long i;
		double max_ = arr[0] > arr[1] ? arr[0] : arr[1];
		for (i = 2ul; i < length; i++) {
			max_ = arr[i] > max_ ? arr[i] : max_;
		}
		return max_;
	} else if (length == 1) {
		return arr[0];
	} else {
		return 0;
	}

}

