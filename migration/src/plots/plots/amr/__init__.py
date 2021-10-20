
__all__ = ["comparison", "galactic_regions", "solar_annulus"]
for i in __all__: exec("from .%s import main as %s" % (i, i))

