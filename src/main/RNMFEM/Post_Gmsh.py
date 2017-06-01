from lib.read_write_TXT_files import  write_file,read_numeric_file_numpy,get_file_block, get_data_from_file,write_numeric_file_numpy
from lib.shape_functions import ShapeFuncions, GaussPoints,Operations
from RNMFEM.structs import File_names
import numpy as np
from scipy import linalg
import os
import math
from lib  import matrix_aux
from materials_library import get_materials_lib


def interpolated_along_line(vol_phys_ID,xyz_list,pre_proc_data,results_path):
	operations=Operations()
	mesh_data=pre_proc_data.MeshData
	get_gauss_points_class=GaussPoints()
	shape_functions=ShapeFuncions()
	file_names=File_names()
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
		if this_element:
			b_at_point=get_B_vector_point_uvp(uvp[0],uvp[1],uvp[2],elem_counter,counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,new_flux,faces_from_to)
			b_at_point=np.array([b_at_point[0,0],b_at_point[1,0],b_at_point[2,0]])
			field.append(b_at_point)
		else:
			b_at_point=np.array([0.0,0.0,0.0])
			field.append(b_at_point)

	Gmsh_file_name=file_names.get_B_Gmsh_line_file_name()
	path=os.path.join(results_path,Gmsh_file_name)
	Create_Vector_field(xyz_list,field,path,"B Vector")

	Gmsh_file_name="line_field.txt"
	path=os.path.join(results_path,Gmsh_file_name)
	write_numeric_file_numpy(path,field)

def integrate_energy(pre_proc_data,results_path):

#Instances
	operations=Operations()
	mesh_data=pre_proc_data.MeshData
	get_gauss_points_class=GaussPoints()
	file_names=File_names()

	regions_material=pre_proc_data.RegionMaterial

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

	mu0=4.0*math.pi*math.pow(10.0,-7.0)
	materials_lib=get_materials_lib()
#Get the magnetic induction, based on the 3D elements interpolation
	energy=0
	counter=-1
	for elem_counter_3D in xrange(number_elements):
		this_elem_type_3D=elem_type[elem_counter_3D]
		nodes_list_3D= mesh_data.ElemNodes[elem_counter_3D]
		gauss_points=get_gauss_points_class.get_gauss_points(this_elem_type_3D)
		num_gauss_points=len(gauss_points)
		if this_elem_type_3D==4:
			counter=counter+1
			material_name=""
			for each_region in regions_material:
				if each_region.RegionNumber==elem_tags[elem_counter_3D][0]:
					material_name=each_region.MaterialName


			mur_r=materials_lib[material_name].Permeability
			mu_elem=mu0*mur_r
			wtri=get_gauss_points_class.get_integration_weight(this_elem_type_3D)

			for each_integ_point in xrange(num_gauss_points):
				u=gauss_points[each_integ_point,0]
				v=gauss_points[each_integ_point,1]
				p=gauss_points[each_integ_point,2]
				b_at_point=get_B_vector_point_uvp(u,v,p,elem_counter_3D,counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,new_flux,faces_from_to)
#				b_at_point=np.array([b_at_point[0,0],b_at_point[1,0],b_at_point[2,0]])

				# Jacobian
				jac=operations.get_jacobian(this_elem_type_3D,nodes_list_3D,nodes_coordenates,u,v,p)
				det_jac=np.linalg.det(jac)
				abs_det_jac=np.abs(det_jac)

#					Element energy
				energy=energy+0.5*(1.0/mu_elem)*wtri*abs_det_jac*matrix_aux.dot_product(b_at_point,b_at_point)


#	Gmsh_file_name=file_names.get_B_Gmsh_surface_file_name()
#	path=os.path.join(results_path,Gmsh_file_name)
#	Create_Vector_field(xy_plot,field,path,"B Vector")

	return energy


def integrate_B_surface(pre_proc_data,face_phys_ID,vol_phys_ID,results_path):

#Instances
	operations=Operations()
	mesh_data=pre_proc_data.MeshData
	get_gauss_points_class=GaussPoints()
	file_names=File_names()

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

	flux=0
	for elem_counter in xrange(number_elements):
		this_elem_type=elem_type[elem_counter]
		if this_elem_type==2 and elem_tags[elem_counter][0]==face_phys_ID:
			nodes_list_2D= mesh_data.ElemNodes[elem_counter]
			gauss_points=get_gauss_points_class.get_gauss_points(this_elem_type)
			num_gauss_points=len(gauss_points)

#Area and normal vector of the 2D element
			node1=elem_nodes[elem_counter][0]
			node2=elem_nodes[elem_counter][1]
			node3=elem_nodes[elem_counter][2]
			P1=np.array([nodes_coordenates[node1][0],nodes_coordenates[node1][1],nodes_coordenates[node1][2]])
			P2=np.array([nodes_coordenates[node2][0],nodes_coordenates[node2][1],nodes_coordenates[node2][2]])
			P3=np.array([nodes_coordenates[node3][0],nodes_coordenates[node3][1],nodes_coordenates[node3][2]])
			A=P2-P1
			B=P3-P1
			AxB=np.cross(A,B)
			nor=linalg.norm(AxB)
			n=AxB/nor
			area=0.5*nor

#Get the real coordinates of the 2D element Gauss points
			xy_local=list()
			for each_integ_point in xrange(num_gauss_points):
				xyz=operations.convert_local_real(this_elem_type,gauss_points[each_integ_point,0],gauss_points[each_integ_point,1],0,nodes_list_2D,nodes_coordenates)
				xy_local.append(xyz)

#Get the magnetic induction, based on the 3D elements interpolation
			counter=-1
			B_list=list()
			for elem_counter_3D in xrange(number_elements):
				this_elem_type_3D=elem_type[elem_counter_3D]
				nodes_list_3D= mesh_data.ElemNodes[elem_counter_3D]
				if this_elem_type_3D==4:
					counter=counter+1
					if elem_tags[elem_counter_3D][0]==vol_phys_ID and set(nodes_list_2D)<set(nodes_list_3D):
						for xyz in xy_local:

#Convert the real coordinates of the 2D element into local coordinates
							uvp=operations.convert_real_to_local(elem_counter_3D,this_elem_type_3D,xyz[0],xyz[1],xyz[2],nodes_list_3D,nodes_coordenates)
							xy_plot.append(xyz)
							b_at_point=get_B_vector_point_uvp(uvp[0],uvp[1],uvp[2],elem_counter_3D,counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,new_flux,faces_from_to)
							b_at_point=np.array([b_at_point[0,0],b_at_point[1,0],b_at_point[2,0]])
							field.append(b_at_point)
							B_list.append(b_at_point)
						break
#Integration process
			for each_integ_point in xrange(num_gauss_points):
				B=B_list[each_integ_point].dot(n)

				flux=flux+B*area/3.0

	Gmsh_file_name=file_names.get_B_Gmsh_surface_file_name()
	path=os.path.join(results_path,Gmsh_file_name)
	Create_Vector_field(xy_plot,field,path,"B Vector")

	return flux

def get_B_vector_point_uvp(u,v,p,elem_ID,elements_3D_counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,flux,faces_from_to):

    #Instances
	shape_functions=ShapeFuncions()
	operations=Operations()

	this_elem_type=elem_type[elem_ID]
	number_local_faces=shape_functions.get_number_faces(this_elem_type)
	this_element_nodes=elem_nodes[elem_ID]
	faces_ID_Elem=faces_ID[elements_3D_counter]
	w_local_this_point=shape_functions.get_facet_shape_function(this_elem_type,u,v,p)
	b_at_point=0

#Interpolation along all the faces
	for local_face_counter in range(0,number_local_faces):
		face_ID=faces_ID_Elem[local_face_counter]
		w_local_1=w_local_this_point[local_face_counter]
		w_real=operations.convert_local_real_Piola(this_elem_type,w_local_1[0,0],w_local_1[0,1],w_local_1[0,2],this_element_nodes,nodes_coordenates)

		flux_at_face=flux[face_ID]
#Takes into account the faces orientation
		if  faces_from_to[face_ID,1]==elements_3D_counter:
			flux_at_face=-flux_at_face
		b_at_point+=flux_at_face*w_real

	return b_at_point


def Create_B_vector_plot(mesh_data,results_path,tags_plot):

#Instances
	file_names=File_names()
	get_gauss_points_class=GaussPoints()

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

# Mesh data
	nodes_coordenates=mesh_data.NodesCoordenates
	elem_tags=mesh_data.ElemTags
	elem_type=mesh_data.ElemType
	elem_nodes=mesh_data.ElemNodes


	B_list=list()
	xy_plot=list()
	number_elements=len(elem_tags)
	operations=Operations()

	elements_3D_counter=0
	for elem_counter in range(0,number_elements):
		run_this_element=False
		if tags_plot=="all" or elem_tags[elem_counter][0] in tags_plot:
			run_this_element=True

		if run_this_element and elem_type[elem_counter]>3:
			this_elem_type=elem_type[elem_counter]

#			gauss_points=get_gauss_points_class.get_gauss_points(this_elem_type)
			gauss_points=get_gauss_points_class.get_local_element_center_point(this_elem_type)
#			number_integ_points=len(gauss_points)
			number_integ_points=1
			this_element_nodes=elem_nodes[elem_counter]

			for each_integ_point in range(0,number_integ_points):

				u=gauss_points[each_integ_point,0]
				v=gauss_points[each_integ_point,1]
				p=gauss_points[each_integ_point,2]
				xy_coord=operations.convert_local_real(this_elem_type,u,v,p,this_element_nodes,nodes_coordenates)
				xy_plot.append(xy_coord)
				b_at_point=get_B_vector_point_uvp(u,v,p,elem_counter,elements_3D_counter,elem_type,elem_nodes,faces_ID,nodes_coordenates,new_flux,faces_from_to)
				B_list.append(np.array([b_at_point[0,0],b_at_point[1,0],b_at_point[2,0]]))
			elements_3D_counter+=1

	Gmsh_file_name=file_names.get_Gmsh_B_field_file_name()
	path=os.path.join(results_path,Gmsh_file_name)
	Create_Vector_field(xy_plot,B_list,path,"B Vector")

#	H_list=list()
#	mu0=4.0*math.pi*pow(10,-7)
#	for each in B_list:
#		H_list.append(each*1.0/mu0)
#	write_numeric_file_numpy(results_path+"\\H_source_FFEM.txt",H_list)


def Create_Vector_field(points,results,path,plot_name):
	'''
	Creates the files to plot a vector field in Gmsh\n
	points: list of points - list[array([ x1,y1,z1]),...]
	results: list of results - list[array([ Vx1,Vy1,Vz1]),...]
	'''
	lines=list()
	lines.append('View "'+str(plot_name)+'" {')
	number_points=len(results)
	for each in range(0,number_points):
		try:
			str_line='VP('+str(points[each][0])+","+str(points[each][1])+","+str(points[each][2])+")"
			str_line=str_line+ '{'+str(results[each][0])+","+str(results[each][1])+","+str(results[each][2])+'};'
			lines.append(str_line)
		except:
			print(each)
	lines.append('// This defines a "time value" for each time step')
	lines.append('TIME{1};')
	lines.append('};')

	write_file(path,lines,'',True)
#	create_annotation_vector_field(points,results,path)

def create_annotation_vector_field(points,results,path):

	lines=list()
	number_points=len(results)
	for each in range(0,number_points):
		lines.append('Plugin(Annotate).Text= "'+str(results[each][0])+","+str(results[each][1])+","+str(0)+'";')
		lines.append('Plugin(Annotate).Font= "Helvetica";')
		lines.append('Plugin(Annotate).Align= "Left";')
		lines.append('Plugin(Annotate).X='+str(points[each][0])+';')
		lines.append('Plugin(Annotate).Y='+str(points[each][1])+';')
		lines.append('Plugin(Annotate).Z=0;')
		lines.append('Plugin(Annotate).ThreeD=1;')
		lines.append('Plugin(Annotate).FontSize=14;')
		lines.append('Plugin(Annotate).View=0;')
		lines.append('Plugin(Annotate).Run;')
	write_file(path+'.opt',lines,'',True)