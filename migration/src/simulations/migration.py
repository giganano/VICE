
from vice.toolkit import hydrodisk


class diskmigration(hydrodisk.hydrodiskstars):

	r"""
	A ``hydrodiskstars`` object which writes extra analog star particle data to
	an output file.

	Parameters
	----------
	radbins : array-like
		The bins in galactocentric radius in kpc corresponding to each annulus.
	mode : ``str`` [default : "linear"]
		A keyword denoting the time-dependence of stellar migration.
		Allowed values:

		- "diffusion"
		- "linear"
		- "sudden"
		- "post-process"

	filename : ``str`` [default : "stars.out"]
		The name of the file to write the extra star particle data to.

	Attributes
	----------
	write : ``bool`` [default : False] 	
		A boolean describing whether or not to write to an output file when
		the object is called. The ``multizone`` object, and by extension the
		``milkyway`` object, automatically switch this attribute to True at the
		correct time to record extra data.
	"""

	def __init__(self, radbins, mode = "diffusion", filename = "stars.out",
		**kwargs):
		super().__init__(radbins, mode = mode, **kwargs)
		if isinstance(filename, str):
			self._file = open(filename, 'w')
			self._file.write("# zone_origin\ttime_origin\tanalog_id\tzfinal\n")
		else:
			raise TypeError("Filename must be a string. Got: %s" % (
				type(filename)))

		# use only disk stars in these simulations
		self.decomp_filter([1, 2])

		# Multizone object automatically swaps this to True in setting up
		# its stellar population zone histories
		self.write = False

	def __call__(self, zone, tform, time):
		if tform == time:
			super().__call__(zone, tform, time) # reset analog star particle
			if self.write:
				if self.analog_index == -1:
					# finalz = 100
					finalz = 0
					analog_id = -1
				else:
					finalz = self.analog_data["zfinal"][self.analog_index]
					analog_id = self.analog_data["id"][self.analog_index]
				self._file.write("%d\t%.2f\t%d\t%.2f\n" % (zone, tform,
					analog_id, finalz))
			else: pass
			return zone
		else:
			return super().__call__(zone, tform, time)

	def close_file(self):
		r"""
		Closes the output file - should be called after the multizone model
		simulation runs.
		"""
		self._file.close()

	@property
	def write(self):
		r"""
		Type : bool

		Whether or not to write out to the extra star particle data output
		file. For internal use by the vice.multizone object only.
		"""
		return self._write

	@write.setter
	def write(self, value):
		if isinstance(value, bool):
			self._write = value
		else:
			raise TypeError("Must be a boolean. Got: %s" % (type(value)))

