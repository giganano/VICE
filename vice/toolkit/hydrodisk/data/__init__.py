r"""
VICE hydrodiskstars data management

Contents
--------
download : ``function``
	Downloads the``h277`` simulation star particle subsamples
_h277_exists : ``function``
	Determines if the ``h277`` subsamples exist
_h277_remove : ``function``
	Removes the ``h277`` subsamples
"""

try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["download", "_h277_exists", "_h277_remove"]
	from .download import download, _h277_exists, _h277_remove

else: pass

