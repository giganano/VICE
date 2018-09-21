
#include <math.h>
#include "specs.h"
#include "enrichment.h"

/*
Returns the time derivative of the mass of an element from CCSNe at the 
current timestep. 

Args:
=====
run:		The INTEGRATION structure for the current execution
index:		The index of the element
*/
extern double mdot_ccsne(INTEGRATION run, int index) {

	return run.elements[index].ccsne_yield * run.SFR;

}

/* 
Sets the elements IMF-integrated CCSNe yield parameter to the specified value.

Args:
=====
e:			A point to the the element struct to hold the yield
value:		The yield itself
*/
extern int set_ccsne_yield(INTEGRATION *run, int index, double value) {

	ELEMENT *e = &((*run).elements[index]);
	e -> ccsne_yield = value;
	return 1;


}

