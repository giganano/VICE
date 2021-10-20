r"""
This file implements a mapping between the Cython extensions and the necessary
C code needed to properly compile. This is used to speed up the compile time
of VICE by excluding unnecessary code for individual extensions.

Notes
-----
In practice, these lists of C source code files are largely determined by
recompiling individual extensions with pieces of the C library and ensuring
that "import vice" does not produce an ImportError.
"""

_CFILES_ = {
	"vice.core._cutils": [
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/io/progressbar.c",
		"./vice/src/utils.c"
	],
	"vice.core._mlr": [
		"./vice/src/ssp/mlr",
		"./vice/src/ssp/mlr.c",
		"./vice/src/objects/interp_scheme_1d.c",
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/toolkit/interp_scheme_1d.c",
		"./vice/src/toolkit/interp_scheme_2d.c",
		"./vice/src/io/utils.c",
		"./vice/src/utils.c"
	],
	"vice.core.dataframe._agb_yield_settings": [],
	"vice.core.dataframe._base": [],
	"vice.core.dataframe._ccsn_yield_table": [],
	"vice.core.dataframe._elemental_settings": [],
	"vice.core.dataframe._entrainment": [],
	"vice.core.dataframe._evolutionary_settings": [],
	"vice.core.dataframe._fromfile": [
		"./vice/src/dataframe/calclogz.c",
		"./vice/src/dataframe/calclookback.c",
		"./vice/src/dataframe/calcz.c",
		"./vice/src/dataframe/fromfile.c",
		"./vice/src/dataframe/utils.c",
		"./vice/src/objects/fromfile.c",
		"./vice/src/io/utils.c",
		"./vice/src/utils.c"
	],
	"vice.core.dataframe._history": [
		"./vice/src/dataframe/calclogz.c",
		"./vice/src/dataframe/calclookback.c",
		"./vice/src/dataframe/calcz.c",
		"./vice/src/dataframe/fromfile.c",
		"./vice/src/dataframe/history.c",
		"./vice/src/dataframe/utils.c",
		"./vice/src/objects/fromfile.c",
		"./vice/src/io/utils.c",
		"./vice/src/utils.c"
	],
	"vice.core.dataframe._noncustomizable": [],
	"vice.core.dataframe._saved_yields": [],
	"vice.core.dataframe._tracers": [
		"./vice/src/dataframe/calclogz.c",
		"./vice/src/dataframe/calclookback.c",
		"./vice/src/dataframe/calcz.c",
		"./vice/src/dataframe/fromfile.c",
		"./vice/src/dataframe/tracers.c",
		"./vice/src/dataframe/utils.c",
		"./vice/src/objects/fromfile.c",
		"./vice/src/io/utils.c",
		"./vice/src/utils.c"
	],
	"vice.core.dataframe._yield_settings": [],
	"vice.core.multizone._migration": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.multizone._multizone": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.multizone._zone_array": [],
	"vice.core.multizone.tests._multizone": [],
	"vice.core.objects._imf": [
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/imf.c"
	],
	"vice.core.objects.tests._agb": [
		"./vice/src/objects/agb.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/objects/tests/agb.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/callback_2arg.c",
		"./vice/src/objects/tests/interp_scheme_2d.c"
	],
	"vice.core.objects.tests._callback_1arg": [
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/tests/callback_1arg.c"
	],
	"vice.core.objects.tests._callback_2arg": [
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/callback_2arg.c"
	],
	"vice.core.objects.tests._ccsne": [
		"./vice/src/objects/ccsne.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/tests/ccsne.c",
		"./vice/src/objects/tests/callback_1arg.c"
	],
	"vice.core.objects.tests._channel": [
		"./vice/src/objects/channel.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/tests/channel.c",
		"./vice/src/objects/tests/callback_1arg.c"
	],
	"vice.core.objects.tests._element": [
		"./vice/src/objects/element.c",
		"./vice/src/objects/agb.c",
		"./vice/src/objects/ccsne.c",
		"./vice/src/objects/sneia.c",
		"./vice/src/objects/channel.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/objects/tests/element.c",
		"./vice/src/objects/tests/agb.c",
		"./vice/src/objects/tests/ccsne.c",
		"./vice/src/objects/tests/sneia.c",
		"./vice/src/objects/tests/channel.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/callback_2arg.c",
		"./vice/src/objects/tests/interp_scheme_2d.c"
	],
	"vice.core.objects.tests._fromfile": [
		"./vice/src/objects/fromfile.c",
		"./vice/src/objects/tests/fromfile.c"
	],
	"vice.core.objects.tests._hydrodiskstars": [
		"./vice/src/objects/hydrodiskstars.c",
		"./vice/src/objects/tests/hydrodiskstars.c"
	],
	"vice.core.objects.tests._imf": [
		"./vice/src/objects/imf.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/tests/imf.c",
		"./vice/src/objects/tests/callback_1arg.c"
	],
	"vice.core.objects.tests._integral": [
		"./vice/src/objects/integral.c",
		"./vice/src/objects/tests/integral.c"
	],
	"vice.core.objects.tests._interp_scheme_1d": [
		"./vice/src/objects/interp_scheme_1d.c",
		"./vice/src/objects/tests/interp_scheme_1d.c"
	],
	"vice.core.objects.tests._interp_scheme_2d": [
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/objects/tests/interp_scheme_2d.c"
	],
	"vice.core.objects.tests._ism": [
		"./vice/src/objects/ism.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/tests/ism.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/callback_2arg.c"
	],
	"vice.core.objects.tests._mdf": [
		"./vice/src/objects/mdf.c",
		"./vice/src/objects/tests/mdf.c"
	],
	"vice.core.objects.tests._migration": [
		"./vice/src/objects/migration.c",
		"./vice/src/objects/tracer.c",
		"./vice/src/objects/tests/migration.c"
	],
	"vice.core.objects.tests._multizone": [
		"./vice/src/objects/multizone.c",
		"./vice/src/objects/migration.c",
		"./vice/src/objects/tracer.c",
		"./vice/src/objects/tests/multizone.c"
	],
	"vice.core.objects.tests._singlezone": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/objects/tests",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.objects.tests._sneia": [
		"./vice/src/objects/sneia.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/tests/sneia.c",
		"./vice/src/objects/tests/callback_1arg.c"
	],
	"vice.core.objects.tests._ssp": [
		"./vice/src/objects/ssp.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/imf.c",
		"./vice/src/objects/tests/ssp.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/imf.c"
	],
	"vice.core.objects.tests._tracer": [
		"./vice/src/objects/tracer.c",
		"./vice/src/objects/tests/tracer.c"
	],
	"vice.core.outputs._history": [],
	"vice.core.outputs._mdf": [],
	"vice.core.outputs._multioutput": [],
	"vice.core.outputs._output": [],
	"vice.core.outputs._tracers": [],
	"vice.core.singlezone._singlezone": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.singlezone.tests._singlezone": [],
	"vice.core.ssp._crf": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.ssp._imf": [
		"./vice/src/imf.c",
		"./vice/src/callback.c",
		"./vice/src/utils.c"
	],
	"vice.core.ssp._msmf": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.ssp._ssp": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.ssp.tests._crf": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/objects/tests",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/ssp/tests",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.ssp.tests._msmf": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/objects/tests",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/ssp/tests",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.ssp.tests._remnants": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/objects/tests",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/ssp/tests",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.core.tests._cutils": [
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/imf.c"
	],
	"vice.src.io.tests._agb": [
		"./vice/src/io/tests/agb.c",
		"./vice/src/io/agb.c",
		"./vice/src/objects/agb.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/ccsne.c",
		"./vice/src/objects/channel.c",
		"./vice/src/objects/element.c",
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/objects/sneia.c",
		"./vice/src/io/utils.c"
	],
	"vice.src.io.tests._ccsne": [
		"./vice/src/io/tests/ccsne.c",
		"./vice/src/io/ccsne.c",
		"./vice/src/io/utils.c"
	],
	"vice.src.io.tests._sneia": [
		"./vice/src/io/tests/sneia.c",
		"./vice/src/io/sneia.c",
		"./vice/src/io/utils.c"
	],
	"vice.src.io.tests._utils": [
		"./vice/src/io/tests/utils.c",
		"./vice/src/io/utils.c"
	],
	"vice.src.multizone.tests.cases._generic": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/multizone/tests",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.multizone.tests.cases._no_migration": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/multizone/tests",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.multizone.tests.cases._separation": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/multizone/tests",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.singlezone.tests._singlezone": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/singlezone/tests",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.singlezone.tests.cases._generic": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/singlezone/tests",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.singlezone.tests.cases._max_age_ssp": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/singlezone/tests",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.singlezone.tests.cases._quiescence": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/singlezone/tests",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.singlezone.tests.cases._zero_age_ssp": [
		"./vice/src/io",
		"./vice/src/multizone",
		"./vice/src/objects",
		"./vice/src/singlezone",
		"./vice/src/singlezone/tests",
		"./vice/src/ssp",
		"./vice/src/ssp/mlr",
		"./vice/src/toolkit",
		"./vice/src/yields",
		"./vice/src"
	],
	"vice.src.tests._callback": [
		"./vice/src/tests/callback.c",
		"./vice/src/callback.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/tests/callback_1arg.c",
		"./vice/src/objects/tests/callback_2arg.c"
	],
	"vice.src.tests._imf": [
		"./vice/src/tests/imf.c",
		"./vice/src/imf.c",
		"./vice/src/callback.c",
		"./vice/src/utils.c",
		"./vice/src/objects/imf.c",
		"./vice/src/objects/callback_1arg.c"
	],
	"vice.src.tests._stats": [
		"./vice/src/tests/stats.c",
		"./vice/src/stats.c",
		"./vice/src/utils.c"
	],
	"vice.src.tests._utils": [
		"./vice/src/tests/utils.c",
		"./vice/src/utils.c"
	],
	"vice.toolkit.hydrodisk._hydrodiskstars": [
		"./vice/src/objects/hydrodiskstars.c",
		"./vice/src/toolkit/hydrodiskstars.c",
		"./vice/src/io/utils.c",
		"./vice/src/utils.c"
	],
	"vice.toolkit.interpolation._interp_scheme_1d": [
		"./vice/src/objects/interp_scheme_1d.c",
		"./vice/src/toolkit/interp_scheme_1d.c",
		"./vice/src/utils.c"
	],
	"vice.toolkit.interpolation._interp_scheme_2d": [
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/toolkit/interp_scheme_2d.c",
		"./vice/src/utils.c"
	],
	"vice.yields.agb._grid_reader": [
		"./vice/src/objects/agb.c",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/callback_2arg.c",
		"./vice/src/objects/ccsne.c",
		"./vice/src/objects/channel.c",
		"./vice/src/objects/element.c",
		"./vice/src/objects/interp_scheme_2d.c",
		"./vice/src/objects/sneia.c",
		"./vice/src/io/agb.c",
		"./vice/src/io/utils.c"
	],
	"vice.yields.ccsne._yield_integrator": [
		"./vice/src/yields",
		"./vice/src/objects/callback_1arg.c",
		"./vice/src/objects/integral.c",
		"./vice/src/objects/imf.c",
		"./vice/src/io/ccsne.c",
		"./vice/src/io/utils.c",
		"./vice/src"
	],
	"vice.yields.sneia._yield_lookup": [
		"./vice/src/io/sneia.c",
		"./vice/src/io/utils.c"
	],
	"vice.yields.tests._integral": [
		"./vice/src/yields/tests/integral.c",
		"./vice/src/yields/integral.c",
		"./vice/src/objects/integral.c",
		"./vice/src/utils.c"
	]

}


