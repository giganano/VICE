r"""
Migration Tools

Provides objects which store prescriptions for the migration of gas and stars
in multizone simulations.

Contents
--------
specs : ``object``
	An object which stores the migration settings of both gas and stars
migration_matrix : ``object``
	An object which describes the mass fraction of gas migrating between
	zones as a function of time.
"""

from __future__ import absolute_import
__all__ = ["specs", "migration_matrix"]
from ._migration import mig_specs as specs
from ._migration import mig_matrix as migration_matrix
