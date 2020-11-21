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

	def __init__(self, initial, final, birth, mode = "diffusion"): 
		self.initial = initial 
		self.final = final 
		self.birth = birth 
		self.mode = mode 

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
			if time < self.__migration_time: 
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
				if self._mode == "sudden": 
					self.__migration_time = self.birth + (
						self.final_time - self.birth) * random.random() 
				else: pass 
			else: 
				raise ValueError("Unrecognized mode: %s" % (value)) 
		else: 
			raise TypeError("Must be a string. Got: %s" % (type(value))) 


def plot_scheme(ax, initial, final, birth, mode = "diffusion", label = False): 
	scheme_ = scheme(initial, final, birth, mode = mode) 
	times = [birth + 0.01 * i for i in range(
		int((scheme.final_time - birth) / 0.01) + 2)] 
	radii = [scheme_(i) for i in times] 
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
	random.seed(a = seed) 
	for i in range(3): 
		initial = 15.5 * random.random() 
		final = 20.0 * random.random() 
		birth = 12. * random.random() 
		for j in scheme.recognized_modes: 
			plot_scheme(ax, initial, final, birth, mode = j, label = not i) 
	leg = ax.legend(loc = mpl_loc("upper left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.02, 0.98), fontsize = 20) 
	plt.tight_layout() 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.close() 

