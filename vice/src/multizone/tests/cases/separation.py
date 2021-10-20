r"""
Implements the stellar migration scheme for the separation test.
"""

def stellar_migration(zone, tform, time):
	r"""
	The stellar migration prescription -> at times larger than the formation
	time, the stars move to the non-star-forming zone.

	The star-forming zone is the zero'th zone.
	"""
	if time == tform:
		return zone
	else:
		return 1

