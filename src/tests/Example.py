#===============================================================================
# Doctoral student: Anderson Santos Nunes
# Date:24/02/2014
# University: UFSC - GRUCAD
#===============================================================================

#===============================================================================
# Import modules following official guidelines:
#===============================================================================
import numpy as np
import Solver
import scipy
import string
clear_all()
#===============================================================================
# Variables
#===============================================================================

##Branch impedance matrix
Zb=np.zeros((17,17))
Zb[0,0]=530516476.972984
Zb[1,1]=68209261.325098
Zb[2,2]=26793761.463282
Zb[3,3]=14283135.9185034
Zb[4,4]=8869315.71409943
Zb[5,5]=6041077.8951375
Zb[6,6]=4378866.15914209
Zb[7,7]=3319416.22132707
Zb[8,8]=2602822.54214739
Zb[9,9]=2095595.23128621
Zb[10,10]=1723433.09695756
Zb[11,11]=1442302.47876816
Zb[12,12]=1224758.69649317
Zb[13,13]=1052973.15939259
Zb[14,14]=914955.565400924
Zb[15,15]=802400.994641028
Zb[16,16]=709409.484977719
#
rows,cols=Zb.shape
Yb=np.zeros((17,17))
for row in range(0,rows):
    for col in range(0,cols):
        if row==col:
            Yb[row,col]=1.0/Zb[row,col]

#Nodal incidence matrix
#Already organized with the link at the right
#A=np.array([
#[-1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#[1,-1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0],
#[0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0],
#[0,0,1,0,0,-1,0,0,0,0,0,-1,0,0,0,0,0],
#[0,0,0,1,0,0,-1,0,0,0,0,1,-1,0,0,0,0],
#[0,0,0,0,1,0,0,-1,0,0,0,0,1,0,0,0,0],
#[0,0,0,0,0,1,0,0,-1,0,0,0,0,1,0,0,0],
#[0,0,0,0,0,0,1,0,0,-1,0,0,0,-1,1,0,0],
#[0,0,0,0,0,0,0,1,0,0,-1,0,0,0,-1,0,0],
#[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,-1,0],
#[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,-1],
#[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1]])
#Aleatory incidence matrix
A=np.array([
[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[-1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,-1,0,0,1,0,1,0,0,0,0,0,0,0,0,0],
[0,0,0,-1,0,-1,1,0,1,0,0,0,0,0,0,0,0],
[0,0,0,0,-1,0,-1,0,0,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,-1,0,0,-1,0,1,0,0,0,0],
[0,0,0,0,0,0,0,0,-1,0,1,-1,0,1,0,0,0],
[0,0,0,0,0,0,0,0,0,-1,0,1,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,1,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1]])

##Branch source matrix
F=np.zeros((17,1))
F[0,0]=1000
F[12,0]=1000
F[13,0]=1000
F[14,0]=1000
#
flux_nodal=Solver.solve_nodal_circuit(A,Yb, F)


#Ex Chua, pg 150
#A=np.array([
#[1,1,0,1,0,0,0,0],
#[0,-1,1,0,1,0,1,0],
#[0,0,0,0,0,0,-1,1],
#[-1,0,-1,0,0,1,0,0]])

#A=np.array([
#[1,1,0,0,0,0,-1],
#[-1,0,0,1,-1,0,0],
#[0,0,0,-1,0,1,0],
#[0,0,-1,0,1,-1,1]])

#Matriz Patrick
#A=np.array([
#[-1,0,-1,0,0],
#[1,0,0,1,0],
#[0,1,0,-1,1],
#[0,-1,1,0,-1]])
print(A)
print("=======================================")

#A,Bl1,Kc2,Ai1,Ai2=Solver.Welsh_1(A)

#B com bl1 do Miguel
#A=np.array([
#[-1,0,1,-1,0,0,0,0,0,0,0,1,0,0,0,0,0],
#[0,-1,0,1,-1,0,0,0,0,0,0,0,1,0,0,0,0],
#[1,0,-1,1,0,-1,1,0,0,0,0,0,0,1,0,0,0],
#[0,1,0,-1,1,0,-1,1,0,0,0,0,0,0,1,0,0],
#[-1,0,1,-1,0,1,-1,0,1,-1,0,0,0,0,0,1,0],
#[0,-1,0,1,-1,0,1,-1,0,1,-1,0,0,0,0,0,1]])
#A=np.array([
#[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#[-1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#[0,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#[0,0,-1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
#[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0],
#[0,0,0,-1,0,-1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
#[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,-1,0,0,0],
#[0,0,0,0,-1,0,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
#[0,0,0,0,0,0,0,-1,0,0,0,-1,1,0,0,0,0,0,0,0,0],
#[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,-1],
#[0,0,0,0,0,0,0,0,-1,0,-1,0,0,1,0,0,0,0,0,0,1],
#[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,-1,0],
#[0,0,0,0,0,0,0,0,0,-1,0,0,0,0,1,0,0,0,0,1,0],
#[0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,1,0,0,0,0,0],
#[0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,1,0,0,0,0],
#[0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,0,0,0,0]])





#rows,cols=B_wel.shape

#for row in range(0,rows):
#    for col in range(0,cols):
#        if B_wel[row,col]>1 or B_wel[row,col]<-1:
#            B_wel[row,col]=B_wel[row,col]/B_wel[row,col]




def combination(mat,pivot_row,row_2,relation,cols):
    """
    Combination:\n
    row_1=row_1+relation*row_2
    """
    for each_col in range(0,cols):
        mat[row_2,each_col]=mat[pivot_row,each_col]+relation*mat[row_2,each_col]
        
    str_relation=""
    if relation!=1:
        str_relation=str(relation)+"*"
    print("row "+str(row_2)+" = row "+str(pivot_row)+" +"+str_relation+" row "+str(row_2))
    print(mat)
    return mat

def welsch(A):
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
                            print("Col: "+str(col)+" Row:" +str(row))
                            relation=-A[row,col]/A[row_2,col]
                            combination(A,row,row_2,relation,cols)
                    break_bool=True
                    row_considered.append(row)
                    tree.append(col)
            if break_bool:
                break
        if max(A[rows-1,:])==0 and min(A[rows-1,:])==0:
            break
    print(rows)
 
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

    Kc2=np.dot(Ai1.T,Ai2)
    Bl1=-Kc2.T
    Bl2=np.identity(Bl1.shape[0])
    Bl=np.hstack((Bl1,Bl2))
    return Bl,tree,co_tree

#A=np.delete(A, (0), axis=0) #Bus incidence matrix
Bl,tree,co_tree=welsch(A)

branches=list()
branches.extend(tree)
branches.extend(co_tree)



new_Zb=np.zeros((17,17))
new_F=np.zeros((17,1))
for counter,each_branche in enumerate(branches):
    new_Zb[counter,counter]=Zb[each_branche,each_branche]
    new_F[counter]=F[each_branche]


flux_B=Solver.solve_mesh_circuit(B,Zb,F)

flux_B_2=Solver.solve_mesh_circuit(Bl.T,new_Zb,new_F)

new_Flux=np.zeros((17,1))
for counter,each_branche in enumerate(branches):
    new_Flux[each_branche]=flux_B_2[counter]


counter=0
for each in flux_B:
    print(str(new_Flux[counter])+" \t- " + str(each) +" \t- "+ str(flux_nodal[counter]))
    counter+=1
#    
    