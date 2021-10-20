
#ifndef TESTS_YIELDS_INTEGRAL_H
#define TESTS_YIELDS_INTEGRAL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef TEST_INTEGRAL_TOLERANCE
#define TEST_INTEGRAL_TOLERANCE 1e-6
#endif /* TEST_INTEGRAL_TOLERANCE */

#include "../../objects.h"

/*
 * Test the numerical quadrature implementation of Euler's method
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_quad_euler(void);

/*
 * Test the numerical quadrature implementation of trapezoid rule
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_quad_trapzd(void);

/*
 * Test the numerical quadrature implementation of midpoint rule
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_quad_midpt(void);

/*
 * Test the numerical quadrature implementation of Simpson's method
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_quad_simp(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_YIELDS_INTEGRAL_H */
