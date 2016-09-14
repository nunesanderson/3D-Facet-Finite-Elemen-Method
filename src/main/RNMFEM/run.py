#%%Import modules following official guidelines
clear_all()
import os
import numpy as np
from scipy import linalg
from lib.shape_functions import Operations,GaussPoints,ShapeFuncions
from lib.pre_proc import get_preproc_data
from RNMFEM.structs import File_names
from RNMFEM.FFEM_RNM_solver import processing
from main.RNMFEM.Post_Gmsh import Create_B_vector_plot,Create_Vector_field,get_B_vector_point_uvp,integrate_B_surface
from lib.read_write_TXT_files import  write_file,read_numeric_file_numpy,get_file_block, get_data_from_file,write_numeric_file_numpy



#%% Directories to run
tests_folder=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes'

#folder_path=os.path.normpath(os.path.join(tests_folder,'17_Malha_3D'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'20_Teste_Relé_Equivalente\\Campo_fonte'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'20_Teste_Rel_Equivalente\\Circuito'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'25_Rele_3D\\02_FFFM_reduced'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'25_Rele_3D\\03_FFFM_complete'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'25_Rele_3D\\05_FFFM_reduced_Source'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'25_Rele_3D\\06_Source_Field'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'27_Teste_Campo_Fonte_3D\\Dispositivo_simples'))

#folder_path=os.path.normpath(os.path.join(tests_folder,'21_Malha_3D_dois_mat'))
#folder_path=os.path.normpath(os.path.join(tests_folder,'30_Subdomain\\Subdomain'))
folder_path=os.path.normpath(os.path.join(tests_folder,'31_Subdomain_Dular_2009\\Subdomain'))


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
tags_plot=list()
tags_plot="all"
#tags_plot.append(175)
Create_B_vector_plot(pre_proc_data.MeshData,results_path,tags_plot)

#Integration over a surface
#face_phys_ID=2064
#vol_phys_ID=2003
#flux=integrate_B_surface(pre_proc_data,face_phys_ID,vol_phys_ID,results_path)
#vol_phys_ID=[2003]
#npoints=251
#x=np.linspace(0.07, 0.15,npoints, endpoint=True)
#xyz_list=list()
#
#for counter in xrange(len(x)):
#	xyz=[x[counter],0.0605978714,0.007927051]
#	xyz_list.append(xyz)

#Defines the points along the line
npoints=250
x=np.linspace(-0.01, 0.06,npoints, endpoint=True)
xyz_list=list()

y=(0.01+0.025)/2.0
z=0.001/2.0

for counter in xrange(len(x)):
	xyz=[x[counter],y,z]
	xyz_list.append(xyz)

vol_phys_ID=[174,175]


operations=Operations()
mesh_data=pre_proc_data.MeshData
get_gauss_points_class=GaussPoints()
shape_functions=ShapeFuncions()

#Mesh data
nodes_coordenates=mesh_data.NodesCoordenates
elem_tags=mesh_data.ElemTags
elem_type=mesh_data.ElemType
elem_nodes=mesh_data.ElemNodes
number_elements=len(elem_tags)
xy_plot=list()
field=list()

#Reads flux file
flux_results_file_name=file_names.flux_results_file_name()
full_path=os.path.join(results_path,flux_results_file_name)
new_flux=read_numeric_file_numpy(full_path)

#Read faces_ID
faces_ID_file_name=file_names.get_faces_ID_file_name()
full_path=os.path.join(results_path,faces_ID_file_name)
data=get_data_from_file(full_path)
faces_ID=get_file_block("$faces_ID","$Endfaces_ID",0,data,int)

#Read faces_from_to
from_to_file_name=file_names.faces_from_to_file_name()
full_path=os.path.join(results_path,from_to_file_name)
faces_from_to=read_numeric_file_numpy(full_path)

for xyz in xyz_list:
	counter=-1
	this_element=False
	for elem_counter in range(0,number_elements):
		this_elem_type=elem_type[elem_counter]
		if this_elem_type==4:
			counter=counter+1
			if elem_tags[elem_counter][0] in vol_phys_ID:
				nodes_list= mesh_data.ElemNodes[elem_counter]
				uvp=operations.convert_real_to_local(elem_counter,this_elem_type,xyz[0],xyz[1],xyz[2],nodes_list,nodes_coordenates)
				N=shape_functions.get_node_shape_function(this_elem_type,uvp[0],uvp[1],uvp[2])
				if max(N)<=1.0 and min(N)>=0.0:
					this_element=True
					break

	b_at_point=get_B_vector_point_uvp(uvp[0],uvp[1],uvp[2],elem_counter,counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,new_flux,faces_from_to)
	b_at_point=np.array([b_at_point[0,0],b_at_point[1,0],b_at_point[2,0]])
	field.append(b_at_point)

Gmsh_file_name=file_names.get_B_Gmsh_line_file_name()
path=os.path.join(results_path,Gmsh_file_name)
Create_Vector_field(xyz_list,field,path,"B Vector")

Gmsh_file_name="line_field.txt"
path=os.path.join(results_path,Gmsh_file_name)
write_numeric_file_numpy(path,field)

Gmsh_file_name="line_coordinates.txt"
path=os.path.join(results_path,Gmsh_file_name)
write_numeric_file_numpy(path,xyz_list)
print "ok"