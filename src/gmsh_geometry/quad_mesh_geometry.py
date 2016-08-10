clear_all()
from src.lib.read_write_TXT_files import write_file

file_name=r"D:\Anderson\Cloud_Drive\10_UFSC\01_Doutorado\10_Testes\16_Atuador_enrolamento_quad\01_FFEM\rele.geo"
lua_file_name=r'D:\Anderson\Cloud_Drive\10_UFSC\01_Doutorado\10_Testes\16_Atuador_enrolamento_quad\02_FEMM\lua_script.lua'


x_dim = [0,10,15,25,45,55,60,85,105,125]
y_dim=[0,20,40,70,75,105,125,145]

num_x=len(x_dim)
num_y=len(y_dim)

counter=0
text=""
file_data=list()
file_data_lua=list()
file_data.append("cl = 0.01;")
file_data.append("mm = 0.01;")
file_data.append("\n//==================================")
file_data.append("//Nodes")
for each_y in y_dim:
    for eac_x in x_dim:
        text="Point(%s) = {%s*mm,%s*mm, 0, cl};" %(counter,eac_x,each_y)
        text_lua="mi_addnode(%s,%s)" %(eac_x/1000.0,each_y/1000.0)
        file_data.append(text)       
        file_data_lua.append(text_lua)
        counter+=1
file_data.append("\n//==================================")
file_data.append("//Lines")
counter_lines=0
counter=0
for counter_1 in range(0,num_y):
    for counter_2 in range(0,num_x-1):
        text="Line(%s) = {%s,%s};" %(counter_lines,counter,counter+1)
        file_data.append(text)    
        counter+=1
        counter_lines+=1
    counter+=1
counter=0


for counter_1 in range(0,num_y-1):
    for counter_2 in range(0,num_x):
        text="Line(%s) = {%s,%s};" %(counter_lines,counter,num_x+counter)
        file_data.append(text)    
        counter+=1
        counter_lines+=1

physical_list=list()
counter=0
counter_lines=199
start=(num_x-1)*num_y
file_data.append("\n//==================================")
file_data.append("//Surfaces")
for counter_1 in range(0,num_y-1):
    for counter_2 in range(0,num_x-1):
        text="Line Loop(%s) = {%s, -%s, -%s, %s};" %(counter_lines,counter,start+counter,counter+num_x-1,start+counter+1)
        file_data.append(text)
        text="Plane Surface(%s) = {%s};" %(counter_lines+1,counter_lines)
        physical_list.append(counter_lines+1)
        file_data.append(text)
        
        counter+=1
        counter_lines+=2
    start+=1



counter_lines=400
phys_teste=list()
file_data.append("\n//==================================")
file_data.append("//Physical surfaces")
for each in physical_list:
    text="Physical Surface(%s) = {%s};" %(counter_lines,each)
    file_data.append(text)
    phys_teste.append(counter_lines)
    counter_lines+=1

text2=""
for each in phys_teste:
    text2+=str(each)+","
    
file_data.append("\n//==================================")
file_data.append("//Quad mesh")
text=("Transfinite Line {72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131} = 5 Using Progression 1;\n"
'Transfinite Line {92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121} = 7 Using Progression 1;\n'
'Transfinite Line {102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 64, 55, 46, 37, 28, 19, 10, 1,5,14,23,32,41,50,59,68} = 2 Using Progression 1;\n'
'Transfinite Line {0, 9,63, 54, 45, 36, 27, 18, 9, 0, 2, 11, 20, 29, 38, 47, 56, 65} = 3 Using Progression 1;\n'
'Transfinite Line {3, 12, 21, 30, 39, 48, 57, 66, 7, 16, 25, 34, 43, 52, 61, 70, 8, 17, 26, 35, 44, 53, 62, 71} = 5 Using Progression 1;\n'
'Transfinite Line {6, 15, 24, 33, 42, 51, 60, 69} = 6 Using Progression 1;\n'
'Transfinite Line {4, 13, 22, 31, 40, 49, 58, 67} = 3 Using Progression 1;\n'
'Transfinite Surface {200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324};\n'
'Recombine Surface {200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324};\n')
file_data.append(text)
write_file(file_name,file_data,"",True)
write_file(lua_file_name,file_data_lua,"",True)