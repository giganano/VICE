"""
This file implements the doctree object, which is used in generating the
restructuredtext files from the docstrings in VICE.
"""

from config import _CONFIG_
import textwrap
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	raise RuntimeError("Requires python 2.7 or >= 3.5.")


class doctree:

	r"""
	A tree object whose nodes are modules within a python object, and whose
	branches are the contents of those modules. Requires the _CONFIG_
	dictionary in config.py.

	Parameters
	----------
	obj : <object>
		The object to create the doctree for

	Attributes
	----------
	filename : ``str``
		The name of the output file to put the documentation in.
	header : ``str``
		The string to put at the top of the documentation file.
	subs : ``list``
		A list of the objects that are a part of ``obj``.

	Functions
	---------
	save : Save the documentation for ``obj`` and all ``subs`` in rst files.
	"""

	def __init__(self, obj):
		self.obj = obj
		self.filename = _CONFIG_[self._obj]["filename"]
		self.header = _CONFIG_[self._obj]["header"]
		self.subs = _CONFIG_[self._obj]["subs"]

	def __repr__(self):
		rep = "%s\n" % (self.header)
		for i in range(len(self.header)):
			rep += "="
		rep += "\n"
		rep += textwrap.dedent(self._obj.__doc__)
		if len(self.subs):
			rep += "\n\n"
			rep += "\n\n"
			rep += ".. toctree::\n"
			rep += "\t:titlesonly:\n"
			rep += "\t:maxdepth: 5\n\n"
			for i in self.subs:
				rep += "\t%s\n" % (i.filename[:-4]) # remove .rst extension
		return rep

	def __str__(self):
		return self.__repr__()

	@property
	def obj(self):
		"""
		Type : ``object``

		The object to generate the restructured text file for given its
		docstring.
		"""
		return self._obj

	@obj.setter
	def obj(self, value):
		if hasattr(value, "__doc__"):
			self._obj = value
		else:
			raise ValueError("Must have attribute '__doc__'.")

	@property
	def filename(self):
		"""
		Type : ``str`` or ``None``

		The name of the file to put the restructuredtext documentation into.
		If ``None``, self.obj.__name__ will be used.
		"""
		if self._filename is None:
			return "%s.rst" % (self._obj.__name__)
		else:
			if self._filename.endswith(".rst"):
				return self._filename
			else:
				return "%s.rst" % (self._filename)

	@filename.setter
	def filename(self, value):
		if isinstance(value, strcomp) or value is None:
			self._filename = value
		else:
			raise TypeError("Filename must be of type str or None. Got: %s" % (
				type(value)))

	@property
	def header(self):
		"""
		Type : ``str`` or ``None``

		The string to use as the header in the restructured text document.
		If ``None``, self.obj.__name__ will be used.
		"""
		if self._header is None:
			return self._obj.__name__
		else:
			return self._header

	@header.setter
	def header(self, value):
		if isinstance(value, strcomp) or value is None:
			self._header = value
		else:
			raise TypeError("Header must be of type str or None. Got: %s" % (
				type(value)))

	@property
	def subs(self):
		"""
		Type : ``tuple``

		The doc objects whose bodies should listed under this one in toctrees
		and the like. These are the "branches" of the tree.
		"""
		return self._subs

	@subs.setter
	def subs(self, value):
		if isinstance(value, list):
			self._subs = len(value) * [None]
			for i in range(len(self._subs)):
				if isinstance(value[i], doctree):
					self._subs[i] = value[i]
				elif value[i] in _CONFIG_.keys():
					self._subs[i] = doctree(value[i])
				else:
					raise ValueError("Invalid sub: %s" % (str(value[i])))
		else:
			raise TypeError("Subs must be of type list. Got: %s" % (
				value))

	def save(self):
		"""
		Produce the output file.

		**Signature**: doctree.save()
		"""
		with open(self.filename, 'w') as f:
			f.write(self.__str__())
			f.close()

		for i in self.subs:
			i.save()

