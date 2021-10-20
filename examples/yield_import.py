"""
In this file we demonstrate how nucleosynthetic yields can be declared in a
.py file and then imported into python.

To do this, we import the file yields.py in this directory, in which the
yield settings are modified.
"""

import vice

print("CCSN yield of O before import: ", vice.yields.ccsne.settings["o"])

# yields.py in this directory
import yields

print("CCSN yield of O after import: ", vice.yields.ccsne.settings["o"])

