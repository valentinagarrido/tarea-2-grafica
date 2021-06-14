# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 23:48:54 2021

@author: hgcol
"""

import glfw
import numpy as np
import grafica.transformations as tr
from random import random
from random import randint
from cave import *

M = len(mapa[:,:,0])
N = len(mapa[:,:,0][0])
F = mapa[:,:,0]

class Lara():
    def __init__(self):
        self.pos = [0,0,-1.8]
        self.model = None
        self.controller = None
        self.collected = 0
        
    def set_model(self, new_model):
        self.model = new_model
        
    def set_controller(self, new_controller):
        self.controller = new_controller
    
    def update(self):
        self.pos = [self.controller.at[0], self.controller.at[1], self.controller.at[2]]
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1],
                                                        self.pos[2]), tr.rotationZ(self.controller.phi),
                                           tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.scale(0.5,0.5,0.5)])
        
        
    def collect(self, pieces):
        c = 0
        for piece in pieces:
            if ((piece.pos[0] - self.pos[0])**2 + (piece.pos[1] - self.pos[1])**2 < 0.1):
                piece.status = 1
            c += piece.status
        self.collected = c
    
class Puzzle():
    def __init__(self):
        x = -6+random()*12
        y = -6+random()*12
        for i in range(M):
            for j in range(N):
                if (-10 + i*(20/N) < x <= -10 + (i + 1)*(20/N)) and (10 - j*(20/M) > y >= 10 - (j + 1)*(20/M)):
                    z = F[j,i]
        self.pos = [x, y, z+0.5]
        self.model = None
        self.controller = None
        self.status = 0
        
    def set_model(self, new_model):
        self.model = new_model
    
    def set_controller(self, new_controller):
        self.controller = new_controller
    
    def update(self):
        if self.status == 0:
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1],self.pos[2]),
                                           tr.rotationY(np.pi/2), 
                                          tr.scale(0.1,0.1,0.01)])
        else:
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1],-8),
                                          tr.rotationZ(self.controller.phi), tr.rotationY(np.pi/2), 
                                          tr.scale(0.1,0.1,0.01)])