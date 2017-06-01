#===============================================================================
# Doctoral student: Anderson Santos Nunes
# University: UFSC - GRUCAD
#===============================================================================

from collections import namedtuple
from constants import GlobalVariables

MeshData = namedtuple("MeshData", "ElemNodes TriElemNodes NodesCoordenates ElemTags ElemType")
MaterialProp=namedtuple('MaterialProp', 'Permitivity Conductivity Permeability Hc')
RegionMaterial=namedtuple('RegionMaterial', 'RegionNumber MaterialName')
RegionExcitation=namedtuple('RegionExcitation', 'RegionNumber Value')
BC=namedtuple('BC', 'LineNumber Value')
ExternalReluctances=namedtuple('ExternalReluctances', 'node_from node_to LS Material fmm flux')
PreProcData=namedtuple('PreProcData', 'MeshData MaterialProp RegionMaterial RegionExcitation BC CoupNet ExternalReluctances ExternalMagneticField')
ReturnGetField=namedtuple('ReturnGetField', 'TpotXY TgradPotXY')
FieldAtPoint=namedtuple('HfieldAtPoint', 'Dist FieldX FieldY MagField')
GaussIntegPoints=namedtuple('GaussIntegPoints', 'u v w')
Branch=namedtuple('Branch','NodeFrom NodeTo Reluctance Fmm')
Reluctance=namedtuple('Reluctance','From To Material')
W_at_GaussPoint=namedtuple('W_at_GaussPoint','xy Wxy Hxy')
CouplingNetworks=namedtuple('CouplingNetworks','PhysLine Node Face_ID_List',)
ExternalMagneticField=namedtuple('ExternalMagneticField', 'RegionNumber Value')


global_variables=GlobalVariables()
str_noflux_face=global_variables.str_noflux_face

class Face(object):

	def __init__(self, nodes_list=None,elem_1=None,elem_2=None,flux=None):
		self.nodes_list=nodes_list
		self.elem_1=elem_1
		self.elem_2=elem_2
		self.flux=flux

	def add_to_list(self,nodes_list,Elem,face_list):
		face_counter=0
		face_ID=""
		add_face=True
		if face_list==None:
			face_list=list()

		for each_face in face_list:
			this_face=True
			for each_node in each_face.nodes_list:
				if each_node not in nodes_list:
					this_face=False
					break
			if this_face:
				if each_face.elem_1!= Elem and face_list[face_counter].elem_2==str_noflux_face:
					new_face=Face(nodes_list,each_face.elem_1,Elem)
					face_list[face_counter]=new_face
				add_face=False
				break
			face_counter+=1


		if add_face:
			new_face=Face(nodes_list,Elem,str_noflux_face)
			face_list.append(new_face)
			face_ID=len(face_list)-1
		else:
			face_ID=face_counter
		return face_ID

	def print_face(self):
		nodes_list_mesh=list()
		for each in self.nodes_list:
			nodes_list_mesh.append(each+1)
		print "Nodes list: %s - \tElement 1: %s - \tElement 2: %s"%(nodes_list_mesh,self.elem_1,self.elem_2)

class File_names():

    def get_Gauss_points_ID_file_name(self):
        return 'Gauss_Points_IDs.txt'

    def get_Gauss_points_coordinates_file_name(self):
        return 'Gauss_Points_Coordinates.txt'

    def get_Gauss_points_H_field_file_name(self):
        return 'Gauss_Points_H_field.txt'

    def get_B_Gmsh_line_file_name(self):
        return 'line_B_field_Gmsh.txt'

    def get_B_Gmsh_surface_file_name(self):
        return 'Surface_B_field_Gmsh.txt'

    def flux_results_file_name(self):
        return 'flux_results.txt'

    def get_H_results_file_name(self):
        return 'Gauss_Points_H_field.txt'

    def get_Gauss_Points_ID_file_name(self):
        return 'Gauss_Points_IDs.txt'

    def get_Gauss_Points_Phys_region_file_name(self):
        return 'Gauss_Points_Phys_region.txt'

    def get_H_Gmsh_pos_proc_file_name(self):
        return 'Gauss_Points_H_field__Gmsh.txt'

    def get_H_Gmsh_pos_proc_file_name_opt(self):
        return 'Gauss_Points_H_field__Gmsh.txt.opt'

    def get_Gauss_points_list_file_name(self):
        return 'Gauss_Points_Coordinates.txt'

    def get_Gmsh_facet_functions_file_name(self):
        return 'facet_functions_Gmsh.txt'

    def get_Gmsh_B_field_file_name(self):
        return 'B_fields_Gmsh.txt'

    def faces_from_to_file_name(self):
        return 'faces_from_to.txt'

    def get_faces_ID_file_name(self):
        return 'faces_ID.txt'

    def get_results_folder_name(self):
        return 'results'