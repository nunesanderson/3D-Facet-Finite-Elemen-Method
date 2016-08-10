from lib.shape_functions import  GaussPoints, Operations
import os
from RNMFEM.structs import File_names
from read_write_TXT_files import write_file,write_numeric_data_file,write_numeric_file_numpy
from lib.pre_proc import get_preproc_data
import numpy as np

def Get_Gauss_points_list(preProcData,does_write_file,folder_path):
	'''
	Get the coordinates of the Guass points for all elements\n
	Return: list(array with the coordinates)\n
	PreProcData: The data from pre processing\n
	does_write_file: boolean. True: write the files containing the results\n
	folder_path: directory of the folder to write the file
	'''
#==============================================================================
# Pre-processor
	mesh_data=preProcData.MeshData
	all_elem_nodes= mesh_data.ElemNodes
	nodes_coordenates=mesh_data.NodesCoordenates
	elem_tags=mesh_data.ElemTags
	elem_type=mesh_data.ElemType

	gauss_points=GaussPoints()
	oper=Operations()
	
	number_elements=len(elem_tags)
	start_3D=0
	number_gauss_points=0
	max_number_points=0
	
	for kl in xrange(number_elements):
		if elem_type[kl]<=3:
			start_3D+=1
		else:
			this_gauss_points=gauss_points.get_gauss_points(elem_type[kl])
			number_gauss_points+=float(this_gauss_points.shape[0])
			number_gauss_points_element=float(this_gauss_points.shape[1])
			if number_gauss_points_element>max_number_points:
				max_number_points=number_gauss_points_element

	gauss_points_coordinates=np.zeros((number_gauss_points,max_number_points))
	
	point_counter=0
	points_ID_list=list()
	phys_region_list=list()
	for kl in range (start_3D,number_elements):
		integPoints=gauss_points.get_gauss_points(elem_type[kl])
		numnodes=integPoints.shape[0]

		nodes=[]
		for eachnode in xrange(numnodes):
			nodes.append(all_elem_nodes[kl][eachnode])
		elem_points_ID=list()
		for integPoint in range(0,numnodes):
			u=integPoints[integPoint,0]
			v= integPoints[integPoint,1]
			p= integPoints[integPoint,2]
			XYZ=oper.convert_local_real(elem_type[kl],u,v,p,nodes,nodes_coordenates)
			
			gauss_points_coordinates[point_counter][0]=XYZ[0]
			gauss_points_coordinates[point_counter][1]=XYZ[1]
			gauss_points_coordinates[point_counter][2]=XYZ[2]
			phys_region_list.append(elem_tags[kl][0])
			point_counter+=1
			elem_points_ID.append(point_counter-1)
		points_ID_list.append(elem_points_ID)

#==============================================================================
# Folder results path
	file_names=File_names()
	results_folder=file_names.get_results_folder_name()
	results_path=os.path.join(folder_path,results_folder)
	path=os.path.join(results_path,file_names.get_Gauss_points_list_file_name())
	path_IDs=os.path.join(results_path,file_names.get_Gauss_Points_ID_file_name())
	path_Phys=os.path.join(results_path,file_names.get_Gauss_Points_Phys_region_file_name())
 
 

	write_numeric_file_numpy(path_Phys,phys_region_list)
	write_numeric_file_numpy(path,gauss_points_coordinates)
 	write_numeric_file_numpy(path_IDs,points_ID_list)
	return gauss_points_coordinates,phys_region_list,points_ID_list