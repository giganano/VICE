
.. _implementation: 

Implemementation
================

Motivation
----------
VICE is designed in such a manner that as few assumptions as possible are made 
by the software itself. In this manner, the power the user has over the 
parameters of their simulations is maximized. With this motivation, any 
quantities that may vary are allowed to do so under user-constructed functions 
in Python_. The only assumption VICE's model adopts is physical plausibility. 

.. _Python: https://www.python.org/ 

Numerical Approach 
------------------
Because VICE is built to handle singlezone and multizone simulations, numerics 
are not the dominant source of error, but rather in the model itself. The 
assumption of instantaneous diffusion of newly produced metals introduces an 
error that which is larger than even modest numerical errors to the equations 
presented in this documentation. 

For this reason, VICE is implemented with a Forward Euler timestep solution, 
and its errors are not dominated by numerics. Furthermore, quantization of the 
timesteps allows the quantization of the episodes of star formation with no 
further assumptions. At several instances in this documentation, this will 
simplify the equations considerably. Adopting a user-specified timestep size, 
this also makes it the computationally cheapest solution by not introducing 
intermediate timesteps. In this manner, VICE is able to achieve a high degree 
of generality while retaining powerful computing speeds. 

Minimization of Dependencies
----------------------------
VICE is implemented in its entirety in ANSI/ISO C, standard library Python_, 
and standard library Cython_. With this implementation, VICE is entirely 
cross platform and independent of the user's version of Anaconda_ (or 
lackthereof). However, VICE is not wrapped for installation in a Windows 
environment without modifying the installation source code. We recommend users 
install and run VICE in a linux environment using the `Windows Terminal`__. 

__ windows_terminal_ 
.. _Cython: https://cython.org/
.. _Anaconda: https://www.anaconda.com/ 
.. _windows_terminal: https://www.microsoft.com/en-us/p/windows-terminal-preview/9n0dx20hk701?activetab=pivot:overviewtab
