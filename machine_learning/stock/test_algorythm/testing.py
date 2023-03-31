from back_testing import *
import os

data = get_data(f'Data{os.sep}RTS{os.sep}SPFB.RTS_200115_230322(15).txt')
print(data)