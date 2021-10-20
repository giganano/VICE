"""
This file declares a mapping of vice functions to the name of output files of
their docstrings.
"""

import warnings
warnings.filterwarnings("ignore")
# partial import -> only documentation aspects required
import builtins
builtins.__VICE_DOCS__ = True
import vice
from vice.yields.presets import JW20
from vice.yields.ccsne import LC18
from vice.yields.ccsne import NKT13
from vice.yields.ccsne import CL13
from vice.yields.ccsne import CL04
from vice.yields.ccsne import WW95
from vice.yields.ccsne import S16
from vice.yields.ccsne.S16 import N20
from vice.yields.ccsne.S16 import W18
from vice.yields.ccsne.S16 import W18F
from vice.yields.sneia import iwamoto99
from vice.yields.sneia import seitenzahl13
from vice.yields.sneia import gronow21
from vice.yields.agb import cristallo11
from vice.yields.agb import karakas10
from vice.yields.agb import ventura13
from vice.yields.agb import karakas16
from vice.core.singlezone.entrainment import entrainment
from vice.toolkit import J21_sf_law
from vice.yields.ccsne.engines.E16 import E16
from vice.yields.ccsne.engines.cutoff import cutoff
from vice.yields.ccsne.engines.S16.N20 import N20
from vice.yields.ccsne.engines.S16.S19p8 import S19p8
from vice.yields.ccsne.engines.S16.W15 import W15
from vice.yields.ccsne.engines.S16.W18 import W18
from vice.yields.ccsne.engines.S16.W20 import W20

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
			vice.mlr,
			vice.yields,
			vice.elements,
			vice.imf,
			vice.singlezone,
			vice.multizone,
			vice.milkyway,
			vice.migration,
			vice.history,
			vice.mdf,
			vice.output,
			vice.multioutput,
			vice.stars,
			vice.mirror,
			vice.toolkit,
			vice.dataframe,
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
		"filename": 	"vice.single_stellar_population.rst",
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
			vice.core.dataframe.agb_yield_settings,
			vice.core.dataframe.ccsn_yield_table,
			vice.core.dataframe.channel_entrainment,
			vice.core.dataframe.elemental_settings,
			vice.core.dataframe.evolutionary_settings,
			vice.core.dataframe.fromfile,
			vice.core.dataframe.history,
			vice.core.dataframe.noncustomizable,
			vice.core.dataframe.saved_yields,
			vice.core.dataframe.tracers,
			vice.core.dataframe.yield_settings
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
		"subs": 		[vice.solar_z.epsilon_to_z_conversion]
	},
	vice.solar_z.epsilon_to_z_conversion: {
		"filename": 	"vice.solar_z.epsilon_to_z_conversion.rst",
		"header": 		"vice.solar_z.epsilon_to_z_conversion",
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
	vice.core.dataframe.agb_yield_settings: {
		"filename": 	"vice.core.dataframe.agb_yield_settings.rst",
		"header": 		"vice.core.dataframe.agb_yield_settings",
		"subs": 		[]
	},
	vice.core.dataframe.ccsn_yield_table: {
		"filename": 	"vice.core.dataframe.ccsn_yield_table.rst",
		"header": 		"vice.core.dataframe.ccsn_yield_table",
		"subs": 		[
			vice.core.dataframe.ccsn_yield_table.masses,
			vice.core.dataframe.ccsn_yield_table.isotopes
		]
	},
	vice.core.dataframe.ccsn_yield_table.masses: {
		"filename": 	"vice.core.dataframe.ccsn_yield_table.masses.rst",
		"header": 		"vice.core.dataframe.ccsn_yield_table.masses",
		"subs": 		[]
	},
	vice.core.dataframe.ccsn_yield_table.isotopes: {
		"filename": 	"vice.core.dataframe.ccsn_yield_table.isotopes.rst",
		"header": 		"vice.core.dataframe.ccsn_yield_table.isotopes",
		"subs": 		[]
	},
	vice.core.dataframe.channel_entrainment: {
		"filename": 	"vice.core.dataframe.channel_entrainment.rst",
		"header": 		"vice.core.dataframe.channel_entrainment",
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
	vice.core.dataframe.tracers: {
		"filename": 	"vice.core.dataframe.tracers.rst",
		"header": 		"vice.core.dataframe.tracers",
		"subs": 		[
			vice.core.dataframe.tracers.name,
			vice.core.dataframe.tracers.size
		]
	},
	vice.core.dataframe.yield_settings: {
		"filename": 	"vice.core.dataframe.yield_settings.rst",
		"header": 		"vice.core.dataframe.yield_settings",
		"subs": 		[
			vice.core.dataframe.yield_settings.restore_defaults,
			vice.core.dataframe.yield_settings.factory_settings,
			vice.core.dataframe.yield_settings.save_defaults
		]
	},
	vice.core.dataframe.yield_settings.restore_defaults: {
		"filename": 	"vice.core.dataframe.yield_settings.restore_defaults.rst",
		"header": 		"vice.core.dataframe.yield_settings.restore_defaults",
		"subs": 		[]
	},
	vice.core.dataframe.yield_settings.factory_settings: {
		"filename": 	"vice.core.dataframe.yield_settings.factory_settings.rst",
		"header": 		"vice.core.dataframe.yield_settings.factory_settings",
		"subs": 		[]
	},
	vice.core.dataframe.yield_settings.save_defaults: {
		"filename": 	"vice.core.dataframe.yield_settings.save_defaults.rst",
		"header": 		"vice.core.dataframe.yield_settings.save_defaults",
		"subs": 		[]
	},
	vice.mlr: {
		"filename": 	"vice.mlr.rst",
		"header": 		"vice.mlr",
		"subs":  		[
			type(vice.mlr).setting,
			type(vice.mlr).recognized,
			vice.mlr.powerlaw,
			vice.mlr.vincenzo2016,
			vice.mlr.hpt2000,
			vice.mlr.ka1997,
			vice.mlr.pm1993,
			vice.mlr.mm1989,
			vice.mlr.larson1974
		]
	},
	type(vice.mlr).setting: {
		"filename": 	"vice.mlr.setting.rst",
		"header": 		"vice.mlr.setting",
		"subs": 		[]
	},
	type(vice.mlr).recognized: {
		"filename": 	"vice.mlr.recognized.rst",
		"header": 		"vice.mlr.recognized",
		"subs": 		[]
	},
	vice.mlr.powerlaw: {
		"filename": 	"vice.mlr.powerlaw.rst",
		"header": 		"vice.mlr.powerlaw",
		"subs": 		[]
	},
	vice.mlr.vincenzo2016: {
		"filename": 	"vice.mlr.vincenzo2016.rst",
		"header": 		"vice.mlr.vincenzo2016",
		"subs": 		[]
	},
	vice.mlr.hpt2000: {
		"filename": 	"vice.mlr.hpt2000.rst",
		"header": 		"vice.mlr.hpt2000",
		"subs": 		[]
	},
	vice.mlr.ka1997: {
		"filename": 	"vice.mlr.ka1997.rst",
		"header": 		"vice.mlr.ka1997",
		"subs": 		[]
	},
	vice.mlr.pm1993: {
		"filename": 	"vice.mlr.pm1993.rst",
		"header": 		"vice.mlr.pm1993",
		"subs": 		[]
	},
	vice.mlr.mm1989: {
		"filename": 	"vice.mlr.mm1989.rst",
		"header": 		"vice.mlr.mm1989",
		"subs": 		[]
	},
	vice.mlr.larson1974: {
		"filename": 	"vice.mlr.larson1974.rst",
		"header": 		"vice.mlr.larson1974",
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
			vice.yields.agb.grid,
			vice.yields.agb.interpolator,
			vice.yields.agb.settings,
			vice.yields.agb.cristallo11,
			vice.yields.agb.karakas10,
			vice.yields.agb.ventura13,
			vice.yields.agb.karakas16
		]
	},
	vice.yields.agb.grid: {
		"filename": 	"vice.yields.agb.grid.rst",
		"header": 		"vice.yields.agb.grid",
		"subs": 		[]
	},
	vice.yields.agb.interpolator: {
		"filename": 	"vice.yields.agb.interpolator.rst",
		"header": 		"vice.yields.agb.interpolator",
		"subs": 		[
			vice.yields.agb.interpolator.masses,
			vice.yields.agb.interpolator.metallicities,
			vice.yields.agb.interpolator.yields
		]
	},
	vice.yields.agb.interpolator.masses: {
		"filename": 	"vice.yields.agb.interpolator.masses.rst",
		"header": 		"vice.yields.agb.interpolator.masses",
		"subs": 		[]
	},
	vice.yields.agb.interpolator.metallicities: {
		"filename": 	"vice.yields.agb.interpolator.metallicities.rst",
		"header": 		"vice.yields.agb.interpolator.metallicities",
		"subs": 		[]
	},
	vice.yields.agb.interpolator.yields: {
		"filename": 	"vice.yields.agb.interpolator.yields.rst",
		"header": 		"vice.yields.agb.interpolator.yields",
		"subs": 		[]
	},
	vice.yields.agb.settings: {
		"filename": 	"vice.yields.agb.settings.rst",
		"header": 		"vice.yields.agb.settings",
		"subs": 		[
			vice.yields.agb.settings.keys,
			vice.yields.agb.settings.todict,
			vice.yields.agb.settings.restore_defaults,
			vice.yields.agb.settings.factory_settings,
			vice.yields.agb.settings.save_defaults
		]
	},
	vice.yields.agb.settings.keys: {
		"filename": 	"vice.yields.agb.settings.keys.rst",
		"header": 		"vice.yields.agb.settings.keys",
		"subs": 		[]
	},
	vice.yields.agb.settings.todict: {
		"filename": 	"vice.yields.agb.settings.todict.rst",
		"header": 		"vice.yields.agb.settings.todict",
		"subs": 		[]
	},
	vice.yields.agb.settings.restore_defaults: {
		"filename": 	"vice.yields.agb.settings.restore_defaults.rst",
		"header": 		"vice.yields.agb.settings.restore_defaults",
		"subs": 		[]
	},
	vice.yields.agb.settings.factory_settings: {
		"filename": 	"vice.yields.agb.settings.factory_settings.rst",
		"header": 		"vice.yields.agb.settings.factory_settings",
		"subs": 		[]
	},
	vice.yields.agb.settings.save_defaults: {
		"filename": 	"vice.yields.agb.settings.save_defaults.rst",
		"header": 		"vice.yields.agb.settings.save_defaults",
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
	vice.yields.agb.ventura13: {
		"filename": 	"vice.yields.agb.ventura13.rst",
		"header": 		"vice.yields.agb.ventura13",
		"subs": 		[]
	},
	vice.yields.agb.karakas16: {
		"filename": 	"vice.yields.agb.karakas16.rst",
		"header": 		"vice.yields.agb.karakas16",
		"subs": 		[]
	},
	vice.yields.ccsne: {
		"filename": 	"vice.yields.ccsne.rst",
		"header": 		"vice.yields.ccsne",
		"subs": 		[
			vice.yields.ccsne.fractional,
			vice.yields.ccsne.table,
			vice.yields.ccsne.settings,
			vice.yields.ccsne.engines,
			vice.yields.ccsne.WW95,
			vice.yields.ccsne.CL04,
			vice.yields.ccsne.CL13,
			vice.yields.ccsne.NKT13,
			vice.yields.ccsne.S16,
			vice.yields.ccsne.LC18
		]
	},
	vice.yields.ccsne.fractional: {
		"filename": 	"vice.yields.ccsne.fractional.rst",
		"header": 		"vice.yields.ccsne.fractional",
		"subs": 		[]
	},
	vice.yields.ccsne.table: {
		"filename": 	"vice.yields.ccsne.table.rst",
		"header": 		"vice.yields.ccsne.table",
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
	vice.yields.ccsne.engines: {
		"filename": 	"vice.yields.ccsne.engines.rst",
		"header": 		"vice.yields.ccsne.engines",
		"subs": 		[
			vice.yields.ccsne.engines.engine,
			cutoff,
			E16,
			vice.yields.ccsne.engines.S16
		]
	},
	vice.yields.ccsne.engines.engine: {
		"filename": 	"vice.yields.ccsne.engines.engine.rst",
		"header": 		"vice.yields.ccsne.engines.engine",
		"subs": 		[
			vice.yields.ccsne.engines.engine.masses,
			vice.yields.ccsne.engines.engine.frequencies
			]
	},
	vice.yields.ccsne.engines.engine.masses: {
		"filename": 	"vice.yields.ccsne.engines.engine.masses.rst",
		"header": 		"vice.yields.ccsne.engines.engine.masses",
		"subs": 		[]
	},
	vice.yields.ccsne.engines.engine.frequencies: {
		"filename": 	"vice.yields.ccsne.engines.engine.frequencies.rst",
		"header": 		"vice.yields.ccsne.engines.engine.frequencies",
		"subs": 		[]
	},
	cutoff: {
		"filename": 	"vice.yields.ccsne.engines.cutoff.rst",
		"header": 		"vice.yields.ccsne.engines.cutoff",
		"subs": 		[cutoff.collapse_mass]
	},
	cutoff.collapse_mass: {
		"filename": 	"vice.yields.ccsne.engines.cutoff.collapse_mass.rst",
		"header": 		"vice.yields.ccsne.engines.cutoff.collapse_mass",
		"subs": 		[]
	},
	E16: {
		"filename": 	"vice.yields.ccsne.engines.E16.rst",
		"header": 		"vice.yields.ccsne.engines.E16",
		"subs": 		[
			E16.m4,
			E16.mu4,
			E16.slope,
			E16.intercept
		]
	},
	E16.m4: {
		"filename": 	"vice.yields.ccsne.engines.E16.m4.rst",
		"header": 		"vice.yields.ccsne.engines.E16.m4",
		"subs": 		[]
	},
	E16.mu4: {
		"filename": 	"vice.yields.ccsne.engines.E16.mu4.rst",
		"header": 		"vice.yields.ccsne.engines.E16.mu4",
		"subs": 		[]
	},
	E16.slope: {
		"filename": 	"vice.yields.ccsne.engines.E16.slope.rst",
		"header": 		"vice.yields.ccsne.engines.E16.slope",
		"subs": 		[]
	},
	E16.intercept: {
		"filename": 	"vice.yields.ccsne.engines.E16.intercept.rst",
		"header": 		"vice.yields.ccsne.engines.E16.intercept",
		"subs": 		[]
	},
	vice.yields.ccsne.engines.S16: {
		"filename": 	"vice.yields.ccsne.engines.S16.rst",
		"header": 		"vice.yields.ccsne.engines.S16",
		"subs": 		[
			N20,
			S19p8,
			W15,
			W18,
			W20
		]
	},
	N20: {
		"filename": 	"vice.yields.ccsne.engines.S16.N20.rst",
		"header": 		"vice.yields.ccsne.engines.S16.N20",
		"subs": 		[]
	},
	S19p8: {
		"filename": 	"vice.yields.ccsne.engines.S16.S19p8.rst",
		"header": 		"vice.yields.ccsne.engines.S16.S19p8",
		"subs": 		[]
	},
	W15: {
		"filename": 	"vice.yields.ccsne.engines.S16.W15.rst",
		"header": 		"vice.yields.ccsne.engines.S16.W15",
		"subs": 		[]
	},
	W18: {
		"filename": 	"vice.yields.ccsne.engines.S16.W18.rst",
		"header": 		"vice.yields.ccsne.engines.S16.W18",
		"subs": 		[]
	},
	W20: {
		"filename": 	"vice.yields.ccsne.engines.S16.W20.rst",
		"header": 		"vice.yields.ccsne.engines.S16.W20",
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
	vice.yields.ccsne.NKT13: {
		"filename": 	"vice.yields.ccsne.NKT13.rst",
		"header": 		"vice.yields.ccsne.NKT13",
		"subs": 		[vice.yields.ccsne.NKT13.set_params]
	},
	vice.yields.ccsne.NKT13.set_params: {
		"filename": 	"vice.yields.ccsne.NKT13.set_params.rst",
		"header": 		"vice.yields.ccsne.NKT13.set_params",
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
	vice.yields.ccsne.S16: {
		"filename": 	"vice.yields.ccsne.S16.rst",
		"header": 		"vice.yields.ccsne.S16",
		"subs": 		[
			vice.yields.ccsne.S16.N20,
			vice.yields.ccsne.S16.W18,
			vice.yields.ccsne.S16.W18F]
	},
	vice.yields.ccsne.S16.N20: {
		"filename": 	"vice.yields.ccsne.S16.N20.rst",
		"header": 		"vice.yields.ccsne.S16.N20",
		"subs": 		[vice.yields.ccsne.S16.N20.set_params]
	},
	vice.yields.ccsne.S16.N20.set_params: {
		"filename": 	"vice.yields.ccsne.S16.N20.set_params.rst",
		"header": 		"vice.yields.ccsne.S16.N20.set_params",
		"subs": 		[]
	},
	vice.yields.ccsne.S16.W18: {
		"filename": 	"vice.yields.ccsne.S16.W18.rst",
		"header": 		"vice.yields.ccsne.S16.W18",
		"subs": 		[vice.yields.ccsne.S16.W18.set_params]
	},
	vice.yields.ccsne.S16.W18.set_params: {
		"filename": 	"vice.yields.ccsne.S16.W18.set_params.rst",
		"header": 		"vice.yields.ccsne.S16.W18.set_params",
		"subs": 		[]
	},
	vice.yields.ccsne.S16.W18F: {
		"filename": 	"vice.yields.ccsne.S16.W18F.rst",
		"header": 		"vice.yields.ccsne.S16.W18F",
		"subs": 		[vice.yields.ccsne.S16.W18F.set_params]
	},
	vice.yields.ccsne.S16.W18F.set_params: {
		"filename": 	"vice.yields.ccsne.S16.W18F.set_params.rst",
		"header": 		"vice.yields.ccsne.S16.W18F.set_params",
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
			vice.yields.sneia.seitenzahl13,
			vice.yields.sneia.gronow21
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
	vice.yields.sneia.gronow21: {
		"filename": 	"vice.yields.sneia.gronow21.rst",
		"header": 		"vice.yields.sneia.gronow21",
		"subs": 		[vice.yields.sneia.gronow21.set_params]
	},
	vice.yields.sneia.gronow21.set_params: {
		"filename": 	"vice.yields.sneia.gronow21.set_params.rst",
		"header": 		"vice.yields.sneia.gronow21.set_params",
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
			vice.elements.recognized,
			vice.elements.element,
			vice.elements.yields
		]
	},
	vice.elements.recognized: {
		"filename": 	"vice.elements.recognized.rst",
		"header": 		"vice.elements.recognized",
		"subs": 		[]
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
		"header": 		"vice.elements.element.atomic_number",
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
		"header": 		"vice.elements.yields.agb",
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
			vice.singlezone.entrainment,
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
	vice.singlezone.entrainment: {
		"filename": 	"vice.singlezone.entrainment.rst",
		"header": 		"vice.singlezone.entrainment",
		"subs": 		[
			entrainment.agb,
			entrainment.ccsne,
			entrainment.sneia
		]
	},
	entrainment.agb: {
		"filename": 	"vice.singlezone.entrainment.agb.rst",
		"header": 		"vice.singlezone.entrainment.agb",
		"subs": 		[]
	},
	entrainment.ccsne: {
		"filename": 	"vice.singlezone.entrainment.ccsne.rst",
		"header": 		"vice.singlezone.entrainment.ccsne",
		"subs": 		[]
	},
	entrainment.sneia: {
		"filename": 	"vice.singlezone.entrainment.sneia.rst",
		"header": 		"vice.singlezone.entrainment.sneia",
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
	vice.multizone: {
		"filename": 	"vice.multizone.rst",
		"header": 		"vice.multizone",
		"subs": 		[
			vice.multizone.run,
			vice.multizone.from_output,
			vice.multizone.name,
			vice.multizone.zones,
			vice.multizone.migration,
			vice.multizone.n_zones,
			vice.multizone.n_stars,
			vice.multizone.verbose,
			vice.multizone.simple
		]
	},
	vice.multizone.run: {
		"filename": 	"vice.multizone.run.rst",
		"header": 		"vice.multizone.run",
		"subs": 		[]
	},
	vice.multizone.from_output: {
		"filename": 	"vice.multizone.from_output.rst",
		"header": 		"vice.multizone.from_output",
		"subs": 		[]
	},
	vice.multizone.name: {
		"filename": 	"vice.multizone.name.rst",
		"header": 		"vice.multizone.name",
		"subs": 		[]
	},
	vice.multizone.zones: {
		"filename": 	"vice.multizone.zones.rst",
		"header": 		"vice.multizone.zones",
		"subs": 		[]
	},
	vice.multizone.migration: {
		"filename": 	"vice.multizone.migration.rst",
		"header": 		"vice.multizone.migration",
		"subs": 		[]
	},
	vice.multizone.n_zones: {
		"filename": 	"vice.multizone.n_zones.rst",
		"header": 		"vice.multizone.n_zones",
		"subs": 		[]
	},
	vice.multizone.n_stars: {
		"filename": 	"vice.multizone.n_stars.rst",
		"header": 		"vice.multizone.n_stars",
		"subs": 		[]
	},
	vice.multizone.verbose: {
		"filename": 	"vice.multizone.verbose.rst",
		"header": 		"vice.multizone.verbose",
		"subs": 		[]
	},
	vice.multizone.simple: {
		"filename": 	"vice.multizone.simple.rst",
		"header": 		"vice.multizone.simple",
		"subs": 		[]
	},
	vice.milkyway: {
		"filename": 	"vice.milkyway.rst",
		"header": 		"vice.milkyway",
		"subs": 		[
			vice.milkyway.annuli,
			vice.milkyway.zone_width,
			vice.milkyway.evolution,
			vice.milkyway.default_evolution,
			vice.milkyway.mode,
			vice.milkyway.elements,
			vice.milkyway.IMF,
			vice.milkyway.mass_loading,
			vice.milkyway.default_mass_loading,
			vice.milkyway.dt,
			vice.milkyway.bins,
			vice.milkyway.delay,
			vice.milkyway.RIa,
			vice.milkyway.smoothing,
			vice.milkyway.tau_ia,
			vice.milkyway.m_upper,
			vice.milkyway.m_lower,
			vice.milkyway.postMS,
			vice.milkyway.Z_solar]
	},
	vice.milkyway.annuli: {
		"filename": 	"vice.milkyway.annuli.rst",
		"header": 		"vice.milkyway.annuli",
		"subs": 		[]
	},
	vice.milkyway.zone_width: {
		"filename": 	"vice.milkyway.zone_width.rst",
		"header": 		"vice.milkyway.zone_width",
		"subs": 		[]
	},
	vice.milkyway.evolution: {
		"filename": 	"vice.milkyway.evolution.rst",
		"header": 		"vice.milkyway.evolution",
		"subs": 		[]
	},
	vice.milkyway.default_evolution: {
		"filename": 	"vice.milkyway.default_evolution.rst",
		"header": 		"vice.milkyway.default_evolution",
		"subs": 		[]
	},
	vice.milkyway.mode: {
		"filename": 	"vice.milkyway.mode.rst",
		"header": 		"vice.milkyway.mode",
		"subs": 		[]
	},
	vice.milkyway.elements: {
		"filename": 	"vice.milkyway.elements.rst",
		"header": 		"vice.milkyway.elements",
		"subs": 		[]
	},
	vice.milkyway.IMF: {
		"filename": 	"vice.milkyway.IMF.rst",
		"header": 		"vice.milkyway.IMF",
		"subs": 		[]
	},
	vice.milkyway.mass_loading: {
		"filename": 	"vice.milkyway.mass_loading.rst",
		"header": 		"vice.milkyway.mass_loading",
		"subs": 		[]
	},
	vice.milkyway.default_mass_loading: {
		"filename": 	"vice.milkyway.default_mass_loading.rst",
		"header": 		"vice.milkyway.default_mass_loading",
		"subs": 		[]
	},
	vice.milkyway.dt: {
		"filename": 	"vice.milkyway.dt.rst",
		"header": 		"vice.milkyway.dt",
		"subs": 		[]
	},
	vice.milkyway.bins: {
		"filename": 	"vice.milkyway.bins.rst",
		"header": 		"vice.milkyway.bins",
		"subs": 		[]
	},
	vice.milkyway.delay: {
		"filename": 	"vice.milkyway.delay.rst",
		"header": 		"vice.milkyway.delay",
		"subs": 		[]
	},
	vice.milkyway.RIa: {
		"filename": 	"vice.milkyway.RIa.rst",
		"header": 		"vice.milkyway.RIa",
		"subs": 		[]
	},
	vice.milkyway.smoothing: {
		"filename": 	"vice.milkyway.smoothing.rst",
		"header": 		"vice.milkyway.smoothing",
		"subs": 		[]
	},
	vice.milkyway.tau_ia: {
		"filename": 	"vice.milkyway.tau_ia.rst",
		"header": 		"vice.milkyway.tau_ia",
		"subs": 		[]
	},
	vice.milkyway.m_upper: {
		"filename": 	"vice.milkyway.m_upper.rst",
		"header": 		"vice.milkyway.m_upper",
		"subs": 		[]
	},
	vice.milkyway.m_lower: {
		"filename": 	"vice.milkyway.m_lower.rst",
		"header": 		"vice.milkyway.m_lower",
		"subs": 		[]
	},
	vice.milkyway.postMS: {
		"filename": 	"vice.milkyway.postMS.rst",
		"header": 		"vice.milkyway.postMS",
		"subs": 		[]
	},
	vice.milkyway.Z_solar: {
		"filename": 	"vice.milkyway.Z_solar.rst",
		"header": 		"vice.milkyway.Z_solar",
		"subs": 		[]
	},
	vice.migration: {
		"filename": 	"vice.migration.rst",
		"header": 		"vice.migration",
		"subs": 		[
			vice.migration.specs,
			vice.migration.migration_matrix
		]
	},
	vice.migration.specs: {
		"filename": 	"vice.migration.specs.rst",
		"header": 		"vice.migration.specs",
		"subs": 		[
			vice.migration.specs.gas,
			vice.migration.specs.stars
		]
	},
	vice.migration.specs.gas: {
		"filename": 	"vice.migration.specs.gas.rst",
		"header": 		"vice.migration.specs.gas",
		"subs": 		[]
	},
	vice.migration.specs.stars: {
		"filename": 	"vice.migration.specs.stars.rst",
		"header": 		"vice.migration.specs.stars",
		"subs": 		[]
	},
	vice.migration.migration_matrix: {
		"filename": 	"vice.migration.migration_matrix.rst",
		"header": 		"vice.migration.migration_matrix",
		"subs": 		[
			vice.migration.migration_matrix.size,
			vice.migration.migration_matrix.tolist,
			vice.migration.migration_matrix.tonumpyarray
		]
	},
	vice.migration.migration_matrix.size: {
		"filename": 	"vice.migration.migration_matrix.size.rst",
		"header": 		"vice.migration.migration_matrix.size",
		"subs": 		[]
	},
	vice.migration.migration_matrix.tolist: {
		"filename": 	"vice.migration.migration_matrix.tolist.rst",
		"header": 		"vice.migration.migration_matrix.tolist",
		"subs": 		[]
	},
	vice.migration.migration_matrix.tonumpyarray: {
		"filename": 	"vice.migration.migration_matrix.tonumpyarray.rst",
		"header": 		"vice.migration.migration_matrix.tonumpyarray",
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
	vice.multioutput: {
		"filename": 	"vice.multioutput.rst",
		"header": 		"vice.multioutput",
		"subs": 		[
			vice.multioutput.name,
			vice.multioutput.zones,
			vice.multioutput.stars
		]
	},
	vice.multioutput.name: {
		"filename": 	"vice.multioutput.name.rst",
		"header": 		"vice.multioutput.name",
		"subs": 		[]
	},
	vice.multioutput.zones: {
		"filename": 	"vice.multioutput.zones.rst",
		"header": 		"vice.multioutput.zones",
		"subs": 		[]
	},
	vice.multioutput.stars: {
		"filename": 	"vice.multioutput.stars.rst",
		"header": 		"vice.multioutput.stars",
		"subs": 		[]
	},
	vice.stars: {
		"filename": 	"vice.stars.rst",
		"header": 		"vice.stars",
		"subs": 		[]
	},
	vice.mirror: {
		"filename": 	"vice.mirror.rst",
		"header": 		"vice.mirror",
		"subs": 		[]
	},
	vice.toolkit: {
		"filename": 	"vice.toolkit.rst",
		"header": 		"vice.toolkit",
		"subs": 		[
			vice.toolkit.hydrodisk,
			vice.toolkit.interpolation,
			vice.toolkit.J21_sf_law
		]
	},
	vice.toolkit.hydrodisk: {
		"filename": 	"vice.toolkit.hydrodisk.rst",
		"header": 		"vice.toolkit.hydrodisk",
		"subs": 		[vice.toolkit.hydrodisk.hydrodiskstars]
	},
	vice.toolkit.hydrodisk.hydrodiskstars: {
		"filename": 	"vice.toolkit.hydrodisk.hydrodiskstars.rst",
		"header": 		"vice.toolkit.hydrodisk.hydrodiskstars",
		"subs": 		[
			vice.toolkit.hydrodisk.hydrodiskstars.radial_bins,
			vice.toolkit.hydrodisk.hydrodiskstars.analog_data,
			vice.toolkit.hydrodisk.hydrodiskstars.analog_index,
			vice.toolkit.hydrodisk.hydrodiskstars.mode,
			vice.toolkit.hydrodisk.hydrodiskstars.decomp_filter
		]
	},
	vice.toolkit.hydrodisk.hydrodiskstars.radial_bins: {
		"filename": 	"vice.toolkit.hydrodisk.hydrodiskstars.radial_bins.rst",
		"header": 		"vice.toolkit.hydrodisk.hydrodiskstars.radial_bins",
		"subs": 		[]
	},
	vice.toolkit.hydrodisk.hydrodiskstars.analog_data: {
		"filename": 	"vice.toolkit.hydrodisk.hydrodiskstars.analog_data.rst",
		"header": 		"vice.toolkit.hydrodisk.hydrodiskstars.analog_data",
		"subs": 		[]
	},
	vice.toolkit.hydrodisk.hydrodiskstars.analog_index: {
		"filename": "vice.toolkit.hydrodisk.hydrodiskstars.analog_index.rst",
		"header": 	"vice.toolkit.hydrodisk.hydrodiskstars.analog_index",
		"subs": 	[]
	},
	vice.toolkit.hydrodisk.hydrodiskstars.mode: {
		"filename": 	"vice.toolkit.hydrodisk.hydrodiskstars.mode.rst",
		"header": 		"vice.toolkit.hydrodisk.hydrodiskstars.mode",
		"subs": 		[]
	},
	vice.toolkit.hydrodisk.hydrodiskstars.decomp_filter: {
		"filename": 	"vice.toolkit.hydrodisk.hydrodiskstars.decomp_filter.rst",
		"header": 		"vice.toolkit.hydrodisk.hydrodiskstars.decomp_filter",
		"subs": 		[]
	},
	vice.toolkit.interpolation: {
		"filename": 	"vice.toolkit.interpolation.rst",
		"header": 		"vice.toolkit.interpolation",
		"subs": 		[
			vice.toolkit.interpolation.interp_scheme_1d,
			vice.toolkit.interpolation.interp_scheme_2d
		]
	},
	vice.toolkit.interpolation.interp_scheme_1d: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_1d.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_1d",
		"subs": 		[
			vice.toolkit.interpolation.interp_scheme_1d.xcoords,
			vice.toolkit.interpolation.interp_scheme_1d.ycoords,
			vice.toolkit.interpolation.interp_scheme_1d.n_points
		]
	},
	vice.toolkit.interpolation.interp_scheme_1d.xcoords: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_1d.xcoords.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_1d.xcoords",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_1d.ycoords: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_1d.ycoords.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_1d.ycoords",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_1d.n_points: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_1d.n_points.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_1d.n_points",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_2d: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d",
		"subs": 		[
			vice.toolkit.interpolation.interp_scheme_2d.xcoords,
			vice.toolkit.interpolation.interp_scheme_2d.ycoords,
			vice.toolkit.interpolation.interp_scheme_2d.zcoords,
			vice.toolkit.interpolation.interp_scheme_2d.n_x_values,
			vice.toolkit.interpolation.interp_scheme_2d.n_y_values
		]
	},
	vice.toolkit.interpolation.interp_scheme_2d.xcoords: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.xcoords.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d.xcoords",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_2d.ycoords: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.ycoords.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d.ycoords",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_2d.zcoords: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.zcoords.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d.zcoords",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_2d.n_x_values: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.n_x_values.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d.n_x_values",
		"subs": 		[]
	},
	vice.toolkit.interpolation.interp_scheme_2d.n_y_values: {
		"filename": 	"vice.toolkit.interpolation.interp_scheme_2d.n_y_values.rst",
		"header": 		"vice.toolkit.interpolation.interp_scheme_2d.n_y_values",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law: {
		"filename": 	"vice.toolkit.J21_sf_law.rst",
		"header": 		"vice.toolkit.J21_sf_law",
		"subs": 		[
			vice.toolkit.J21_sf_law.area,
			vice.toolkit.J21_sf_law.molecular,
			vice.toolkit.J21_sf_law.present_day_molecular,
			vice.toolkit.J21_sf_law.molecular_index,
			vice.toolkit.J21_sf_law.Sigma_g1,
			vice.toolkit.J21_sf_law.Sigma_g2,
			vice.toolkit.J21_sf_law.index1,
			vice.toolkit.J21_sf_law.index2
		]
	},
	vice.toolkit.J21_sf_law.area: {
		"filename": 	"vice.toolkit.J21_sf_law.area.rst",
		"header": 		"vice.toolkit.J21_sf_law.area",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.molecular: {
		"filename": 	"vice.toolkit.J21_sf_law.molecular.rst",
		"header": 		"vice.toolkit.J21_sf_law.molecular",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.present_day_molecular: {
		"filename": 	"vice.toolkit.J21_sf_law.present_day_molecular.rst",
		"header": 		"vice.toolkit.J21_sf_law.present_day_molecular",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.molecular_index: {
		"filename": 	"vice.toolkit.J21_sf_law.molecular_index.rst",
		"header": 		"vice.toolkit.J21_sf_law.molecular_index",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.Sigma_g1: {
		"filename": 	"vice.toolkit.J21_sf_law.Sigma_g1.rst",
		"header": 		"vice.toolkit.J21_sf_law.Sigma_g1",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.Sigma_g2: {
		"filename": 	"vice.toolkit.J21_sf_law.Sigma_g2.rst",
		"header": 		"vice.toolkit.J21_sf_law.Sigma_g2",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.index1: {
		"filename": 	"vice.toolkit.J21_sf_law.index1.rst",
		"header": 		"vice.toolkit.J21_sf_law.index1",
		"subs": 		[]
	},
	vice.toolkit.J21_sf_law.index2: {
		"filename": 	"vice.toolkit.J21_sf_law.index2.rst",
		"header": 		"vice.toolkit.J21_sf_law.index2",
		"subs": 		[]
	}

}

