
import os
import copy
from scipy.sparse import *
from lib.shape_functions import ShapeFuncions, GaussPoints, Operations
import numpy as np
from RNMFEM.structs import Face,File_names
from materials_library import get_materials_lib
from RNMFEM import Biot_Savart,Post_Gmsh
from RNMFEM.Post_Gmsh import Create_Vector_field
from lib.read_write_TXT_files import  get_Field_solution
from main.RNMFEM import permanent_magnets
from lib.constants import Vacuum,GlobalVariables
from lib.error import Errors
from lib.messages import print_message
from read_write_TXT_files import write_numeric_data_file,write_numeric_file_numpy,write_numeric_file_sparse_csr
import scipy
from scipy import sparse
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as splinalg
from lib  import matrix_aux
import math
def write_files(faces_list,results_path,faces_ID,complete_flux):
	#flux
	file_names=File_names()
	flux_results_file_name=file_names.flux_results_file_name()
	full_path=os.path.join(results_path,flux_results_file_name)
	write_numeric_file_numpy(full_path,complete_flux)

	#faces from to
	number_faces=len(faces_list)
	from_to=np.zeros((number_faces,2))
	counter=0
	for each_face in faces_list:
		from_to[counter,0]=each_face.elem_1
		from_to[counter,1]=each_face.elem_2
		counter+=1
	from_to_file_name=file_names.faces_from_to_file_name()
	full_path=os.path.join(results_path,from_to_file_name)
	write_numeric_file_numpy(full_path,from_to)

	#faces ID
	faces_ID_file_name=file_names.get_faces_ID_file_name()
	full_path=os.path.join(results_path,faces_ID_file_name)
	write_numeric_data_file(full_path,faces_ID,"faces_ID",True)


def run_solver(faces_rel_matrix,incidence_matrix,faces_fmm_matrix,source_flux_sparse,faces_ID_deleted_list,faces_list,faces_deleted_list,BC_nodes,BC_values):

	from main.RNM_Solver import Solver

	if isinstance(faces_rel_matrix,sparse.csr_matrix):
		faces_rel_matrix=faces_rel_matrix.toarray()

	admitance_matrix=np.linalg.inv(faces_rel_matrix)
	del(faces_rel_matrix)

	flux=Solver.SolveMagneticCircuit(incidence_matrix,admitance_matrix,faces_fmm_matrix,source_flux_sparse,BC_nodes,BC_values)
	del(incidence_matrix)
	del(admitance_matrix)
	del(faces_fmm_matrix)

	# Organize the flux
	number_complete_flux=len(faces_ID_deleted_list)+flux.shape[0]
	complete_flux=np.zeros((number_complete_flux,1))

	counter=0
	counter_face=0
	for each in xrange(number_complete_flux):
		if not each in faces_ID_deleted_list:
			complete_flux[each,0]=flux[counter,0]
			counter+=1
		else:
			faces_list.insert(each,faces_deleted_list[counter_face])
			counter_face+=1
	return complete_flux

def processing(folder_path,preProcData):
	faces_rel_spare,incidence_matrix_sparse,fmm_sparse,source_flux_sparse,faces_ID,results_path,faces_ID_deleted_list,faces_list,faces_deleted_list,BC_nodes,BC_values=integration_process(folder_path,preProcData)
	complete_flux=run_solver(faces_rel_spare,incidence_matrix_sparse,fmm_sparse,source_flux_sparse,faces_ID_deleted_list,faces_list,faces_deleted_list,BC_nodes,BC_values)
	write_files(faces_list,results_path,faces_ID,complete_flux)


def integration_process(folder_path,preProcData):
	file_names=File_names()
	results_folder=file_names.get_results_folder_name()
	results_path=os.path.join(folder_path,results_folder)

#	Source field
	mu0=4.0*math.pi*math.pow(10.0,-7.0)
	run_surface_integral=False
	run_biot_savart=True
	run_VS=False

#%% Instances and geral definitions
	global_variables=GlobalVariables()
	error=Errors()
	operations=Operations()
	materials_lib=get_materials_lib()
	vacuum=Vacuum()
	get_gauss_points_class=GaussPoints()
	shape_functions=ShapeFuncions()
	operations=Operations()

	str_noflux_face=global_variables.str_noflux_face
	results_folder=file_names.get_results_folder_name()

	face=Face()
	#------------------------------------------------------------------------------
	# Setup
	regions_material=preProcData.RegionMaterial
	regions_excitation=preProcData.RegionExcitation
	boundary=preProcData.BC
	external_reluctances=preProcData.ExternalReluctances
	coupling=preProcData.CoupNet


	#------------------------------------------------------------------------------
	# Mesh
	mesh_data=preProcData.MeshData
	all_elem_nodes_3D= mesh_data.ElemNodes
	nodes_coordenates=mesh_data.NodesCoordenates
	elem_tags=mesh_data.ElemTags
	elem_type=mesh_data.ElemType

	#%% Get 2D and 3D elements, with their materials name
	elem_2D_ID=list()
	elem_type_3D=list()
	elem_nodes_3D=list()
	elem_tags_3D=list()
	region_ID_list_3D=list()
	number_elements_2D=0

	for counter,each_elem in enumerate(all_elem_nodes_3D):
		this_elem_type=elem_type[counter]
		if this_elem_type<4:
			elem_2D_ID.append(counter)
			number_elements_2D+=1
		else:
			elem_nodes_3D.append(each_elem)
			elem_type_3D.append(elem_type[counter])
			elem_tags_3D.append(elem_tags[counter])

			find=False
			for each_region in regions_material:
				if each_region.RegionNumber==elem_tags[counter][0]:
					region_ID_list_3D.append(each_region.MaterialName)
					find=True
			if not find:
			   error.physical_surface_not_defined(str(each_region.RegionNumber),elem_tags[counter][0])

	number_elements=len(elem_nodes_3D)
	number_nodes=len(nodes_coordenates)
	faces_ID=list()
	faces_list=list()
	plot_test_coord=list()
	plot_test_field=list()

	#%%Get source field
	field_solution=list()
	run_permanent_magnets=False

#	Run Permanent Magnets
	for each_region in regions_material:
		for each in materials_lib[each_region.MaterialName].Hc:
			if each !=0.0:
				permanent_magnets.run_permanent_magnets(preProcData,folder_path)
				run_permanent_magnets=True
				break

	#Read the fields
	if run_biot_savart or run_permanent_magnets:

		results_folder=file_names.get_results_folder_name()
		folder_name=os.path.join(folder_path,results_folder)

		#Gauss points IDs
		this_file_name=file_names.get_Gauss_points_ID_file_name()
		full_path=os.path.join(folder_name,this_file_name)
		points_IDs = np.genfromtxt(full_path,delimiter=' ',dtype='int', usecols=(1,2,3,4))
		points_ID_elem = np.genfromtxt(full_path,delimiter=' ',dtype='int', usecols=(0))
		points_ID_elem=points_ID_elem-number_elements_2D
		points_ID_elem=points_ID_elem.tolist()


#		Gauss points coordinates
		this_file_name=file_names.get_Gauss_points_coordinates_file_name()
		full_path=os.path.join(folder_name,this_file_name)
		coordinates = np.genfromtxt(full_path,delimiter=' ',dtype='double')


#		Fields
		this_file_name=file_names.get_Gauss_points_H_field_file_name()
#		this_file_name="H_source_FFEM.txt"

		full_path=os.path.join(folder_name,this_file_name)
		fields = np.genfromtxt(full_path,delimiter=' ',dtype='double')
		for elem_counter in range(0,number_elements):
			this_elem_type=elem_type_3D[elem_counter]
			gauss_points=get_gauss_points_class.get_gauss_points(this_elem_type)
			number_integ_points=len(get_gauss_points_class.get_gauss_points(this_elem_type))
			this_points_field=list()
			if elem_counter in points_ID_elem:

				this_elem=points_ID_elem.index(elem_counter)
				for k in points_IDs[this_elem].tolist():
					Hxy=np.zeros((3,1))
					Hxy[0,0]=fields[k,0]
					Hxy[1,0]=fields[k,1]
					Hxy[2,0]=fields[k,2]
					plot_test_field.append(Hxy)
					plot_test_coord.append(coordinates[k])

					this_points_field.append(Hxy)

			else:
				for k in xrange(number_integ_points):
					Hxy=np.zeros((3,1))
					this_points_field.append(Hxy)
			field_solution.append(this_points_field)


	run_external_circuit=False
	if len(coupling)>0:
		run_external_circuit=True


#%%Creates the face list
	print_message("Creating faces list")
	for elem_counter in range(0,number_elements):
		number_local_faces=shape_functions.get_number_faces(this_elem_type)
		this_elem_type=elem_type_3D[elem_counter]
		this_element_nodes=elem_nodes_3D[elem_counter]
		faces_nodes_ID=shape_functions.get_nodes_ID_2_face(this_elem_type)
		number_faces,nodes_per_face=faces_nodes_ID.shape
		local_faces_ID=list()
		for local_face_counter in range(0,number_faces):
			nodes_list=list()
			for node_counter in range(nodes_per_face):
				node_ID=faces_nodes_ID[local_face_counter,node_counter]
				nodes_list.append(this_element_nodes[node_ID])
			local_faces_ID.append(face.add_to_list(nodes_list,elem_counter,faces_list))
		faces_ID.append(local_faces_ID)
	print_message("Creating faces list - Done")


#%%Integration
	print_message("Integration process")

	num_meshed_rel=len(faces_list)
	num_non_meshed_rel=len(external_reluctances)
	num_total_rel=num_meshed_rel+num_non_meshed_rel

#sparse matrix
	cols_rel_sparse=list()
	rows_rel_sparse=list()

#reluctance matrix
	diagonal=list()
	for each_element_faces in faces_ID:
		numbre_faces_this_element=len(each_element_faces)
		for face_counter_1 in xrange(numbre_faces_this_element):
			pos_1=each_element_faces[face_counter_1]
			for face_counter_2 in xrange(numbre_faces_this_element):
				pos_2=each_element_faces[face_counter_2]
				if pos_1==pos_2:
					if pos_1 not in diagonal:
						rows_rel_sparse.append(pos_1)
						cols_rel_sparse.append(pos_2)
						diagonal.append(pos_1)
				else:
					rows_rel_sparse.append(pos_1)
					cols_rel_sparse.append(pos_2)

	data_rel_sparse=np.zeros(len(rows_rel_sparse))
	faces_rel_spare=csr_matrix((data_rel_sparse, (rows_rel_sparse, cols_rel_sparse)), shape=(num_total_rel, num_total_rel))

#fmm matrix
	cols_fmm_sparse=np.zeros(num_meshed_rel)
	rows_fmm_sparse=xrange(0,num_meshed_rel)
	data_fmm_sparse=np.zeros(num_meshed_rel)
	fmm_sparse=csr_matrix((data_fmm_sparse, (rows_fmm_sparse, cols_fmm_sparse)), shape=(num_total_rel,1))

#source_flux matrix
	cols_source_flux_sparse=np.zeros(num_meshed_rel)
	rows_source_flux_sparse=xrange(0,num_meshed_rel)
	data_source_flux_sparse=np.zeros(num_meshed_rel)
	source_flux_sparse=csr_matrix((data_source_flux_sparse, (rows_source_flux_sparse, cols_source_flux_sparse)), shape=(num_total_rel,1))
#grad_phi matrix
#	cols_grad_phi_sparse=np.zeros(num_meshed_rel)
#	rows_grad_phi_sparse=xrange(0,num_meshed_rel)
#	data_grad_phi_sparse=np.zeros(num_meshed_rel)
#	grad_phi_sparse=csr_matrix((data_grad_phi_sparse, (rows_grad_phi_sparse, cols_grad_phi_sparse)), shape=(num_total_rel,1))

	this_elem_type=""
	for elem_counter in xrange(number_elements):
		this_elem_type_changed=elem_type_3D[elem_counter]
		if this_elem_type!=this_elem_type_changed:
			this_elem_type=this_elem_type_changed
			gauss_points=get_gauss_points_class.get_gauss_points(this_elem_type)
			number_local_faces=shape_functions.get_number_faces(this_elem_type)
			number_integ_points=len(get_gauss_points_class.get_gauss_points(this_elem_type))
			wtri=get_gauss_points_class.get_integration_weight(this_elem_type)

		faces_ID_Elem=faces_ID[elem_counter]
		this_element_nodes=elem_nodes_3D[elem_counter]
		mur_r=materials_lib[region_ID_list_3D[elem_counter]].Permeability
		mu_elem=vacuum.mu0*mur_r

		k_sf=1.0
		if run_VS:
			if mur_r>1.0:
				k_sf=-1.0*mu0*((1.0/mu_elem)-(1.0/mu0))
			else:
				k_sf=0


# Get W at reference element
		w_local_this_element=list() #[gauss point][face]
		for each_integ_point in xrange(number_integ_points):

#u,v,w coordinates
			u=gauss_points[each_integ_point,0]
			v=gauss_points[each_integ_point,1]
			w=gauss_points[each_integ_point,2]

# Shape functions @ reference element
			w_local_this_point=shape_functions.get_facet_shape_function(this_elem_type,u,v,w)
			w_local_this_element.append(w_local_this_point)

# Shape functions @ real element for each face
		w_real_all_points=list() # w_real_lista[0] contains  the shape function of all points for face 0

#   Face 0...Fn
#P0  W
#Pn

		for face_counter in xrange(number_local_faces):
			w_real_this_point=list()
			for point_counter in  range(0,number_integ_points):
				w_local=w_local_this_element[point_counter][face_counter]
				w_real=operations.convert_local_real_Piola(this_elem_type,w_local[0,0],w_local[0,1],w_local[0,2],this_element_nodes,nodes_coordenates)
				w_real_this_point.append(w_real)
			w_real_all_points.append(w_real_this_point)

# Source fields
		for local_face_counter in xrange(number_local_faces):

			w_1=copy.deepcopy(w_real_all_points[local_face_counter])
			face_ID_1=faces_ID_Elem[local_face_counter]

			if faces_list[face_ID_1].elem_2==elem_counter:
				for each in w_1:
					each=matrix_aux.invert_w(each)

# mmf source integration process
			source=0
			for each_integ_point in xrange(number_integ_points):
				if run_biot_savart or run_permanent_magnets:
					Hxy=field_solution[elem_counter][each_integ_point]
					if Hxy[0,0]!=0 or Hxy[1,0]!=0 or Hxy[2,0]!=0:

						w_1_this_point=w_1[each_integ_point]

#u,v,p coordinates
						u=gauss_points[each_integ_point,0]
						v=gauss_points[each_integ_point,1]
						p=gauss_points[each_integ_point,2]
						w=w_1_this_point
# Jacobian
						jac=operations.get_jacobian(this_elem_type,this_element_nodes,nodes_coordenates,u,v,p)
						det_jac=np.linalg.det(jac)
						abs_det_jac=np.abs(det_jac)
#Integration
						source=source+wtri*abs_det_jac*matrix_aux.dot_product(w,Hxy)


			fmm_sparse[face_ID_1,0]=fmm_sparse[face_ID_1,0]+source

# Relutances integration process
			for local_face_counter_2 in xrange(number_local_faces):
				w_2=copy.deepcopy(w_real_all_points[local_face_counter_2])
				face_ID_2=faces_ID_Elem[local_face_counter_2]

				if faces_list[face_ID_2].elem_2==elem_counter:
					 for each in w_2:
						 each=matrix_aux.invert_w(each)

				wtot=0.0
				for each_integ_point in range(0,number_integ_points):
					 u=gauss_points[each_integ_point,0]
					 v=gauss_points[each_integ_point,1]
					 p=gauss_points[each_integ_point,2]

# Jacobian
					 jac=operations.get_jacobian(this_elem_type,this_element_nodes,nodes_coordenates,u,v,p)
					 det_jac=np.linalg.det(jac)
					 abs_det_jac=np.abs(det_jac)

# Reluctance
					 w_1_this_point=w_1[each_integ_point]
					 w_2_this_point=w_2[each_integ_point]
					 wtot=wtot+wtri*abs_det_jac*matrix_aux.dot_product(w_1_this_point,w_2_this_point)/mu_elem

				faces_rel_spare[face_ID_1,face_ID_2]+=wtot
	print_message("Integration process - Done")


#%% Connection between the physical line with the circuit node
	print_message("External faces")

	for counter,each_face in enumerate(faces_list):
		if each_face.elem_2==str_noflux_face:
			for each_face_con in elem_2D_ID:
				nodes_face_shared=all_elem_nodes_3D[each_face_con]
				phys_line=elem_tags[each_face_con][0]

#Coupling with external reluctances
				for each_coupling in coupling:
					if each_coupling.PhysLine==phys_line:

						bool_connect=True
						for each_node_this_face in each_face.nodes_list:
							if each_node_this_face not in nodes_face_shared:
								bool_connect=False

						if bool_connect:
# Redefine the face
							   new_face=Face(each_face.nodes_list,each_face.elem_1,each_coupling.Node+number_elements)
							   faces_list[counter]=new_face
							   each_coupling.Face_ID_List.append(counter)

#%% Insert the flux sources

	BC_nodes=list()
	if run_surface_integral:
		folder_name=os.path.join(folder_path,results_folder)
		full_path=os.path.join(folder_name,"flux_surface.txt")
		flux_data = np.genfromtxt(full_path,delimiter=' ',dtype='double')
		flux_source =flux_data[:,1]
		flux_source_elem_ID=flux_data[:,0]
		num_faces_surface_integral=len(flux_source_elem_ID)
#		external_node_surface_ID_counter=0

		for face_counter in xrange(num_faces_surface_integral):
			this_elem_face_ID=int(flux_source_elem_ID[face_counter])
			this_face_nodes_elem=set(all_elem_nodes_3D[this_elem_face_ID])

			for counter,each_face in enumerate(faces_list):
				this_face_nodes=set(each_face.nodes_list)
				if this_face_nodes_elem.issubset(this_face_nodes):
#					print this_elem_face_ID
#					external_node_surface_ID=len(coupling)+number_elements-1
#					BC_nodes.append(external_node_surface_ID)
#					external_node_surface_ID_counter+=1
					new_face=Face(each_face.nodes_list,each_face.elem_1,each_face.elem_2)
					faces_list[counter]=new_face
					source_flux_sparse[counter]=flux_source[face_counter]
					faces_rel_spare[counter,counter]=10000000000000000.0
					fmm_sparse[counter,0]=0.0
#					print each_face.elem_1
#					break

	BC_values=[0]*len(BC_nodes)


#%% Delete the faces without external connections
	faces_ID_deleted_list=list()
	faces_deleted_list=list()

#Delete from reluctances and fmm matrix
	counter=0
	for face_counter in  xrange(len(faces_list)):
		if faces_list[face_counter].elem_2==str_noflux_face:
			faces_ID_deleted_list.append(face_counter)

	faces_rel_spare=matrix_aux.delete_sparse_mask(faces_rel_spare,faces_ID_deleted_list,0)
	faces_rel_spare=matrix_aux.delete_sparse_mask(faces_rel_spare,faces_ID_deleted_list,1)
	fmm_sparse=matrix_aux.delete_sparse_mask(fmm_sparse,faces_ID_deleted_list,0)
	source_flux_sparse=matrix_aux.delete_sparse_mask(source_flux_sparse,faces_ID_deleted_list,0)

##Delete from faces_list
	counter=0
	for each in faces_ID_deleted_list:
		face_ID=each+counter
		this_face=faces_list[face_ID]
		faces_list.remove(this_face)
		faces_deleted_list.append(this_face)
		counter-=1

#%% Add the external circuit reluctances
	number_deleted=len(faces_deleted_list)
	for counter in xrange(num_non_meshed_rel):

#reluctance value
		material=external_reluctances[counter].Material
		mur=materials_lib[material].Permeability
		LS=external_reluctances[counter].LS
		mu_elem=vacuum.mu0*mur
		reluctance_value=LS/mu_elem

		this_position=num_meshed_rel-number_deleted+counter
		faces_rel_spare[this_position,this_position]=reluctance_value
		fmm_sparse[this_position]=external_reluctances[counter].fmm
		source_flux_sparse[this_position]=external_reluctances[counter].flux


	external_nodes_list=list()

	for each in external_reluctances:

#Get the list of external nodes
		if each.node_from not in external_nodes_list:
			external_nodes_list.append(each.node_from)
		if each.node_to not in external_nodes_list:
			external_nodes_list.append(each.node_to)

#create a new face in the faces_list
		new_face=Face([],each.node_from+number_elements,each.node_to+number_elements)
		faces_list.append(new_face)

#Get the list of external nodes
	for each in coupling:
		if each.Node not in external_nodes_list:
			external_nodes_list.append(each.Node )

	print_message("External faces - Done")


#%% Incidence matrix
	print_message("Incidence matrix")
	external_nodes=0

	if run_external_circuit:
		external_nodes+=len(external_nodes_list)
#	elif run_surface_integral:
#		external_nodes+=len(BC_nodes)
	else:
		external_nodes+=0

	number_faces_list=len(faces_list)
	total_nodes=number_elements+external_nodes

	rows_incidence_sparse=list()
	cols_incidence_sparse=list()
	data_incidence_sparse=list()

	for counter in xrange(number_faces_list):
		this_face=faces_list[counter]
		rows_incidence_sparse.append(this_face.elem_1)
		cols_incidence_sparse.append(counter)
		data_incidence_sparse.append(1.0)

		rows_incidence_sparse.append(this_face.elem_2)
		cols_incidence_sparse.append(counter)
		data_incidence_sparse.append(-1.0)

	incidence_matrix_sparse=csr_matrix((data_incidence_sparse, (rows_incidence_sparse, cols_incidence_sparse)), shape=(total_nodes,number_faces_list))

	Gmsh_file_name="teste.txt"
	path=os.path.join(results_path,Gmsh_file_name)
	Create_Vector_field(plot_test_coord,plot_test_field,path,"H test")
	print_message("Incidence matrix - Done")

	return faces_rel_spare,incidence_matrix_sparse,fmm_sparse,source_flux_sparse,faces_ID,results_path,faces_ID_deleted_list,faces_list,faces_deleted_list,BC_nodes,BC_values


