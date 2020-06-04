""" 
This file declares a mapping of vice functions to the name of output files of 
their docstrings. 
""" 

import warnings 
warnings.filterwarnings("ignore") 
import vice 
from vice.yields.presets import JW20 
from vice.yields.ccsne import LC18 
from vice.yields.ccsne import CL13 
from vice.yields.ccsne import CL04 
from vice.yields.ccsne import WW95 
from vice.yields.sneia import iwamoto99 
from vice.yields.sneia import seitenzahl13 
from vice.yields.agb import cristallo11 
from vice.yields.agb import karakas10 

r""" 
Each element of the _CONFIG_ dictionary should map an object in VICE to a 
filename, a header, and subs. VICE itself is the root of the doctree. 	
""" 

_CONFIG_ = {
	vice: {
		"filename": 	"index.rst", 
		"header": 		"Package Contents", 
		"subs": 		[
			vice.version, 
			vice.atomic_number, 
			vice.primordial, 
			vice.solar_z, 
			vice.sources, 
			vice.stable_isotopes, 
			vice.cumulative_return_fraction, 
			vice.main_sequence_mass_fraction, 
			vice.single_stellar_population, 
			vice.dataframe, 
			vice.yields, 
			vice.elements, 
			vice.imf, 
			vice.singlezone, 
			vice.history, 
			vice.mdf, 
			vice.output, 
			vice.mirror, 
			vice.ScienceWarning, 
			vice.VisibleRuntimeWarning, 
			vice.VisibleDeprecationWarning, 
		]  
	}, 
	vice.version: {
		"filename": 	"vice.version.rst", 
		"header": 		"vice.version", 
		"subs": 		[]  
	}, 
	vice.ScienceWarning: {
		"filename": 	"vice.ScienceWarning.rst", 
		"header": 		"vice.ScienceWarning", 
		"subs": 		[] 
	}, 
	vice.VisibleRuntimeWarning: {
		"filename": 	"vice.VisibleRuntimeWarning.rst", 
		"header": 		"vice.VisibleRuntimeWarning", 
		"subs": 		[] 
	}, 
	vice.VisibleDeprecationWarning: {
		"filename": 	"vice.VisibleDeprecationWarning.rst", 
		"header": 		"vice.VisibleDeprecationWarning", 
		"subs": 		[] 
	}, 
	vice.atomic_number: {
		"filename": 	"vice.atomic_number.rst", 
		"header": 		"vice.atomic_number", 
		"subs": 		[] 
	}, 
	vice.primordial: {
		"filename": 	"vice.primordial.rst", 
		"header": 		"vice.primordial", 
		"subs": 		[] 
	}, 
	vice.solar_z: {
		"filename": 	"vice.solar_z.rst", 
		"header": 		"vice.solar_z", 
		"subs": 		[] 
	}, 
	vice.sources: {
		"filename": 	"vice.sources.rst", 
		"header": 		"vice.sources", 
		"subs": 		[] 
	}, 
	vice.stable_isotopes: {
		"filename": 	"vice.stable_isotopes.rst", 
		"header": 		"vice.stable_isotopes", 
		"subs": 		[] 
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
	vice.dataframe: {
		"filename":		"vice.core.dataframe.base.rst", 
		"header": 		"vice.dataframe", 
		"subs": 		[
			vice.dataframe.keys, 
			vice.dataframe.todict, 
			vice.dataframe.remove, 
			vice.dataframe.filter, 
			vice.core.dataframe.builtin_elemental_data, 
			vice.core.dataframe.elemental_settings, 
			vice.core.dataframe.evolutionary_settings, 
			vice.core.dataframe.fromfile, 
			vice.core.dataframe.noncustomizable, 
			vice.core.dataframe.history, 
			vice.core.dataframe.saved_yields 
		]  
	}, 
	vice.dataframe.keys: {
		"filename": 	"vice.core.dataframe.base.keys.rst", 
		"header": 		"vice.dataframe.keys", 
		"subs": 		[] 
	}, 
	vice.dataframe.todict: {
		"filename": 	"vice.core.dataframe.base.todict.rst", 
		"header": 		"vice.dataframe.todict", 
		"subs": 		[] 
	}, 
	vice.dataframe.remove: {
		"filename": 	"vice.core.dataframe.base.remove.rst", 
		"header": 		"vice.dataframe.remove", 
		"subs": 		[] 
	}, 
	vice.dataframe.filter: {
		"filename": 	"vice.core.dataframe.base.filter.rst", 
		"header": 		"vice.dataframe.filter", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.builtin_elemental_data: {
		"filename": 	"vice.core.dataframe.builtin_elemental_data.rst", 
		"header": 		"vice.core.dataframe.builtin_elemental_data", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.elemental_settings: {
		"filename": 	"vice.core.dataframe.elemental_settings.rst", 
		"header": 		"vice.core.dataframe.elemental_settings", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.evolutionary_settings: {
		"filename": 	"vice.core.dataframe.evolutionary_settings.rst", 
		"header": 		"vice.core.dataframe.evolutionary_settings", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.fromfile: {
		"filename": 	"vice.core.dataframe.fromfile.rst", 
		"header": 		"vice.core.dataframe.fromfile", 
		"subs": 		[
			vice.core.dataframe.fromfile.name, 
			vice.core.dataframe.fromfile.size 
		]  
	}, 
	vice.core.dataframe.fromfile.name: {
		"filename": 	"vice.core.dataframe.fromfile.name.rst", 
		"header": 		"vice.core.dataframe.fromfile.name", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.fromfile.size: {
		"filename": 	"vice.core.dataframe.fromfile.size.rst", 
		"header": 		"vice.core.dataframe.fromfile.size", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.noncustomizable: {
		"filename": 	"vice.core.dataframe.noncustomizable.rst", 
		"header": 		"vice.core.dataframe.noncustomizable", 
		"subs": 		[] 
	}, 
	vice.core.dataframe.history: {
		"filename": 	"vice.core.dataframe.history.rst", 
		"header": 		"vice.core.dataframe.history", 
		"subs": 		[
			vice.core.dataframe.history.name, 
			vice.core.dataframe.history.size 
		]  
	}, 
	vice.core.dataframe.saved_yields: {
		"filename": 	"vice.core.dataframe.saved_yields.rst", 
		"header": 		"vice.core.dataframe.saved_yields", 
		"subs": 		[] 
	}, 
	vice.yields: {
		"filename": 	"vice.yields.rst", 
		"header": 		"vice.yields", 
		"subs": 		[
			vice.yields.agb, 
			vice.yields.ccsne, 
			vice.yields.sneia, 
			vice.yields.presets 
		]  
	}, 
	vice.yields.agb: {
		"filename": 	"vice.yields.agb.rst", 
		"header": 		"vice.yields.agb", 
		"subs": 		[
			vice.yields.agb.grid 
		]  
	}, 
	vice.yields.agb.grid: {
		"filename": 	"vice.yields.agb.grid.rst", 
		"header": 		"vice.yields.agb.grid", 
		"subs": 		[] 
	}, 
	vice.yields.agb.cristallo11: {
		"filename": 	"vice.yields.agb.cristallo11.rst", 
		"header": 		"vice.yields.agb.cristallo11", 
		"subs": 		[] 
	}, 
	vice.yields.agb.karakas10: {
		"filename": 	"vice.yields.agb.karakas10.rst", 
		"header": 		"vice.yields.agb.karakas10", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne: {
		"filename": 	"vice.yields.ccsne.rst", 
		"header": 		"vice.yields.ccsne", 
		"subs": 		[
			vice.yields.ccsne.fractional, 
			vice.yields.ccsne.settings, 
			vice.yields.ccsne.WW95, 
			vice.yields.ccsne.CL04, 
			vice.yields.ccsne.CL13, 
			vice.yields.ccsne.LC18 
		]  
	}, 
	vice.yields.ccsne.fractional: {
		"filename": 	"vice.yields.ccsne.fractional.rst", 
		"header": 		"vice.yields.ccsne.fractional", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.settings: {
		"filename": 	"vice.yields.ccsne.settings.rst", 
		"header": 		"vice.yields.ccsne.settings", 
		"subs": 		[
			vice.yields.ccsne.settings.keys, 
			vice.yields.ccsne.settings.todict, 
			vice.yields.ccsne.settings.restore_defaults, 
			vice.yields.ccsne.settings.factory_settings, 
			vice.yields.ccsne.settings.save_defaults
		] 
	}, 
	vice.yields.ccsne.settings.keys: {
		"filename": 	"vice.yields.ccsne.settings.keys.rst", 
		"header": 		"vice.yields.ccsne.settings.keys", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.settings.todict: {
		"filename": 	"vice.yields.ccsne.settings.todict.rst", 
		"header": 		"vice.yields.ccsne.settings.todict", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.settings.restore_defaults: {
		"filename": 	"vice.yields.ccsne.settings.restore_defaults.rst", 
		"header": 		"vice.yields.ccsne.settings.restore_defaults", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.settings.factory_settings: {
		"filename": 	"vice.yields.ccsne.settings.factory_settings.rst", 
		"header": 		"vice.yields.ccsne.settings.factory_settings", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.settings.save_defaults: {
		"filename": 	"vice.yields.ccsne.settings.save_defaults.rst", 
		"header": 		"vice.yields.ccsne.settings.save_defaults", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.WW95: {
		"filename": 	"vice.yields.ccsne.WW95.rst", 
		"header": 		"vice.yields.ccsne.WW95", 
		"subs":			[vice.yields.ccsne.WW95.set_params] 
	}, 
	vice.yields.ccsne.WW95.set_params: {
		"filename": 	"vice.yields.ccsne.WW95.set_params.rst", 
		"header": 		"vice.yields.ccsne.WW95.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.CL04: {
		"filename": 	"vice.yields.ccsne.CL04.rst", 
		"header": 		"vice.yields.ccsne.CL04", 
		"subs": 		[vice.yields.ccsne.CL04.set_params]  
	}, 
	vice.yields.ccsne.CL04.set_params: {
		"filename": 	"vice.yields.ccsne.CL04.set_params.rst", 
		"header": 		"vice.yields.ccsne.CL04.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.CL13: {
		"filename": 	"vice.yields.ccsne.CL13.rst", 
		"header": 		"vice.yields.ccsne.CL13", 
		"subs": 		[vice.yields.ccsne.CL13.set_params]  
	}, 
	vice.yields.ccsne.CL13.set_params: {
		"filename": 	"vice.yields.ccsne.CL13.set_params.rst", 
		"header": 		"vice.yields.ccsne.CL13.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.ccsne.LC18: {
		"filename": 	"vice.yields.ccsne.LC18.rst", 
		"header": 		"vice.yields.ccsne.LC18", 
		"subs": 		[vice.yields.ccsne.LC18.set_params] 
	}, 
	vice.yields.ccsne.LC18.set_params: {
		"filename": 	"vice.yields.ccsne.LC18.set_params.rst", 
		"header": 		"vice.yields.ccsne.LC18.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.sneia: {
		"filename": 	"vice.yields.sneia.rst", 
		"header": 		"vice.yields.sneia", 
		"subs": 		[
			vice.yields.sneia.single, 
			vice.yields.sneia.fractional, 
			vice.yields.sneia.settings, 
			vice.yields.sneia.iwamoto99, 
			vice.yields.sneia.seitenzahl13 
		]  
	}, 
	vice.yields.sneia.single: {
		"filename": 	"vice.yields.sneia.single.rst", 
		"header": 		"vice.yields.sneia.single", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.fractional: {
		"filename": 	"vice.yields.sneia.fractional.rst", 
		"header": 		"vice.yields.sneia.fractional", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.settings: {
		"filename": 	"vice.yields.sneia.settings.rst", 
		"header": 		"vice.yields.sneia.settings", 
		"subs": 		[
			vice.yields.sneia.settings.keys, 
			vice.yields.sneia.settings.todict, 
			vice.yields.sneia.settings.restore_defaults, 
			vice.yields.sneia.settings.factory_settings, 
			vice.yields.sneia.settings.save_defaults 
		]  
	}, 
	vice.yields.sneia.settings.keys: {
		"filename": 	"vice.yields.sneia.settings.keys.rst", 
		"header" :		"vice.yields.sneia.settings.keys", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.settings.todict: {
		"filename": 	"vice.yields.sneia.settings.todict.rst", 
		"header": 		"vice.yields.sneia.settings.todict", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.settings.restore_defaults: {
		"filename": 	"vice.yields.sneia.settings.restore_defaults.rst", 
		"header": 		"vice.yields.sneia.settings.restore_defaults", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.settings.factory_settings: {
		"filename": 	"vice.yields.sneia.settings.factory_settings.rst", 
		"header": 		"vice.yields.sneia.settings.factory_settings", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.settings.save_defaults: {
		"filename": 	"vice.yields.sneia.settings.save_defaults.rst", 
		"header": 		"vice.yields.sneia.settings.save_defaults", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.iwamoto99: {
		"filename": 	"vice.yields.sneia.iwamoto99.rst", 
		"header": 		"vice.yields.sneia.iwamoto99", 
		"subs": 		[vice.yields.sneia.iwamoto99.set_params]  
	}, 
	vice.yields.sneia.iwamoto99.set_params: { 
		"filename": 	"vice.yields.sneia.iwamoto99.set_params.rst", 
		"header": 		"vice.yields.sneia.iwamoto99.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.sneia.seitenzahl13: {
		"filename": 	"vice.yields.sneia.seitenzahl13.rst", 
		"header": 		"vice.yields.sneia.seitenzahl13", 
		"subs": 		[vice.yields.sneia.seitenzahl13.set_params]  
	}, 
	vice.yields.sneia.seitenzahl13.set_params: {
		"filename": 	"vice.yields.sneia.seitenzahl13.set_params.rst", 
		"header": 		"vice.yields.sneia.seitenzahl13.set_params", 
		"subs": 		[] 
	}, 
	vice.yields.presets: {
		"filename": 	"vice.yields.presets.rst", 
		"header": 		"vice.yields.presets", 
		"subs": 		[
			vice.yields.presets.save, 
			vice.yields.presets.remove, 
			vice.yields.presets.JW20 
		] 
	}, 
	vice.yields.presets.save: {
		"filename": 	"vice.yields.presets.save.rst", 
		"header": 		"vice.yields.presets.save", 
		"subs": 		[] 
	}, 
	vice.yields.presets.remove: {
		"filename": 	"vice.yields.presets.remove.rst", 
		"header": 		"vice.yields.presets.remove", 
		"subs": 		[] 
	}, 
	vice.yields.presets.JW20: {
		"filename": 	"vice.yields.presets.JW20.rst", 
		"header": 		"vice.yields.presets.JW20", 
		"subs": 		[ 
			vice.yields.presets.JW20.alt_cc_sr_linear, 
			vice.yields.presets.JW20.alt_cc_sr_limitexp 
		] 
	}, 
	vice.yields.presets.JW20.alt_cc_sr_linear: {
		"filename": 	"vice.yields.presets.JW20.alt_cc_sr_linear.rst", 
		"header": 		"vice.yields.presets.JW20.alt_cc_sr_linear", 
		"subs": 		[] 
	}, 
	vice.yields.presets.JW20.alt_cc_sr_limitexp: {
		"filename": 	"vice.yields.presets.JW20.alt_cc_sr_limitexp.rst", 
		"header": 		"vice.yields.presets.JW20.alt_cc_sr_limitexp", 
		"subs": 		[] 
	}, 
	vice.elements: {
		"filename": 	"vice.elements.rst", 
		"header": 		"vice.elements", 
		"subs": 		[
			vice.elements.element, 
			vice.elements.yields 
		] 
	}, 
	vice.elements.element: {
		"filename": 	"vice.elements.element.rst", 
		"header": 		"vice.elements.element", 
		"subs": 		[
			vice.elements.element.symbol, 
			vice.elements.element.name, 
			vice.elements.element.yields, 
			vice.elements.element.atomic_number, 
			vice.elements.element.primordial, 
			vice.elements.element.solar_z, 
			vice.elements.element.sources, 
			vice.elements.element.stable_isotopes 
		]  
	}, 
	vice.elements.element.symbol: {
		"filename": 	"vice.elements.element.symbol.rst", 
		"header": 		"vice.elements.element.symbol", 
		"subs": 		[] 
	}, 
	vice.elements.element.name: {
		"filename": 	"vice.elements.element.name.rst", 
		"header": 		"vice.elements.element.name", 
		"subs": 		[] 
	}, 
	vice.elements.element.yields: {
		"filename": 	"vice.elements.element.yields.rst", 
		"header": 		"vice.elements.element.yields", 
		"subs": 		[] 
	}, 
	vice.elements.element.atomic_number: {
		"filename": 	"vice.elements.element.atomic_number.rst", 
		"header": 		"vice.elements.element.atmoic_number", 
		"subs": 		[] 
	}, 
	vice.elements.element.primordial: {
		"filename": 	"vice.elements.element.primordial.rst", 
		"header": 		"vice.elements.element.primordial", 
		"subs": 		[] 
	}, 
	vice.elements.element.solar_z: {
		"filename": 	"vice.elements.element.solar_z.rst", 
		"header": 		"vice.elements.element.solar_z", 
		"subs": 		[] 
	}, 
	vice.elements.element.sources: {
		"filename": 	"vice.elements.element.sources.rst", 
		"header": 		"vice.elements.element.sources", 
		"subs": 		[] 
	}, 
	vice.elements.element.stable_isotopes: {
		"filename": 	"vice.elements.element.stable_isotopes.rst", 
		"header": 		"vice.elements.element.stable_isotopes", 
		"subs": 		[] 
	}, 
	vice.elements.yields: {
		"filename": 	"vice.elements.yields.rst", 
		"header": 		"vice.elements.yields", 
		"subs": 		[
			vice.elements.yields.agb, 
			vice.elements.yields.ccsne, 
			vice.elements.yields.sneia 
		]  
	}, 
	vice.elements.yields.agb: {
		"filename": 	"vice.elements.yields.agb.rst", 
		"header": 		"vice.elements.yield.agb", 
		"subs": 		[] 
	}, 
	vice.elements.yields.ccsne: {
		"filename": 	"vice.elements.yields.ccsne.rst", 
		"header": 		"vice.elements.yields.ccsne", 
		"subs": 		[] 
	}, 
	vice.elements.yields.sneia: {
		"filename": 	"vice.elements.yields.sneia.rst", 
		"header": 		"vice.elements.yields.sneia", 
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
			vice.singlezone.run, 
			vice.singlezone.from_output, 
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
	vice.singlezone.run: {
		"filename": 	"vice.singlezone.run.rst", 
		"header": 		"vice.singlezone.run", 
		"subs": 		[] 
	}, 
	vice.singlezone.from_output: {
		"filename": 	"vice.singlezone.from_output.rst", 
		"header": 		"vice.singlezone.from_output", 
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
	}, 
	vice.history: {
		"filename": 	"vice.history.rst", 
		"header": 		"vice.history", 
		"subs": 		[] 
	}, 
	vice.mdf: {
		"filename": 	"vice.mdf.rst", 
		"header": 		"vice.mdf", 
		"subs": 		[] 
	}, 
	vice.output: {
		"filename": 	"vice.output.rst", 
		"header": 		"vice.output", 
		"subs": 		[
			vice.output.name, 
			vice.output.elements, 
			vice.output.history, 
			vice.output.mdf, 
			vice.output.agb_yields, 
			vice.output.ccsne_yields, 
			vice.output.sneia_yields, 
			vice.output.show, 
			vice.output.zip, 
			vice.output.unzip 
		]  
	}, 
	vice.output.name: {
		"filename": 	"vice.output.name.rst", 
		"header": 		"vice.output.name", 
		"subs": 		[] 
	}, 
	vice.output.elements: {
		"filename": 	"vice.output.elements.rst", 
		"header": 		"vice.output.elements", 
		"subs": 		[] 
	}, 
	vice.output.history: {
		"filename": 	"vice.output.history.rst", 
		"header": 		"vice.output.history", 
		"subs": 		[] 
	}, 
	vice.output.mdf: {
		"filename": 	"vice.output.mdf.rst", 
		"header": 		"vice.output.mdf", 
		"subs": 		[] 
	}, 
	vice.output.agb_yields: {
		"filename": 	"vice.output.agb_yields.rst", 
		"header": 		"vice.output.agb_yields", 
		"subs": 		[] 
	}, 
	vice.output.ccsne_yields: {
		"filename": 	"vice.output.ccsne_yields.rst", 
		"header": 		"vice.output.ccsne_yields", 
		"subs": 		[] 
	}, 
	vice.output.sneia_yields: {
		"filename": 	"vice.output.sneia_yields.rst", 
		"header": 		"vice.output.sneia_yields", 
		"subs": 		[] 
	}, 
	vice.output.show: {
		"filename": 	"vice.output.show.rst", 
		"header": 		"vice.output.show", 
		"subs": 		[] 
	}, 
	vice.output.zip: {
		"filename": 	"vice.output.zip.rst", 
		"header": 		"vice.output.zip", 
		"subs": 		[] 
	}, 
	vice.output.unzip: {
		"filename": 	"vice.output.unzip.rst", 
		"header": 		"vice.output.unzip", 
		"subs": 		[] 
	}, 
	vice.mirror: {
		"filename": 	"vice.mirror.rst", 
		"header": 		"vice.mirror", 
		"subs": 		[] 
	}

}

