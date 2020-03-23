""" 
This file declares a mapping of vice functions to the name of output files of 
their docstrings. 
""" 

import warnings 
warnings.filterwarnings("ignore") 
import vice 

_MAPPING_ = {
	vice.cumulative_return_fraction:	"vice.cumulative_return_fraction", 
	vice.main_sequence_mass_fraction: 	"vice.main_sequence_mass_fraction", 
	vice.single_stellar_population: 	"vice.single_stellar_population", 
	vice.imf.kroupa: 					"vice.imf.kroupa", 
	vice.imf.salpeter: 					"vice.imf.salpeter", 
	vice.singlezone: 					"vice.singlezone", 
	vice.singlezone.from_output: 		"vice.singlezone.from_output", 
	vice.singlezone.run: 				"vice.singlezone.run", 
	vice.singlezone.name: 				"vice.singlezone.name", 
	vice.singlezone.func: 				"vice.singlezone.func", 
	vice.singlezone.mode: 				"vice.singlezone.mode", 
	vice.singlezone.verbose: 			"vice.singlezone.verbose", 
	vice.singlezone.elements: 			"vice.singlezone.elements", 
	vice.singlezone.IMF: 				"vice.singlezone.IMF", 
	vice.singlezone.eta: 				"vice.singlezone.eta", 
	vice.singlezone.enhancement: 		"vice.singlezone.enhancement", 
	vice.singlezone.entrainment: 		"vice.singlezone.entrainment", 
	vice.singlezone.Zin: 				"vice.singlezone.Zin", 
	vice.singlezone.recycling: 			"vice.singlezone.recycling", 
	vice.singlezone.bins: 				"vice.singlezone.bins", 
	vice.singlezone.delay: 				"vice.singlezone.delay", 
	vice.singlezone.RIa: 				"vice.singlezone.RIa", 
	vice.singlezone.Mg0: 				"vice.singlezone.Mg0", 
	vice.singlezone.smoothing: 			"vice.singlezone.smoothing", 
	vice.singlezone.tau_ia: 			"vice.singlezone.tau_ia", 
	vice.singlezone.tau_star: 			"vice.singlezone.tau_star", 
	vice.singlezone.dt: 				"vice.singlezone.dt", 
	vice.singlezone.schmidt: 			"vice.singlezone.schmidt", 
	vice.singlezone.MgSchmidt: 			"vice.singlezone.MgSchmidt", 
	vice.singlezone.schmidt_index: 		"vice.singlezone.schmidt_index", 
	vice.singlezone.m_upper: 			"vice.singlezone.m_upper", 
	vice.singlezone.m_lower: 			"vice.singlezone.m_lower", 
	vice.singlezone.postMS: 			"vice.singlezone.postMS", 
	vice.singlezone.Z_solar: 			"vice.singlezone.Z_solar", 
	vice.singlezone.agb_model: 			"vice.singlezone.agb_model" 	
}

