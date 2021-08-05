r""" 
This file implements a mapping between the Cython extensions and the necessary 
C code needed to properly compile. This is used to speed up the compile time 
of VICE by excluding unnecessary code for individual extensions. 
""" 

_CFILES_ = {
	"vice.core._cutils": [
		"./vice/src/objects/callback_1arg.c", 
		"./vice/src/objects/callback_2arg.c", 
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
	# "vice.core.multizone._migration": [
	# 	"./vice/src/multizone/migration.c", 
	# 	"./vice/src/objects/integral.c", 
	# 	"./vice/src/singlezone", 
	# 	"./vice/src/ssp", 
	# 	"./vice/src/yields/integral.c", 
	# 	"./vice/src/io/singlezone.c", 
	# 	"./vice/src/callback.c", 
	# 	"./vice/src/imf.c", 
	# 	"./vice/src/utils.c" 
	# ], 
	"vice.core.multizone._zone_array": [], 
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
	] 
}


