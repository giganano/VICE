#!/usr/bin/env python
#
# This file is part of the VICE package.
# Copyright (C) 2019 James W. Johnson (giganano9@gmail.com).
# License: MIT License. See LICENSE in top-level directory
# at: https://github.com/giganano/VICE.git.
r"""
This file implements VICE's versioning.
"""

import importlib.metadata
import warnings
import re
__ISRELEASED__ = False


class VersionWarning(Warning):

	r"""
	A ``Warning`` class for drawing the user's attention to their current
	version of TrackStar (e.g., if they are using an alpha release or a
	development version).

	Although it is not recommended, this class of warnings can be silenced via

	>>> warnings.filterwarnings("ignore", category = vice.VersionWarning)

	Alternatively, to silence all warnings within VICE:

	>>> vice.warnings.filterwarnings("ignore")

	However, the above lines are moot in practice, because one must first
	import VICE, which will either raise a ``VersionWarning`` or not *before*
	this ``Warning`` class can be silenced.

	To silence all warnings globally:

	>>> warnings.filterwarnings("ignore")
	"""
	pass


class VersionError(Exception):

	r"""
	An ``Exception`` class that is raised when VICE's version information is
	invalid. If you are not a VICE developer and have seen this error class
	raised on your system, please open an issue at
	https://github.com/giganano/VICE/issues.
	"""
	pass


class version:

	r"""
	**VICE Version Information**

	The version number in string format can be accessed via

	>>> vice.__version__
	>>> str(vice.version)

	Components of the version number can be accessed as attributes. For
	example:

	>>> major = vice.version.major
	>>> minor = vice.version.minor

	The version number can also be type-cast to a tuple and iterated over
	according to

	>>> version = tuple(vice.version)
	>>> for item in version: print(item)

	The version number can also be indexed as a list, which accesses the same
	items as ``tuple``:

	>>> major = vice.version[0]
	>>> minor = vice.version[1]

	To get the information in dictionary format:

	>>> vice.version.todict()

	.. note::

		VICE adopts the PEP 440 [1]_ convention for software versioning.
		As stipulated by both standard software versioning conventions and the
		PEP 440 standard, any release may be either an alpha, a beta, or a
		release candidate, but not more than one.

		.. [1] https://peps.python.org/pep-0440/

	.. seealso::

		Special exceptions ``VersionWarning`` and ``VersionError``.
	"""

	ERR_MSG = """\
Internal Error: invalid version information. Please open an issue at \
https://github.com/giganano/VICE/issues."""

	def __init__(self):
		if not isinstance(__ISRELEASED__, bool): raise VersionError(
			self._ERR_MSG_)
		breakdown = version._parse_version_number(
			importlib.metadata.version(__name__.split('.')[0]))
		self._epoch = breakdown["epoch"]
		self._major = breakdown["major"]
		self._minor = breakdown["minor"]
		self._micro = breakdown["micro"]
		self._alpha = breakdown["alpha"]
		self._beta = breakdown["beta"]
		self._rc = breakdown["rc"]
		self._post = breakdown["post"]
		self._dev = breakdown["dev"]
		self._isreleased = __ISRELEASED__
		if self.alpha is not None: warnings.warn("""\
Using an alpha version of VICE. We strongly advise consulting with the VICE \
developers. Be advised that buggy behavior and/or numerical artifacts are \
possible. Please open an issue at https://github.com/giganano/VICE/issues \
if you suspect either.""", VersionWarning)
		if self.beta is not None: warnings.warn("""\
Using a beta version of VICE. We strongly advise consulting with the VICE \
developers. Be advised that buggy behavior and/or numerical artifacts are \
possible. Please open an issue at https://github.com/giganano/VICE/issues \
if you suspect either.""", VersionWarning)
		if self.rc is not None: warnings.warn("""\
Using a release candidate of VICE. Be advised that buggy behavior and/or \
numerical artifacts are possible. If you suspect either, please open an issue \
at https://github.com/giganano/VICE/issues.""", VersionWarning)
		if self.dev is not None: warnings.warn("""\
Using a development version of VICE. Be advised that buggy behavior and/or \
numerical artifacts are possible. If you suspect either, please open an issue \
at https://github.com/giganano/VICE/issues.""", VersionWarning)
		if not self.isreleased: warnings.warn("""\
Using an un-released version of VICE.""", VersionWarning)


	@staticmethod
	def _parse_version_number(number):
		breakdown = {
			"epoch": None,
			"major": None,
			"minor": None,
			"micro": None,
			"alpha": None,
			"beta": None,
			"rc": None,
			"post": None,
			"dev": None
		}
		p = re.compile(
r"^(\d+!)?(\d+){1}(.\d+){1}(.\d+)?(a\d+|b\d+|rc\d+)?(.post\d+)?(.dev\d+)?$")
		match = p.match(number)
		if match is None: raise VersionError(version._ERR_MSG_)
		groups = match.groups()
		if groups[0] is not None:
			if not groups[0].endswith("!"): raise VersionError(version._ERR_MSG_)
			if not groups[0][:-1].isdigit(): raise VersionError(version._ERR_MSG_)
			breakdown["epoch"] = int(groups[0][:-1])
		else: pass
		if groups[1] is None: raise VersionError(version._ERR_MSG_)
		if not groups[1].isdigit(): raise VersionError(version._ERR_MSG_)
		breakdown["major"] = int(groups[1])
		if groups[2] is None: raise VersionError(version._ERR_MSG_)
		if not groups[2].startswith("."): raise VersionError(version._ERR_MSG_)
		if not groups[2][1:].isdigit(): raise VersionError(version._ERR_MSG_)
		breakdown["minor"] = int(groups[2][1:])
		for group in groups[3:]:
			if group is None:
				continue
			elif group.startswith("."):
				if not (group[1:].isdigit() or group[1:5] == "post" or
					group[1:4] == "dev"): raise VersionError(version._ERR_MSG_)
				if group[1:].isdigit():
					breakdown["micro"] = int(group[1:])
				elif group[1:5] == "post":
					breakdown["post"] = int(group[5:])
				else:
					breakdown["dev"] = int(group[4:])
			elif group.startswith("a"):
				if not group[1:].isdigit(): raise VersionError(version._ERR_MSG_)
				breakdown["alpha"] = int(group[1:])
			elif group.startswith("b"):
				if not group[1:].isdigit(): raise VersionError(version._ERR_MSG_)
				breakdown["beta"] = int(group[1:])
			elif group.startswith("rc"):
				if not group[2:].isdigit(): raise VersionError(version._ERR_MSG_)
				breakdown["rc"] = int(group[2:])
			else:
				raise VersionError(version._ERR_MSG_)
		return breakdown


	def __repr__(self):
		r"""The X.Y.Z version string."""
		rep = ""
		if self.epoch is not None: rep += "%d!" % (self.epoch)
		rep += "%d.%d" % (self.major, self.minor)
		if self.micro is not None: rep += ".%d" % (self.micro)
		if self.alpha is not None:
			rep += "a%d" % (self.alpha)
		elif self.beta is not None:
			rep += "b%d" % (self.beta)
		elif self.rc is not None:
			rep += "rc%d" % (self.rc)
		else: pass
		if self.post is not None: rep += ".post%d" % (self.post)
		if self.dev is not None: rep += ".dev%d" % (self.dev)
		return rep


	def __iter__(self):
		r"""Type-casts to a tuple."""
		if self.epoch is not None: yield self.epoch
		yield self.major
		yield self.minor
		yield self.micro
		yield self.alpha
		yield self.beta
		yield self.rc
		yield self.post
		yield self.dev
		yield self.isreleased


	def __getitem__(self, key):
		r"""Type-casts to a tuple and calls its ``__getitem__`` method."""
		return tuple(self).__getitem__(key)


	@property
	def epoch(self):
		r"""
		Type : ``int`` or ``None``

		The epoch version number. In general, this property will always be
		``None`` as the TrackStar developers do not anticipate a need to modify
		its version number handling in the foreseeable future.
		"""
		return self._epoch


	@property
	def major(self):
		r"""
		Type : ``int``

		The major version number.
		"""
		return self._major

	@property
	def minor(self):
		r"""
		Type : ``int``

		The minor version number.
		"""
		return self._minor

	@property
	def micro(self):
		r"""
		Type : ``int`` or ``None``

		The micro version number. Also commonly known as a patch number.
		``None`` or ``0`` if this release is not a patch.
		"""
		return self._micro

	@property
	def alpha(self):
		r"""
		Type : ``int`` or ``None``

		The alpha release version number. ``None`` if this is not an alpha
		release.
		"""
		return self._alpha

	@property
	def beta(self):
		r"""
		Type : ``int`` or ``None``

		The beta release version number. ``None`` if this is not a beta
		release.
		"""
		return self._beta

	@property
	def rc(self):
		r"""
		Type : ``int`` or ``None``

		The release candidate version number. ``None`` if this is not a
		release candidate.
		"""
		return self._rc

	@property
	def post(self):
		r"""
		Type : ``int`` or ``None``

		The post release version number. ``None`` if this is not a post
		release.
		"""
		return self._post

	@property
	def dev(self):
		r"""
		Type : ``int`` or ``None``

		The development release version number. ``None`` if this is not a
		development release.
		"""
		return self._dev

	@property
	def isreleased(self):
		r"""
		Type : ``bool``

		Whether or not this version has been tagged and released.
		"""
		return self._isreleased

	def todict(self):
		r"""
		Convert this object into a dictionary.
		"""
		return {
			"epoch": 		self.epoch,
			"major": 		self.major,
			"minor": 		self.minor,
			"micro": 		self.micro,
			"alpha": 		self.alpha,
			"beta": 		self.beta,
			"rc": 			self.rc,
			"post": 		self.post,
			"dev": 			self.dev,
			"isreleased": 	self.isreleased
		}

version = version()

