
Contributing to VICE
====================
VICE is written in a cohesive manner around a core set of objects.
That is, VICE's implementation shares one library, with considerable overlap
between relevant calculations (e.g. the ``multizone`` object makes use of the
``singlezone`` object, which makes use of the ``dataframe`` objects, and so
on).
The ``dataframe`` being the exception which is implemented in ``Cython``,
the majority of these objects are implemented in C, declared via
``typedef struct`` statements in the file ``vice/src/objects/objects.h``.
VICE's entire C library can be found in the directory ``vice/src/``, and the
major components of its python implementation in ``vice/core/``.
This includes the ``singlezone`` and ``multizone`` objects, the ``dataframe``
and all derived classes, the ``output`` and ``multioutput`` objects, and
single stellar population routines in the ``vice/core/ssp/`` subdirectory.
The hierarchical file structure of these directories are designed to mirror
one another.
The ``yields`` module, however, is separate from the VICE ``core``, and it
implements all of the nucleosynthetic yield calculations, inependent of the
chemical evolution model/simulation features.
Those wishing to contribute to VICE are strongly encouraged to reach out
to our :ref:`contributors <contributors>` or to `join us on Slack`__; we are
happy to collaborate with those interested in extending VICE's capabilities!

__ slack_
.. _slack: https://join.slack.com/t/vice-astro/shared_invite/zt-tqwa1syp-faiQu0P9oe83cazb0q9tJA

.. note:: The primary author (James W. Johnson) reserves the right to make
	revisions to all contributed code and associated documentation.

Building a New Extension
------------------------
To contribute to VICE, first fork the repository and develop the necessary
objects and functions in the fork.
The changes should reflect the overall design of the package and should, to
the best of one's ability, comply with the stylistic conventions adopted
throughout the code base.

All extensions should be given unit tests, making use of the ``moduletest``
and ``unittest`` objects scripted in the files ``vice/testing/moduletest.py``
and ``vice/testing/unittest.py``.
These objects can be created from the ``@unittest`` and ``@moduletest``
decorators implemented in ``vice/testing/decorators.py``.
The associated documentation should provide adequate instruction on how to
make use of these objects.

Documenting Changes
-------------------
All docstrings visible to the user after installation should be in the
``numpydocs`` format.
This is not required (though recommended) for docstrings not accessible to
the user.
Any C routines added to the source code should be given comment headers with
descriptions of their purpose, any parameters they accept, what they return,
and the header files they're declared in.
These comment headers should reflect the style of those already present in
the C library.
Finally, add the new features to the API reference config file at
``docs/src/api/pkgcontents/gen/config.py`` and generate the
documentation by running ``make`` in the ``docs/`` directory.

Submitting a Contribution
-------------------------
To submit your contribution, first conduct the steps outlined above, then
please open a `pull request`__, and label it as an *enhancement*.

__ pulls_
.. _pulls: https://github.com/giganano/VICE/pulls
