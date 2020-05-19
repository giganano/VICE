# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from .....core.singlezone._singlezone cimport c_singlezone 
from .....core.objects._singlezone cimport SINGLEZONE 

### For use in constructing the quiescence edge-case test ### 
cdef class quiescence(c_singlezone): 
	pass 


cdef extern from "../../singlezone.h": 
	unsigned short singlezone_setup(SINGLEZONE *sz) 
	void singlezone_evolve_no_setup_no_clean(SINGLEZONE *sz) 


cdef extern from "../../mdf.h": 
	void normalize_MDF(SINGLEZONE *sz) 


cdef extern from "../../../io/singlezone.h": 
	void write_mdf_output(SINGLEZONE sz) 



### Quiescence edge-case unit tests ### 
cdef extern from "../agb.h": 
	unsigned short quiescence_test_m_AGB(SINGLEZONE *sz) 

cdef extern from "../ccsne.h": 
	unsigned short quiescence_test_m_ccsne(SINGLEZONE *sz) 

cdef extern from "../element.h": 
	unsigned short quiescence_test_update_element_mass(SINGLEZONE *sz) 
	unsigned short quiescence_test_onH(SINGLEZONE *sz) 

cdef extern from "../ism.h": 
	unsigned short quiescence_test_update_gas_evolution(SINGLEZONE *sz) 
	unsigned short quiescence_test_get_outflow_rate(SINGLEZONE *sz) 
	unsigned short quiescence_test_singlezone_unretained(SINGLEZONE *sz) 

