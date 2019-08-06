""" 
Johnson & Weinberg (2019) Nucleosynthetic Yield Settings 
======================================================== 
Importing this module sets the yields of oxygen, iron, and strontium to that 
adopted in the Johnson & Weinberg (2019) paper on starbursts scenarios. 

Yield Settings 
============== 

	CCSNe 
	----- 
		o  :: 0.015 
		fe :: 0.0012 
		sr :: 3.5e-08 

	SNe Ia 
	------ 
		o  :: 0.0 
		fe :: 0.0017 
		sr :: 0.0 
""" 

import vice 

vice.yields.ccsne.settings["o"] = 0.015 
vice.yields.ccsne.settings["sr"] = 3.5e-8 
vice.yields.ccsne.settings["fe"] = 0.0012 
vice.yields.sneia.settings["o"] = 0.0 
vice.yields.sneia.settings["sr"] = 0.0 
vice.yields.sneia.settings["fe"] = 0.0017 

