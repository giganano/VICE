
Contributing to VICE 
====================
VICE is written in a cohesive manner around a core set of objects. That is, 
VICE's implementation shares one library, with considerable overlap between 
relevant calculations (e.g. the ``multizone`` object makes use of the 
``singlezone`` object, which makes use of the ``dataframe`` objects, and so 
on). The ``dataframe`` being the exception which is implemented in ``Cython``, 
the majority of these objects are implemented in C, declared via 
``typedef struct`` statements in the file ``vice/src/objects/objects.h``. 
VICE's entire C library can be found in the directory ``vice/src/``, and the 
major components of its python implementation in ``vice/core/``. This includes 
the ``singlezone`` and ``multizone`` objects, the ``dataframe`` and all 
derived classes, the ``output`` and ``multioutput`` objects, and single 
stellar population routines in the ``vice/core/ssp/`` subdirectory. The 
hierarchical file structure of these directories is designed to mirror one 
another. Separate from the VICE ``core`` is the ``yields`` module, in which 
all nucleosynthetic yield calculations are implemented, independent of the 
simulation features. 

.. note:: The primary author (James W. Johnson) reserves the right to make 
	revisions to all contributed code and associated documentation. 

Building a New Extension 
------------------------
To contribute to VICE, first fork the repository and add any necessary 
routines in the fork. These changes should reflect the overall design of the 
package: with all C extensions in ``vice/src/``; deviating from this pattern 
will cause a broken import following installation of the modified version of 
the code. Unless the modification is to the ``vice/yields/`` module, the 
python wrapping of these functions should be in ``vice/core/``. 

All extensions should be given unit tests, making use of the ``moduletest`` 
and ``unittest`` objects scripted in the files ``vice/testing/moduletest.py`` 
and ``vice/testing/unittest.py``. These objects can be created from functions 
via ``decorators``. Place ``@unittest`` before a function returning a string 
describing the dot-notation path to the function and the unit test function 
itself to obtain a ``unittest`` object. Similarly, place ``@moduletest`` 
before a function return a string describing the dot-notation path to the 
module and a list of ``unittest`` and ``moduletest`` objects to obtain a 
``moduletest`` object. Finally, link the tests to that of the parent 
directory's ``moduletest`` object. 

Documenting Changes 
-------------------
All docstrings visible to the user after installation should be in the 
``numpydocs`` format. This is not required (though recommended) for docstrings 
not accessible to the user. Any C routines added to the source code should be 
given comment headers with descriptions of their purpose, any parameters they 
accept, what they return, and the header files they're declared in. These 
comment headers should reflect the style of those already present in the C 
library. Finally, add the new features to the API reference config file at 
``docs/src/users_guide/pkgcontents/gen/config.py`` and generate the 
documentation by running ``make`` in the ``docs/`` directory. 

Submitting a Contribution 
-------------------------
To submit your contribution, first conduct the steps outlined above, then 
please open a `pull request`__, and label it as an *enhancement*. 

__ pulls_ 
.. _pulls: https://github.com/giganano/VICE/pulls 
