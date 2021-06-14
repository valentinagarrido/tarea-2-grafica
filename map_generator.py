# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 11:59:48 2021

@author: hgcol
"""

import numpy as np

M = 20
N = 20

mapa = np.ndarray(shape=(M, N, 4), dtype=np.float32)

# suelo, todo fijo en 10
mapa[:, :, 0] = -2
mapa[:, :, 0][0:int(M/2),0:int(N/2)] = -1.8
# cielo, fijo en 40
for i in range(M):
    mapa[i, :, 1] = -2 + 4*((M-1-i)/M)
#mapa[:, :, 1] = 2

# indices textura suelo
mapa[:, :, 2] = 4
mapa[0:int(M/2), :, 2] = 0

# indices textura cielo
mapa[:, :, 3] = 9

# Nota: sí, tambien se pueden llenar con un for, pero es algo mas lento :)

#guardando a disco
np.save("map.npy", mapa)

mapa_0 = np.ndarray(shape=(M, N, 4), dtype=np.float32)

# suelo
x = np.linspace(-10,10,M)
y = np.linspace(-10,10,N)
X, Y = np.meshgrid(x,y)
mapa_0[:, :, 0] = (X**2 + Y**2)*0.01 - 2
# cielo
mapa_0[:, :, 1] = (X**2 + Y**2)*0.05

# indices textura suelo
mapa_0[:, :, 2] = 0

# indices textura cielo
mapa_0[:, :, 3] = 2

# Nota: sí, tambien se pueden llenar con un for, pero es algo mas lento :)

#guardando a disco
np.save("map_0.npy", mapa_0)