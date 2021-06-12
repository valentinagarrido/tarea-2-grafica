# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:59:48 2021

@author: hgcol
"""

import numpy as np

M = 100
N = 100

mapa = np.ndarray(shape=(M, N, 4), dtype=np.float32)

# suelo, todo fijo en 10
mapa[:, :, 0] = -2
# cielo, fijo en 40
for i in range(M):
    mapa[i, :, 1] = -2 + 4*((M-1-i)/M)
#mapa[:, :, 1] = 2

# indices textura suelo
mapa[:, :, 2] = 4

# indices textura cielo
mapa[:, :, 3] = 7

# Nota: sí, tambien se pueden llenar con un for, pero es algo mas lento :)

#guardando a disco
np.save("map.npy", mapa)