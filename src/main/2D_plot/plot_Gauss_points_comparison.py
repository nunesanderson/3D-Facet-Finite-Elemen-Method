clear_all()
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font',family='Times New Roman')
axis_font = { 'size':'20'}
plt.close("all")
savepath=r"C:\Anderson\Pessoal\01_Doutorado\5_Figuras_Inkscape\Tese"
mesh_type="grossa"


def get_error(x,aprox, exat, tol):
    
    ans_error=list()
    ans_x=list();
    counter=0;
    max_field=max(exat)*tol/100.0;
    for each_x in x:
        if exat[counter]>=max_field:    
            ans_x.append(each_x)
            ans_error.append(100.0*abs(aprox[counter]-exat[counter])/exat[counter]  )
        counter=counter+1
    return ans_x,ans_error
            
#===================================================
#Line along Z
#===================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\analyt_z.txt"
data = np.genfromtxt(data,delimiter=' ')
analyt_z_x=data[:,0]*1000
analyt_z_y=abs(data[:,1])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\one_z.txt"
data = np.genfromtxt(data,delimiter=' ')
one_z_x=data[:,0]*1000
one_z_y=abs(data[:,1])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\four_z.txt"
data = np.genfromtxt(data,delimiter=' ')
four_z_x=data[:,0]*1000
four_z_y=abs(data[:,1])
    
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\five_z.txt"
data = np.genfromtxt(data,delimiter=' ')
five_z_x=data[:,0]*1000
five_z_y=abs(data[:,1])



erro_one=100*abs((one_z_y-analyt_z_y))/analyt_z_y
erro_four=100*abs((four_z_y-analyt_z_y))/analyt_z_y
erro_five=100*abs((five_z_y-analyt_z_y))/analyt_z_y

plt.figure(1)
plt.plot(analyt_z_x, analyt_z_y,label='Analítico',color="black")
plt.plot(one_z_x, one_z_y,label='Um ponto',color="gray",lw=2)
plt.plot(four_z_x, four_z_y,label='Quatro pontos',color="black",linestyle='--',lw=3)
plt.plot(five_z_x, five_z_y,label='Cinco pontos',color="black",linestyle='-.',lw=3)
plt.xlabel('Distância z [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid(True)
plt.savefig(savepath+"\solido_H_"+mesh_type+"_z_Gauss.pdf", bbox_inches='tight')


fig = plt.figure(2)
plt.semilogy(analyt_z_x, erro_one,label='Um ponto',color="gray",lw=2)
plt.semilogy(analyt_z_x, erro_four,label='Quatro pontos',color="black",linestyle='--',lw=3)
plt.semilogy(analyt_z_x, erro_five,label='Cinco pontos',color="black",linestyle='-.',lw=3)
plt.xlabel('Distância z [mm]',**axis_font)
plt.ylabel('Dif. [%]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tight_layout()
plt.grid(True,which='minor')
plt.grid(True)
plt.savefig(savepath+"\solido_erro_"+mesh_type+"_z_Gauss.pdf", bbox_inches='tight')

#===================================================
#Line along X
#===================================================
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\one_x.txt"
data = np.genfromtxt(data,delimiter=' ')
one_x_x=data[:,0]*1000
one_x_y=(data[:,1])

data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\four_x.txt"
data = np.genfromtxt(data,delimiter=' ')
four_x_x=data[:,0]*1000
four_x_y=(data[:,1])
    
data=r"C:\Anderson\Pessoal\01_Doutorado\10_Testes\23_Biot_Savart_3D\Solid winding\145 GaussPoints\five_x.txt"
data = np.genfromtxt(data,delimiter=' ')
five_x_x=data[:,0]*1000
five_x_y=(data[:,1])

plt.figure(3)
plt.plot(one_x_x, one_x_y,label='Um ponto',color="gray",lw=2)
plt.plot(four_x_x, four_x_y,label='Quatro pontos',color="black",linestyle='--',lw=3)
plt.plot(five_x_x, five_x_y,label='Cinco pontos',color="black",linestyle='-.',lw=3)
plt.xlabel('Distância x [mm]',**axis_font)
plt.ylabel('Campo magnético [A/m]',**axis_font)
legend = plt.legend(fontsize='20',loc=0)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.axvline(x=-45, color='blue',lw=2 )
plt.axvline(x=-60, color='blue',lw=2 )
plt.axvline(x=45, color='blue',lw=2 )
plt.axvline(x=60, color='blue',lw=2 )
plt.grid(True)

ans_x_1,erro_one=get_error(five_x_x,one_x_y,five_x_y,0.0)
ans_x,erro_four=get_error(five_x_x,four_x_y,five_x_y,0.0)

plt.savefig(savepath+"\solido_H_"+mesh_type+"_x_Gauss.pdf", bbox_inches='tight')

fig = plt.figure(4)
plt.semilogy(ans_x_1, erro_one,label='Um ponto',color="gray",lw=2)
plt.semilogy(ans_x, erro_four,label='Quatro pontos',color="black",linestyle='--',lw=3)
plt.axvline(x=-45, color='blue',lw=2 )
plt.axvline(x=-60, color='blue',lw=2)
plt.axvline(x=45, color='blue',lw=2 )
plt.axvline(x=60, color='blue',lw=2 )
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

plt.savefig(savepath+"\solido_erro_"+mesh_type+"_x_Gauss.pdf", bbox_inches='tight')
print("Done")