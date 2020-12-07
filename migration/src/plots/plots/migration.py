r""" 
Produces a plot of the migration schema implemented in Johnson et al. (2021). 
""" 

from .. import env 
import matplotlib.pyplot as plt 
from .utils import named_colors, mpl_loc 
import math as m 
import numbers 
import random 


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel("Time [Gyr]") 
	ax.set_ylabel(r"$R_\text{gal}$ [kpc]") 
	ax.set_xlim([-1, 14]) 
	ax.set_ylim([-2, 22]) 
	return ax 


class scheme: 

	recognized_modes = ["diffusion", "linear", "post-process", "sudden"] 
	final_time = 12.8 # Gyr 

	def __init__(self, initial, final, birth, mode = "diffusion", 
		sudden_migration_time = 10): 
		self.initial = initial 
		self.final = final 
		self.birth = birth 
		self.mode = mode 
		self.sudden_migration_time = sudden_migration_time 

	def __call__(self, time): 
		if self.mode == "linear": 
			return (
				(self.final - self.initial) / (self.final_time - self.birth) * 
				(time - self.birth) + self.initial 
			) 
		elif self.mode == "diffusion": 
			return (
				(self.final - self.initial) * m.sqrt(
					(time - self.birth) / 
					(self.final_time - self.birth) 
				) + self.initial 
			) 
		elif self.mode == "sudden": 
			if time < self.sudden_migration_time: 
				return self.initial 
			else: 
				return self.final 
		elif self.mode == "post-process": 
			if time >= self.final_time: 
				return self.final 
			else: 
				return self.initial 
		else: 
			raise SystemError("Internal Error.") 

	@property 
	def initial(self): 
		return self._initial 

	@initial.setter 
	def initial(self, value): 
		if isinstance(value, numbers.Number): 
			if 0 <= value <= 20: 
				self._initial = float(value) 
			else: 
				raise ValueError("Out of range: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def final(self): 
		return self._final 

	@final.setter 
	def final(self, value): 
		if isinstance(value, numbers.Number): 
			if 0 <= value <= 20: 
				self._final = float(value) 
			else: 
				raise ValueError("Out of range: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def birth(self): 
		return self._birth 

	@birth.setter 
	def birth(self, value): 
		if isinstance(value, numbers.Number): 
			if 0 <= value <= self.final_time: 
				self._birth = float(value) 
			else: 
				raise ValueError("Out of range: %g" % (value)) 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 

	@property 
	def mode(self): 
		return self._mode 

	@mode.setter 
	def mode(self, value): 
		if isinstance(value, str): 
			if value.lower() in self.recognized_modes: 
				self._mode = value.lower() 
			else: 
				raise ValueError("Unrecognized mode: %s" % (value)) 
		else: 
			raise TypeError("Must be a string. Got: %s" % (type(value))) 

	@property 
	def sudden_migration_time(self): 
		return self._sudden_migration_time 

	@sudden_migration_time.setter 
	def sudden_migration_time(self, value): 
		if isinstance(value, numbers.Number): 
			if value > self.birth: 
				self._sudden_migration_time = float(value) 
			else: 
				raise ValueError("Must be larger than birth time.") 
		else: 
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value))) 


def plot_scheme(ax, initial, final, birth, label = False, **kwargs): 
	scheme_ = scheme(initial, final, birth, **kwargs) 
	times = [birth + 0.01 * i for i in range(
		int((scheme.final_time - birth) / 0.01) + 2)] 
	radii = [scheme_(i) for i in times] 
	mode = kwargs["mode"] 
	kwargs = {
		"c": 			named_colors()[{
			"diffusion": 		"crimson", 
			"linear": 			"lime", 
			"sudden": 			"blue", 
			"post-process": 	"black" 
		}[mode.lower()]], 
		"linestyle": 	{
			"diffusion": 		"-", 
			"linear": 			"-.", 
			"sudden": 			"--", 
			"post-process": 	":" 
		}[mode.lower()] 
	} 
	if label: kwargs["label"] = mode.capitalize() 
	ax.plot(times, radii, **kwargs) 


def main(stem, seed = 66): 
	ax = setup_axis() 
	initial = [1, 14, 4] # birth radii in kpc 
	final = [9, 10, 17] # final radii in kpc 
	birth = [3, 5, 7] # birth times in Gyr 
	sudden = [9.1, 6.8, 11] # times for sudden migration 
	for i in range(2): 
		for j in scheme.recognized_modes: 
			plot_scheme(ax, initial[i], final[i], birth[i], label = not i, 
				mode = j, sudden_migration_time = sudden[i]) 
	leg = ax.legend(loc = mpl_loc("upper left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.02, 0.98), fontsize = 20) 
	plt.tight_layout() 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.close() 

