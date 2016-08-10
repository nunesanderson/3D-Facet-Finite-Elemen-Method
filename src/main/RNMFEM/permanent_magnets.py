from lib.pre_proc import get_preproc_data
from main.RNMFEM.Post_Gmsh import Create_Vector_field
import os
from RNMFEM.structs import  File_names
from materials_library import get_materials_lib
from main.RNMFEM.get_Gauss_points import Get_Gauss_points_list
from read_write_TXT_files import write_numeric_data_file,write_numeric_file_numpy
import numpy as np
from lib.shape_functions import GaussIntegPoints

def run_permanent_magnets(preProcData, folder_path):
    print("Running permanent magnetic field solution")

#===============================================================================
# Pre-processor
    mesh_data=preProcData.MeshData
    all_elem_nodes= mesh_data.ElemNodes
    elem_tags=mesh_data.ElemTags
    regions_material=preProcData.RegionMaterial
    materials_lib=get_materials_lib()
    elem_type=mesh_data.ElemType
 
  
#==============================================================================
# Get the Hc value from materials lib
    gauss_points_coordinates,phys_region_list,points_ID_list=Get_Gauss_points_list(preProcData,True,folder_path)
    global_Hc_list=list()
    for each_point_phys_region in phys_region_list:
        for each_region in regions_material:
                if each_region.RegionNumber==each_point_phys_region:
                    matrial_name=each_region.MaterialName
        Hc=materials_lib[matrial_name].Hc
        global_Hc_list.append(Hc)

        
#==============================================================================
# Folder results path
    file_names=File_names()
    results_folder=file_names.get_results_folder_name()
    folder_path=os.path.join(folder_path,results_folder)

#==============================================================================
# Write file with the results
    file_names=File_names()
    h_field_results_file_name=file_names.get_H_results_file_name()
    full_path=os.path.join(folder_path,h_field_results_file_name)
    write_numeric_file_numpy(full_path,global_Hc_list)
    
#==============================================================================
# GMSH post processing
    file_names=File_names()
    Gmsh_file_name=file_names.get_H_Gmsh_pos_proc_file_name()
    path=os.path.join(folder_path,Gmsh_file_name)

    Create_Vector_field(gauss_points_coordinates,global_Hc_list,path,"Hc source")