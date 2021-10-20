

#ifndef YIELDS_H
#define YIELDS_H

#ifdef __cplusplus
extern "C" {
#endif

/* hash-code for euler's method */
#ifndef EULER
#define EULER 541
#endif /* EULER */

/* hash-code for trapezoid rule */
#ifndef TRAPEZOID
#define TRAPEZOID 978
#endif /* TRAPEZOID */

/* hash-code for midpoint rule */
#ifndef MIDPOINT
#define MIDPOINT 868
#endif /* MIDPOINT */

/* hash-code for simpson's rule */
#ifndef SIMPSON
#define SIMPSON 777
#endif /* SIMPSON */

#include "objects.h"
#include "objects/integral.h"
#include "objects/ccsne.h"
#include "yields/integral.h"
#include "yields/ccsne.h"

#ifdef __cplusplus
}
#endif

#endif /* YIELDS_H */
