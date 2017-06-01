import numpy as np
from lib.read_write_TXT_files import write_numeric_data_file
import time
import os

path=r'C:\Anderson\Pessoal\01_Doutorado\10_Testes\19_read_wrtite_txt_files'


def run(n):
	array=np.arange(n*n).reshape(n,n)
	this_file='file_own.txt'
	this_path=os.path.join(path,this_file)
	try:
		os.remove(this_path)
	except:
		pass
	start_time = time.time()
	write_numeric_data_file(this_path,array,"",True)
	end_time = time.time()
	write_own_time=end_time-start_time
	
	
	
	this_file='file_np.txt'
	this_path=os.path.join(path,this_file)
	try:
		os.remove(this_path)
	except:
		pass
	start_time = time.time()
	np.savetxt(this_path, array, delimiter=',')
	end_time = time.time()
	write_np_time=end_time-start_time
	
	return write_own_time,write_np_time

teste=list()

for cada in range(100):
	teste.append(cada)

this_file='file_np.txt'
this_path=os.path.join(path,this_file)
np.savetxt(this_path, teste, delimiter=',')