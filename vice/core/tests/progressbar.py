
__all__ = ["test_progressbar"]
from ..._globals import _VERSION_ERROR_
from ...testing import moduletest
from ...testing import unittest
from .._cutils import progressbar
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


class test_progressbar:

	r"""
	**VICE Developer's Documentation**

	This object runs a test instance of a progressbar and tests the output
	and attributes at each iteration.
	"""

	ITERTEST_MAXVAL = int(1e4)

	def __init__(self):
		self._TEST_PBAR_ = None
		self._string = True
		self._left_hand_side = True
		self._right_hand_side = True
		self._update = True


	@moduletest
	def __call__(self):
		r"""
		vice.core._cutils.progressbar.__init__ unit test
		"""
		return ["vice.core._cutils.progressbar", 
			[
				self.test_initialize(),
				self.test_maxval(),
				self.test_start(),
				self.test_left_hand_side(),
				self.test_right_hand_side(),
				self.test_finish(),
				self.test_update(),
				self.test_refresh(),
				self.iterative_test(run = False)
			]
		]


	@moduletest
	def iterative_test(self):
		r"""
		vice.core._cutils.progressbar iterative test
		"""
		msg = "vice.core._cutils.progressbar [iterative]"
		try:
			self._TEST_PBAR_ = progressbar(self.ITERTEST_MAXVAL)
			self._TEST_PBAR_._testing = True
			self._TEST_PBAR_.start()
		except:
			return [msg, None]
		for i in range(self.ITERTEST_MAXVAL):
			self._itertest_update(i + 1)
			self._itertest_string()
			self._itertest_left_hand_side()
			self._itertest_right_hand_side()
		tests = [
			self.itertest_update(),
			self.itertest_string(),
			self.itertest_left_hand_side(),
			self.itertest_right_hand_side()
		]
		return [msg, tests]


	@unittest
	def test_initialize(self):
		r"""
		vice.core._cutils.progressbar.__init__ unit test
		"""
		def test():
			try:
				self._TEST_PBAR_ = progressbar()
			except:
				return False
			try:
				self._TEST_PBAR_._testing = True
			except: pass
			return isinstance(self._TEST_PBAR_, progressbar)
		return ["vice.core._cutils.progressbar.__init__", test]


	@unittest
	def itertest_string(self):
		r"""
		vice.core._cutils.progressbar.string iterative test
		"""
		def test():
			return self._string
		return ["vice.core._cutils.progressbar.string [iterative]", test]


	def _itertest_string(self):
		r"""
		Test the progressbar string at each iteration.
		"""
		if (isinstance(self._TEST_PBAR_, progressbar) and
			self._string is not None):
			try:
				str(self._TEST_PBAR_)
			except:
				self._string = False
			# Only compare to terminal size if this isn't GitHub actions
			# GitHub actions has a different ioctl than a Mac OS or Linux
			# desktop, so getting the window width the routine at
			# vice/src/io/progressbar.c doesn't work. Instead, when CI testing
			# with GitHub actions that routine simply assumes a window width
			# of 100.
			if ("GITHUB_ACTIONS" in os.environ.keys() and
				os.environ["GITHUB_ACTIONS"] == "true"):
				self._string &= len(str(self._TEST_PBAR_)) == 100
			else:
				# One space is left for the cursor at the end of the line
				length = len(str(self._TEST_PBAR_))
				self._string &= length == os.get_terminal_size().columns - 1
			self._string &= str(self._TEST_PBAR_).startswith(
				self._TEST_PBAR_.left_hand_side)
			self._string &= str(self._TEST_PBAR_).endswith(
				self._TEST_PBAR_.right_hand_side)
		else: 
			self._string = None


	@unittest
	def test_maxval(self):
		r"""
		vice.core._cutils.progressbar.maxval unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			status = True
			try:
				self._TEST_PBAR_.maxval = 50
			except:
				return False
			status &= self._TEST_PBAR_.maxval == 50
			try:
				self._TEST_PBAR_.maxval = 25
			except:
				return False
			status &= self._TEST_PBAR_.maxval == 25
			try:
				self._TEST_PBAR_.maxval = 100
			except:
				return False
			status &= self._TEST_PBAR_.maxval == 100
			return status
		return ["vice.core._cutils.progressbar.maxval", test]


	@unittest
	def test_left_hand_side(self):
		r"""
		vice.core._cutils.progressbar.left_hand_side unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			status = isinstance(self._TEST_PBAR_.left_hand_side, strcomp)
			try:
				self._TEST_PBAR_.left_hand_side = "foo"
			except:
				return False
			status &= self._TEST_PBAR_.left_hand_side == "foo"
			status &= str(self._TEST_PBAR_).startswith("foo")
			try:
				self._TEST_PBAR_.left_hand_side = "bar"
			except:
				return False
			status &= self._TEST_PBAR_.left_hand_side == "bar"
			status &= str(self._TEST_PBAR_).startswith("bar")
			try:
				self._TEST_PBAR_.left_hand_side = None
			except:
				return False
			return status
		return ["vice.core._cutils.progressbar.left_hand_side", test]


	@unittest
	def itertest_left_hand_side(self):
		r"""
		vice.core._cutils.progressbar.left_hand_side iterative test.
		"""
		def test():
			return self._left_hand_side
		return ["vice.core._cutils.progressbar.left_hand_side [iterative]",
			test]


	def _itertest_left_hand_side(self):
		r"""
		Tests vice.core._cutils.progressbar.left_hand_side at each iteration
		"""
		status = isinstance(self._TEST_PBAR_, progressbar)
		status &= 'h' not in self._TEST_PBAR_.left_hand_side
		status &= 'm' not in self._TEST_PBAR_.left_hand_side
		status &= 's' not in self._TEST_PBAR_.left_hand_side
		status &= "of" in self._TEST_PBAR_.left_hand_side
		return status


	@unittest
	def test_right_hand_side(self):
		r"""
		vice.core._cutils.progressbar.right_hand_side unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			status = isinstance(self._TEST_PBAR_.right_hand_side, strcomp)
			try:
				self._TEST_PBAR_.right_hand_side = "foo"
			except:
				return False
			status &= self._TEST_PBAR_.right_hand_side == "foo"
			status &= str(self._TEST_PBAR_).endswith("foo")
			try:
				self._TEST_PBAR_.right_hand_side = "bar"
			except:
				return False
			status &= self._TEST_PBAR_.right_hand_side == "bar"
			status &= str(self._TEST_PBAR_).endswith("bar")
			try:
				self._TEST_PBAR_.right_hand_side = None
			except:
				return False
			return status
		return ["vice.core._cutils.progressbar.right_hand_side", test]


	@unittest
	def itertest_right_hand_side(self):
		r"""
		vice.core._cutils.progressbar.right_hand_side iterative test
		"""
		def test():
			return self._right_hand_side
		return ["vice.core._cutils.progressbar.right_hand_side [iterative]",
			test]

	def _itertest_right_hand_side(self):
		r"""
		Tests vice.core._cutils.progressbar.right_hand_side at each iteration
		"""
		status = isinstance(self._TEST_PBAR_, progressbar)
		status &= 'h' in self._TEST_PBAR_.right_hand_side
		status &= 'm' in self._TEST_PBAR_.right_hand_side
		status &= 's' in self._TEST_PBAR_.right_hand_side
		status &= "of" not in self._TEST_PBAR_.right_hand_side
		return status


	@unittest
	def test_start(self):
		r"""
		vice.core._cutils.progressbar.start unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			try:
				self._TEST_PBAR_.start()
			except:
				return False
			status = self._TEST_PBAR_.current == 0
			status &= self._TEST_PBAR_.left_hand_side.startswith("0")
			status &= self._TEST_PBAR_.right_hand_side == "ETA: 00h00m00s"
			return status
		return ["vice.core._cutils.progressbar.start", test]


	@unittest
	def test_finish(self):
		r"""
		vice.core._cutils.progressbar.finish unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			try:
				self._TEST_PBAR_.finish()
			except:
				return False
			status = self._TEST_PBAR_.current == self._TEST_PBAR_.maxval
			status &= self._TEST_PBAR_.left_hand_side == "%d of %d" % (
				self._TEST_PBAR_.maxval, self._TEST_PBAR_.maxval)
			status &= self._TEST_PBAR_.right_hand_side == "ETA: 00h00m00s"
			return status
		return ["vice.core._cutils.progressbar.finish", test]


	@unittest
	def test_update(self):
		r"""
		vice.core._cutils.progressbar.update unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			try:
				self._TEST_PBAR_.start()
			except:
				return None
			status = self._TEST_PBAR_.current == 0
			try:
				self._TEST_PBAR_.update(1)
			except:
				return False
			status &= self._TEST_PBAR_.current == 1
			try:
				self._TEST_PBAR_.update(2)
			except:
				return False
			status &= self._TEST_PBAR_.current == 2
			try:
				self._TEST_PBAR_.current = 3
			except:
				return False
			status &= self._TEST_PBAR_.current == 3
			try:
				self._TEST_PBAR_.current = 4
			except:
				return False
			status &= self._TEST_PBAR_.current == 4
			return status
		return ["vice.core._cutils.progressbar.update", test]


	@unittest
	def itertest_update(self):
		r"""
		vice.core._cutils.progressbar.update iterative test
		"""
		def test():
			return self._update
		return ["vice.core._cutils.progressbar.update [iterative]", test]


	def _itertest_update(self, value):
		r"""
		Tests vice.core._cutils.progressbar.update at each iteration

		Parameters
		----------
		value : ``int``
			The new number of iterations the progressbar has gone through.
		"""
		assert isinstance(value, int), "Internal Error"
		try:
			self._TEST_PBAR_.update(value)
		except:
			self._update = False


	@unittest
	def test_refresh(self):
		r"""
		vice.core._cutils.progressbar.refresh unit test
		"""
		def test():
			if not isinstance(self._TEST_PBAR_, progressbar): return None
			try:
				self._TEST_PBAR_.refresh()
			except:
				return False
			return True
		return ["vice.core._cutils.progressbar.refresh", test]

