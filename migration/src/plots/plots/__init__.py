
__modules__ = ["amr", "tracks"] 
__files__ = ["age_ofe", "eta", "evol", "ia_rate", "mdf_3panel", 
	"metallicity_gradient", "ofe_mdfs", "sfe", "surface_density_gradient"] 
__all__ = __modules__ + __files__ 

for i in __modules__: exec("from . import %s" % (i)) 
for i in __files__: exec("from .%s import main as %s" % (i, i)) 

