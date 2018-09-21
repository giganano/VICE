
#include <math.h>
#include "cc_yields.h"

/* The Salpeter IMF as a function of mass, up to a normalization constant */
extern double salpeter(double m) {

	return pow(m, -2.35);

}

/* The Kroupa IMF as a function of mass, up to a normalization constant */
extern double kroupa(double m) {

	if (m < 0.08) {
		return pow(m, -0.3);
	} else if (0.08 <= m && m <= 0.5) {
		return pow(m, -1.3);
	} else {
		return pow(m, -2.3);
	}

}

