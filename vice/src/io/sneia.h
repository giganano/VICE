
#ifndef IO_SNEIA_H
#define IO_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Lookup the mass yield of a given element from type Ia supernovae
 *
 * Parameters
 * ==========
 * file: 		The name of the yield file, passed from python
 *
 * Returns
 * =======
 * The total mass yield in Msun of the given element reported by the built-in
 * study's data
 *
 * source: sneia.c
 */
extern double single_ia_mass_yield_lookup(char *file);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_SNEIA_H */

