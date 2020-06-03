
.. _migration: 

Migration 
=========
The fundamental contrast between singlezone and multizone models is that gas 
and stars migrate between zones in multizone models. In nature, migration 
is expected to vary on a galaxy-by-galaxy basis. In keeping with VICE's 
philosophy of making as few assumptions as possible to maximize the user's 
power over their simulations, VICE is implemented with an agnostic approach 
to the migration prescription in a multizone model. 

In multizone models, VICE knows nothing of the spatial configuration of the 
zones the user is operating under. The only piece of information identifying 
a zone is an integer index (a *zero-based* integer index, specifically). These 
zones can be coupled via migration by moving gas and stars from one zone to 
any other zone under a user-constructed prescription. In principle, this 
allows the construction of 1-, 2-, and 3-dimensional zone configurations with 
an arbitrary migration prescription. 

.. _migration_stars: 

.. include:: stars.rst 

.. _migration_gas: 

.. include:: gas.rst 

