#===============================================================================
# Doctoral student: Anderson Santos Nunes
# Date:24/02/2014
# University: UFSC - GRUCAD
#===============================================================================

#===============================================================================
# Import modules following official guidelines:
#===============================================================================
import numpy as np
from lib.messages import print_message
from lib import matrix_aux
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

def SolveMagneticCircuit(Ac,Yb, F,J,BC_nodes,BC_values):
	print_message("Running circuit solver")
	flux=__solve_nodal_circuit(Ac,Yb, F,J,BC_nodes,BC_values)
#	flux=solve_nodal_circuit_diagonal(Ac,Yb, F)
	print_message("Running circuit solver - Done")
	return flux


def __solve_nodal_circuit(Ac,Yb,E,J,BC_nodes,BC_values):
	'''

	Based on Chua, 1975
	Solve circuit based on nodal  analysis\n
	Ac: nodal incidence matrix (with reference node)\n
	Yb: branch admitance matrix\n
	E: branch source vector
	'''
	if isinstance(Ac,csr_matrix):
		Ac=Ac.toarray()
	if isinstance(Yb,csr_matrix):
		Yb=Yb.toarray()
	if isinstance(E,csr_matrix):
		E=E.toarray()

	A=np.delete(Ac, (0), axis=0)
	del(Ac)
	At=A.T
	Yn=np.dot(np.dot(A,Yb),At)
	Jn=np.dot(A,J-np.dot(Yb,E))
	del(A)

#Applies the boundaries conditions
	for counter,each_BC_node in enumerate(BC_nodes):
		Yn[each_BC_node,:]=0.0
		Yn[each_BC_node,each_BC_node]=1.0
		Jn[each_BC_node]=BC_values[counter]

	vn=np.linalg.linalg.solve(Yn, Jn)
	del(Yn)
	del(Jn)
	v_b=np.dot(At,vn)
	del(At)
	v=v_b+E
	i=np.dot(Yb,v)

	return i-J

def __solve_nodal_circuit_sparse(Ac,Yb,E):
	'''
	Based on Chua, 1975
	Solve circuit based on nodal  analysis\n
	Ac: nodal incidence matrix (with reference node)\n
	Yb: branch admitance matrix\n
	E: branch source vector
	'''
	if isinstance(Ac,csr_matrix) and isinstance(Yb,csr_matrix) and isinstance(E,csr_matrix):
		A=matrix_aux.delete_sparse_mask(Ac,[0],0)
		del(Ac)
		At=csr_matrix.transpose(A)
		Yn=A.dot(Yb).dot(At)
		Jn=-A.dot(Yb).dot(E)
		del(A)
		vn=spsolve(Yn, Jn)
		del(Yn)
		del(Jn)
		vn=vn.T
		v_b=At.dot(vn)
#		v_b=csr_matrix.dot(At,vn)
		v=(v_b+E.T).T
		i=Yb.dot(v)
	return i

def __solve_nodal_circuit_diagonal(Ac,Yb,E):
	'''
	Based on Chua, 1975
	Solve circuit based on nodal  analysis\n
	Ac: nodal incidence matrix (with reference node)\n
	Yb: branch admitance matrix\n
	E: branch source vector
	'''
	lines,cols=Yb.shape
	Yb_dia=np.zeros((lines,cols))
	for line in range(0,lines):
		for col in range(0,cols):
			if Yb[line,col]!=0:
				if line==col:
					Yb_dia[line,col]=Yb[line,col]
	A=np.delete(Ac, (0), axis=0) #Bus incidence matrix
	At=A.T
	Yn=np.dot(np.dot(A,Yb_dia),At)
	Jn=-np.dot(np.dot(A,Yb_dia),E)
	vn=np.linalg.linalg.solve(Yn, Jn)
	v_b=np.dot(At,vn)
	v=v_b+E
	i=np.dot(Yb_dia,v)
	return i

#%% Node circuit solver
def __solve_node_circuit(Ac,Yb, F):
	'''
	Solve circuit based on nodal  analysis\n
	Ac: nodal incidence matrix (with reference node)\n
	Yb: branch admitance matrix\n
	F: branch source vector
	'''

	#------------------------------------------------------------------------------
	# Incidence matrix without the reference node
	A=np.delete(Ac, (0), axis=0) #Bus incidence matrix
	AYP=np.dot(A,Yb)
	YB=np.dot(AYP,np.transpose(A))
	F_IN=np.dot(-AYP,F)

	#------------------------------------------------------------------------------
	# Solves the linear system
	print("Solving linear system")
	V=np.linalg.linalg.solve(YB, F_IN)
	V=np.insert(V, 0, [0], axis=0)

	#------------------------------------------------------------------------------
	# Post processing - Flux at each reluctance
	flux=np.zeros((len(F),1))

	for eachCol in range(0,len(A[0])):
		relNodes=Ac[:,eachCol]

		for eachNode in range(0,len(Ac[:,eachCol])):
			if relNodes[eachNode]==1.0:
				node1=eachNode
			elif relNodes[eachNode]==-1.0:
				node2=eachNode

		gradV=V[node1]-V[node2]+F[eachCol]
		flux[eachCol]=gradV*Yb[eachCol,eachCol]

	return flux

#%%
def __solve_mesh(B,Zb,F):
	'''
	Solve circuit based on mesh  analysis\n
	B: branch incidence matrix \n
	Zb: branch impedance matrix\n
	F: branch source vector
	'''
	Bt=np.transpose(B)
	Egm=np.dot(Bt,F)
	Zm=np.dot(np.dot(Bt,Zb),B)
	Im=np.dot(np.linalg.inv(Zm),Egm)
	Ib=np.dot(B,Im)

	return Ib


def __combination(mat,pivot_row,row_2,relation,cols):
	"""
	Linear combination between two lines\n
	mat[row_2,each_col]=mat[pivot_row,each_col]+relation*mat[row_2,each_col]\n
	pivot_row: pivot row\n
	row_2: row to be combined\n
	relation: relation between the two rows\n
	relation=-A[row,col]/A[row_2,col]\n
	cols: number of cols
	"""
	for each_col in range(0,cols):
		mat[row_2,each_col]=mat[pivot_row,each_col]+relation*mat[row_2,each_col]
	return mat

def __welsch(A):
	'''
	Runs the Welsch algorithm in order to find the tree and co-tree of a network\n
	A: nodal incidence matrix
	'''
#	Welsch algo
	row_considered=list()
	tree=list()
	rows,cols=A.shape
	for col in range(0,cols):
		for row in range(0,rows):
			break_bool=False
			if A[row,col]!=0:
				if not row in row_considered:
					for row_2 in range(0,rows):
						if row!=row_2 and A[row_2,col]!=0:
							relation=-A[row,col]/A[row_2,col]
							__combination(A,row,row_2,relation,cols)
					break_bool=True
					row_considered.append(row)
					tree.append(col)
			if break_bool:
				break
		if max(A[rows-1,:])==0 and min(A[rows-1,:])==0:
			break

# Reorganize the matrix A in Ai1(branches) and Ai2 (links)
	co_tree=list()
	counter_tree=0
	counter_co_tree=0
	for counter_col in range(0,cols):
		trans=A[0:rows-1,counter_col].copy()
		trans=trans.reshape(rows-1,1)
		if counter_col in tree:
			if counter_tree==0:
				Ai1=trans
			else:
				Ai1=np.concatenate((Ai1,trans),axis=1)
			counter_tree+=1
		else:
			if counter_co_tree==0:
				Ai2=trans
			else:
				Ai2=np.concatenate((Ai2,trans),axis=1)
			counter_co_tree+=1
			co_tree.append(counter_col)

#Loop matrix Bl
	Kc2=np.dot(Ai1.T,Ai2)
	Bl1=-Kc2.T
	Bl2=np.identity(Bl1.shape[0])
	Bl=np.hstack((Bl1,Bl2))
	return Bl,tree,co_tree

def __solve_mesh_circuit(A,Zb, F):

	Bl,tree,co_tree=__welsch(A)
	branches=list()
	branches.extend(tree)
	branches.extend(co_tree)
	num_branches=len(branches)

	#Reorganize the Z,F matrices based on the tree
	new_Zb=np.zeros((num_branches,num_branches))
	new_F=np.zeros((num_branches,1))
	for counter,each_branche in enumerate(branches):
		new_Zb[counter,counter]=Zb[each_branche,each_branche]
		new_F[counter]=F[each_branche]

	flux_mesh_welsch=__solve_mesh(Bl.T,new_Zb,new_F)

	#Reorganize the flux matrix based on the tree
	new_Flux=np.zeros((num_branches,1))
	for counter,each_branche in enumerate(branches):
		new_Flux[each_branche]=flux_mesh_welsch[counter]

	return new_Flux