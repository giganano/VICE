
#ifndef MODELING_LIKELIHOOD_H
#define MODELING_LIKELIHOOD_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Compute the natural logarithm of the likelihood that a given data vector
 * (in practice, a single star) arose from a model-predicted track through some
 * observed space (in practice, chemical-age space).
 *
 * Parameters
 * ==========
 * d: 		The datum itself as a vector in the observed space
 * t: 		The track itself as a matrix in the observed space. This may contain
 * 			more quantities than are present in the datum. The appropriate
 * 			quantities to base the calculation on will be determined by a
 * 			comparison of the datum and track labels.
 *
 * Returns
 * =======
 * ln L(D_i | M), defined as the line integral of a weighted likelihood
 * estimate along the length of the track. See Johnson et al. (2022) for
 * details.
 *
 * References
 * ==========
 * Johnson et al. (2022), arxiv:2210.01816
 *
 * source: likelihood.c
 */
extern double loglikelihood(DATUM d, TRACK t);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MODELING_LIKELIHOOD_H */
