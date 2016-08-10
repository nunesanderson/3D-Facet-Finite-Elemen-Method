#===============================================================================
# Doctoral student: Anderson Santos Nunes
# University: UFSC - GRUCAD
#===============================================================================

from RNMFEM.structs import MeshData
import collections
import math
import os
import numpy as np
from scipy.sparse import csr_matrix
from lib.messages import print_message




def get_gauss_points(folder_name):
    points_IDs=folder_name+"\\results\\IDs_Gauss_Points.txt"
    points_IDs = np.genfromtxt(points_IDs,delimiter=' ',dtype='int')
    
    coordinates=folder_name+"\\results\\Coordinates_Gauss_Points.txt"
    coordinates = np.genfromtxt(coordinates,delimiter=' ',dtype='double')
    
    fields=folder_name+"\\results\\Hfield_Gauss_Points.txt"
    fields = np.genfromtxt(fields,delimiter=' ',dtype='double')

    return points_IDs,coordinates,fields

def get_mesh(file_name):
	'''
	Reads the mesh file\n
	file_name: mesh file name (with path)
	'''
	elem_types=list()
	elem_tags = list()
	elem_nodes = list()
	tri_elem_nodes=list()
	nodes_coordenates=list()
	is_2D=True
	
	data=get_data_from_file(file_name)
	nodes_data=get_file_block("$Nodes","$EndNodes",1,data,float)
	mesh_data_elements=get_file_block("$Elements","$EndElements",1,data,int)


#==============================================================================
# Nodes coordenates 
	for each_node_data in nodes_data:
		each_node_coordinates=list()
		for each_coordinate in range(0,3):
			each_node_coordinates.append(each_node_data[each_coordinate+1])
		nodes_coordenates.append(each_node_coordinates)

	
	for each_element_data in mesh_data_elements:

#==============================================================================
# Type
		this_element_type=each_element_data[1]
		elem_types.append(this_element_type)
		
#==============================================================================
#Tags
		num_tags=each_element_data[2]
		this_element_tags=list()
		for tag_counter in range(3, num_tags + 3):
			this_element_tags.append(each_element_data[tag_counter])
		elem_tags.append(this_element_tags)
#==============================================================================
# Nodes
		this_element_nodes=list()
		for nodes_counter in range(num_tags + 3, len(each_element_data)):
			this_element_nodes.append(each_element_data[nodes_counter]-1)
		
		if this_element_type==2 or this_element_tags==3:
			if is_2D:
#				this_element_nodes=sort_local_nodes(this_element_nodes, nodes_coordenates)
				pass
		if this_element_type==2:
			tri_elem_nodes.append(this_element_nodes)
		elem_nodes.append(this_element_nodes)
	
	return MeshData(ElemNodes=elem_nodes, TriElemNodes=tri_elem_nodes, NodesCoordenates=nodes_coordenates, ElemTags=elem_tags,ElemType=elem_types)

def get_Field_solution(path):
    '''
    Get the H solution data\n
    path: the project folder path
    retunrs:(H_field[element][Gauss point])
    '''
    points_IDs,coordinates,fields=get_gauss_points(path)
    
    list_fields=list()
    for each_elem in points_IDs:
        this_points=list()
        for each_point_ID in each_elem:
            this_points.append(fields[each_point_ID])
        list_fields.append(this_points)

    
    return list_fields

def get_file_block(start,end, stepFirst, data,data_type):
	'''
	Get a file block\n
	start: first line\n
	stepFirst: jump "stepFirst" first lines\n
	data_type: the type of the data returned (int, float...)\n
	ex:\n
	data=get_data_from_file(file_name)\n
	H_field=get_file_block("$HResults","$EndHResults",0,data,float)
	'''
	
	content = []
	lines = []
	for line in data:
		line = str(line).replace('\n', "")
		if not line.startswith('#'):
			line = line.split(" ")
			if line[0].startswith("["):
				list_regions=str(line[0])
				list_regions=list_regions.replace("[","")
				list_regions=list_regions.replace("]","")
				list_regions=list_regions.split(",")
				for each in list_regions:
					new_region=list()
					new_region.append(each)
					new_region.append(line[1])
					lines.append(new_region)
			else:
				lines.append(line)
	
	for line_counter in range(0, len(lines)):
		line = lines[line_counter]
		if str(start) in line[0]:
			line_counter += 1 + stepFirst
			continue_raw = True
			while continue_raw:
				line = lines[line_counter]
				if str(end) in line[0]:
					continue_raw = False
				if continue_raw:
					str_to_data_type=[]
					for each_str in line:
						try:
							str_to_data_type.append(data_type(each_str))
						except:
							str_to_data_type.append(each_str)
					content.append(str_to_data_type)
				line_counter += 1	
	return content

def get_data_from_file(file_name):
	
	data=""
	(root,ext)=os.path.splitext(file_name)

	if ext=='':
		file_name=file_name+'.txt'
	with open(file_name) as f:
		data = f.readlines()
	  
	return data

def get_distance_points (x1,y1,x2,y2):
	return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

def get_angle_points(x1,y1,x2,y2):
	angle= math.atan2(y2-y1, x2-x1)
	if angle<0:
		angle=2*math.pi+angle
	
	return angle

def sort_local_nodes(nodes,nodes_coordenates):
	'''Sort the nodes of a first order triangle'''
	point={}
	
#------------------------------------------------------------------------------ 
# Centroid coordinates
	
	x_bar=0
	y_bar=0
	for node_counter in range(0,len(nodes)):
		x_bar=nodes_coordenates[nodes[node_counter]][0]+x_bar
		y_bar=nodes_coordenates[nodes[node_counter]][1]+y_bar
	
	x_bar=x_bar/len(nodes)
	y_bar=y_bar/len(nodes)
	
	for each_node in nodes:
		x=nodes_coordenates[each_node][0]
		y=nodes_coordenates[each_node][1]
		point[get_angle_points(x_bar,y_bar,x,y)]=each_node
#------------------------------------------------------------------------------ 

	points_sorted=collections.OrderedDict(sorted(point.items()))
	point_return=[]
	for dir_point in points_sorted.values():
		point_return.append(dir_point)
	
	return point_return

def write_numeric_file_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def read_numeric_file_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])


def read_numeric_file_numpy(file_name):
	(path_file_local,path_name_local)=os.path.split(file_name)
	print_message('Reading file: '+str(path_name_local))
	return np.loadtxt(file_name)
	print_message('Reading file: '+str(path_name_local)+" - Done!")

def write_numeric_file_numpy(file_name, data_array):
	
	(path_file_local,path_name_local)=os.path.split(file_name)
	print_message('Writing file: '+str(path_name_local))
	
	if not os.path.exists(path_file_local):
		os.mkdir(path_file_local) 
	np.savetxt(file_name,data_array)
	print_message('Writing file: '+str(path_name_local)+" - Done!")



def write_numeric_data_file(file_name,list_array,key,does_clear_document):
	''' Creates the field file blocks\n
	file_name: The complete directory+file name\n
	list_array: list of points - list[array([ x1,y1,z1]),...]\n
	key: The block key - if key="", block structure is not created\n
	clear_document: bool (clear the previous document?)
	'''
	separator=" "
	list_print=list()
	for eachw in list_array:
		this_line=list()
		str_line=""
		if isinstance(eachw, list):
			this_line=eachw
		if isinstance(eachw,np.float64):
			this_line.append(eachw)
			
		elif isinstance(eachw,np.ndarray):
			for k in range(0,len(eachw)):
				this_line.append(eachw[k])
						
		len_each=len(this_line)
		for each_pos in range(0,len_each):
			if each_pos < len_each-1:
				write=str(this_line[each_pos]).replace(" ","")
				str_line=str_line+write+separator
			else:
				write=str(this_line[each_pos]).replace(" ","")
				str_line=str_line+ write
			
			
		list_print.append(str_line)
	write_file (file_name,list_print,key,does_clear_document)
	

def write_file (file_name,file_data,key,clear_document):
	'''
	Write a txt file\n
	file_name: The complete directory+file name\n
	file_data: A list containing the data to write\n
	key: The block key - if key="", block structure is not created\n
	clear_document: bool (clear the previous document?)
	'''
	(path_file_local,path_name_local)=os.path.split(file_name)
	print_message('Writing file: '+str(path_name_local))
	
	if not os.path.exists(path_file_local):
		os.mkdir(path_file_local) 
	
	if clear_document:
		file_open_mode="w"
	else:
		file_open_mode="a"
	
	
	try:
		f = open(file_name, file_open_mode)
		try:
			if key!='':
				f.writelines('$'+key+'\n') # Write a string to a file
			for each_line in file_data:
				each_line=str(each_line)
				each_line=each_line.replace("]","")
				each_line=each_line.replace("[","")
				f.write(str(each_line)+'\n')
			if key!='':
				f.write('$End'+key+"\n") # Write a string to a file
		finally:
			f.close()
			print_message('Writing file: '+str(path_name_local) +"- Done!")
	except IOError:
		
		pass
