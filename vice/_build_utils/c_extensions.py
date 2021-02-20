r""" 
This file stores a mapping between the names of Cython extensions to the 
required C source files to build the extension. 
""" 

C_EXTENSIONS = {
	"vice.core.dataframe._agb_yield_settings": [], 
	"vice.core.dataframe._base": [], 
	"vice.core.dataframe._ccsn_yield_table": [], 
	"vice.core.dataframe._elemental_settings": [], 
	"vice.core.dataframe._entrainment": [], 
	"vice.core.dataframe._evolutionary_settings": [], 
	"vice.core.dataframe._fromfile": [ 
		"./vice/src/dataframe/fromfile.c", 
		"./vice/src/dataframe/utils.c", 
		"./vice/src/io/utils.c"], 
	"vice.core.dataframe._history": [
		"./vice/src/dataframe", 
		"./vice/src/io/utils.c"], 
	"vice.core.dataframe._noncustomizable": [], 
	"vice.core.dataframe._saved_yields": [], 
	"vice.core.dataframe._tracers": [
		"./vice/src/dataframe", 
		"./vice/src/io/utils.c"], 
	"vice.core.dataframe._yield_settings": [], 
	"vice.core.multizone._migration": [
		"./vice/src/singlezone/singlezone.c", 
		"./vice/src/multizone/migration.c"], 
	"vice.core.multizone._multizone": [
		"./vice/src/multizone", 
		"./vice/src/io", 
		"./vice/src/toolkit/hydrodiskstars.c"], 
	"vice.core.multizone.tests._multizone": [], 
	"vice.core.multizone._zone_array": [], 
	"vice.core.objects._imf": ["./vice/src/objects/imf.c"], 
	"vice.core.objects.tests._agb": [
		"./vice/src/objects/agb.c", 
		"./vice/src/objects/tests/agb.c"], 
	"vice.core.objects.tests._callback_1arg": [
		"./vice/src/objects/callback_1arg.c", 
		"./vice/src/objects/tests/callback_1arg.c"], 
	"vice.core.objects.tests._callback_2arg": [
		"./vice/src/objects/callback_2arg.c", 
		"./vice/src/objects/tests/callback_2arg.c"], 
	"vice.core.objects.tests._ccsne": [
		"./vice/src/objects/ccsne.c", 
		"./vice/src/objects/tests/ccsne.c"], 
	"vice.core.objects.tests._channel": [
		"./vice/src/objects/channel.c", 
		"./vice/src/objects/tests/channel.c"], 
	"vice.core.objects.tests._dataset": [
		"./vice/src/objects/dataset.c", 
		"./vice/src/objects/tests/dataset.c"], 
	"vice.core.objects.tests._element": [
		"./vice/src/objects/element.c", 
		"./vice/src/objects/tests/element.c", 
		"./vice/src/objects/tests/sneia.c"], 
	"vice.core.objects.tests._fromfile": [
		"./vice/src/objects/fromfile.c", 
		"./vice/src/objects/tests/fromfile.c"], 
	"vice.core.objects.tests._hydrodiskstars": [
		"./vice/src/objects/hydrodiskstars.c", 
		"./vice/src/objects/tests/hydrodiskstars.c"], 
	"vice.core.objects.tests._imf": [
		"./vice/src/objects/imf.c", 
		"./vice/src/objects/tests/imf.c"], 
	"vice.core.objects.tests._integral": [
		"./vice/src/objects/integral.c", 
		"./vice/src/objects/tests/integral.c"], 
	"vice.core.objects.tests._interp_scheme_1d": [
		"./vice/src/objects/interp_scheme_1d.c", 
		"./vice/src/objects/tests/interp_scheme_1d.c"], 
	"vice.core.objects.tests._ism": [
		"./vice/src/objects/ism.c", 
		"./vice/src/objects/tests/ism.c"], 
	"vice.core.objects.tests._mdf": [
		"./vice/src/objects/mdf.c", 
		"./vice/src/objects/tests/mdf.c"], 
	"vice.core.objects.tests._migration": [
		"./vice/src/objects/migration.c", 
		"./vice/src/objects/tests/migration.c"], 
	"vice.core.objects.tests._multizone": [
		"./vice/src/objects/multizone.c", 
		"./vice/src/objects/tests/multizone.c"], 
	"vice.core.objects.tests._singlezone": [
		"./vice/src/objects/singlezone.c", 
		"./vice/src/objects/tests/singlezone.c", 
		"./vice/src/objects/tests/ssp.c"], 
	"vice.core.objects.tests._sneia": [
		"./vice/src/objects/sneia.c", 
		"./vice/src/objects/tests/sneia.c"], 
	"vice.core.objects.tests._ssp": [
		"./vice/src/objects/ssp.c", 
		"./vice/src/objects/tests/ssp.c"], 
	"vice.core.objects.tests._tracer": [
		"./vice/src/objects/tracer.c", 
		"./vice/src/objects/tests/tracer.c"], 
	"vice.core.outputs._history": [], 
	"vice.core.outputs._mdf": [], 
	"vice.core.outputs._multioutput": [], 
	"vice.core.outputs._output": [], 
	"vice.core.outputs._tracers": [], 
	"vice.core.singlezone._singlezone": [
		"./vice/src", 
		"./vice/src/io/agb.c", 
		"./vice/src/io/ccsne.c", 
		"./vice/src/io/singlezone.c", 
		"./vice/src/io/sneia.c", 
		"./vice/src/io/utils.c", 
		"./vice/src/objects", 
		"./vice/src/singlezone", 
		"./vice/src/ssp", 
		"./vice/src/yields/integral.c"], 
	"vice.core.singlezone.tests._singlezone": [], 
	"vice.core.ssp._crf": [], 
	"vice.core.ssp._imf": ["./vice/src/imf.c"], 
	"vice.core.ssp._msmf": [], 
	"vice.core.ssp._ssp": ["./vice/src/ssp"], 
	"vice.core.ssp.tests._crf": ["./vice/src/ssp/tests/crf.c"], 
	"vice.core.ssp.tests._mlr": ["./vice/src/ssp/tests/mlr.c"], 
	"vice.core.ssp.tests._msmf": ["./vice/src/ssp/tests/msmf.c"], 
	"vice.core.ssp.tests._remnants": ["./vice/src/ssp/tests/remnants.c"], 
	"vice.core._cutils": [
		"./vice/src/utils.c", 
		"./vice/src/objects/callback_1arg.c", 
		"./vice/src/objects/callback_2arg.c"], 
	"vice.core.tests._cutils": ["./vice/src/objects/imf.c"], 
	"vice.src.io.tests._agb": [
		"./vice/src/io/agb.c", 
		"./vice/src/io/tests/agb.c"], 
	"vice.src.io.tests._ccsne": [
		"./vice/src/io/ccsne.c", 
		"./vice/src/io/tests/ccsne.c"], 
	"vice.src.io.tests._sneia": [
		"./vice/src/io/sneia.c", 
		"./vice/src/io/tests/sneia.c"], 
	"vice.src.io.tests._utils": [
		"./vice/src/io/utils.c", 
		"./vice/src/io/tests/utils.c"], 
	"vice.src.multizone.tests.cases._generic": [
		"./vice/src/multizone", 
		"./vice/src/io/multizone.c", 
		"./vice/src/multizone/tests/tracer.c"], 
	"vice.src.multizone.tests.cases._no_migration": [
		"./vice/src/multizone/tests"], 
	"vice.src.multizone.tests.cases._separation": [
		"./vice/src/multizone/tests"], 
	"vice.src.singlezone.tests._singlezone": [
		"./vice/src/singlezone/singlezone.c"], 
	"vice.src.singlezone.tests.cases._generic": [
		"./vice/src/singlezone", 
		"./vice/src/io/singlezone.c"], 
	"vice.src.singlezone.tests.cases._max_age_ssp": [
		"./vice/src/singlezone/tests"], 
	"vice.src.singlezone.tests.cases._quiescence": [
		"./vice/src/singlezone/tests"], 
	"vice.src.singlezone.tests.cases._zero_age_ssp": [
		"./vice/src/singlezone/tests"], 
	"vice.src.tests._callback": [
		"./vice/src/tests/callback.c", 
		"./vice/src/objects/tests/callback_1arg.c", 
		"./vice/src/objects/tests/callback_2arg.c"], 
	"vice.src.tests._imf": ["./vice/src/tests/imf.c"], 
	"vice.src.tests._stats": ["./vice/src/tests/stats.c"], 
	"vice.src.tests._utils": ["./vice/src/tests/utils.c"], 
	"vice.toolkit.hydrodisk._hydrodiskstars": [
		"./vice/src/toolkit/hydrodiskstars.c", 
		"./vice/src/utils.c"], 
	"vice.toolkit.interpolation._interp_scheme_1d": [
		"./vice/src/toolkit/interp_scheme_1d.c"], 
	"vice.yields.agb._grid_reader": [], 
	"vice.yields.ccsne._yield_integrator": ["./vice/src/yields/ccsne.c"], 
	"vice.yields.sneia._yield_lookup": ["./vice/src/io/sneia.c"], 
	"vice.yields.tests._integral": ["./vice/src/yields/tests/integral.c"] 
}

