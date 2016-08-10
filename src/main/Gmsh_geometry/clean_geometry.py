clear_all()
from lib.read_write_TXT_files import get_data_from_file
import os
import numpy as np

folder= r'C:\Anderson\Pessoal\01_Doutorado\2_Modelos_Codigos_Externos\05_Impedance'
file_name=os.path.join(folder,'geometry.geo')

data=get_data_from_file(file_name) 

original_points=list()

def clean_line(this_str,line):
	line=line.replace("cl__1","")
	line=line.replace("{","")
	line=line.replace("}","")
	line=line.replace(";","")
	line=line.replace("=","")
	line=line.replace(" ","")
	line=line.replace("\n","")
	line=line.replace(this_str,"")
	return line



for each_line in data:
	this_str="Point"
	if this_str in each_line:
		this_point= clean_line(this_str,each_line)
		this_point=this_point.split(")") 
		this_point=this_point[1]
		this_point=this_point.split(",")
		coord=np.array([float(this_point[0]),float(this_point[1]),float(this_point[2])])
		original_points.append(coord)

cleaned_points=list()
for each_point in original_points:
	bool_add=True
	for each_point_2 in original_points:
		if (each_point==each_point_2).all():
			break
			bool_add=False
	if bool_add:
		cleaned_points.append(each_point)

print("Done!")