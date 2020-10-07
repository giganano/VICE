
from .disks import diskmodel 
from .config import config 

class suite: 

	def __init__(self, **kwargs): 
		self._config = config(**kwargs) 
		self._simulations = [] 

	@property 
	def config(self): 
		r""" 
		Type : config 

		The config object for this suite of simulations. 
		""" 
		return self._config 

	@property 
	def simulations(self): 
		r""" 
		Type : list [elements are of type ``diskmodel``] 

		The simulations that are a part of this suite. 
		""" 
		return self._simulations 

	def add_simulation(self, model): 
		r""" 
		Add a simulation to the suite. 

		Parameters 
		----------
		model : ``diskmodel`` 
			The diskmodel object to add to the suite. 
		""" 
		if isinstance(model, diskmodel): 
			self._simulations.append(model) 
		else: 
			raise TypeError("Must be of type diskmodel. Got: %s" % (
				type(model))) 

	def run(self, **kwargs): 
		r""" 
		Run the simulations in the suite. 

		Parameters 
		----------
		**kwargs : boolean 
			Keywords ``overwrite`` and ``capture`` to be passed down to the 
			``run`` function of the ``vice.multizone`` base class. 
		""" 
		for i in self.simulations: i.run(self.config.output_times, **kwargs) 
