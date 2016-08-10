#===============================================================================
# Doctoral student: Anderson Santos Nunes
# University: UFSC - GRUCAD
#===============================================================================

#===============================================================================
# Import classes and starts the time counter
#===============================================================================
from lib.shape_functions import ShapeFuncions,Operations
import numpy as np
import numpy
from numpy import math
import time
from lib.read_write_TXT_files import write_file
import os
from lib.structs import File_names
from lib.pre_proc import get_preproc_data
timeStart=time.time()


def FEM_1order_Solver (preProcData):
    print ('Solving...')
    timeStart=time.time()

#===============================================================================
# Initial data
#===============================================================================
    shapeFunctions=ShapeFuncions()
    gradN=shapeFunctions.grad_nod_tri_1order()
    mu0=4*np.pi*math.pow(10, -7)
    
#------------------------------------------------------------------------------
# Pre-processor
    meshData=preProcData.MeshData
    elemNodes= meshData.ElemNodes
    nodesCoordenates=meshData.NodesCoordenates
    elemTags=meshData.ElemTags
    elemType=meshData.ElemType
    n=len(nodesCoordenates)

#------------------------------------------------------------------------------
# Materials library
    materialProp=preProcData.MaterialProp
    
#------------------------------------------------------------------------------
# Setup
    regionMaterial=preProcData.RegionMaterial
    regionExcitation=preProcData.RegionExcitation
    boundary=preProcData.BC
    
#===============================================================================
#Integration points for Gauss method
#===============================================================================
    u=np.array([1.0/6.0,2.0/3.0,1.0/6.0])
    v=np.array([1.0/6.0,1.0/6.0,2.0/3.0])
    w=1.0/6.0;
    qtdNumInted=3
    Integdudv=0.5
    
#===============================================================================
# Global Matrix initialization
#===============================================================================
    MatGlobal_esq=np.zeros((n,n))
    MatGlobal_dir=np.zeros((n,1))


#===============================================================================
# Main loop over the elements
#===============================================================================
    for k in range (0,len(elemTags)):
        if elemType[k]==2:
    
#------------------------------------------------------------------------------
# Element material propriety
            prop=0
            elemMatProperties=0
            for eachRegion in regionMaterial:
                if eachRegion.RegionNumber==elemTags[k][0]:
                    materialName=eachRegion.MaterialName
                    elemMatProperties=materialProp[materialName].Permeability
                    break
            prop=1.0/(mu0*elemMatProperties)
#------------------------------------------------------------------------------
# Nodes coordinates
            nodes=[]
            nodes.append(elemNodes[k][0])
            nodes.append(elemNodes[k][1])
            nodes.append(elemNodes[k][2])
            
            coordJ=np.array([[nodesCoordenates[nodes[0]][0], nodesCoordenates[nodes[0]][1]],
                             [nodesCoordenates[nodes[1]][0], nodesCoordenates[nodes[1]][1]],
                             [nodesCoordenates[nodes[2]][0], nodesCoordenates[nodes[2]][1]]])

#------------------------------------------------------------------------------
# Jacobian
#            coordJ=coordJ.T
#            gradN=gradN.T
            operations=Operations()
            Jac=operations.get_jacobian_triangle(k,elemNodes,nodesCoordenates)
            invJac=np.linalg.inv(Jac)
            detJac=np.linalg.det(Jac)
            invJacGradN=invJac*gradN
    
#------------------------------------------------------------------------------
# Left side integral
            matLocal_esq=np.zeros((3,3))
            for pinteg in range(0,qtdNumInted):
                matLocal_esq=matLocal_esq+np.transpose(invJacGradN)*invJacGradN*detJac*Integdudv*w*prop
    
# Left side matrix assembling
            for im in range (0,3):
                for jm in range(0,3):
                    MatGlobal_esq[elemNodes[k][im],elemNodes[k][jm]]=MatGlobal_esq[elemNodes[k][im],elemNodes[k][jm]]+ matLocal_esq[im,jm]
    
#------------------------------------------------------------------------------
# Right side integral
            matLocal_dir=np.zeros((3,1))

# Get Js
            Js=0
            for eachregion in regionExcitation:
                if eachregion.RegionNumber==elemTags[k][0]:
                    Js=eachregion.Value
                    break
    
# Right side integral    
            for pinteg in range(0,qtdNumInted):
                uinteg=u[pinteg]
                vinteg=v[pinteg]
                N_prim=shapeFunctions.Nod_Tri_1order(uinteg, vinteg)
                matLocal_dir=matLocal_dir+detJac*Integdudv*w*Js*np.transpose(N_prim)
    
# Right side matrix assembling
            for im in range (0,3):
                MatGlobal_dir[elemNodes[k][im],0]=MatGlobal_dir[elemNodes[k][im],0]+matLocal_dir[im,0]
    
    
#===============================================================================
# Boundary conditions
#===============================================================================
# Get values
    nodesBC = GetBCs(elemNodes, elemTags, boundary)
                    
# Apply values
    for eachNodeBC in nodesBC:
        MatGlobal_esq[eachNodeBC,:]=np.zeros(n)
        MatGlobal_esq[eachNodeBC,eachNodeBC]=1.0
        MatGlobal_dir[eachNodeBC]=nodesBC[eachNodeBC]

#===============================================================================
# Linear system
#===============================================================================
    results=np.linalg.solve(MatGlobal_esq,MatGlobal_dir)

#===============================================================================
# Time control
#===============================================================================

    timeEnd=time.time()
    dtime=timeEnd-timeStart
    print ('Solved in '+ str(dtime)+'ms')
    
#===============================================================================
# Save the results
#===============================================================================
    write_file("resultsFile",results,'Results')
    

#===============================================================================
# Get the boundary condition at each point
#===============================================================================
def GetBCs(elemNodes, elemTags, boundary):
    nodesBC = {} #Dictionary
    for i in range(0, len(elemTags)):
        for eachBC in boundary:
            if elemTags[i][0] == eachBC.LineNumber:
                for eachnode in elemNodes[i]:
                    nodesBC[eachnode] = eachBC.Value
    
    return nodesBC
    
setup_file_name=os.path.join(folder_path,setup_file)
mesh_file_name =os.path.join(folder_path,mesh_file)

file_names=File_names()

#===============================================================================
# Pre Processing
#===============================================================================
preProcData= get_preproc_data(mesh_file_name, setup_file_name) 
FEM_1order_Solver (preProcData)