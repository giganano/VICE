
#ifndef YIELDS_INTEGRAL_H
#define YIELDS_INTEGRAL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Evaluate an integral from a to b numerically using quadrature
 *
 * Parameters
 * ==========
 * intgrl: 		The integral object
 *
 * Returns
 * =======
 * 0 on success, 1 on an error larger than the tolerance, and 2 on an
 * unrecognized evaluation method
 *
 * Notes & References
 * ==================
 * The methods of numerical quadrature implemented in this function and its
 * subroutines are adopted from Chapter 4 of Numerical Recipes (Press,
 * Teukolsky, Vetterling & Flannery 2007), Cambridge University Press.
 *
 * source: integral.c
 */
extern unsigned short quad(INTEGRAL *intgrl);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* YIELDS_INTEGRAL_H */

