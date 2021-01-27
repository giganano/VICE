r""" 
This file implements testing of the explodability engines in the parent 
directory. 
""" 

from __future__ import absolute_import 
from ......_globals import _DIRECTORY_ 
from ......testing import unittest 
from ..W18 import W18 


@unittest 
def test(): 
	r""" 
	Performs a unit test on the ``W18`` constructor. 
	""" 
	def test(): 
		try: 
			test_ = W18() 
		except: 
			return False 
		status = isinstance(test_, W18) 

		# Base the rest of the test on whether or not the ``masses`` and 
		# ``frequencies`` attribute match the W18.dat file. 
		if status: 
			filename = "%syields/ccsne/engines/S16/W18.dat" % (_DIRECTORY_) 
			with open(filename, 'r') as f: 
				while True: 
					line = f.readline() 
					if line[0] != '#': break 
				n = 0 
				status = True 
				while line != "": 
					line = [float(i) for i in line.split()] 
					status &= test_.masses[n] == line[0] 
					status &= test_.frequencies[n] == line[1] 
					if not status: break 
					n += 1 
					line = f.readline() 
				f.close() 
		else: pass 
		return status 
	return ["vice.yields.ccsne.engines.S16.W18", test] 

