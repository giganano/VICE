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
	vice.singlezone.name: 				"vice.singlezone.name", 
	vice.singlezone.func: 				"vice.singlezone.func", 
	vice.singlezone.mode: 				"vice.singlezone.mode", 
	vice.singlezone.verbose: 			"vice.singlezone.verbose", 
	vice.singlezone.elements: 			"vice.singlezone.elements", 
	vice.singlezone.IMF: 				"vice.singlezone.IMF", 
	vice.singlezone.eta: 				"vice.singlezone.eta" 
}

