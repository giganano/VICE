# cython: language_level = 3, boundscheck = False 
"""
This file wraps the C objects scripted in vice/src/objects.h. Their 
documentation is not duplicated here. See their source code for more details. 
"""

from libc.stdio cimport FILE 

cdef extern from "../src/objects.h": 
	ctypedef struct AGB_YIELD_GRID: 
		double **grid
		double *m
		double *z
		unsigned long n_m
		unsigned long n_z

	ctypedef struct CCSNE_YIELD_SPECS: 
		double *yield_ 
		double *grid 

	ctypedef struct SNEIA_YIELD_SPECS: 
		char *dtd 
		double yield_ 
		double *RIa 
		double tau_ia 
		double t_d 

	ctypedef struct ELEMENT: 
		AGB_YIELD_GRID *agb_grid 
		CCSNE_YIELD_SPECS *ccsne_yields 
		SNEIA_YIELD_SPECS *sneia_yields 
		char *symbol 
		double *Z 
		double *Zin 
		double mass 
		double solar 

	ctypedef struct ISM: 
		char *mode 
		double *specified 
		double mass 
		double star_formation_rate 
		double infall_rate 
		double *star_formation_history 
		double *eta 
		double *enh 
		double *tau_star 
		double schmidt_index 
		double mgschmidt 
		double smoothing_time 
		int schmidt 

	ctypedef struct MDF: 
		double **abundance_distributions 
		double **ratio_distributions 
		double *bins 
		unsigned long n_bins 

	ctypedef struct SSP: 
		char *imf 
		double *crf 
		double *msmf 
		double m_upper 
		double m_lower 
		double R0 
		int continuous 

	ctypedef struct SINGLEZONE: 
		char *name 
		FILE *history_writer 
		FILE *mdf_writer 
		double dt 
		double current_time 
		double *output_times 
		unsigned long timestep 
		unsigned long n_outputs 
		double Z_solar 
		unsigned int n_elements 
		int verbose 
		ELEMENT **elements 
		ISM *ism 
		MDF *mdf 
		SSP *ssp 

	ctypedef struct TRACER: 
		double mass 
		unsigned int zone_origin 
		unsigned int zone_current 
		unsigned long timestep_origin 

	ctypedef struct MULTIZONE: 
		char *name 
		SINGLEZONE **zones 
		unsigned int n_zones 
		unsigned int n_tracers 
		double ***migration_matrix_gas 
		double ***migration_matrix_tracers 
		unsigned long tracer_count 
		TRACER **tracers 
		int verbose 

	ctypedef struct FROMFILE: 
		char *name 
		char **labels 
		unsigned long n_rows 
		unsigned int n_cols 
		double **data 
