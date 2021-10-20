
#ifndef IO_AGB_H
#define IO_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Import a built-in AGB star yields grid.
 *
 * Parameters
 * ==========
 * e: 		A pointer to the element struct to import the grid into
 * file: 	The name of the file containing the AGB yield grid. These are
 * 			include in VICE's data directory, and direct user access to them
 * 			is strongly discouraged.
 *
 * Returns
 * =======
 * 0 on success; nonzer on failure
 *
 * source: agb.c
 */
extern unsigned short import_agb_grid(ELEMENT *e, char *file);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_AGB_H */

