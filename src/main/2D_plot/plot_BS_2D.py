clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font',family='Times New Roman')
plt.close("all")
axis_font = { 'size':'20'}
savepath=r"C:\Anderson\Pessoal\01_Doutorado\5_Figuras_Inkscape\Tese"
mesh_type="grossa"

#===================================================
#FEM
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\GetDP\h_along_y.dat"
data = np.genfromtxt(data,delimiter=' ')
h_along_y_x=data[:,4]*1000
h_along_y_y=abs(data[:,12])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\GetDP\h_along_x.dat"
data = np.genfromtxt(data,delimiter=' ')
h_along_x_x=data[:,3]*1000
h_along_x_y=abs(data[:,12])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\BS\results\BiotSavartXFirst.txt"
data = np.genfromtxt(data,delimiter=' ')
BiotSavartXFirst_x=data[:,0]*1000
BiotSavartXFirst_y=abs(data[:,1])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\BS\results\BiotSavartXSecond.txt"
data = np.genfromtxt(data,delimiter=' ')
BiotSavartXSecond_x=data[:,0]*1000
BiotSavartXSecond_y=abs(data[:,1])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\BS\results\BiotSavartYFirst.txt"
data = np.genfromtxt(data,delimiter=' ')
BiotSavartYFirst_x=data[:,0]*1000
BiotSavartYFirst_y=data[:,1]

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\2D\BS\results\BiotSavartYSecond.txt"
data = np.genfromtxt(data,delimiter=' ')
BiotSavartYSecond_x=data[:,0]*1000
BiotSavartYSecond_y=data[:,1]


#===================================================
#Error
error_first_y=100*abs(BiotSavartYFirst_y-h_along_y_y)/h_along_y_y
error_second_y=100*abs(BiotSavartYSecond_y-h_along_y_y)/h_along_y_y

error_first_x=100*abs(BiotSavartXFirst_y-h_along_x_y)/h_along_x_y
error_second_x=100*abs(BiotSavartXSecond_y-h_along_x_y)/h_along_x_y

#===================================================
#PLots
plt.figure(1)
plt.plot(h_along_y_x, h_along_y_y,label='MEF',color="black")
plt.plot(BiotSavartYFirst_x, BiotSavartYFirst_y,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(BiotSavartYSecond_x, BiotSavartYSecond_y,label='Segunda ordem',color="black",linestyle='--',lw=3)
plt.xlabel('Distância y [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc='center right')
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)
plt.axvline(x=-25, color='blue',lw=2)
plt.axvline(x=-50, color='blue',lw=2 )
plt.axvline(x=25, color='blue',lw=2)
plt.axvline(x=50, color='blue',lw=2 )
plt.savefig(savepath+"\supe_H_"+mesh_type+"_y.pdf", bbox_inches='tight')

fig = plt.figure(2)
ax1 = fig.add_subplot(111)
ax1.semilogy(BiotSavartYFirst_x, error_first_y,label='Primeira ordem',color="black",linestyle='-.',lw=3)
ax1.semilogy(BiotSavartYFirst_x, error_second_y,label='Segunda ordem',color="black")
plt.xlabel('Distância y [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-25, color='blue',lw=2)
plt.axvline(x=-50, color='blue',lw=2 )
plt.axvline(x=25, color='blue',lw=2)
plt.axvline(x=50, color='blue',lw=2 )
plt.savefig(savepath+"\supe_erro_"+mesh_type+"_y.pdf", bbox_inches='tight')


fig = plt.figure(3)
ax1 = fig.add_subplot(111)
ax1.semilogy(BiotSavartYFirst_x, error_first_y,label='Primeira ordem',color="black",linestyle='-.',lw=3)
ax1.semilogy(BiotSavartYFirst_x, error_second_y,label='Segunda ordem',color="black")
plt.xlabel('Distância y [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
if mesh_type=="grossa":
    plt.ylim(ymin=1.0,ymax=20.0)
else:
    plt.ylim(ymin=0.08,ymax=3.0)
    
plt.grid(True,which='minor')
plt.grid(True)
plt.axvline(x=-25, color='blue',lw=2)
plt.axvline(x=-50, color='blue',lw=2 )
plt.axvline(x=25, color='blue',lw=2)
plt.axvline(x=50, color='blue',lw=2 )
plt.savefig(savepath+"\supe_erro_"+mesh_type+"_y_zoom.pdf", bbox_inches='tight')

plt.figure(4)
plt.plot(h_along_x_x, h_along_x_y,label='MEF',color="black")
plt.plot(BiotSavartXFirst_x, BiotSavartXFirst_y,label='Primeira ordem',color="black",linestyle='-.',lw=3)
plt.plot(BiotSavartXSecond_x, BiotSavartXSecond_y,label='Segunda ordem',color="black",linestyle='--',lw=3)
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True)
plt.savefig(savepath+"\supe_H_"+mesh_type+"_x.pdf", bbox_inches='tight')

fig = plt.figure(5)
ax1 = fig.add_subplot(111)
ax1.semilogy(BiotSavartXFirst_x, error_first_x,label='Primeira ordem',color="black",linestyle='-.',lw=3)
ax1.semilogy(BiotSavartXFirst_x, error_second_x,label='Segunda ordem',color="black")
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True,which='minor')
plt.grid(True)
if mesh_type=="grossa":
    plt.ylim(ymin=0.03,ymax=20.0)
else:
    plt.ylim(ymin=0.03,ymax=3.0)
    
plt.savefig(savepath+"\supe_erro_"+mesh_type+"_x.pdf", bbox_inches='tight')
print("Done")