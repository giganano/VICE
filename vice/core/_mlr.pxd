# cython: language_level = 3, boundscheck = False

cdef class _mlr_linker:
	pass

cdef extern from "../src/ssp/mlr.h":
	unsigned short get_mlr_hashcode()
	unsigned short set_mlr_hashcode(unsigned short hashcode)




cdef class _powerlaw:
	pass

cdef extern from "../src/ssp/mlr/powerlaw.h":
	double powerlaw_turnoffmass(double time, double postMS, double Z)
	double powerlaw_lifetime(double mass, double postMS, double Z)




cdef class _vincenzo2016:
	cdef unsigned short _imported

cdef extern from "../src/ssp/mlr/vincenzo2016.h":
	double vincenzo2016_turnoffmass(double time, double postMS, double Z)
	double vincenzo2016_lifetime(double mass, double postMS, double Z)
	unsigned short vincenzo2016_import(char *filename)
	void vincenzo2016_free()




cdef class _hpt2000:
	cdef unsigned short _imported

cdef extern from "../src/ssp/mlr/hpt2000.h":
	double hpt2000_turnoffmass(double time, double postMS, double Z)
	double hpt2000_lifetime(double mass, double postMS, double Z)
	unsigned short hpt2000_import(char *filename)
	void hpt2000_free()




cdef class _ka1997:
	cdef unsigned short _imported

cdef extern from "../src/ssp/mlr/ka1997.h":
	double ka1997_turnoffmass(double time, double postMS, double Z)
	double ka1997_lifetime(double mass, double postMS, double Z)
	unsigned short ka1997_import(char *filename)
	void ka1997_free()




cdef class _pm1993:
	pass

cdef extern from "../src/ssp/mlr/pm1993.h":
	double pm1993_turnoffmass(double time, double postMS, double Z)
	double pm1993_lifetime(double mass, double postMS, double Z)




cdef class _mm1989:
	pass

cdef extern from "../src/ssp/mlr/mm1989.h":
	double mm1989_turnoffmass(double time, double postMS, double Z)
	double mm1989_lifetime(double mass, double postMS, double Z)




cdef class _larson1974:
	pass

cdef extern from "../src/ssp/mlr/larson1974.h":
	double larson1974_turnoffmass(double time, double postMS, double Z);
	double larson1974_lifetime(double mass, double postMS, double Z);

