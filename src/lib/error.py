class Errors:
	def physical_surface_not_defined(self,physical_surface_ID_region,physical_surface_ID_mesh):
		'''
		Returns the exception when the physical surface in the setup file is not used in the mesh file/n
		physical_surface_ID: The ID of the physical surface
		'''
		text_error="Physical surface error: The physical surface {0} (in the mesh file) or {1} (in the setup file) is not defined.".format(physical_surface_ID_region,physical_surface_ID_mesh)
		raise Exception(text_error)

	def dimensions_dont_match(self,dim_1,dim_2):
		'''
		Returns the exception when the dimensions of arrays dont match/n
		dim_1: dimension 1\n
		dim_2: dimension 2\n
		'''
		raise Exception("Array dimension error: dim 1:"+str(dim_1)+" dim 2:"+str(dim_2))
	def face_not_found(self,node_1,node_2):
		'''
		Returns the exception when the face is not found/n
		node_1:node 1
		node_2:node 2
		'''
		raise Exception("Face not found error: node1:"+str(node_1)+" - node2:"+str(node_2))
	def is_not_triangle(self,number_nodes):
		raise Exception("This element does not contais 3 nodes, it contais "+str(number_nodes)++" nodes")
		
	def element_type_not_implemented(self,elem_type):
		raise Exception("This element %s was not implemented."%(elem_type))
									
		