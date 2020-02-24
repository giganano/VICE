
from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 


if not __VICE_SETUP__: 

	from vice.tests import test 
	from vice._globals import _VERSION_ERROR_ 
	import sys 
	import os 
	if sys.version_info[:2] == (2, 7): 
		strcomp = basestring 
		input = raw_input 
	elif sys.version_info[:2] >= (3, 5): 
		strcomp = str 
	else: 
		_VERSION_ERROR_() 

	if "test.vice" in os.listdir(os.getcwd()): 
		answer = input("""This program will overwrite the vice output at \
%s/test.vice. Proceed? (y | n) """ % (os.getcwd())) 
		while answer.lower() not in ["yes", "y", "no", "n"]: 
			answer = input("Please enter either 'y' or 'n': ") 
		if answer.lower() in ["yes", "y"]: 
			test(run = True) 
		else: 
			pass 
	else: 
		test(run = True) 

else: 
	pass 

