
#==============================================================================
# Import modules folloping official guidelines:
#==============================================================================
import numpy as np
import math
from structs import GaussIntegPoints
from lib.error import Errors
error=Errors()

#==============================================================================
# Mathematical operations
#==============================================================================
class Operations:

	def get_area_triangle(self,elem_ID,elem_nodes,nodes_coordenates):
		'''
		returns the area of the element\n
		elem_ID: ID of the element in the elem_nodes list\n
		elem_nodes: list pith the element nodes\n
		nodes_coordenates: list of the cordinates of the nodes'''
		error=Errors()
		coord_jac=self.get_coord_j(elem_ID,elem_nodes,nodes_coordenates)
		lines,cols=np.shape(coord_jac)
		if lines!=3:
			error.is_not_triangle(lines)

		StriMat=np.zeros((3,3))
		for i in range(0,lines):
			StriMat[i,0]=coord_jac[i,0]
			StriMat[i,1]=coord_jac[i,1]
			StriMat[i,2]=1.0
		return 0.5*np.abs(np.linalg.det(StriMat))

	def get_area_triangle_nep(self,nodes_list,nodes_coordenates):
		'''
		returns the area of the element\n
		elem_ID: ID of the element in the elem_nodes list\n
		elem_nodes: list pith the element nodes\n
		nodes_coordenates: list of the cordinates of the nodes'''
		coord_jac=self.get_coord_j_nep(nodes_list,nodes_coordenates)
		lines,cols=np.shape(coord_jac)
		if lines!=3:
			error.is_not_triangle(lines)

		StriMat=np.zeros((3,3))
		for i in range(0,lines):
			StriMat[i,0]=coord_jac[i,0]
			StriMat[i,1]=coord_jac[i,1]
			StriMat[i,2]=1.0
		return 0.5*np.abs(np.linalg.det(StriMat))

	def  get_area_element(self,elem_type,nodes_list,nodes_coordenates):
		'''
		elem_type = 2 : 3-node triangle\n
		elem_type = 3 : 4-node quadrangle\n
		elem_type = 4 : 4-node tetrahedron\n
		nodes_list: list pith the nodes of the element
		nodes_coordenates: coordinates of all the nodels
		'''
		elem_area=0
		if elem_type==2:
		   elem_area= self.get_area_triangle_nep(nodes_list,nodes_coordenates)

		if elem_type==3:
			list_nodes=list()
			list_nodes.append(nodes_list[0])
			list_nodes.append(nodes_list[1])
			list_nodes.append(nodes_list[2])
			elem_area= self.get_area_triangle_nep(list_nodes,nodes_coordenates)
			list_nodes=list()
			list_nodes.append(nodes_list[0])
			list_nodes.append(nodes_list[2])
			list_nodes.append(nodes_list[3])
			elem_area= self.get_area_triangle_nep(list_nodes,nodes_coordenates)+elem_area
		return elem_area

	def get_jacobian(self, elem_type, nodes_list,nodes_coordenates,u=0,v=0,p=0):

		shape_functions=ShapeFuncions()
		gradN=shape_functions.get_grad_shape_function(elem_type,u,v,p)
		coord_jac=self.get_coord_j_nep(nodes_list,nodes_coordenates)

		return np.dot(gradN,coord_jac)

	def get_jacobian_triangle(self,elem_ID,elem_nodes,nodes_coordenates):
		'''
		returns the Jacobian of the element\n
		elem_ID: ID of the element in the elem_nodes list\n
		elem_nodes: list pith the element nodes
		nodes_coordenates: list of the cordinates of the nodes
		'''
		shape_functions=ShapeFuncions()
		gradN_tri=shape_functions.__grad_nod_tri_1order()

		coord_jac=self.get_coord_j(elem_ID,elem_nodes,nodes_coordenates)
#		coord_jac=coord_jac.T
		return np.dot(gradN_tri,coord_jac)

	def get_jacobian_reference_element_tri(self):
		shape_functions=ShapeFuncions()
		gradN_tri=shape_functions.grad_nod_tri_1order()
		coord_Jac=np.array([[1.0,0.0],[0.0,1.0],[0.0,0.0]])
		return np.dot(gradN_tri,coord_Jac)

	def convert_global_to_local_quad(self,x,y,nodes_list,nodes_coordenates):
		'''
		Convert from global to local coordinates - Quadrilateral elements\n
		x,y: global coordinates\n
		elem_nodes: list pith the element nodes\n
		nodes_coordenates: list of the cordinates of the nodes
		'''
		stop_criteria=1/100000.0	# precision stop criteria
		u=0.5					   # local coordinates guess
		v=0.5					   # local coordinates guess
		shape_functions=ShapeFuncions()
		r_x=1
		r_y=1
		coord_jac=self.get_coord_j_nep(nodes_list,nodes_coordenates)
		does_continue=True
		counter=0
		while does_continue:
			N=shape_functions.nod_quad_1order(u, v)
			XY_act=np.dot(N,coord_jac)
			r_x=XY_act[0,0]/x
			r_y=XY_act[0,1]/y

			if np.abs((np.abs(r_x)-1))<stop_criteria and np.abs((np.abs(r_y)-1))<stop_criteria :
				does_continue=False
			u=u/r_x
			v=v/r_y
		counter+=1

		return  np.array([[u,v]])


	def get_coord_j_nep(self,elem_nodes_list,nodes_coordenates):
		'''
		Get the matrix pith the coordinates of the nodes\n
		elem_nodes_list: list pith nodes of this specific element\n
		nodes_coordenates: list pith the coordinates of the mesh nodes\n
		ex:\n
		x1 y1\n
		x2 y2\n
		x3 y3\n
		'''
		num_nodes=len(elem_nodes_list)
		coord_jac=np.zeros((num_nodes,3))

		for each_node in range(0,num_nodes):
			coord_jac[each_node,0]=nodes_coordenates[elem_nodes_list[each_node]][0]
			coord_jac[each_node,1]=nodes_coordenates[elem_nodes_list[each_node]][1]
			coord_jac[each_node,2]=nodes_coordenates[elem_nodes_list[each_node]][2]
		return coord_jac

	def convert_local_real_Piola(self,elem_type,u,v,p,nodes_list,nodes_coordenates):
		'''Convert the cordinate  based on local element to real element\n
		element_ID:the index of the element in the elem_nodes list\n
		node: node index\n
		elem_type: 2: triangular 3: quadrangular\n
		u,v: cordinates based on reference element\n
		elem_nodes: list pith all nodes, for each element\n
		nodes_coordenates: list pith the coordinates of the mesh nodes'''

		uvp=np.array([[u],[v],[p]])
		jac=self.get_jacobian(elem_type,nodes_list,nodes_coordenates,u=u,v=v,p=p)

		jac_T=jac.T
		detJacT=np.linalg.det(jac_T)
		detJacT=abs(detJacT)
		xyz=(1.0/detJacT)*np.dot(jac_T,uvp)
		return xyz

	def convert_vector_local_real(self,elem_type,u,v,nodes_list,nodes_coordenates):
		'''
		Convert the cordinate  based on local element to real element\n
		element_ID:the index of the element in the elem_nodes list\n
		node: node index\n
		elem_type: 2: triangular 3: quadrangular\n
		u,v: cordinates based on reference element\n
		elem_nodes: list pith all nodes, for each element\n
		nodes_coordenates: list pith the coordinates of the mesh nodes
		'''

		shape_functions=ShapeFuncions()
		coord_jac=self.get_coord_j_nep(nodes_list,nodes_coordenates)
		u_in=0.0
		v_in=0.0
		N=shape_functions.get_node_shape_function(elem_type,u_in,v_in)
		XY_in=np.dot(N,coord_jac)

		N=shape_functions.get_node_shape_function(elem_type,u,v)
		XY=np.dot(N,coord_jac)
		XY_final=XY-XY_in

		return XY_final.T

	def convert_local_real(self,elem_type,u,v,p,nodes_list,nodes_coordenates):
		'''
		Convert the cordinate  based on local element to real element\n
		element_ID:the index of the element in the elem_nodes list\n
		node: node index\n
		elem_type: 2: triangular 3: quadrangular\n
		u,v: cordinates based on reference element\n
		elem_nodes: list pith all nodes, for each element\n
		nodes_coordenates: list pith the coordinates of the mesh nodes
		'''

		shape_functions=ShapeFuncions()
		coord_jac=self.get_coord_j_nep(nodes_list,nodes_coordenates)
		N=shape_functions.get_node_shape_function(elem_type,u,v,p)
		XYZ=np.dot(N,coord_jac)
		return np.transpose(XYZ)


	def convert_real_to_local(self,element_ID,elem_type,x,y,z,elem_nodes,nodes_coordenates):
		'''Convert the cordinate  based on local element to real element\n
		element_ID:the index of the element in the elem_nodes list\n
		node: node index\n
		elem_type: type of the element based on Gmsh documentation\n
		x,y: cordinates based on real element\n
		elem_nodes: list with all nodes, for each element\n
		nodes_coordenates: list with the coordinates of the mesh nodes'''
		xyz=np.array([[x],[y],[z]])
		get_jac=Operations()
		jac=get_jac.get_jacobian(elem_type,elem_nodes,nodes_coordenates)
		coord_jac=self.get_coord_j_nep(elem_nodes,nodes_coordenates)
		coord_jac_1=np.zeros((3,1))
		elem=0

		coord_jac_1[0,0]=coord_jac[elem,0]
		coord_jac_1[1,0]=coord_jac[elem,1]
		coord_jac_1[2,0]=coord_jac[elem,2]


		UV=np.dot(np.linalg.inv(jac.T),(xyz-coord_jac_1))

		return UV


#==============================================================================
# Gauss integration points
#==============================================================================
class GaussPoints:

	def get_gauss_points(self,elem_type):
		'''
		elem_type = 2 : 3-nodes triangle\n
		elem_type = 3 : 4-nodes quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes tetrahedral\n
		'''
		if elem_type==2:
			gauss_points=self.__integpoints_triangle_inside()
		elif elem_type==3:
			gauss_points=self.__integpoints_quadrangle()
		elif elem_type==4:
			gauss_points=self.__integpoints_tetrahedral_4points()
		elif elem_type==5:
			gauss_points=self.__integpoints_hexahedral_inside()
		else:
			error.element_type_not_implemented(elem_type)
		return gauss_points

	def get_local_element_center_point(self, elem_type):
		'''
		Returns the elemenent center
		'''
		if elem_type==2:
			uv=np.array([[1.0/3.0,1.0/3.0]])
		elif elem_type==3:
			uv=np.array([[0.0,0.0]])
		elif elem_type==4:
			uv=np.array([[1.0/4.0,1.0/4.0,1.0/4.0]])

		elif elem_type==5:
			uv=np.array([[0.0,0.0,0.0]])

		else:
			error.element_type_not_implemented(elem_type)
		return uv

	def get_integration_weight(self,elem_type):
		'''
		elem_type = 2 : 3-node triangle\n
		elem_type = 3 : 4-node quadrangle\n
		elem_type = 4 : 4-node tetrahedron\n
		'''

		integ_wei=0
		if elem_type==2:
			integ_wei=self.__integration_weight_triangle()
		elif elem_type==3:
			integ_wei=self.__integration_weight_quadrangle()
		elif elem_type==4:
			integ_wei=self.__integration_weight_tetrahedral_4points()
		elif elem_type==5:
			integ_wei=self.__integration_weight_hexahedral()
		else:
			error.element_type_not_implemented(elem_type)
		return integ_wei


	def __integpoints_triangle_inside (self):
		'''
		First order triangular element \n
		Gauss integration points - points inside\n
		Nathan pg 311
		'''

		uv=np.array([[1.0/6.0,1.0/6.0],
					 [2.0/3.0,1.0/6.0],
					 [1.0/6.0,2.0/3.0]])
		return uv
	def __integpoints_triangle_mid(self):
		'''
		First order triangular element \n
		Gauss integration points - points at mid
		Nathan pg 311
		'''
		uv=np.array([[1.0/2.0,1.0/2.0],
					 [0.0/3.0,1.0/2.0],
					 [1.0/2.0,0.0/3.0]])
		return uv
	def __integpoints_quadrangle(self):
		'''
		First order quadrilateral element - Gauss integration points - points inside\n
		Referece: Nathan Ida, pg 317
		'''
		r_3=1.0/math.sqrt(3.0)

		uv=np.array([[r_3,r_3],
					 [-r_3,r_3],
					 [r_3,-r_3],
					 [-r_3,-r_3]])
		return uv

	def __integpoints_hexahedral_inside (self):
		'''
		First order hexahedral element - Gauss integration points - 4 points\n
		Referece: Nathan Ida, pg 321\n
		Retunrs uvp
		'''

		r_3=1.0/math.sqrt(3.0)

		uvp=np.array([
				[r_3,r_3,r_3],
				[-r_3,r_3,r_3],
				[r_3,-r_3,r_3],
				[-r_3,-r_3,r_3],
				[r_3,r_3,-r_3],
				[-r_3,r_3,-r_3],
				[r_3,-r_3,-r_3],
				[-r_3,-r_3,-r_3]])

		return uvp

	def __integpoints_tetrahedral_4points(self):
		'''
		First order tetrahedral element - Gauss integration points - 4 points\n
		Referece: Nathan Ida, pg 320, table 8.11\n
		Retunrs uvp
		'''
		a=0.1381966
		b=0.5854102

		uvp=np.array([
			[a,a,a],
			[a,a,b],
			[a,b,a],
			[b,a,a]])

		return uvp

	def __integpoints_tetrahedral_1point(self):
		'''
		First order tetrahedral element - Gauss integration points - 1 point\n
		Referece: Nathan Ida, pg 320, table 8.11\n
		Retunrs uvp
		'''
		a=1.0/4.0

		uvp=np.array([[a,a,a]])

		return uvp

	def __integration_weight_tetrahedral_4points(self):
		'''
		Intgegration peight for tetrahedral (4 points)\n
		Referece: Nathan Ida, pg 317
		'''
		return 1.0/24.0

	def __integration_weight_tetrahedral_1point(self):
		'''
		Intgegration peight for tetrahedral (1 point)\n
		Referece: Nathan Ida, pg 320
		'''
		return 1.0/6.0

	def __integration_weight_hexahedral(self):
		'''
		Intgegration peight for hexahedral\n
		Referece: Nathan Ida, pg 321
		'''
		return 1.0
	def __integration_weight_quadrangle(self):
		'''
		Intgegration peight for quadrangle\n
		Referece: Nathan Ida, pg 317
		'''
		return 1.0

	def __integration_weight_triangle(self):
		'''
		Intgegration peight for quadrilateral \n
		Referece: Nathan Ida, pg 317
		'''
		return 1.0/6.0

#==============================================================================
# Shape functions class
#==============================================================================
class ShapeFuncions:

	def get_reference_element_area(self,elem_type):
		'''
		elem_type = 2 : 3-nodes triangle\n
		elem_type = 3 : 4-nodes quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		return volume\n
		elem_type = 5 : 8-nodes haxahedral\n
		return volume\n

		'''
		if elem_type==2:
			area=0.5
		elif elem_type==3:
			area=4.0
		else:
			error.element_type_not_implemented(elem_type)
		return area

	def get_node_shape_function(self,elem_type,u,v,p=None):
		'''
		elem_type = 2 : 3-nodes triangle\n
		elem_type = 3 : 4-nodes quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes haxahedral\n
		'''
		if elem_type==2:
			shape_function=self.__nod_tri_1order(u,v)
		elif elem_type==3:
			shape_function=self.__nod_quad_1order(u,v)
		elif elem_type==4:
			shape_function=self.__node_tetrahedral_1order(u,v,p)
		elif elem_type==5:
			shape_function=self.__node_hexahedral_1order(u,v,p)
		elif elem_type==7:
			shape_function=self.__node_pyramidal_1order(u,v,p)
		else:
			error.element_type_not_implemented(elem_type)

		return shape_function

	def get_grad_shape_function(self,elem_type,u=None,v=None,p=None):
		'''
		elem_type = 2 : 3-node triangle\n
		elem_type = 3 : 4-node quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes haxahedral\n
		'''
		if elem_type==2:
			gradN=self.__grad_nod_tri_1order()
		elif elem_type==3:
			gradN=self.__grad_nod_quad_1order(u,v)
		elif elem_type==4:
			gradN=self.__grad_node_tetrahedral_1order(u,v,p)
		elif elem_type==5:
			gradN=self.__grad_node_hexahedral_1order(u,v,p)
		else:
			error.element_type_not_implemented(elem_type)
		return gradN

	def get_facet_shape_function(self,elem_type,u,v,p=None):
		'''
		elem_type = 2 : 3-node triangle\n
		elem_type = 3 : 4-node quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes haxahedral\n
		elem_type = 7 : 5-nodes pyramidal\n
		'''
		if elem_type==2:
			shape_function=self.__face_tri_1order(u,v)
		elif elem_type==3:
			shape_function=self.__face_quad_1order(u,v)
		elif elem_type==4:
			shape_function=self.__face_tetrahedral_1order(u,v,p)
		elif elem_type==5:
			shape_function=self.__face_hexahedral_1order(u,v,p)
		elif elem_type==7:
			shape_function=self.__face_pyramidal_1order(u,v,p)
		else:
			error.element_type_not_implemented(elem_type)
		return shape_function

	def get_number_faces(self,elem_type):
		'''
		elem_type = 2 : 3-node triangle\n
		elem_type = 3 : 4-node quadrangle\n
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes haxahedral\n
		elem_type = 7 : 5-nodes pyramidal\n
		'''
		number_faces=0
		if elem_type==2:
			number_faces=3
		if elem_type==3:
			number_faces=4
		elif elem_type==4:
			number_faces=4
		elif elem_type==5:
			number_faces=6
		elif elem_type==7:
			number_faces=5
		else:
			error.element_type_not_implemented(elem_type)

		return number_faces

	def get_nodes_ID_2_face(self,elem_type):
		'''
		elem_type = 4 : 4-nodes tetrahedral\n
		elem_type = 5 : 8-nodes haxahedral\n'''

		if elem_type==4:
			node_ID=self.__faces_nodes_tetrahedral_1order()
		elif elem_type==5:
			node_ID=self.__faces_nodes_hexahedral_1order()
		elif elem_type==7:
			node_ID=self.__faces_nodes_pyramidal_1order
		else:
			error.element_type_not_implemented(elem_type)
		return node_ID


#==============================================================================
# Triangular elements
	def __tri_element_local_coordinates(self):
		'''
		Ref:\n
		Ferrouillat 2012, appendix C, page XI\n
		returns:\n
		[u1 u2 u3\n
		v1 v2 v3]
		'''
		return np.array([[1.0,0.0,0.0],[0.0,1.0,0.0]])

	def __nod_tri_1order(self, u,v):
		'''
		ref:\n
		Ferrouillat 2012, appendix B, page VI\n
		returns:\n
		[N1 N2 N3]
		'''
		N0=u
		N1=v
		N2=1.0-u-v

		return np.hstack((N0, N1, N2))

	def __grad_nod_tri_1order(self):
		'''
		Ref:\n
		Ferrouillat 2012, appendix B, page VI\n
		returns:\n
		[dN1/du dN2/du dN3/du\n
		dN1/dv dN2/dv dN3/dv]
		'''
		return np.array([[1.0,0.0,-1.0],
				      [0.0,1.0,-1.0]])

	def __edge_tri_1order(self, u,v):
		'''
		 Ref:\n
		Ferrouillat 2012, appendix B, page VII\n
		returns:\n
		[N1\n
		N2\n
		N3]
		'''
		unit_u=np.matrix([1,0])
		unit_v=np.matrix([0,1])

		N1=-v*unit_u+u*unit_v
		N2=-v*unit_u+(-1.0+u)*unit_v
		N3=(1.0-v)*unit_u+u*unit_v

		return np.vstack((N1, N2, N3))

	def __face_tri_1order(self,u,v):
		'''
		 Ref:\n
		Ferrouillat 2012, appendix C, page XI\n
		returns:\n
		[N1\n
		N2\n
		N3]
		'''
		unit_u=np.matrix([1.0,0.0])
		unit_v=np.matrix([0.0,1.0])

		N1=u*unit_u+v*unit_v		  #Face 0-1
		N2=(-1.0+u)*unit_u+v*unit_v   #Face 1-2
		N3=u*unit_u+(-1.0+v)*unit_v   #Face 2-0

		return np.vstack((N1, N2, N3))
#==============================================================================
# Quadrangular elements

	def __nod_quad_1order(self, u,v):
		'''
		ref:\n
		Bastos 2003, pg 189
		# x-----------x\n
		# | (4)   (3) |\n
		# |		   |\n
		# |		   |\n
		# |		   |\n
		# | (1)   (2) |\n
		# x-----------x\n
		returns:\n
		[N1 N2 N3 N4]

		'''
		N1=(1.0-u)*(1.0-v)*1.0/4.0
		N2=(1.0+u)*(1.0-v)*1.0/4.0
		N3=(1.0+u)*(1.0+v)*1.0/4.0
		N4=(1.0-u)*(1.0+v)*1.0/4.0
		return np.hstack((N3, N4, N1,N2))

	def __grad_nod_quad_1order(self,u,v):
		'''
		ref:\n
		Bastos 2003, pg 189
		First order quad element
		returns:\n
		[dN1/du dN2/du dN3/du dN4/du\n
		dN1/dv dN2/dv dN3/dv dN4/dv]
		'''
		gradN_1=np.array([[(-1.0+v)/4.0],[(-1.0+u)/4.0]])
		gradN_2=np.array([[(1.0-v)/4.0],[(-1.0-u)/4.0]])
		gradN_3=np.array([[(1.0+v)/4.0],[(1.0+u)/4.0]])
		gradN_4= np.array([[(-1.0-v)/4.0],[(1.0-u)/4.0]])

		return np.hstack((gradN_3, gradN_4, gradN_1, gradN_2))

	def __face_quad_1order(self,u,v):
		'''
		First order quadrangular element interpolation function (facet element)
		Ref:\n
		Ferrouillat 2012, appendix B, page XI\n
		returns:\n
		[N1\n
		N2\n
		N3\n
		N4]
		'''
		unit_u=np.matrix([1.0,0.0,0.0])
		unit_v=np.matrix([0.0,1.0,0.0])
		N1=0.25*(0.0*unit_u+(1.0+v)*unit_v)	#Face 0-1
		N2=0.25*((-1.0+u)*unit_u+0.0*unit_v)   #Face 1-2
		N3=0.25*(0.0*unit_u+(-1.0+v)*unit_v)   #Face 2-3
		N4=0.25*((1.0+u)*unit_u+0.0*unit_v)	#Face 3-0

		return np.vstack((N1, N2, N3, N4))
#==============================================================================
# Tetrahedral elements
	def __node_tetrahedral_1order(self,u,v,p):
			'''
			First order tetrahedral element interpolation function (node element)
			Ref:\n
			Ida&Bastos, pg 319, table 8.9
			returns:\n
			[N1 N2 N3 N4]
			'''
			N1=1.0-u-v-p
			N2=u
			N3=v
			N4=p

#			return np.hstack((N1, N2, N3,N4))
   			return np.hstack((N1, N3, N4,N2))

	def __grad_node_tetrahedral_1order(self,u,v,p):
		'''
		ref:\n
		Ida&Bastos, pg 319, table 8.9
		First order tetrahedral element\n
		returns:\n
		[dN1/du dN2/du dN3/du dN4/du\n
		dN1/dv dN2/dv dN3/dv dN4/dv
		dN1/dp dN2/dp dN3/dp dN4/dp\n]
		'''
		gradN_1=np.array([[-1.0],[-1.0],[-1.0]])
		gradN_2=np.array([[1.0],[0.0],[0.0]])
		gradN_3=np.array([[0.0],[1.0],[0.0]])
		gradN_4=np.array([[0.0],[0.0],[1.0]])

		return np.hstack((gradN_1, gradN_3, gradN_4, gradN_2))

	def __face_tetrahedral_1order(self,u,v,p):
		'''
		First order tetrahedral element interpolation function (facet element)
		Ref:\n
		Ferrouillat 2012, appendix B, page XI\n
		returns:\n
		[N1\n
		N2\n
		N3\n
		N4]
		'''
		unit_u=np.matrix([1.0,0.0,0.0])
		unit_v=np.matrix([0.0,1.0,0.0])
		unit_p=np.matrix([0.0,0.0,1.0])
		k=2.0

		N1=k*((u*unit_u)+(v*unit_v)+(-1.0+p)*unit_p)     #Face 1-3-2
		N2=k*((u*unit_u)+(v*unit_v)+(p*unit_p))	       #Face 2-3-4
		N3=k*((-1.0+u)*unit_u+(v*unit_v)+(p*unit_p))	 #Face 3-1-4
		N4=k*((u*unit_u)+(-1.0+v)*unit_v+p*unit_p) 	 #Face 4-1-2

		return np.vstack((N1, N2, N3, N4))

	def __faces_nodes_tetrahedral_1order(self):
		'''
		Nodes ID that form each face\n
		Puline's faces numbering\n
		Returns:\n
		face0[[node 0,node 1,node 2..]\n
		face1 [node 0,node 1,node 2..]]\n
		'''
#  		return np.array([[0,2,1],
#					[1,2,3],
#					[2,0,3],
#					[3,0,1]])
  		return np.array([[0,1,3],
					[3,1,2],
					[1,0,2],
					[2,0,3]])

#==============================================================================
# hexahedral elements
	def __node_hexahedral_1order(self,u,v,p):
		'''
		First order hexahedral element interpolation function (node element)
		Ref:\n
		Ida&Bastos, pg 321, table 8.12
		returns:\n
		[N1 N2 N3 N4 N5 N6 N7 N8]
		'''
		a1=1.0+u
		a2=1.0-u
		b1=1.0+v
		b2=1.0-v
		c1=1.0+p
		c2=1.0-p

		N1=a2*b2*c2/8.0
		N2=a1*b2*c2/8.0
		N3=a1*b1*c2/8.0
		N4=a2*b1*c2/8.0
		N5=a2*b2*c1/8.0
		N6=a1*b2*c1/8.0
		N7=a1*b1*c1/8.0
		N8=a2*b1*c1/8.0
		return np.hstack((N1, N2, N3,N4,N5,N6,N7,N8))

	def __grad_node_hexahedral_1order(self,u,v,p):
		'''
		ref:\n
		Ida&Bastos, pg 319, table 8.9
		First order tetrahedral element\n
		returns:\n
		[dN1/du dN2/du dN3/du dN4/du..dN8/du\n
		dN1/dv dN2/dv dN3/dv dN4/dv...dN8/dv\n
		dN1/dp dN2/dp dN3/dp dN4/dp...dN8/dp]\n
		'''
		a1=1.0+u
		a2=1.0-u
		b1=1.0+v
		b2=1.0-v
		c1=1.0+p
		c2=1.0-p

		k=1.0/8.0

		gradN_1=k*np.array([[-b2*c2],[-a2*c2],[-a2*b2]])
		gradN_2=k*np.array([[b2*c2],[-a1*c2],[-a1*b2]])
		gradN_3=k*np.array([[b1*c2],[a1*c2],[-a1*b1]])
		gradN_4=k*np.array([[-b1*c2],[a2*c2],[-a2*b1]])
		gradN_5=k*np.array([[-b2*c1],[-a2*c1],[a2*b2]])
		gradN_6=k*np.array([[b2*c1],[-a1*c1],[a1*b2]])
		gradN_7=k*np.array([[b1*c1],[a1*c1],[a1*b1]])
		gradN_8=k*np.array([[-b1*c1],[a2*c1],[a2*b1]])

		return np.hstack((gradN_1, gradN_2, gradN_3, gradN_4, gradN_5, gradN_6, gradN_7, gradN_8))

	def __face_hexahedral_1order(self,u,v,p):
		'''
		First order tetrahedral element interpolation function (facet element)
		Ref:\n
		Ferrouillat 2012, appendix B, page XII\n
		returns:\n
		[N1\n
		N2\n
		N3\n
		N4\n
		.\n
		.\n
		.\n
		N6]
		'''
		unit_u=np.matrix([1.0,0.0,0.0])
		unit_v=np.matrix([0.0,1.0,0.0])
		unit_p=np.matrix([0.0,0.0,1.0])
		k=1.0/8.0

		N1=k*(1.0+p)*unit_p     #Face1-2-3-4
		N2=k*(-1.0+p)*unit_p     #Face 5-8-7-6
		N3=k*(1.0+v)*unit_v     #Face 1-5-6-2
		N4=k*(-1.0+u)*unit_u     #Face 2-6-7-3
		N5=k*(-1.0+v)*unit_v     #Face 3-7-8-4
		N6=k*(1.0+u)*unit_u    #Face

#		return np.vstack((N6, N4, N3, N5,N1,N2))
		return np.vstack((N1, N2, N3, N4,N5,N6))

	def __faces_nodes_hexahedral_1order(self):
		'''
		Nodes ID that form each face\n
		Ref: Paline faces numbering\n
		Returns:\n
		face0[[node 0,node 1,node 2..]\n
		face1 [node 0,node 1,node 2..]]\n
		'''
		return np.array([[0,1,2,3],
					[4,7,6,5],
					[0,4,5,1],
					[1,5,6,2],
					[2,6,7,3],
					[0,3,7,4]])

#==============================================================================
# pyramidal elements
	def __node_pyramidal_1order(self,u,v,p):
		'''
		First order pyramidal element interpolation function (node element)
		Ref:\n
		Zgainski - 1996 - A nep family of finite elements the pyramidal elements
		returns:\n
		[N1 N2 N3 N4 N5]
		'''
		if p==1.0:
			u=0.0
			v=0.0

		r=(u*v*p)/(1.0-p)

		N1=0.25 * ((1.-u) * (1.-v) - p + r)
		N2=0.25 * ((1.+u) * (1.-v) - p - r)
		N3=0.25 * ((1.+u) * (1.+v) - p + r)
		N4=0.25 * ((1.-u) * (1.+v) - p - r)
		N5=p

		return np.hstack((N1, N2, N3,N4,N5))

	def __SQU(a):
		return a**2

	def __grad_node_pyramidal_1order(self,u,v,p):
		'''
		ref:\n
		Ida&Bastos, pg 319, table 8.9
		First order tetrahedral element\n
		returns:\n
		[dN1/du dN2/du dN3/du dN4/du..dN8/du\n
		dN1/dv dN2/dv dN3/dv dN4/dv...dN8/dv\n
		dN1/dp dN2/dp dN3/dp dN4/dp...dN8/dp]\n
		'''
		if p==1.0:
			u=0.0
			v=0.0

		gradN_1=k*np.array([[( v/(1 - p) - 1)],[( u/(1 - p) - 1)],[( u*v/__SQU(1 - p) - 1)]])
		gradN_2=k*np.array([[(-v/(1 - p) + 1)],[(-u/(1 - p) - 1)],[(-u*v/__SQU(1 - p) - 1)]])
		gradN_3=k*np.array([[( v/(1 - p) + 1)],[( u/(1 - p) + 1)],[( u*v/__SQU(1 - p) - 1)]])
		gradN_4=k*np.array([[(-v/(1 - p) - 1)],[(-u/(1 - p) + 1)],[(-u*v/__SQU(1 - p) - 1)]])
		gradN_5=k*np.array([[0.0],[0.0],[1.0]])

		return np.hstack((gradN_1, gradN_2, gradN_3, gradN_4, gradN_5))

	def __face_pyramidal_1order(self,u,v,p):
		'''
		First order tetrahedral element interpolation function (facet element)
		Ref:\n
		Ferrouillat 2012, appendi x B, page XII\n
		returns:\n
		[N1\n
		N2\n
		N3\n
		N4\n
		.\n
		.\n
		.\n
		N6]
		'''
		unit_u=np.matrix([1.0,0.0,0.0])
		unit_v=np.matrix([0.0,1.0,0.0])
		unit_p=np.matrix([0.0,0.0,1.0])
		if p==1.0:
			u=0.0
			v=0.0
		N1=(-0.25 * u * p / (1. - p))*unit_u+(0.25 * (-2. + v + v / (1. - p)))*unit_v+( 0.25 * p)*unit_p
		N2=( 0.25 * u)*unit_u+(0.25 * v)*unit_v+( -0.25 * (1. - p))*unit_p
		N3=(0.25 * (-2. + u + u / (1. - p)))*unit_u+(-0.25 * v * p / (1. - p))*unit_v+(0.25 * p)*unit_p
		N4=(0.25 * ( 2. + u + u / (1. - p)))*unit_u+( -0.25 * v * p / (1. - p))*unit_v+(0.25 * p )*unit_p
		N5=(-0.25 * u * p / (1. - p))*unit_u+(0.25 * ( 2. + v + v / (1. - p)))*unit_v+(0.25 * p )*unit_p

		return np.vstack((N1, N2, N3, N4,N5))
	def __faces_nodes_pyramidal_1order(self):
		'''
		Nodes ID that form each face\n
		Ref: Pauline faces numbering\n
		Returns:\n
		face0[[node 0,node 1,node 2..]\n
		face1 [node 0,node 1,node 2..]]\n
		'''
		return np.array([[0,1,2,3],
					[0,4,1],
					[0,3,4],
					[2,4,3],
					[1,4,2]])
