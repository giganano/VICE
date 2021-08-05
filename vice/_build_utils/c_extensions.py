r""" 
This file implements a mapping between the Cython extensions and the necessary 
C code needed to properly compile. This is used to speed up the compile time 
of VICE by excluding unnecessary code for individual extensions. 
""" 

_CFILES_ = {
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
	"vice.core.dataframe._yield_settings": [] 
}


