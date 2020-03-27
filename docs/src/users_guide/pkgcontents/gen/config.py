""" 
This file declares a mapping of vice functions to the name of output files of 
their docstrings. 
""" 

import warnings 
warnings.filterwarnings("ignore") 
import vice 


_CONFIG_ = {
	vice: {
		"filename": 	"index.rst", 
		"header": 		"Package Contents", 
		"subs": 		[
			vice.cumulative_return_fraction, 
			vice.main_sequence_mass_fraction, 
			vice.single_stellar_population, 
			vice.imf, 
			vice.singlezone 
		]  
	}, 
	vice.cumulative_return_fraction: {
		"filename": 	"vice.cumulative_return_fraction.rst", 
		"header": 		"vice.cumulative_return_fraction", 
		"subs": 		[] 
	}, 
	vice.main_sequence_mass_fraction: {
		"filename": 	"vice.main_sequence_mass_fraction.rst", 
		"header": 		"vice.main_sequence_mass_fraction", 
		"subs": 		[] 
	}, 
	vice.single_stellar_population: {
		"filename": 	"vice.single_stellar_populaiton.rst", 
		"header": 		"vice.single_stellar_population", 
		"subs": 		[] 
	}, 
	vice.imf: {
		"filename": 	"vice.imf.rst", 
		"header": 		"vice.imf", 
		"subs": 		[
			vice.imf.kroupa, 
			vice.imf.salpeter 
		] 
	}, 
	vice.imf.kroupa: {
		"filename": 	"vice.imf.kroupa.rst", 
		"header": 		"vice.imf.kroupa", 
		"subs": 		[] 
	}, 
	vice.imf.salpeter: {
		"filename": 	"vice.imf.salpeter.rst", 
		"header": 		"vice.imf.salpeter", 
		"subs": 		[] 
	}, 
	vice.singlezone: {
		"filename": 	"vice.singlezone.rst", 
		"header": 		"vice.singlezone", 
		"subs": 		[
			vice.singlezone.from_output, 
			vice.singlezone.run, 
			vice.singlezone.name, 
			vice.singlezone.func, 
			vice.singlezone.mode, 
			vice.singlezone.verbose, 
			vice.singlezone.elements, 
			vice.singlezone.IMF, 
			vice.singlezone.eta, 
			vice.singlezone.enhancement, 
			vice.singlezone.Zin, 
			vice.singlezone.recycling, 
			vice.singlezone.bins, 
			vice.singlezone.delay, 
			vice.singlezone.RIa, 
			vice.singlezone.Mg0, 
			vice.singlezone.smoothing, 
			vice.singlezone.tau_ia, 
			vice.singlezone.tau_star, 
			vice.singlezone.dt, 
			vice.singlezone.schmidt, 
			vice.singlezone.schmidt_index, 
			vice.singlezone.MgSchmidt, 
			vice.singlezone.m_upper, 
			vice.singlezone.m_lower, 
			vice.singlezone.postMS, 
			vice.singlezone.Z_solar, 
			vice.singlezone.agb_model 
		] 
	}, 
	vice.singlezone.from_output: {
		"filename": 	"vice.singlezone.from_output.rst", 
		"header": 		"vice.singlezone.from_output", 
		"subs": 		[] 
	}, 
	vice.singlezone.run: {
		"filename": 	"vice.singlezone.run.rst", 
		"header": 		"vice.singlezone.run", 
		"subs": 		[] 
	}, 
	vice.singlezone.name: {
		"filename": 	"vice.singlezone.name.rst", 
		"header": 		"vice.singlezone.name", 
		"subs": 		[] 
	}, 
	vice.singlezone.func: {
		"filename": 	"vice.singlezone.func.rst", 
		"header": 		"vice.singlezone.func", 
		"subs": 		[] 
	}, 
	vice.singlezone.mode: {
		"filename": 	"vice.singlezone.mode.rst", 
		"header": 		"vice.singlezone.mode", 
		"subs": 		[] 
	}, 
	vice.singlezone.verbose: {
		"filename": 	"vice.singlezone.verbose.rst", 
		"header": 		"vice.singlezone.verbose", 
		"subs": 		[] 
	}, 
	vice.singlezone.elements: {
		"filename": 	"vice.singlezone.elements.rst", 
		"header": 		"vice.singlezone.elements", 
		"subs": 		[] 
	}, 
	vice.singlezone.IMF: {
		"filename": 	"vice.singlezone.IMF.rst", 
		"header": 		"vice.singlezone.IMF", 
		"subs": 		[] 
	}, 
	vice.singlezone.eta: {
		"filename": 	"vice.singlezone.eta.rst", 
		"header": 		"vice.singlezone.eta", 
		"subs": 		[] 
	}, 
	vice.singlezone.enhancement: {
		"filename": 	"vice.singlezone.enhancement.rst", 
		"header": 		"vice.singlezone.enhancement", 
		"subs": 		[] 
	}, 
	vice.singlezone.Zin: {
		"filename": 	"vice.singlezone.Zin.rst", 
		"header": 		"vice.singlezone.Zin", 
		"subs": 		[] 
	}, 
	vice.singlezone.recycling: {
		"filename": 	"vice.singlezone.recycling.rst", 
		"header": 		"vice.singlezone.recycling", 
		"subs": 		[] 
	}, 
	vice.singlezone.bins: {
		"filename":		"vice.singlezone.bins.rst", 
		"header": 		"vice.singlezone.bins", 
		"subs": 		[] 
	}, 
	vice.singlezone.delay: {
		"filename": 	"vice.singlezone.delay.rst", 
		"header": 		"vice.singlezone.delay", 
		"subs": 		[] 
	}, 
	vice.singlezone.RIa: {
		"filename": 	"vice.singlezone.RIa.rst", 
		"header": 		"vice.singlezone.RIa", 
		"subs": 		[] 
	}, 
	vice.singlezone.Mg0: {
		"filename": 	"vice.singlezone.Mg0.rst", 
		"header": 		"vice.singlezone.Mg0", 
		"subs": 		[] 
	}, 
	vice.singlezone.smoothing: {
		"filename": 	"vice.singlezone.smoothing.rst", 
		"header": 		"vice.singlezone.smoothing", 
		"subs": 		[] 
	}, 
	vice.singlezone.tau_ia: { 
		"filename": 	"vice.singlezone.tau_ia.rst", 
		"header": 		"vice.singlezone.tau_ia", 
		"subs": 		[] 
	}, 
	vice.singlezone.tau_star: {
		"filename": 	"vice.singlezone.tau_star.rst", 
		"header": 		"vice.singlezone.tau_star", 
		"subs": 		[] 
	}, 
	vice.singlezone.dt: {
		"filename": 	"vice.singlezone.dt.rst", 
		"header": 		"vice.singlezone.dt", 
		"subs": 		[] 
	}, 
	vice.singlezone.schmidt: {
		"filename": 	"vice.singlezone.schmidt.rst", 
		"header": 		"vice.singlezone.schmidt", 
		"subs": 		[] 
	}, 
	vice.singlezone.schmidt_index: {
		"filename": 	"vice.singlezone.schmidt_index.rst", 
		"header": 		"vice.singlezone.schmidt_index", 
		"subs": 		[] 
	}, 
	vice.singlezone.MgSchmidt: {
		"filename": 	"vice.singlezon.MgSchmidt.rst", 
		"header": 		"vice.singlezone.MgSchmidt", 
		"subs": 		[] 
	}, 
	vice.singlezone.m_upper: {
		"filename": 	"vice.singlezone.m_upper.rst", 
		"header": 		"vice.singlezone.m_upper", 
		"subs": 		[] 
	}, 
	vice.singlezone.m_lower: {
		"filename": 	"vice.singlezone.m_lower.rst", 
		"header": 		"vice.singlezone.m_lower", 
		"subs": 		[] 
	}, 
	vice.singlezone.postMS: {
		"filename": 	"vice.singlezone.postMS.rst", 
		"header": 		"vice.singlezone.postMS", 
		"subs": 		[] 
	}, 
	vice.singlezone.Z_solar: {
		"filename": 	"vice.singlezone.Z_solar.rst", 
		"header": 		"vice.singlezone.Z_solar", 
		"subs": 		[] 
	}, 
	vice.singlezone.agb_model: {
		"filename": 	"vice.singlezone.agb_model.rst", 
		"header": 		"vice.singlezone.agb_model", 
		"subs": 		[] 
	}
}

