
__all__ = ["model_comparison", "galactic_regions"] 
for i in __all__: exec("from .%s import main as %s" % (i, i)) 

