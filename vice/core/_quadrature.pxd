# cython: language_level = 3, boundscheck = False 

cdef extern from "../src/quadrature.h": 
	double *quad(double (*func)(double), double a, double b, 
		double tolerance, char *method, long Nmax, long Nmin)

