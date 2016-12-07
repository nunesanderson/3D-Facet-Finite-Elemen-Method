clear_all()
import os
import numpy as np
from scipy import linalg
import math
from main.RNMFEM.Post_Gmsh import Create_B_vector_plot,Create_Vector_field,get_B_vector_point_uvp,integrate_B_surface

start=-1.0
end=1.0
n_points=80
I=1.0
a=0.1
m=I*math.pi*pow(a,2)

x=np.linspace(start, end,n_points, endpoint=True)
y=np.linspace(start, end,n_points, endpoint=True)
z=np.linspace(start, end,n_points, endpoint=True)
coordinates=list()
field=list()

for each_x in x:
	for each_y in y:
		for each_z in z:
			r=math.sqrt(pow(each_x,2.0)+pow(each_y,2.0)+pow(each_z,2))
			this_coordinates=[each_x,each_y,each_z]
			coordinates.append(this_coordinates)

			bx=3*m*each_x*each_z/pow(r,5.0)
			by=3*m*each_y*each_z/pow(r,5.0)
			bz=m*(3*pow(each_z,2.0)-pow(r,2.0))/pow(r,5.0)

			this_field=[bx,by,bz]
			field.append(this_field)

path=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes\32_Dipole\teste.txt'
Create_Vector_field(coordinates,field,path,"B Vector")