array = [[1,2,3,7,4,5],
        [4,5,6,3,6,7],
        [7,8,9,1,3,2],
        [2,4,6,8,1,5],
        [5,4,3,6,8,9],
        [7,9,1,2,3,4]
        ]

out = []
while len(array):
    out += array.pop(0)
    array = list(zip(*array))[::-1] # Rotate
print(out)

"""
import numpy as np

def snail(array):
    m = []
    array = np.array(array)
    while len(array) > 0:
        m += array[0].tolist()
        array = np.rot90(array[1:])
    return m
"""