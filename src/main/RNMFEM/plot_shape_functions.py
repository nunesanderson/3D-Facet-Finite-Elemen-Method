#===============================================================================
# Import modules following official guidelines:
#===============================================================================
clear_all()
import os
from scipy.sparse import *
from scipy import *
from lib.pre_proc import get_preproc_data
from lib.shape_functions import ShapeFuncions,Operations
import numpy as np
from main.RNMFEM.structs import Face,W_at_GaussPoint,File_names
from main.RNMFEM.Post_Gmsh import Create_Vector_field
from lib.shape_functions import GaussPoints
operations=Operations()
# Pre Processing
#===============================================================================
tests_folder=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes'
folder_path=os.path.normpath(os.path.join(tests_folder,'18_reference_element_3D'))

#===============================================================================
# Variables
n=20
elem_type=4
which_face=2
#===============================================================================
# Interpolations functions
integ_nodes_coordinates=[]
integ_nodes_results=[]
region_ID_list=[]
shape_functions=ShapeFuncions()
xy_plot=list()
B_list=list()

u_start=-1.0
v_start=-1.0
p_start=-1.0

uvp_end=1.0
duvp=(uvp_end-v_start)/n

for u in frange(u_start,uvp_end,duvp):
	for v in frange(v_start,uvp_end,duvp):
		for p in frange(p_start,uvp_end*0.9,duvp):
			
			bool_run=True
			
			if p==1.0:
				bool_run=False
				
			N_nodal=shape_functions.get_node_shape_function(elem_type,u,v,p)
			for k in range(0,N_nodal.size):
				if N_nodal[k]<0.0 or N_nodal[k]>1.0:
					bool_run=False

			if bool_run:
				N=shape_functions.get_facet_shape_function(elem_type,u,v,p)
				Wuv=np.zeros((3,1))
				Wuv[0,0]=N[which_face,0]
				Wuv[1,0]=N[which_face,1]
				Wuv[2,0]=N[which_face,2]
				uv=np.zeros((3,1))
				uv[0,0]=u
				uv[1,0]=v
				uv[2,0]=p
				xy_plot.append(uv)
				B_list.append(Wuv)

#===============================================================================
# PLot
file_names=File_names()
results_folder=file_names.get_results_folder_name()
results_path=os.path.join(folder_path,results_folder)
Gmsh_file_name=file_names.get_Gmsh_B_field_file_name()
path=os.path.join(results_path,Gmsh_file_name)
Create_Vector_field(xy_plot,B_list,path,"W face")
