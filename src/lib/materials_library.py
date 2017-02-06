#===============================================================================
# Doctoral student: Anderson Santos Nunes
# University: UFSC - GRUCAD
#===============================================================================

#===============================================================================
# Import classes
#===============================================================================
from structs import MaterialProp
import math
import numpy as np
#===============================================================================
# Material library
#===============================================================================

def get_materials_lib():
#    Hc_zero=np.array([[0],[0],[0]])
#    Hc_NdFe35=np.array([[0],[-890000.0],[0]])
    Hc_zero=np.array([0.0,0.0,0.0])
    Hc_NdFe35=np.array([-0.0,0.0,890000])
    Hc_test_air=np.array([0.0,0.0,795774.7155])
    MaterialsDic = {
        'Copper':MaterialProp(Permitivity=1.0, Conductivity=58.0 * math.pow(10, 6), Permeability=1.0,Hc=Hc_zero),
        'Open':MaterialProp(Permitivity=1.0, Conductivity=58.0 * math.pow(10, 6), Permeability=math.pow(10, -15),Hc=Hc_zero),
        'Aluminum':MaterialProp(Permitivity=1.0, Conductivity=34.0 * math.pow(10, 6), Permeability=1.0,Hc=Hc_zero),
        'Air':MaterialProp(Permitivity=1.0, Conductivity=0.0 * math.pow(10, 6), Permeability=1.0,Hc=Hc_zero),
        'Iron_perf':MaterialProp(Permitivity=1.0, Conductivity=0.0 * math.pow(10.0, 6.0), Permeability=20000000000.0,Hc=Hc_zero),
        'Iron':MaterialProp(Permitivity=1.0, Conductivity=0.0 * math.pow(10.0, 6.0), Permeability=2000.0,Hc=Hc_zero),
        'MDSteel':MaterialProp(Permitivity=1.0, Conductivity=5.0 * math.pow(10, 6), Permeability=300.0,Hc=Hc_zero),
        'NdFe35':MaterialProp(Permitivity=1.0, Conductivity=0.0 * math.pow(10, 6), Permeability=1.0997785406,Hc=Hc_NdFe35)
        }
    return MaterialsDic