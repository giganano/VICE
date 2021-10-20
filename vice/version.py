r"""
This file implements the version_info class.
"""

from __future__ import absolute_import
from . import version_breakdown
import sys
if sys.version_info[:3] < tuple(
	[int(_) for _ in version_breakdown.MIN_PYTHON_VERSION.split('.')]):
	raise RuntimeError("""This version of VICE requires python >= %s. \
Current version: %d.%d.%d""" % (version_breakdown.MIN_PYTHON_VERSION,
		sys.version_info.major, sys.version_info.minor,
		sys.version_info.micro))
else: pass


class version_info:

	r"""
	**VICE Version Information**

	In keeping with convention, VICE's version string can be accessed via
	``vice.__version__``. Alternatively, this object can simply be type-casted
	to a string via ``str(vice.version)``.

	VICE records its version number according to the semantic versioning method
	described in PEP 440 [1]_.

	Attributes
	----------
	major : ``int``
		The major version number of this release.
	minor : ``int``
		The minor version number of this release.
	micro : ``int``
		The micro version number of this release (also known as patch number).
	dev : ``int``
		The development version number of this release. ``None`` if this is not
		a development release.
	alpha : ``int``
		The alpha version number of this release. ``None`` if this is not an
		alpha release.
	beta : ``int``
		The beta version number of this release. ``None`` if this is not a beta
		release.
	rc : ``int``
		The release candidate number of this release. ``None`` if this is not a
		release candidate.
	post : ``int``
		The post number of this release. ``None`` if this is not a post release.
	isreleased : ``bool``
		Whether or not this version has been released. If False, users are
		advised to contact a contributor to VICE if they are not a contributor
		themselves.

	.. note:: At most one of the attributes ``dev``, ``alpha``, ``beta``,
		``rc``, and ``post`` will not be ``None``.

	Notes
	-----
	This object can be type-cast to a tuple of the form:

		``(major, minor, micro, dev, alpha, beta, rc, post)``

	Alternatively, the information can be obtained in dictionary format via
	``vice.version.todict()``.

	.. [1] https://www.python.org/dev/peps/pep-0440/
	"""

	def __repr__(self):
		rep = "%d.%d.%d" % (self.major, self.minor, self.micro)
		if self.dev is not None:
			assert isinstance(self.dev, int), "Invalid version information"
			rep += ".dev%d" % (self.dev)
		elif self.alpha is not None:
			assert isinstance(self.alpha, int), "Invalid version information"
			rep += "a%d" % (self.alpha)
		elif self.beta is not None:
			assert isinstance(self.beta, int), "Invalid version information"
			rep += "b%d" % (self.beta)
		elif self.rc is not None:
			assert isinstance(self.rc, int), "Invalid version information"
			rep += "rc%d" % (self.rc)
		elif self.post is not None:
			assert isinstance(self.post, int), "Invalid version information"
			rep += ".post%d" % (self.post)
		else: pass
		return rep

	def __iter__(self):
		yield self.major
		yield self.minor
		yield self.micro
		yield self.dev
		yield self.alpha
		yield self.beta
		yield self.rc
		yield self.post

	def __getitem__(self, key):
		return tuple(self).__getitem__(key)

	def todict(self):
		r"""
		Convert this object into a dictionary.
		"""
		return {
			"major": self.major,
			"minor": self.minor,
			"micro": self.micro,
			"dev": self.dev,
			"alpha": self.alpha,
			"beta": self.beta,
			"rc": self.rc,
			"post": self.post
		}

	@property
	def major(self):
		r"""
		The major version number.
		"""
		return version_breakdown.MAJOR

	@property
	def minor(self):
		r"""
		The minor version number.
		"""
		return version_breakdown.MINOR

	@property
	def micro(self):
		r"""
		The micro version number (also known as patch number).
		"""
		return version_breakdown.MICRO

	@property
	def dev(self):
		r"""
		The development number for this release. ``None`` if this is not a
		development release.
		"""
		return version_breakdown.DEV

	@property
	def alpha(self):
		r"""
		The alpha number for this release. ``None`` if this is not an alpha
		release.
		"""
		return version_breakdown.ALPHA

	@property
	def beta(self):
		r"""
		The beta number for this release. ``None`` if this is not a beta
		release.
		"""
		return version_breakdown.BETA

	@property
	def rc(self):
		r"""
		The rc number for this release. ``None`` if this is not a release
		candidate.
		"""
		return version_breakdown.RC

	@property
	def post(self):
		r"""
		The post number for this release. ``None`` if this is not a post
		release.
		"""
		return version_breakdown.POST

	@property
	def isreleased(self):
		r"""
		If True, this version of VICE has been released.
		"""
		return version_breakdown.ISRELEASED


version = version_info()

