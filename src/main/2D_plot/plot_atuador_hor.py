clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt
import math

mu0=4*math.pi*pow(10,-7)

plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'20'}
#savepath=r"C:\Anderson\Pessoal\01_Doutorado\08_Relatorios_Papers\4_CEFC_2016\Four_pages\Figures"

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\05_Getdp_ref\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
y_FEM=(data[:,4])
z_FEM=(data[:,5])

#===================================================
# FEM - Ref
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\05_Getdp_ref\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
B_FEM_ref_x=data[:,12]
B_FEM_ref_y=data[:,13]
B_FEM_ref_z=data[:,14]
B_list=list()


#===================================================
# FEM - coarse
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\07_Getdp_coarse\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])
B_FEM_coarse_x=data[:,12]
B_FEM_coarse_y=data[:,13]
B_FEM_coarse_z=data[:,14]
B_list=list()

#===================================================
# FEM - fine
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\01_Getdp_fine\bLine.dat"
data = np.genfromtxt(data,delimiter=' ')
x_FEM=(data[:,3])*1000
B_FEM_fine_x=data[:,12]
B_FEM_fine_y=data[:,13]
B_FEM_fine_z=data[:,14]
B_list=list()

#===================================================
# FFEM - 04_FFEM_coarse
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\04_FFEM_coarse\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_FFEM_coarse_x=(data[:,0])
B_FFEM_coarse_y=(data[:,1])
B_FFEM_coarse_z=(data[:,2])

#===================================================
# FFEM - Fine
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\08_FFEM_fine\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_FFEM_coarse_x=(data[:,0])
B_FFEM_coarse_y=(data[:,1])
B_FFEM_fine_z=(data[:,2])


#===================================================
# FFEM - Fine - coupled
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\09_FFEM_Circuit_coupling\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_FFEM_couple_x=(data[:,0])
B_FFEM_couple_y=(data[:,1])
B_FFEM_couple_z=(data[:,2])

#===================================================
# FFEM - Fine - perfect
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\37_Atuador_hor\10_FFEM_Circuit_coupling_perfect\results\line_field.txt"
data = np.genfromtxt(data,delimiter=' ')
B_FFEM_couple_perfect_x=(data[:,0])
B_FFEM_couple_perfect_y=(data[:,1])
B_FFEM_couple_perfect_z=(data[:,2])

error_B_FFEM_couple_z=list()
error_B_FFEM_couple_perfect_z=list()

for counter,each in enumerate(B_FFEM_couple_z):
	error_B_FFEM_couple_z.append(100*(abs(B_FFEM_fine_z[counter]-B_FFEM_couple_z[counter])/abs(B_FFEM_fine_z[counter])))
	error_B_FFEM_couple_perfect_z.append(100*(abs(B_FFEM_fine_z[counter]-B_FFEM_couple_perfect_z[counter])/abs(B_FFEM_fine_z[counter])))


	if x_FEM[counter]>-20 and x_FEM[counter]<20:
		B_FFEM_couple_z[counter]='nan'
		B_FFEM_couple_perfect_z[counter]='nan'
		error_B_FFEM_couple_z[counter]='nan'
		error_B_FFEM_couple_perfect_z[counter]='nan'
#		B_FFEM_fine_z[counter]='nan'
#		x_FEM[counter]='nan'

	if error_B_FFEM_couple_perfect_z[counter]<0.07:
		error_B_FFEM_couple_perfect_z[counter]=error_B_FFEM_couple_perfect_z[counter-1]

	if error_B_FFEM_couple_z[counter]<0.07:
		error_B_FFEM_couple_z[counter]=error_B_FFEM_couple_perfect_z[counter-1]
#=========================
#Plots
plt.figure(1)
#plt.plot(x_FEM, B_FEM_z,label='FEM',color="black",lw=3,linestyle='-',alpha=0.5)
#plt.plot(x_FEM, B_FEM_ref_z,label='FEM - Ref.',color="red",lw=3,linestyle='-')
#plt.plot(x_FEM, B_FEM_coarse_z,label='FEM (Coarse)',color="black",linestyle='--',lw=3,)
#plt.plot(x_FEM, B_FEM_fine_z,label='FEM (Fine)',color="black",linestyle='-',lw=3)
#plt.plot(x_FEM, B_FFEM_coarse_z,label='FFEM (Coarse)',color="blue",linestyle='--',lw=3,alpha=0.5)
plt.plot(x_FEM, B_FFEM_fine_z,label='FFEM (Fine)',color="blue",linestyle='-',lw=1,alpha=1)
plt.plot(x_FEM, B_FFEM_couple_z,label='Coupling 1',color="black",linestyle='--',lw=3,alpha=1)
plt.plot(x_FEM, B_FFEM_couple_perfect_z,label='Coupling 2',color="red",linestyle='-.',lw=3,alpha=1)



plt.xlabel('Position along the probe line [mm]',**axis_font)
plt.ylabel('Bz [T]',**axis_font)
legend = plt.legend(fontsize='20')
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.xlim(xmin=-60,xmax=60)
plt.axvline(x=-55, color='red',lw=2,linestyle='--')
plt.axvline(x=-25, color='red',lw=2,linestyle='--' )
plt.axvline(x=55, color='red',lw=2,linestyle='--')
plt.axvline(x=25, color='red',lw=2,linestyle='--' )
plt.text(40, 0.01, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
plt.text(-40, -0.04, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)
#plt.savefig(savepath+"\linha_gap_3D_B.pdf", bbox_inches='tight')

#===================================================
# Errors
plt.figure(2)
plt.semilogy(x_FEM, error_B_FFEM_couple_z,label='Coupling 1',color="black",lw=3,alpha=1)
plt.semilogy(x_FEM, error_B_FFEM_couple_perfect_z,label='Coupling 2',color="blue",lw=3,alpha=0.5)
plt.xlabel('Position along the probe line [mm]',**axis_font)
plt.ylabel('Rel. dif. [%]',**axis_font)
legend = plt.legend(fontsize='20')
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.xlim(xmin=-60,xmax=60)
plt.axvline(x=-55, color='red',lw=2,linestyle='--')
plt.axvline(x=-25, color='red',lw=2,linestyle='--' )
plt.axvline(x=55, color='red',lw=2,linestyle='--')
plt.axvline(x=25, color='red',lw=2 ,linestyle='--')
plt.text(40, 1, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
plt.text(-40, 1, 'Probe line in \n the air gap', fontsize=20,horizontalalignment='center',color="red")
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)


#===================================================
# Errors
error_B_FEM_coarse_z=list()
error_B_FEM_fine_z=list()
error_B_FFEM_coarse_z=list()
error_B_FFEM_fine_z=list()
error_x=list()
for counter in range(0,len(x_FEM),1):
	if abs(x_FEM[counter])>0.2*max(x_FEM):
		error_B_FEM_coarse_z.append(100*abs((B_FEM_ref_z[counter]-B_FEM_coarse_z[counter])/B_FEM_ref_z[counter]))
		error_B_FEM_fine_z.append(100*abs((B_FEM_ref_z[counter]-B_FEM_fine_z[counter])/B_FEM_ref_z[counter]))
		error_B_FFEM_coarse_z.append(100*abs((B_FEM_ref_z[counter]-B_FFEM_coarse_z[counter])/B_FEM_ref_z[counter]))
		error_B_FFEM_fine_z.append(100*abs((B_FEM_ref_z[counter]-B_FFEM_fine_z[counter])/B_FEM_ref_z[counter]))
		error_x.append(x_FEM[counter])


plt.figure(3)
plt.plot(error_x, error_B_FEM_coarse_z,label='FEM (Coarse) - AVG: '+str(round(np.mean(error_B_FEM_coarse_z),2)),color="black",linestyle='--',lw=3,)
plt.plot(error_x, error_B_FEM_fine_z,label='FEM (Fine)',color="black",linestyle='-',lw=3)
plt.plot(error_x, error_B_FFEM_coarse_z,label='FFEM (Coarse)',color="blue",linestyle='--',lw=3,alpha=0.5)
plt.plot(error_x, error_B_FFEM_fine_z,label='FFEM (Fine)',color="blue",linestyle='-',lw=3,alpha=0.5)

plt.xlabel('Position along the probe line [mm]',**axis_font)
plt.ylabel('Rel. dif. [%]',**axis_font)
legend = plt.legend(fontsize='20')
plt.axvline(x=-55, color='red',lw=2,linestyle='--')
plt.axvline(x=-25, color='red',lw=2,linestyle='--' )
plt.axvline(x=55, color='red',lw=2,linestyle='--')
plt.axvline(x=25, color='red',lw=2 ,linestyle='--')
plt.text(40, 1, 'Air gap region', fontsize=20,horizontalalignment='center',color="red")
plt.text(-40, 1, 'Air gap region', fontsize=20,horizontalalignment='center',color="red")
plt.tick_params(axis='x', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.xlim(xmin=-60,xmax=60)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)

print("Avg error_B_FEM_coarse_z="+str(np.mean(error_B_FEM_coarse_z)))
print("Avg error_B_FEM_fine_z="+str(np.mean(error_B_FEM_fine_z)))
print("Avg error_B_FFEM_coarse_z="+str(np.mean(error_B_FFEM_coarse_z)))
print("Avg error_B_FFEM_fine_z="+str(np.mean(error_B_FFEM_fine_z)))