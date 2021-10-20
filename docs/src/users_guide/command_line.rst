
From the Command Line
=====================
Included with VICE is a command line entry which runs simple one-zone models
from a terminal. This feature allows the parameters of the model to be
specified as command-line arguments; for usage guidelines, run
``python3 -m vice --help`` from a terminal after installing VICE (from any
directory except the source tree, if installed from source).
While these command-line capabilities are useful for their ease, VICE is
severaly limited in capability when ran from the command-line in comparison
to when ran from the python_ interpreter.

This same command-line entry can be used for automatic access to the tutorial
and the documentation. The commands are ``python3 -m vice --docs`` and
``python3 -m vice --tutorial``.

These features can also be accessed via the simpler command ``vice`` (e.g.
``python3 -m vice --docs`` should do the same thing as ``vice --docs``).

.. _python: https://www.python.org/

