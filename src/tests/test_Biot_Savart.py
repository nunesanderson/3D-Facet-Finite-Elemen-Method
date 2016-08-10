#==============================================================================
# Import modules following official guidelines:
#==============================================================================
import os
from scipy.sparse import *
from scipy import *
from lib.pre_proc import get_preproc_data
from lib.shape_functions import  Operations
from lib.structs import File_names
from materials_library import get_materials_lib
from RNMFEM import Biot_Savart_3
from main.RNMFEM.get_Gauss_points import Get_Gauss_points_list
from lib.constants import Vacuum
from main.RNMFEM import permanent_magnets
#==============================================================================
# Input data
#==============================================================================

tests_folder=r'D:\Anderson\Dropbox\BKP\10_UFSC\01_Doutorado\3_Codigos\FacetElement\tests'
folder_path=os.path.normpath(os.path.join(tests_folder,'13_Elem_Quad'))
setup_file='setup.txt'
mesh_file='1Elem_quad.msh'

setup_file_name=os.path.join(folder_path,setup_file)
mesh_file_name =os.path.join(folder_path,mesh_file)

nodes_per_element=3
faces_per_element=3
str_noflux_face="iahahaha"

#==============================================================================
# Results path 
file_names=File_names()
results_folder=file_names.get_results_folder_name()
results_path=os.path.join(folder_path,results_folder)

#===============================================================================
# Pre Processing
#===============================================================================
preProcData= get_preproc_data(mesh_file_name, setup_file_name) 
#------------------------------------------------------------------------------
# Setup
regions_material=preProcData.RegionMaterial
regions_excitation=preProcData.RegionExcitation
boundary=preProcData.BC
external_reluctances=preProcData.ExternalReluctances
coupling=preProcData.CoupNet
#------------------------------------------------------------------------------
# Pre-processor
mesh_data=preProcData.MeshData
all_elem_nodes= mesh_data.ElemNodes
tri_elem_nodes=mesh_data.TriElemNodes
nodes_coordenates=mesh_data.NodesCoordenates
elem_tags=mesh_data.ElemTags
elem_type=mesh_data.ElemType
integ_gauss_points_coordinates=Get_Gauss_points_list(preProcData,True,folder_path)
#------------------------------------------------------------------------------
# Materials library
materials_lib=get_materials_lib()
operations=Operations()
vacuum=Vacuum()
#==============================================================================
# Get field solution
#==============================================================================
#Biot-Savart
field_solution=Biot_Savart_3.run_Biot_Savart(setup_file_name,mesh_file_name,folder_path)
# Run Permanent Magnets
#run_permanent_magnets=False
#for each_region in regions_material:
#    for each in materials_lib[each_region.MaterialName].Hc:
#        if each !=0.0:
#            field_solution=permanent_magnets.run_permanent_magnets(preProcData,folder_path)
#            run_permanent_magnets=True
#            break
