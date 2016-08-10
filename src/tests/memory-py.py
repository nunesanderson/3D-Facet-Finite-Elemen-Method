clear_all()
import numpy as np
import psutil
import os

n=100000*4
a=np.arange(0,n)

process = psutil.Process(os.getpid())
mem_1= process.memory_info().rss
#%%
del a
process = psutil.Process(os.getpid())
print mem_1-process.memory_info().rss

