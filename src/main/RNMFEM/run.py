#%%Import modules following official guidelines
clear_all()
import os
import numpy as np
from scipy import linalg
from lib.shape_functions import Operations,GaussPoints,ShapeFuncions
from lib.pre_proc import get_preproc_data
from RNMFEM.structs import File_names
from RNMFEM.FFEM_RNM_solver import processing
from main.RNMFEM.Post_Gmsh import Create_B_vector_plot,Create_Vector_field,get_B_vector_point_uvp,integrate_B_surface,interpolated_along_line,integrate_energy
from lib.read_write_TXT_files import  write_file,read_numeric_file_numpy,get_file_block, get_data_from_file,write_numeric_file_numpy


#%% Directories to run
tests_folder=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes'
#tests_folder=r'D:\Work\Nova pasta\01_Doutorado\10_Testes'
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_VS'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\FFEM_only_corrected_BS'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_VS'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_VS_corrected'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_VS_Only_corrected'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'35_Subdomain_Dular_2009_electric\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'36_Subdomain_Dular_2009_magnetic\FFEM_Complete_finite'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'36_Subdomain_Dular_2009_magnetic\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'37_Atuador_hor\\04_FFEM_coarse'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'37_Atuador_hor\\08_FFEM_fine'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'37_Atuador_hor\\09_FFEM_Circuit_coupling'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'37_Atuador_hor\\10_FFEM_Circuit_coupling_perfect'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'37_Atuador_hor\\02_BS_algo'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'38_convergence\\FFEM'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'39_H_discon\\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'39_H_discon\\FFEM_Complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\FFEM_3D_Acopla'))
folder_path=os.path.normpath(os.path.join(tests_folder,'40_3D_Winding\\algo'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'40_3D_Winding\\normal'))
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
#tags_plot=[10002]
Create_B_vector_plot(pre_proc_data.MeshData,results_path,tags_plot)

#==============================================================================
# Integration over a surface
#==============================================================================
#face_phys_ID=1012
#vol_phys_ID=1004
#flux=integrate_B_surface(pre_proc_data,face_phys_ID,vol_phys_ID,results_path)
energy=integrate_energy(pre_proc_data,results_path)


#==============================================================================
# Interpolate along the line
#==============================================================================
vol_phys_ID=[10001,10002]

#data=os.path.normpath(os.path.join(tests_folder,'34_Atuador_vert\\GetDP_3D_completo\\bLine.dat'))
#data = np.genfromtxt(data,delimiter=' ')
#x=data[:,3]
#y=data[:,4]
#z=data[:,5]
xyz_list=list()
counter=0
npoints=50
x=np.zeros(npoints)
y=np.zeros(npoints)
z=np.arange(-0.08,0.08,0.08*2.0/npoints)
for each_x in range(0,npoints):
	this_point=[x[counter],y[counter],np.round(z[counter],8)]
	xyz_list.append(this_point)
	counter+=1
np.savetxt(folder_path+"\\results\\"+'line_coordinates.txt', xyz_list, delimiter=' ')
interpolated_along_line(vol_phys_ID,xyz_list,pre_proc_data,results_path)
#

print "ok"