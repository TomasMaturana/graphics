# coding=utf-8
"""Textures and transformations in 3D"""

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

__author__ = "Daniel Calderon"
__license__ = "MIT"

############################################################################
########################################################################################################################################################
def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def createShip(pipeline):
    # Se crean las shapes en GPU
    gpuShip = createGPUShape(createColorPyramid(0.4, 0.2, 0), pipeline) 
    gpuSail = createGPUShape(bs.createRGBTriangle(0.9, 0.9, 1), pipeline) 

    baseNode= sg.SceneGraphNode("base")
    baseNode.childs = [gpuShip]
    baseNode.transform = tr.rotationY(np.pi)
    
    sailNode= sg.SceneGraphNode("sail")
    sailNode.childs = [gpuSail]
    sailNode.transform = tr.matmul([tr.translate(0, 0.4, 0.25), tr.scale(0.5, 0.5, 1), tr.rotationY(np.pi/2)])

    # Node
    shipNode = sg.SceneGraphNode("ship")
    shipNode.childs = [baseNode, sailNode]
    return shipNode


def catmullRomMatrix(P1, P2, P3, P4):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, P3, P4), axis=1)
    
    # Hermite base matrix is a constant
    Mcr = (1/2)*np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])    
    
    return np.matmul(G, Mcr)


def evalCurve(N, plusY=0):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada

    # Puntos 
    P0 = np.array([[-7, -2+plusY, 0.02]]).T
    P1 = np.array([[-5, -4+plusY, 0.02]]).T
    P2 = np.array([[-1, -2+plusY, 0.02]]).T
    P3 = np.array([[1, 3+plusY, 0.02]]).T
    P4 = np.array([[5, 5+plusY, 0.02]]).T
    P5 = np.array([[7, 3+plusY, 0.02]]).T
    # Matrices de Hermite y Beziers
    H_cr1 = catmullRomMatrix(P0, P1, P2, P3)
    H_cr2 = catmullRomMatrix(P1, P2, P3, P4)
    H_cr3 = catmullRomMatrix(P2, P3, P4, P5)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N//3)
    offset = N//3 
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts) * 3, 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(H_cr1, T).T
        curve[i + offset, 0:3] = np.matmul(H_cr2, T).T
        curve[i + 2*offset, 0:3] = np.matmul(H_cr3, T).T
        
    return curve

def createColorRiver(r, g, b):
    # Crea un shape del chasis de un auto a partir de una curva personalizada
    vertices = []
    indices = []
    curve1 = evalCurve(96) # Se obtienen los puntos de la curva
    curve2 = evalCurve(96, plusY=1) # Se obtienen los puntos de la curva
    delta = 1 / len(curve1) # distancia del step /paso
    x_0 = -0.5 # Posicion x inicial de la recta inferior
    y_0 = -0.2 # Posicion y inicial de la recta inferior
    counter = 0 # Contador de vertices, para indicar los indices

    # Se generan los vertices
    for i in range(len(curve1)-1):
        c_0 = curve1[i] # punto i de la curva
        r_0 = curve2[i] # punto i de la recta
        c_1 = curve1[i + 1] # punto i + 1 de la curva
        r_1 = curve2[i+1] # punto i + 1 de la recta
        vertices += [c_0[0], c_0[1], 0, r + 0.2, g + 0.2, b + 0.2]
        vertices += [r_0[0], r_0[1], 0, r, g, b]
        vertices += [c_1[0], c_1[1], 0, r + 0.1, g + 0.1, b + 0.1]
        vertices += [r_1[0], r_1[1], 0, r, g, b]
        indices += [counter + 0, counter +1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    return bs.Shape(vertices, indices)


def createRiver(pipeline):
    # Se crean las shapes en GPU
    gpuRiver = createGPUShape(createColorRiver(0, 0.2, 0.9), pipeline) 

    # Node
    riverNode = sg.SceneGraphNode("river")
    riverNode.childs = [gpuRiver]
    return riverNode



########################################################################################################################################################
############################################################################

def createColorPyramid(r, g ,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, 0.5,  0,  r, g, b,
         0.5, -0.5, 0,  r, g, b,
         0.5, 0.5,  0,  r, g, b,
        -0.5, -0.5, 0,  r, g, b,
         0, 0,  0.5,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 1, 3,
         0, 2, 4,
         2, 4, 1,
         3, 4, 1,
         0, 4, 3]

    return bs.Shape(vertices, indices)

def create_tree(pipeline):
    # Piramide verde
    green_pyramid = createColorPyramid(0, 1, 0)
    gpuGreenPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreenPyramid)
    gpuGreenPyramid.fillBuffers(green_pyramid.vertices, green_pyramid.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_quad = bs.createColorCube(139/255, 69/255, 19/255)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brown_quad.vertices, brown_quad.indices, GL_STATIC_DRAW)

    # Tronco
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.scale(0.05, 0.05, 0.2)
    tronco.childs += [gpuBrownQuad]

    # Hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.uniformScale(0.25)])
    hojas.childs += [gpuGreenPyramid]

    # Arbol
    tree = sg.SceneGraphNode("arbol")
    tree.transform = tr.identity()
    tree.childs += [tronco, hojas]

    return tree


def create_house(pipeline):
    # Piramide cafe
    brown_pyramid = createColorPyramid(166/255, 112/255, 49/255)
    gpuBrownPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownPyramid)
    gpuBrownPyramid.fillBuffers(brown_pyramid.vertices, brown_pyramid.indices, GL_STATIC_DRAW)

    # Cubo rojo
    red_cube = bs.createColorCube(1, 0, 0)
    gpuRedCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRedCube)
    gpuRedCube.fillBuffers(red_cube.vertices, red_cube.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_cube = bs.createColorCube(166/255, 112/255, 49/255)
    gpuBrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownCube)
    gpuBrownCube.fillBuffers(brown_cube.vertices, brown_cube.indices, GL_STATIC_DRAW)

    # Techo
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.scale(0.2, 0.4, 0.2)])
    techo.childs += [gpuBrownPyramid]

    # Base
    base = sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.2, 0.4, 0.2)])
    base.childs += [gpuRedCube]

    # Puerta
    puerta = sg.SceneGraphNode("puerta")
    puerta.transform = tr.matmul([tr.translate(0, -0.2, 0), tr.scale(0.05, 0.001, 0.1)])
    puerta.childs += [gpuBrownCube]

    # Casa
    casa = sg.SceneGraphNode("house")
    casa.transform = tr.identity()
    casa.childs += [techo, base, puerta]

    return casa

def create_skybox(pipeline):
    shapeSky = bs.createTextureCube('paisaje.jfif')
    gpuSky = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath("paisaje2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    return skybox

def create_floor(pipeline):
    shapeFloor = bs.createTextureQuad(8, 8)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("grass.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

def create_decorations(pipeline):
    tree1 = create_tree(pipeline)
    tree1.transform = tr.translate(0.5, 0, 0)

    tree2 = create_tree(pipeline)
    tree2.transform = tr.translate(-0.5, 0, 0)

    tree3 = create_tree(pipeline)
    tree3.transform = tr.translate(0, -0.5, 0)

    tree4 = create_tree(pipeline)
    tree4.transform = tr.translate(-0.2, 0.5, 0)

    tree5 = create_tree(pipeline)
    tree5.transform = tr.translate(0.2, 0.5, 0)

    house = create_house(pipeline)
    house.transform = tr.translate(0, 0.5, 0)

    river = createRiver(pipeline)
    river.transform = tr.matmul([tr.translate(0, -0.3, 0.001), tr.scale(0.2, 0.15, 1)])

    decorations = sg.SceneGraphNode("decorations")
    decorations.transform = tr.identity()
    decorations.childs += [river, tree1, tree2, tree3, tree4, tree5, house]    

    return decorations


############################################################################

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.ship = False
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]
        self.at = [0, 1, 0.1]
        self.up = [0, 0, 1]
###########################################################


# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    if key == glfw.KEY_H:
        controller.ship = not controller.ship

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
###########################################################

    elif key == glfw.KEY_W:
        controller.eye += (controller.at - controller.eye) * 0.05
        controller.at += (controller.at - controller.eye) * 0.05
    elif key == glfw.KEY_D:
        controller.theta -= np.pi*0.05
    elif key == glfw.KEY_A:
        controller.theta += np.pi*0.05

###########################################################
    else:
        print('Unknown key')


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

###########################################################################################
    # Creating shapes on GPU memory

    decorations = create_decorations(colorShaderProgram)
    skybox = create_skybox(textureShaderProgram)
    floor = create_floor(textureShaderProgram)
    ship = createShip(colorShaderProgram)
    shipCurve = evalCurve(96, plusY=0.5)

###########################################################################################

    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
    stepStep=0
    curveStep=0

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

###########################################################################

        at_x = controller.eye[0] + np.cos(controller.theta)
        at_y = controller.eye[1] + np.sin(controller.theta)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        # Drawing (no texture)
        glUseProgram(colorShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(decorations, colorShaderProgram, "model")

        if controller.ship:
            if(stepStep==50):
                stepStep=0
                curveStep=(curveStep+1)%96
            ship.transform = tr.matmul([tr.translate(shipCurve[curveStep][0]*0.2, (shipCurve[curveStep][1]*0.15) -0.3, 0.03), tr.scale(0.1, 0.1, 0.1)])
            sg.drawSceneGraphNode(ship, colorShaderProgram, "model")
            stepStep+=1

        # Drawing dice (with texture, another shader program)
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(skybox, textureShaderProgram, "model")
        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")       

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
