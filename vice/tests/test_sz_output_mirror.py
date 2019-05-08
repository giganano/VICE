
from __future__ import print_function, division
import math 
import vice 
import warnings 
import sys 
sys.stdout.flush() 

try: 
	import numpy as np 
	_OUTTIMES_ = np.linspace(0, 10, 201) 
except (ImportError, ModuleNotFoundError): 
	_OUTTIMES_ = 201 * [0.] 
	for i in range(201): 
		_OUTTIMES_[i] = 0.05 * i 

def main(): 
	"""
	Runs the tests on the singlezone object, the output object, and the 
	mirror function. 
	"""
	warnings.filterwarnings("ignore") 
	print("=================================================================")
	print("TESTING: vice.singlezone") 
	print("         vice.output") 
	print("         vice.mirror") 
	out = open("test_sz_output_mirror.out", 'w') 
	_MODES_ = ["ifr", "sfr", "gas"] 
	_IMF_ = ["kroupa", "salpeter"] 
	_ETA_ = [2.5, lambda t: 2.5 * math.exp( -t / 4.0 )] 
	_ZIN_ = [0, 1.0e-8, lambda t: 1.0e-8 * (t / 10.0), {
		"o":		lambda t: 0.0057 * (t / 10.0),  
		"fe": 		0.0013
	}]
	_RECYCLING_ = ["continuous", 0.4] 
	_RIA_ = ["plaw", "exp", lambda t: t**-1.5] 
	_TAU_STAR_ = [2.0, lambda t: 2.0 + t / 10.0] 
	_SCHMIDT_ = [False, True] 
	_AGB_MODEL_ = ["cristallo11", "karakas10"] 

	a = 0 
	b = 2304 
	keys = ["success", "failure"] 
	singlezone_tracker = dict(zip(keys, [0, 0])) 
	mirror_tracker = dict(zip(keys, [0, 0])) 
	output_tracker = dict(zip(keys, [0, 0])) 
	history_tracker = dict(zip(keys, [0, 0])) 
	mdf_tracker = dict(zip(keys, [0, 0])) 
	for i in _MODES_: 
		for j in _IMF_: 
			for k in _ETA_: 
				for l in _ZIN_: 
					for m in _RECYCLING_: 
						for n in _RIA_: 
							for o in _TAU_STAR_: 
								for p in _SCHMIDT_: 
									for q in _AGB_MODEL_: 
										metadata = dict(
											elements = ["fe", "o", "c"], 
											mode = i, 
											IMF = j, 
											eta = k, 
											Zin = l, 
											recycling = m, 
											RIa = n, 
											tau_star = o, 
											schmidt = p, 
											agb_model = q, 
											dt = 0.05
										) 
										try: 
											vice.singlezone(**metadata).run(
												_OUTTIMES_, 
												overwrite = True) 
											singlezone_tracker["success"] += 1
										except: 
											singlezone_tracker["failure"] += 1 
										try: 
											foo = vice.history(
												"onezonemodel") 
											assert isinstance(foo, 
												vice.dataframe) 
											history_tracker["success"] += 1
										except: 
											history_tracker["failure"] += 1 
										try: 
											foo = vice.mdf(
												"onezonemodel") 
											assert isinstance(foo, 
												vice.dataframe) 
											mdf_tracker["success"] += 1
										except: 
											mdf_tracker["failure"] += 1 
										success = True 
										try: 
											foo = vice.output(
												"onezonemodel") 
											assert isinstance(foo, 
												vice.output) 
											assert isinstance(foo.history, 
												vice.dataframe) 
											assert isinstance(foo.mdf, 
												vice.dataframe) 
											assert isinstance(
												foo.ccsne_yields, 
												vice.dataframe) 
											assert isinstance(
												foo.sneia_yields, 
												vice.dataframe) 
											assert isinstance(
												foo.elements, 
												tuple) 
											output_tracker["success"] += 1
											try: 
												mir = vice.mirror(foo) 
												assert isinstance(mir, 
													vice.singlezone) 	
												mirror_tracker["success"] += 1
											except: 
												mirror_tracker["failure"] += 1
										except: 
											output_tracker["failure"] += 1

										a += 1
										sys.stdout.write("Progress: %.1f%%\r" % (
											a / b * 100)) 
										sys.stdout.flush() 
										
	#######
	message = """\
vice.singlezone :: %d successes :: %d failures 
vice.history :: %d successes :: %d failures 
vice.mdf :: %d successes :: %d failures 
vice.output :: %d successes :: %d failures 
vice.mirror :: %d successes :: %d failures \
""" % (
		singlezone_tracker["success"], singlezone_tracker["failure"], 
		history_tracker["success"], history_tracker["failure"], 
		mdf_tracker["success"], mdf_tracker["failure"], 
		output_tracker["success"], output_tracker["failure"], 
		mirror_tracker["success"], mirror_tracker["failure"]
		)
	print(message) 
	out.write(message) 
	out.close() 

if __name__ == "__main__": 
	main() 





