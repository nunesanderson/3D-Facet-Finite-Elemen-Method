clear_all()

from src.lib.read_write_TXT_files import get_gauss_points
import numpy as np
from RNMFEM import Post_Gmsh

folder_name=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes\27_Teste_Campo_Fonte_3D\Dispositivo_simples\results'
points_IDs=folder_name+"\\IDs_Gauss_Points.txt"
points_IDs = np.genfromtxt(points_IDs,delimiter=' ',dtype='int')

coordinates=folder_name+"\\Coordinates_Gauss_Points.txt"
coordinates = np.genfromtxt(coordinates,delimiter=' ',dtype='double')

fields=folder_name+"\Hfield_Gauss_Points.txt"
fields = np.genfromtxt(fields,delimiter=' ',dtype='double')

Post_Gmsh.Create_Vector_field(coordinates,fields,folder_name+"\\HTeste.txt","W")


list_fields=list()
for each_elem in points_IDs:
    this_points=list()
    for each_point_ID in each_elem:
        this_points.append(fields[each_point_ID])
    list_fields.append(this_points)


teste_fields=list()
teste_coordinates=list()
counter=0
for each_elem in list_fields:
    for each_point in each_elem:
        teste_fields.append(each_point)
        teste_coordinates.append(coordinates[counter])
        counter=+1

Post_Gmsh.Create_Vector_field(coordinates,fields,folder_name+"\\HTeste__2.txt","W")