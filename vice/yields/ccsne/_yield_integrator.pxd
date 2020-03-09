# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h": 
	ctypedef struct IMF_: 
		char *spec 
		double m_lower 
		double m_upper 
		double *mass_distribution 
		CALLBACK_1ARG *custom_imf 

	ctypedef struct CALLBACK_1ARG: 
		double (*callback)(double, void *) 
		void *user_func 

	ctypedef struct INTEGRAL: 
		double (*func)(double) 
		double a 
		double b 
		double tolerance 
		unsigned long method 
		unsigned long Nmax 
		unsigned long Nmin 
		unsigned long iters 
		double result 
		double error 


cdef extern from "../../src/objects/integral.h": 
	INTEGRAL *integral_initialize() 
	void integral_free(INTEGRAL *intgrl) 


cdef extern from "../../src/objects/callback_1arg.h": 
	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 


cdef extern from "../../src/yields/ccsne.h": 
	unsigned short IMFintegrated_fractional_yield_numerator(
		INTEGRAL *intgrl, IMF_ *imf, CALLBACK_1ARG *explodability, 
		char *file) 
	extern unsigned short IMFintegrated_fractional_yield_denominator(
		INTEGRAL *intgrl, IMF_ *imf) 


cdef extern from "../../src/imf.h": 
	void imf_free(IMF_ *imf) 

