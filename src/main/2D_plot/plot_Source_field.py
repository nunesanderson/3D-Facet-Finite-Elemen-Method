clear_all()
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
axis_font = { 'size':'20'}
savepath=r"C:\Anderson\Pessoal\01_Doutorado\5_Figuras_Inkscape\Tese"
results_path=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\31_Subdomain_Dular_2009\Subdomain\line_results"


#===================================================
#Coordinates
this_file="line_coordinates.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
x=data[:,0]
y=data[:,1]
z=data[:,2]


#===================================================
#Reaction
this_file="reaction_field_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')
B1_x=data[:,0]
B1_y=data[:,1]
B1_z=data[:,2]


#===================================================
#Source field
this_file="source_field_BS.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')

B2_x=data[:,0]*mu
B2_y=data[:,1]*mu
B2_z=data[:,2]*mu

#===================================================
#Source field
this_file="source_field_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')

B4_x=data[:,0]
B4_y=data[:,1]
B4_z=data[:,2]


#===================================================
#Source field
this_file="source_field_FFEM_refined.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')

B5_x=data[:,0]
B5_y=data[:,1]
B5_z=data[:,2]

#===================================================
#STotal field FFEM
this_file="total_field_FFEM.txt"

data=os.path.join(results_path,this_file)
data = np.genfromtxt(data,delimiter=' ')

B3_x=data[:,0]
B3_y=data[:,1]
B3_z=data[:,2]


#===================================================
#PLots
plt.figure(1)
plt.plot(x, B1_y,label='RF',linestyle='--',color="black",lw=3)
plt.plot(x, B2_y,label='SF(BS)',color="black",linestyle='-.',lw=3)
plt.plot(x, B4_y,label='SF(FFEM)',color="blue",linestyle='-.',lw=3)
plt.plot(x, B5_y,label='SF(FFEM refined)',color="red",linestyle='-.',lw=3)
plt.plot(x, (B1_y+B2_y),label='TF=RF+SF(BS)',color="black",lw=3)
plt.plot(x, (B1_y+B4_y),label='TF=RF+SF(FFEM)',color="blue",lw=3)
plt.plot(x, B3_y,label='TF(FFEM)',color="gray",lw=3)
#plt.plot(x, B4_y,label='TF(FFEM)',color="blue",lw=3)
plt.xlabel('Distance [mm]',**axis_font)
plt.ylabel('By [T]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)