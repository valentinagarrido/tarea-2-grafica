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
import grafica.lighting_shaders as ls
import my_shapes as ms
from grafica.assets_path import getAssetPath
from map_generator import *
from model import *
import sys


inp = sys.argv
mapa = np.load(inp[1])
textures = inp[2]
N = int(inp[3])

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.phi = 0
        self.Phi = 0
        self.change = False
        self.mouse = (0,0)
        self.eye = np.array([0, 0, -1.7])
        self.at = np.array([0.5, 0, -1.7])
        self.up = np.array([0, 0, 1])
        self.light = 1


# global controller as communication with the callback function
controller = Controller()

def height_cell(x, y, mat):
    M = len(mat)
    N = len(mat[0])
    F = mat[:,:,0]
    S = mat[:,:,1]
    for i in range(M):
        for j in range(N):
            if (-10 + i*(20/N) < x <= -10 + (i + 1)*(20/N)) and (10 - j*(20/M) > y >= 10 - (j + 1)*(20/M)):
                H = S[j,i] - F[j,i]
    return H

def angle(x, y, at, mat):
    M = len(mat)
    N = len(mat[0])
    F = mat[:,:,0]
    S = mat[:,:,1]
    for i in range(M):
        for j in range(N):
            if (-10 + i*(20/N) < x <= -10 + (i + 1)*(20/N)) and (10 - j*(20/M) > y >= 10 - (j + 1)*(20/M)):
                z = F[j,i]
    c1 = z - (at[2]-0.2)
    c2 = np.sqrt((x - at[0])**2 + (y - at[1])**2)
    sin = c1/c2
    angle = np.abs(np.arcsin(sin))
    return [angle, z]
    
            

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
        
    elif key == glfw.KEY_1:
        controller.light = 1
        
    elif key == glfw.KEY_2:
        controller.light = 0.5
        
    elif key == glfw.KEY_3:
        controller.light = 0.1


def cursor(window, x, y):
    global controller
    controller.phi = controller.Phi + np.pi/4 - (x/(600/90))*(np.pi/180)

def mouse(window, button, action, mods):
    global controller
    if (action == glfw.PRESS):
        controller.change = not controller.change
        M = len(mapa)
        N = len(mapa[0])
        if (button == glfw.MOUSE_BUTTON_1):
            controller.Phi = controller.phi
            at_x = controller.eye[0] + np.cos(controller.phi)
            at_y = controller.eye[1] + np.sin(controller.phi)
            h = height_cell(at_x,at_y,mapa)
            a = angle(at_x, at_y, controller.at, mapa)
            ang = a[0]
            at_z = a[1] + 0.3
            if h > 0.7 and ang < (np.pi/4):
                controller.at = np.array([at_x, at_y, at_z])
                controller.eye += (controller.at - controller.eye) * 0.5
                controller.at += (controller.at - controller.eye) * 0.5

        if (button == glfw.MOUSE_BUTTON_2):
            controller.Phi = controller.phi
            at_x = controller.eye[0] + np.cos(controller.phi)
            at_y = controller.eye[1] + np.sin(controller.phi)
            at_z = angle(at_x, at_y, controller.at, mapa)[1] + 0.3
            h = height_cell(at_x - 2*np.cos(controller.phi),
                            at_y - 2*np.sin(controller.phi),mapa)
            a = angle(at_x - 2*np.cos(controller.phi), 
                      at_y - 2*np.sin(controller.phi), controller.at, mapa)
            ang = a[0]
            if h > 0.7 and ang < (np.pi/4):
                controller.at = np.array([at_x, at_y, controller.at[2]])
                controller.eye -= (controller.at - controller.eye) * 0.5
                controller.at -= (controller.at - controller.eye) * 0.5



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "LARA JONES!!!¡", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback functions
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor)
    glfw.set_mouse_button_callback(window, mouse)

    # Creating shader programs for turetures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    normalTextureShaderProgram = ls.SimpleTexturePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)
    
        # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)


    # Creating shapes on GPU memory

    shapeFloor = ms.createSurface(mapa, "floor")
    gpuFloor = es.GPUShape().initBuffers()
    normalTextureShaderProgram.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath(textures), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    floorNode = sg.SceneGraphNode("floor")
    floorNode.childs = [gpuFloor]

    shapeSky = ms.createSurface(mapa, "sky")
    gpuSky = es.GPUShape().initBuffers()
    normalTextureShaderProgram.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath(textures), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    skyNode = sg.SceneGraphNode("sky")
    skyNode.childs = [gpuSky]


    shapeWall = ms.createWall(2)
    gpuWall = es.GPUShape().initBuffers()
    normalTextureShaderProgram.setupVAO(gpuWall)
    gpuWall.fillBuffers(shapeWall.vertices, shapeWall.indices, GL_STATIC_DRAW)
    gpuWall.texture = es.textureSimpleSetup(
        getAssetPath(textures), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    wallNode1 = sg.SceneGraphNode("wall1")
    wallNode1.transform = tr.matmul([tr.translate(10,0,0),tr.rotationY(np.pi/2)])
    wallNode1.childs = [gpuWall]
    
    wallNode2 = sg.SceneGraphNode("wall2")
    wallNode2.transform = tr.matmul([tr.translate(-10,0,0),tr.rotationY(np.pi/2)])
    wallNode2.childs = [gpuWall]
    
    wallsNode1 = sg.SceneGraphNode("walls1")
    wallsNode1.childs = [wallNode1, wallNode2]
    
    wallsNode2 = sg.SceneGraphNode("walls2")
    wallsNode2.transform = tr.rotationZ(np.pi/2)
    wallsNode2.childs = [wallNode1, wallNode2]
    
    
    shapeLara1 = ms.createTextureQuad(0,0,0.5,1)
    gpuLara1 = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuLara1)
    gpuLara1.fillBuffers(shapeLara1.vertices, shapeLara1.indices, GL_STATIC_DRAW)
    gpuLara1.texture = es.textureSimpleSetup(
        getAssetPath("lara.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shapeLara2 = ms.createTextureQuad(0.5,0,1,1)
    gpuLara2 = es.GPUShape().initBuffers()
    textureShaderProgram.setupVAO(gpuLara2)
    gpuLara2.fillBuffers(shapeLara2.vertices, shapeLara2.indices, GL_STATIC_DRAW)
    gpuLara2.texture = es.textureSimpleSetup(
        getAssetPath("lara.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    laraNode = sg.SceneGraphNode("lara")
    laraNode.transform = tr.matmul([tr.translate(controller.at[0],controller.at[1],
                                                controller.at[2]), 
                                   tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.scale(0.5,0.5,0.5)])
    
    
    Lara = Lara()
    Lara.set_controller(controller)
    
    shapeQuad = bs.createColorCube(1,0,0)
    gpuQuad = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuQuad)
    gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)
    
    pieces = []
    
    shapeEar = ms.createCurve()
    gpuEar = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuEar)
    gpuEar.fillBuffers(shapeEar.vertices, shapeEar.indices, GL_STATIC_DRAW)
    
    
    piecesNode = sg.SceneGraphNode("pieces")
    for i in range(N):    
        quadNode = sg.SceneGraphNode("quad")
        quadNode.transform = tr.scale(1,1,1)
        quadNode.childs = [gpuQuad]
        ear1Node = sg.SceneGraphNode("ear1")
        ear1Node.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(1,1,1),
                                        tr.scale(1,1,4)])
        ear1Node.childs = [gpuEar]
        ear2Node = sg.SceneGraphNode("ear2")
        ear2Node.transform = tr.matmul([tr.translate(0, -0.5, 0), tr.rotationX(np.pi), tr.scale(1,1,4)])
        ear2Node.childs = [gpuEar]
        
        pieceNode = sg.SceneGraphNode("piece")
        pieceNode.childs = [quadNode, ear1Node, ear2Node]
        piecesNode.childs += [pieceNode]
        
        PuzzlePiece = Puzzle()
        pieces += [PuzzlePiece]
        PuzzlePiece.set_controller(controller)
        PuzzlePiece.set_model(pieceNode)
        
    
    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.childs = [floorNode, skyNode, wallsNode1, wallsNode2]

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

        projection = tr.perspective(90, 1, 0.1, 100)

        view = tr.lookAt(
            controller.eye,
            controller.at,
            controller.up
        )

        
        if controller.change == False:
            laraNode.childs = [gpuLara1]
        if controller.change == True:
            laraNode.childs = [gpuLara2]
            
        Lara.set_model(laraNode)
        Lara.update()
        for PuzzlePiece in pieces:
            PuzzlePiece.update()
        Lara.collect(pieces)
        
        if Lara.collected == N:
            glfw.set_window_should_close(window, True)
        
        # Posicion de la fuente de luz
        lightposition = controller.at - 0.5*(controller.at - controller.eye)
        
        # Dibujar con el pipeline de ilumiacion de phong
        glUseProgram(normalTextureShaderProgram.shaderProgram)

        # Entregar a los shaders los coeficientes de iluminacion ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "La"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "Ld"), 0.3, 0.3, 0.3)
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "Ls"), 0.2, 0.2, 0.2)

        # Entregar a los shaders los coeficientes de reflexion de los objetos ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "Kd"), 0.3, 0.3, 0.3)
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "Ks"), 0.2, 0.2, 0.2)

        # Entregar valores a los shaders de la posicion de luz, posicion de camara y shininess
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        glUniform3f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "viewPosition"), controller.eye[0], controller.eye[1], controller.eye[2])
        glUniform1ui(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "shininess"), 10)
        
        # Entregar valores a los shaders los coeficientes de atenuacion
        glUniform1f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "constantAttenuation"), 0.0)
        glUniform1f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "quadraticAttenuation"), controller.light)

        # Entregar valores a los shaders de las matrices para la proyeccion de la camara
        glUniformMatrix4fv(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(normalTextureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        # Se dibujan los objetos
        sg.drawSceneGraphNode(sceneNode, normalTextureShaderProgram, "model")
        
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        # sg.drawSceneGraphNode(sceneNode, textureShaderProgram, "model")
        sg.drawSceneGraphNode(laraNode, textureShaderProgram, "model")
        
        glUseProgram(colorShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(piecesNode, colorShaderProgram, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuFloor.clear()
    gpuSky.clear()
    gpuWall.clear()
    gpuLara1.clear()
    gpuLara2.clear()
    
    glfw.terminate()
