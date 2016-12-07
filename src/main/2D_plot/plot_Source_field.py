#clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt
import math
import os
mu=4*math.pi*math.pow(10,-7)

plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'24'}
savepath=r"C:\Anderson\Pessoal\01_Doutorado\12_ACE meetings\20160923_V2"
results_path=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\31_Subdomain_Dular_2009\Line_results"


#===================================================
#Coordinates
this_file="line_coordinates.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
x=data[:,0]
y=data[:,1]
z=data[:,2]



#===================================================
#Source FEM
this_file="line_field_source_FEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B1_x=data[:,0]
B1_y=data[:,1]
B1_z=data[:,2]


#===================================================
#Source BS
this_file="line_field_source_BS.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B2_x=data[:,0]*mu
B2_y=data[:,1]*mu
B2_z=data[:,2]*mu


#===================================================
#Source FFEM
this_file="line_field_source_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B3_x=data[:,0]
B3_y=data[:,1]
B3_z=data[:,2]

#===================================================
#Source FFEM
this_file="line_field_source_FFEM_open.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B3_x_open=data[:,0]
B3_y_open=data[:,1]
B3_z_open=data[:,2]

#===================================================
#Reaction FFEM
this_file="line_field_reaction_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B4_x=data[:,0]
B4_y=data[:,1]
B4_z=data[:,2]

#===================================================
#Totalo FEM
this_file="line_field_complet_FEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B5_x=data[:,0]
B5_y=data[:,1]
B5_z=data[:,2]


#===================================================
#Total FFEM
this_file="line_field_complet_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B6_x=data[:,0]
B6_y=data[:,1]
B6_z=data[:,2]

#===================================================
#Reaction FFEM+BS
this_file="line_field_complet_FFEM_BS.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B7_x=data[:,0]
B7_y=data[:,1]
B7_z=data[:,2]

##===================================================
##line_field_reaction_BS_corrected
this_file="line_field_reaction_BS_corrected.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B8_x=data[:,0]
B8_y=data[:,1]
B8_z=data[:,2]


#===================================================
#PLots
plt.figure(1)
plt.figure(figsize=(22, 17))
#plt.plot(x, B5_y,label='Complete (FEM 2D)',color="green",lw=1,linestyle='-')
plt.plot(x, B6_y,label='Complete (FFEM)',color="green",lw=5,linestyle='-',alpha=0.5)

#plt.plot(x, B1_y,label='SF (FEM 2D)',color="red",lw=3)
#plt.plot(x, B2_y,label='SF (BS)',color="red",lw=3,linestyle='-')
#plt.plot(x, B3_y,label='SF (FFEM)',color="red",lw=3,linestyle='--')
#plt.plot(x, B3_y_open,label='SF (FFEM) - Open',color="red",lw=3,alpha=0.5)
#
#plt.plot(x, B7_y,label='RF (FFEM) using SF (BS)',color="blue",lw=3,linestyle='-')
#plt.plot(x, B4_y,label='RF (FFEM) using SF (FFEM)',color="blue",lw=3,linestyle='--')
#plt.plot(x, B8_y,label='RF (FFEM) corrected',color="blue",lw=3,alpha=0.5)

plt.plot(x, B4_y+B3_y,label='TF = RF (FFEM+FFEM) + SF (FFEM)',lw=1,color='black')
plt.plot(x, B7_y+B2_y,label='TF = RF (FFEM+BS) + SF (BS)',lw=3,linestyle='-.',color='black')
plt.plot(x, B8_y+B2_y,label='TF=RF(FFEM) corrected + SF (BS)',lw=3,linestyle='--',color='black')

plt.xlabel('Distance [mm]',**axis_font)
plt.ylabel('By [T]',**axis_font)
legend = plt.legend(fontsize='24')
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.ylim(ymin=0.12,ymax=0.2)
plt.xlim(xmin=0.01,xmax=0.05)
plt.tick_params(axis='x', labelsize=24)
plt.tick_params(axis='y', labelsize=24)
plt.tight_layout()
plt.grid(True)
#plt.xlim(xmax=0.15)
plt.savefig(savepath+'\\figure_7.pdf')
