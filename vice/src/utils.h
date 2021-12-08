/*
 * Utility functions
 */

#ifndef UTILS_H
#define UTILS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

extern unsigned long (*checksum)(char *);

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
 * source: utils.c
 */
extern unsigned long choose(unsigned long a, unsigned long b);

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
 * source: utils.c
 */
extern double absval(double x);

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
 * source: utils.c
 */
extern short sign(double x);

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
 * source: utils.c
 */
extern unsigned long simple_hash(char *str);

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
 * source: utils.c
 */
extern void seed_random(void);

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
 * source: utils.c
 */
extern double rand_range(double minimum, double maximum);

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
 * y: The expected value for y such that (x, y) lies on the same line defined
 * by (x1, y1) and (x2, y2).
 *
 * source: utils.c
 */
extern double interpolate(double x1, double x2, double y1, double y2,
	double x);

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
 * f: 		A pointer to the values [f(x1, y1), f(x1, y2), f(x2, y1), f(x2, y2)]
 * x0: 		The x-coordinate of the point of interest
 * y0: 		The y-coordinate of the point of interest
 *
 * Returns
 * =======
 * An estimate of the value of f(x, y) via three 1-dimensional linear
 * interpolation operations, allowing for extrapolation to points of
 * interest (x0, y0) not bound by the square definfed by x1, x2, y1, and y2.
 *
 * source: utils.c
 */
extern double interpolate2D(double x[2], double y[2], double f[2][2], double x0,
	double y0);

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
 * source: utils.c
 */
extern double interpolate_sqrt(double x1, double x2, double y1, double y2,
	double x);

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
 * source: utils.c
 */
extern long get_bin_number(double *binspace, unsigned long num_bins,
	double value);

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
 * source: utils.c
 */
extern double scale_metallicity(SINGLEZONE sz, unsigned long timestep);

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
 * source: utils.c
 */
extern double *binspace(double start, double stop, unsigned long N);

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
 * source: utils.c
 */
extern double *bin_centers(double *edges, unsigned long n_bins);

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
 * source: utils.c
 */
extern double sum(double *arr, unsigned long len);

/*
 * Sets the value of a string according to the ordinals of its values. Assumes
 * that the destination char * has already had memory allocated, which is
 * true for all C-level objects in VICE.
 *
 * Parameters
 * ==========
 * dest: 		The destination char pointer
 * ords: 		The ordinals for the string
 * length: 		The length of the string
 *
 * source: utils.c
 */
 extern void set_char_p_value(char *dest, int *ords, int length);

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
 * source: utils.c
 */
extern double max(double *arr, unsigned long length);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* UTILS_H */

