# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 15:26:39 2021

@author: hgcol
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from map_generator import *

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.phi = 0
        self.eye = np.array([0, 0, -1.8])
        self.at = np.array([0.5, 0, -1.8])
        self.up = np.array([0, 0, 1])

mapa = np.load("map.npy")

# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
    elif key == glfw.KEY_LEFT:
        controller.phi += np.pi/10
        
    elif key == glfw.KEY_RIGHT:
        controller.phi -= np.pi/10
    elif key == glfw.KEY_UP:
        controller.eye += (controller.at - controller.eye) * 0.1
        controller.at += (controller.at - controller.eye) * 0.1
        
        

    else:
        print('Unknown key')


mapa = np.load("map.npy")

def createFloor(mat):
    V = mat[:, :, 0]
    I = mat[:, :, 2]
    M = len(V)
    N = len(V[0])
    
    L = 1/12
    vertices = []
    indices = []
    for i in range(M):
        for j in range(N):
            vertices += [
                -2+(4/(N-1))*j, 2-(4/(M-1))*i, V[i,j], (I[i,j] + j%2)*L, (i%2)
                ]
    for i in range(M-1):
        for j in range(N-1):
            indices += [
                j+i*N, j+1+i*N, j+(i+1)*N,
                j+1+i*N, j+(i+1)*N, j+(i+1)*N+1]
    
    return bs.Shape(vertices, indices)

def createSky(mat):
    V = mat[:, :, 1]
    I = mat[:, :, 3]
    M = len(V)
    N = len(V[0])
    
    L = 1/12
    vertices = []
    indices = []
    for i in range(M):
        for j in range(N):
            vertices += [
                -2+(4/(N-1))*j, 2-(4/(M-1))*i, V[i,j], (I[i,j] + j%2)*L, (i%2)
                ]
    for i in range(M-1):
        for j in range(N-1):
            indices += [
                j+i*N, j+1+i*N, j+(i+1)*N,
                j+1+i*N, j+(i+1)*N, j+(i+1)*N+1]
    return bs.Shape(vertices, indices)

def createWalls():
    vertices = [
        -2, 2, 2, 1/12, 0,
        2, 2, 2, 2/12, 0,
        -2, 2, -2, 1/12, 1,
        2, 2, -2, 2/12, 1,
        2, -2, 2, 3/12, 0,
        2, -2, -2, 3/12, 1]
    
    indices = [
        0, 1, 2, 1, 2, 3, 1, 4, 5, 1, 5, 3
        ]
    return bs.Shape(vertices, indices)


    



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Dice", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    shapeFloor = createFloor(mapa)
    gpuFloor = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("textures.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    floorNode = sg.SceneGraphNode("floor")
    floorNode.childs = [gpuFloor]

    shapeSky = createSky(mapa)
    gpuSky = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath("textures.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    skyNode = sg.SceneGraphNode("sky")
    skyNode.childs = [gpuSky]


    shapeWalls = createWalls()
    gpuWalls = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(shapeWalls.vertices, shapeWalls.indices, GL_STATIC_DRAW)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("textures.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    wallsNode = sg.SceneGraphNode("walls")
    wallsNode.childs = [gpuWalls]
    
    
    shapeBoo = bs.createTextureQuad(1,1)
    gpuBoo = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuBoo)
    gpuBoo.fillBuffers(shapeBoo.vertices, shapeBoo.indices, GL_STATIC_DRAW)
    gpuBoo.texture = es.textureSimpleSetup(
        getAssetPath("boo.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    booNode = sg.SceneGraphNode("boo")
    booNode.transform = tr.matmul([tr.translate(controller.at[0],controller.at[1],
                                                controller.at[2]), 
                                   tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.scale(0.5,0.5,0.5)])
    booNode.childs = [gpuBoo]
    
    red_cube = bs.createColorCube(1, 0, 0)
    gpuRedCube = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuRedCube)
    gpuRedCube.fillBuffers(red_cube.vertices, red_cube.indices, GL_STATIC_DRAW)
    cubeNode = sg.SceneGraphNode("cube")
    cubeNode.transform =tr.matmul([tr.translate(0,1,-1.8), tr.scale(0.5,0.5,0.5)])
    cubeNode.childs = [gpuRedCube]
    
    
    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.childs = [floorNode, skyNode, wallsNode, booNode]
    

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = tr.perspective(60, 1, 0.1, 100)

        at_x = controller.eye[0] + np.cos(controller.phi)
        at_y = controller.eye[1] + np.sin(controller.phi)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(
            controller.eye,
            controller.at,
            controller.up
        )

        theta = glfw.get_time()
        axis = np.array([1,-1,1])
        axis = axis / np.linalg.norm(axis)
        model = tr.translate(0,0,0)
        
        booNode.transform = tr.matmul([tr.translate(controller.at[0],controller.at[1],
                                                    controller.at[2]), tr.rotationZ(controller.phi),
                                       tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.scale(0.5,0.5,0.5)])

        # Drawing dice (with texture, another shader program)
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, model)  
        sg.drawSceneGraphNode(sceneNode, textureShaderProgram, "model")
        
        #glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        #glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        
        #glUseProgram(colorShaderProgram.shaderProgram)
        #sg.drawSceneGraphNode(cubeNode, colorShaderProgram, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuFloor.clear()
    gpuSky.clear()
    gpuWalls.clear()
    gpuBoo.clear()

    glfw.terminate()
