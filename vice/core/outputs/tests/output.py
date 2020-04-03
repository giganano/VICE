
from __future__ import absolute_import 
__all__ = ["test"] 
from ....testing import moduletest 
from ....testing import unittest 
from ...singlezone import singlezone 
from ..output import output 
import os 

_OUTTIMES_ = [0.01 * i for i in range(1001)] 


@moduletest 
def test(): 
	r""" 
	vice.output moduletest 
	""" 
	return ["vice.output", 
		[ 
			test_zip(), 
			test_unzip() 
		] 
	] 


@unittest 
def test_zip(): 
	r""" 
	vice.output.zip unittest 
	""" 
	def test(): 
		if os.path.exists("test.vice"): os.system("rm -rf test.vice") 
		try: 
			singlezone.singlezone(name = "test").run(_OUTTIMES_)  
			output.zip("test") 
		except: 
			return False 
		return os.path.exists("test.vice.zip") 
	return ["vice.output.zip", test] 


@unittest 
def test_unzip(): 
	r""" 
	vice.output.unzip unittest 
	""" 
	def test(): 
		if os.path.exists("test.vice.zip"): os.system("rm -rf test.vice") 
		try: 
			singlezone.singlezone(name = "test").run(_OUTTIMES_) 
			output.zip("test") 
			os.system("rm -rf test.vice") 
			output.unzip("test") 
		except: 
			return False 
		return os.path.exists("test.vice") 
	return ["vice.output.unzip", test] 

