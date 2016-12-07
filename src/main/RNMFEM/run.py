#%%Import modules following official guidelines
clear_all()
import os
import numpy as np
from scipy import linalg
from lib.shape_functions import Operations,GaussPoints,ShapeFuncions
from lib.pre_proc import get_preproc_data
from RNMFEM.structs import File_names
from RNMFEM.FFEM_RNM_solver import processing
from main.RNMFEM.Post_Gmsh import Create_B_vector_plot,Create_Vector_field,get_B_vector_point_uvp,integrate_B_surface,interpolated_along_line
from lib.read_write_TXT_files import  write_file,read_numeric_file_numpy,get_file_block, get_data_from_file,write_numeric_file_numpy



#%% Directories to run
tests_folder=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes'

#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador\\01_hor\\04_FFEM_complet'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador\\03_vert - Subproblems\\03_FFEM_VS'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador\\03_vert - Subproblems\\02_FFEM_complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_VS'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_VS_corrected'))
folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_Complete'))
setup_file='setup.txt'
mesh_file='model.msh'

#%% Pre processing
file_names=File_names()
results_folder=file_names.get_results_folder_name()
setup_file_name=os.path.join(folder_path,setup_file)
mesh_file_name =os.path.join(folder_path,mesh_file)
results_path=os.path.join(folder_path,results_folder)
pre_proc_data= get_preproc_data(mesh_file_name, setup_file_name)

#%%Processing
processing(folder_path,pre_proc_data)


#%%Post processing

#==============================================================================
# Plot B
#==============================================================================
tags_plot=list()
tags_plot="all"
#tags_plot.append(1003)
Create_B_vector_plot(pre_proc_data.MeshData,results_path,tags_plot)

#==============================================================================
# Integration over a surface
#==============================================================================
#face_phys_ID=2062
#vol_phys_ID=2001
#flux=integrate_B_surface(pre_proc_data,face_phys_ID,vol_phys_ID,results_path)


#==============================================================================
# Interpolate along the line
#==============================================================================
vol_phys_ID=[2001]

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\34_Atuador_vert\GetDP_3D\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x=data[:,3]
y=data[:,4]
z=data[:,5]
xyz_list=list()
counter=0
for each_x in x:
	this_point=[each_x,y[counter],z[counter]]
	xyz_list.append(this_point)
	counter+=1

np.savetxt(folder_path+"\\results\\"+'line_coordinates.txt', xyz_list, delimiter=' ')
interpolated_along_line(vol_phys_ID,xyz_list,pre_proc_data,results_path)


print "ok"