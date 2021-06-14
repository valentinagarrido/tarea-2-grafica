# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 23:09:34 2021

@author: hgcol
"""

import math
import numpy as np
import grafica.basic_shapes as bs

def createTextureQuad(nx1, ny1, nx2, ny2):
    O = [0,0,1]
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, 0.5, 0.0,  nx1, ny1,
        -0.5, -0.5, 0.0, nx1, ny2,
         0.5,  0.5, 0.0, nx2, ny1,
        0.5,  -0.5, 0.0,  nx2, ny2]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         1, 2, 3]

    return bs.Shape(vertices, indices)

def createSurface(mat, ty):
    if ty == "floor":
        t = 0
        O = [0,0,1]
    if ty == "sky":
        t = 1
        O = [0,0,-1]
    V = mat[:, :, 0+t]
    I = mat[:, :, 2+t]
    M = len(V)
    N = len(V[0])
    
    L = 1/12
    vertices = []
    indices = []
    c = 0
    for i in range(M):
        for j in range(N):
            if (j < (N - 1)) and(i < (M - 1)):
                tx = I[i,j]
                v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i+1,j], tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i+1,j+1], (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j+1], (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            elif (j < (N - 1)):
                tx = I[i,j]
                v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i,j], tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i,j+1], (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j+1], (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            elif (i < (M - 1)):
                tx = I[i,j]
                v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i+1,j], tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i+1,j], (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j], (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            else:
                tx = I[i,j]
                v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i,j], tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i,j], (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j], (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            
    return bs.Shape(vertices, indices)
                    
# def createSurface(mat, ty):
#     if ty == "floor":
#         t = 0
#     if ty == "sky":
#         t = 1
#     V = mat[:, :, 0+t]
#     I = mat[:, :, 2+t]
#     M = len(V)
#     N = len(V[0])
    
#     L = 1/12
#     vertices = []
#     indices = []
#     c = 0
#     for i in range(M):
#         for j in range(N):
#             if (j < (N - 1)) and(i < (M - 1)):
#                 tx = I[i,j]
#                 v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0]
#                 v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i+1,j], tx*L, 1]
#                 v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i+1,j+1], (tx+1)*L, 1]
#                 v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j+1], (tx+1)*L, 0]
#                 c += 4
#                 vertices += v0+v1+v2+v3
#                 indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
#             elif (j < (N - 1)):
#                 tx = I[i,j]
#                 v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0]
#                 v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i,j], tx*L, 1]
#                 v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i,j+1], (tx+1)*L, 1]
#                 v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j+1], (tx+1)*L, 0]
#                 c += 4
#                 vertices += v0+v1+v2+v3
#                 indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
#             elif (i < (M - 1)):
#                 tx = I[i,j]
#                 v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0]
#                 v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i+1,j], tx*L, 1]
#                 v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i+1,j], (tx+1)*L, 1]
#                 v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j], (tx+1)*L, 0]
#                 c += 4
#                 vertices += v0+v1+v2+v3
#                 indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
#             else:
#                 tx = I[i,j]
#                 v0 = [-10+j*(20/M), 10 - i*(20/N), V[i,j], tx*L, 0]
#                 v1 = [-10+j*(20/M), 10-(i+1)*(20/N), V[i,j], tx*L, 1]
#                 v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), V[i,j], (tx+1)*L, 1]
#                 v3 = [-10+(j+1)*(20/M), 10-i*(20/N), V[i,j], (tx+1)*L, 0]
#                 c += 4
#                 vertices += v0+v1+v2+v3
#                 indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            
#     return bs.Shape(vertices, indices)
    

def createWall(tx):
    M = 20
    N = 20
    
    L = 1/12
    vertices = []
    indices = []
    O = [0,0,1]
    c = 0
    for i in range(M):
        for j in range(N):
            if (j < (N - 1)) and(i < (M - 1)):
                v0 = [-10+j*(20/M), 10 - i*(20/N), 0, tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), 0, tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), 0, (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), 0, (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            elif (j < (N - 1)):
                v0 = [-10+j*(20/M), 10 - i*(20/N), 0, tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N),0, tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), 0, (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), 0, (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            elif (i < (M - 1)):
                v0 = [-10+j*(20/M), 10 - i*(20/N), 0, tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), 0, tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), 0, (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), 0, (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            else:
                v0 = [-10+j*(20/M), 10 - i*(20/N), 0, tx*L, 0] + O
                v1 = [-10+j*(20/M), 10-(i+1)*(20/N), 0, tx*L, 1] + O
                v2 = [-10+(j+1)*(20/M), 10-(i+1)*(20/N), 0, (tx+1)*L, 1] + O
                v3 = [-10+(j+1)*(20/M), 10-i*(20/N), 0, (tx+1)*L, 0] + O
                c += 4
                vertices += v0+v1+v2+v3
                indices += [0+c, 1+c, 2+c, 0+c, 2+c, 3+c]
            
    return bs.Shape(vertices, indices)


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

def bezierMatrix(P0, P1, P2, P3):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
    return np.matmul(G, Mb)

def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve



def createCurve():
    P0 = np.array([[-0.2, 0, 0]]).T
    P1 = np.array([[-0.4, 0.4, 0]]).T
    P2 = np.array([[0.4, 0.4, 0]]).T
    P3 = np.array([[0.2, 0, 0]]).T
    bm = bezierMatrix(P0, P1, P2, P3)
    ps = 20
    BM = evalCurve(bm, ps)
    vertices = []
    indices = []
    c = 0
    for i in range(ps-1):
        if i == 0:
            vertices += list(BM[0]) + [1, 0, 0]
            vertices += list(BM[1]) + [1, 0, 0]
            vertices += [list(BM[1])[0]] + [0, 0, 1, 0, 0]
            indices += [0, 1, 2]
            c += 1
        elif (0 < i < ps - 2):
            vertices += list(BM[i+1]) + [1, 0, 0]
            vertices += [list(BM[i+1])[0]] + [0, 0, 1, 0, 0]
            indices += [c + 0, c + 1, c + 2,
                        c + 1, c + 2, c + 3]
            c += 2
        else:
            vertices += list(BM[ps-1]) + [1, 0, 0]
            indices += [c + 0, c + 1, c + 2]
    return bs.Shape(vertices, indices)