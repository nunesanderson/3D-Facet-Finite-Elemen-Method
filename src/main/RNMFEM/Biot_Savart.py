##===============================================================================
## Import classes and starts the time counter
##===============================================================================
#import math
#from lib.pre_proc import get_preproc_data
#from lib.shape_functions import Operations
#import numpy as np
#from numpy import linalg as LA
#from main.RNMFEM.Post_Gmsh import Create_Vector_field
#import os
#from RNMFEM.structs import  File_names
#from read_write_TXT_files import write_numeric_data_file
#from main.RNMFEM.get_Gauss_points import Get_Gauss_points_list
#import matplotlib.pyplot as plt
##from lib.error import Errors
#
#def Biot_Svart_law(P_coord,dl_start,dl_end,current):
#	
#	dl=(dl_end-dl_start)
#	L=dl_end-(dl)/2.0
#	R=P_coord-L
#	R_abs=LA.norm(R)
#	vector_product=np.cross(dl,R)
#	dH_P=(current/(4.0*math.pi))*vector_product/math.pow(R_abs,3.0)
#
#	return dH_P
#
#def create_line(start_point,end_point,n):
#	'''
#	Discretize a line
#	
#	Parameters
#	----------
#	
#	start_point: np.array([x,y,z])\n
#	end_point: np.array([x,y,z])\n
#	n: number of discretes elements
#	
#	Returns
#	----------
#	starts,ends\n
#	np.array([x0,y0,z0],
#		    [xn,y,zn])
#	'''
#	starts=np.zeros((n,3))
#	ends=np.zeros((n,3))
#	k=np.arange(0,n)
#	dxyz=(end_point-start_point)/(float(n))
#	
#	starts[:,0]=k*dxyz[0]
#	starts[:,1]=k*dxyz[1]
#	starts[:,2]=k*dxyz[2]
#	
#	ends[:,0]=(k+1)*dxyz[0]
#	ends[:,1]=(k+1)*dxyz[1]
#	ends[:,2]=(k+1)*dxyz[2]
#	return starts,ends
#
#def crate_circular_loop(radius,center,orientation):
#	'''
#	Discretize a loop
#	
#	Parameters
#	----------
#	radius: the radius of the loop [m]
#	center: the center of the loop [m]
#	orientation:xy, xz,yz
#
#
#	Returns
#	----------
#	starts,ends\n
#	np.array([x0,y0,z0],
#		    [xn,y,zn])
#	'''
#	
#	n=400	
#	div=float(n)
#	t_start=np.linspace(0,2*math.pi*(div-1.0)/div,n)
#	t_ends=np.linspace(2*math.pi/div,2*math.pi,n)
#	starts=np.zeros((n,3))
#	ends=np.zeros((n,3))
#	
#	if Orientation == 'xy':
#		starts[:,0] = center[0]+radius*sin(t_start)
#		starts[:,1] = center[1]+radius*cos(t_start)
#		
#		ends[:,0] = center[0]+radius*sin(t_ends)
#		ends[:,1] = center[1]+radius*cos(t_ends)
#	elif Orientation == 'xz':
#		starts[:,0] = center[0]+radius*sin(t_start)
#		starts[:,2] = center[1]+radius*cos(t_start)
#		
#		ends[:,0] = center[0]+radius*sin(t_ends)
#		ends[:,2] = center[1]+radius*cos(t_ends)
#	elif Orientation == 'yz':
#		starts[:,1] = center[0]+radius*sin(t_start)
#		starts[:,2] = center[1]+radius*cos(t_start)
#		
#		ends[:,1] = center[0]+radius*sin(t_ends)
#		ends[:,2] = center[1]+radius*cos(t_ends)
#	return starts,ends
#
#
#x_pos=100
#start_point=np.array([0,0,0])
#end_point=np.array([x_pos,0,0])
#position=np.array([0,1,0])
#current=50
#H=Biot_Svart_law(position,start_point,end_point,current)
#
#print"===================="
#print H
#
#
#n=x_pos*1000
#radius=4.0
#Orientation='xy'
#center=np.array([0,0])
#
#starts,ends=create_line(start_point,end_point,n)
#starts,ends=crate_circular_loop(radius,center,Orientation)
#
#pos=0.5
#current=10.0
#
#H_an=current/(2.0*math.pi*pos)
#
#print H_an
#x_pos=float(x_pos)
#
#position=np.array([0,0,0])
#
#
#def run_Biot_Savart_along(position,starts,ends,current):
#	n=len(starts)
#	H=np.zeros((3))
#	for k in xrange(n):
#		H+=Biot_Svart_law(position,starts[k,:],ends[k,:],current)
#	return H
#print run_Biot_Savart_along(position,starts,ends,current)
#
#from RNMFEM.get_Gauss_points import Get_Gauss_points_list
#
#tests_folder=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes'
#folder_path=os.path.normpath(os.path.join(tests_folder,'24_Biot_Savart_3D'))
#
#setup='setup.txt'
#mesh='model.msh'
#
#setup_file_name=os.path.join(folder_path,setup)
#mesh_file_name =os.path.join(folder_path,mesh)
#
#
#preProcData= get_preproc_data(mesh_file_name,setup_file_name)
#teste_2=Get_Gauss_points_list(preProcData,True,folder_path) 
#mesh_data=preProcData.MeshData
#all_elem_nodes= mesh_data.ElemNodes
#nodes_coordenates=mesh_data.NodesCoordenates
#elem_tags=mesh_data.ElemTags
#elem_type=mesh_data.ElemType
#
#
#start_list=list()
#end_list=list()
#counter=0
#for each_elem in elem_type:
#	if each_elem==1:
#		start_list.append(all_elem_nodes[counter][0])
#		end_list.append(all_elem_nodes[counter][1])
#	elif each_elem>1:
#		break
#	counter+=1
#	
#I=1.0
#H=np.array([0,0,0])
#counter=0
#r=2
#P_coord=np.array([50,r,0])
#start=np.zeros((3))
#end=np.zeros((3))
#for each_start in start_list:
#	start_with_list=nodes_coordenates[each_start]
#	start[0]=start_with_list[0]
#	start[1]=start_with_list[1]
#	start[2]=start_with_list[2]
#	
#	end_node=end_list[counter]
#	end_with_list=nodes_coordenates[end_node]
#	end[0]=end_with_list[0]
#	end[1]=end_with_list[1]
#	end[2]=end_with_list[2]
#	
#	H=H+Biot_Svart_law(P_coord,start,end,I)
#	counter+=1
#
#print "Biot-savart:",H
#
#print "Analytical:", I/(2.0*math.pi*r)
#
#
#
#
#
##n_radius=100
##radius=np.linspace(0.01,1.0,n_radius)
##
##L_wire=1000.0
##I=2.0
##H_Bot=list()
##H_ana=list()
##
##div=1000
##len_div=L_wire/div
##for k in range(0,n_radius):
##	r=radius[k]
##	P_coord=np.array([L_wire/2.0,r,0])
##	H=np.array([0,0,0])
##	for counter in xrange(div):
##		start=np.array([counter*len_div,0,0])
##		end=np.array([(counter+1)*len_div,0,0])
##		H=H+Biot_Svart_law(P_coord,start,end,I)
###		print H
##	
##	H_Bot.append(LA.norm(H[2]))
#
##H_ana=I/(2.0*math.pi*radius)
##
##print "Ok"
##plt.close("all")
##fig, ax = plt.subplots()
##ax.plot(radius, H_Bot, 'k--', label='Biot-Savart')
##ax.plot(radius, H_ana, 'k', label='$I/2*pi*r$')
##legend = ax.legend(loc='upper center', shadow=True)
##plt.show()
##def run_Biot_Savart(setupFileName,meshFileName,folder_path):
##    '''
##    Runs the Biot-Savart method\n
##    setupFileName: setup file name\n
##    meshFileName: file name of the mesh\n
##    folder_path: path of solution folder\n
##    example:\n
##    field_solution=Biot_Savart.run_Biot_Savart(setup_file_name,mesh_file_name,folder_path)
##    '''
##    print("Running Biot-Savart law")
##    #===============================================================================
##    # Pre Processing
##    #===============================================================================
##    preProcData= get_preproc_data(meshFileName, setupFileName)
##    integ_gauss_points_coordinates=Get_Gauss_points_list(preProcData,True,folder_path)
##
##    #===============================================================================
##    # Initial data
##    #===============================================================================
##   
##    # Setup
##    regions_excitation=preProcData.RegionExcitation
##    #------------------------------------------------------------------------------
##    # Pre-processor
##    mesh_data=preProcData.MeshData
##    all_elem_nodes= mesh_data.ElemNodes
##    nodes_coordenates=mesh_data.NodesCoordenates
##    elem_tags=mesh_data.ElemTags
##    elem_type=mesh_data.ElemType
##    operations=Operations()
##    
##    global_nodes=list()
##    counter=0
##    global_values=list()
##    
##    for each_elem in integ_gauss_points_coordinates:
##        local=list()
##        for each_point in each_elem:
##            local.append(np.array([0,0,0]))
##        global_values.append(local)
##
##    for elem_counter, each_element in  enumerate(all_elem_nodes):
##        if elem_type[elem_counter]>1:      
##            I=0
##            for eachregion in regions_excitation:
##                if eachregion.RegionNumber==elem_tags[elem_counter][0]:
##                    Js=eachregion.Value
##                    element_area=operations.get_area_element(elem_type[elem_counter],all_elem_nodes[elem_counter],nodes_coordenates)
##                    I=math.fabs(Js*element_area)
##                    break
##            if I!=0:
##                dl=np.array([0,0,Js/math.fabs(Js)])
##																
###baricenter of the element with current density
##                xbar=0
##                ybar=0
##                zbar=0
##                nodes=all_elem_nodes[elem_counter]
##                for nodeCounter in range(0,len(nodes)):
##                    xbar=nodes_coordenates[nodes[nodeCounter]][0]+xbar
##                    ybar=nodes_coordenates[nodes[nodeCounter]][1]+ybar
##                    zbar=nodes_coordenates[nodes[nodeCounter]][2]+zbar
##                num_nodes=len(nodes)
##                baricenter_coordinates=np.array([xbar/num_nodes,ybar/num_nodes,zbar/num_nodes])
##
##                local=list()        
##                for elem_inner_counter, inner_elem_coodinates in enumerate(integ_gauss_points_coordinates):
##                    for node_counter,each_node in enumerate(inner_elem_coodinates):
##                        r= each_node-baricenter_coordinates
##                        abs_r=LA.norm(r)
###==============================================================================
###                         Biot_savart equation
###==============================================================================
##                        H_field=I*(1.0/(2.0*math.pi))*np.cross(dl,r)/math.pow(abs_r,2)
##                        global_values[elem_inner_counter][node_counter]=global_values[elem_inner_counter][node_counter]+H_field
###List containing all the integration points coordinates
##    points_list=list()  
##    counter=0
##    for each_elem in integ_gauss_points_coordinates:
##        local=list()
##        local_nodes=list()
##        for each_point in each_elem:
##            local.append(counter)
##            points_list.append(each_point)
##            local_nodes.append(counter)
##            counter+=1
##        global_nodes.append(local_nodes)
##
### Folder results path
##    file_names=File_names()
##    results_folder=file_names.get_results_folder_name()
##    results_path=os.path.join(folder_path,results_folder)
###==============================================================================
### Write file with the results
##    integPOintResults=list()
##    for each_element in global_values:
##        for each in  each_element:
##            integPOintResults.append(each)
##    counter=0
##    h_field_results_file_name=file_names.get_H_results_file_name()
##    full_path=os.path.join(results_path,h_field_results_file_name)
##    write_numeric_data_file(full_path,integPOintResults,"HResults",True)
##
### Write file with the points numbering
##    global_list=list()
##    for eachw in global_nodes:
##        local=list()
##        for each in eachw:
##            local.append(each)
##        global_list.append(local)
##    h_field_results_file_name=file_names.get_H_results_file_name()
##    full_path=os.path.join(results_path,h_field_results_file_name)
##    write_numeric_data_file(full_path,global_list,"Points",False)
##
###==============================================================================
### GMSH post processing
##    Gmsh_file_name=file_names.get_H_Gmsh_pos_proc_file_name()
##    path=os.path.join(results_path,Gmsh_file_name)
##    Create_Vector_field(points_list,integPOintResults,path,"H vector")