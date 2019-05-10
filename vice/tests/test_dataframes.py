
from __future__ import print_function 
from vice._globals import _RECOGNIZED_ELEMENTS_ 
from vice import atomic_number 
from vice import sources 
from vice import solar_z 
from vice import singlezone 
from vice import dataframe 
from vice.yields.ccsne import settings as cc_settings
from vice.yields.sneia import settings as ia_settings 
import warnings 
import numbers 
import sys 

if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str 
else: 
	raise SystemError("Unsupported version of python: %d" % (
		sys.version_info[0]))

def test_frame(frame, name, filestream, assertions_function): 
	success = True 
	message = "%s :: " % (name) 
	for i in _RECOGNIZED_ELEMENTS_: 
		try: 
			foo = frame[i] 
			assertions_function(foo) 
		except: 
			success = False 
	if success: 
		message += "Success" 
	else: 
		message += "Failed" 
	print(message) 
	filestream.write("%s\n" % (message)) 

def atomic_number_assertions(x): 
	assert isinstance(x, numbers.Number) 
	assert x % 1 == 0 

def sources_assertions(x): 
	assert isinstance(x, list) 
	assert all(list(map(lambda x: isinstance(x, strcomp), x))) 

def solar_z_assertions(x): 
	assert isinstance(x, numbers.Number) 
	assert x < 0.02  

def cc_settings_assertions(x): 
	if isinstance(x, numbers.Number): 
		pass_ = True 
	elif callable(x): 
		if not singlezone()._singlezone__args(x): 
			pass_ = True 
		else:
			pass_ = False 
	else: 
		pass_ = False 
	assert pass_ 

def ia_settings_assertions(x): 
	assert isinstance(x, numbers.Number) 

def test_dummy(x): 
	row = {
		"zero":		0, 
		"one":		1, 
		"two": 		2, 
		"three": 	3, 
		"four": 	4, 
		"five": 	5, 
		"six": 		6, 
		"seven": 	7, 
		"eight": 	8, 
		"nine": 	9
	}
	assert isinstance(x, dataframe) 
	assert isinstance(x.todict(), dict) 
	for i in x.keys(): 
		assert isinstance(x[i], list) 
		assert all(list(map(lambda x: isinstance(x, numbers.Number), x[i]))) 
	for i in range(10): 
		assert x[i] == dataframe(row) 

def main(): 
	"""
	Runs the tests on the VICE dataframe. 
	"""
	warnings.filterwarnings("ignore")
	out = open("test_dataframes.out", 'w') 

	print("=================================================================")
	print("TESTING: vice.atomic_number")
	test_frame(atomic_number, "vice.atomic_number", out, 
		atomic_number_assertions) 

	print("=================================================================")
	print("TESTING: vice.sources") 
	test_frame(sources, "vice.sources", out, sources_assertions) 

	print("=================================================================")
	print("TESTING: vice.solar_z") 
	test_frame(solar_z, "vice.solar_z", out, solar_z_assertions) 

	print("=================================================================")
	print("TESTING: vice.yields.ccsne.settings") 
	test_frame(cc_settings, "vice.yields.ccsne.settings", out, 
		cc_settings_assertions) 

	print("=================================================================")
	print("TESTING: vice.yields.sneia.settings") 
	test_frame(ia_settings, "vice.yields.sneia.settings", out, 
		ia_settings_assertions) 

	print("=================================================================")
	print("TESTING: vice.dataframe") 
	message = "vice.dataframe :: "
	success = True 
	try: 
		test_dummy(dataframe({
			"zero":		10 * [0], 
			"one":		10 * [1], 
			"two": 		10 * [2], 
			"three": 	10 * [3], 
			"four": 	10 * [4], 
			"five": 	10 * [5], 
			"six": 		10 * [6], 
			"seven": 	10 * [7], 
			"eight": 	10 * [8], 
			"nine": 	10 * [9]
		})) 
	except: 
		success = False 
	if success: 
		message += "Success" 
	else: 
		message += "Failed" 
	print(message) 
	out.write("%s\n" % (message)) 
	out.close() 

if __name__ == "__main__": 
	main() 
	




