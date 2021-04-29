"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createColorTriangle(r, g, b):
    # Funcion para crear un triangulo con un color personalizado

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.0,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)

def createColorCircle(N, r, g, b):
    # Funcion para crear un circulo con un color personalizado
    # Poligono de N lados 

    # First vertex at the center, white color
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return bs.Shape(vertices, indices)

def createPlayerShape(shape, pipeline, path, ximgs, yimgs):
    # Creamos una lista para guardar todas las gpu shapes necesarias
    shapes = []
    # Creamos una gpushape por cada frame de textura
    for j in range(yimgs):
        shapesY = []
        for i in range(ximgs):
            gpuPlayer = es.GPUShape().initBuffers()
            pipeline.setupVAO(gpuPlayer)

            shapePlayer = bs.createTextureQuad2(i/ximgs, (i + 1)/ximgs, j/yimgs,(j + 1)/yimgs)

            gpuPlayer.fillBuffers(shapePlayer.vertices, shapePlayer.indices, GL_STATIC_DRAW)

            gpuPlayer.texture = es.textureSimpleSetup(path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

            shapesY.append(gpuPlayer)
        shapes.append(shapesY)
    return shapes


# def createCar(pipeline):
#     # Se crea la escena del auto de la pregunta 1

#     # Se crean las shapes en GPU
#     gpuChasis = createGPUShape(createColorChasis(0.7, 0, 0), pipeline) # Shape del chasis 
#     gpuGrayCircle =  createGPUShape(createColorCircle(20, 0.4, 0.4, 0.4), pipeline) # Shape del circulo gris
#     gpuBlackCircle =  createGPUShape(createColorCircle(20, 0, 0, 0), pipeline) # Shape del circulo negro
#     gpuBlueQuad = createGPUShape(bs.createColorQuad(0.2, 0.2, 1), pipeline) # Shape de quad azul

#     # Nodo del chasis rojo
#     redChasisNode = sg.SceneGraphNode("redChasis")
#     redChasisNode.childs = [gpuChasis]

#     # Nodo del circulo gris
#     grayCircleNode = sg.SceneGraphNode("grayCircleNode")
#     grayCircleNode.childs = [gpuGrayCircle]
    
#     # Nodo del circulo negro
#     blackCircleNode = sg.SceneGraphNode("blackCircle")
#     blackCircleNode.childs = [gpuBlackCircle]

#     # Nodo del quad celeste
#     blueQuadNode = sg.SceneGraphNode("blueQuad")
#     blueQuadNode.childs = [gpuBlueQuad]

#     # Nodo del circulo gris escalado
#     scaledGrayCircleNode = sg.SceneGraphNode("slGrayCircle")
#     scaledGrayCircleNode.transform = tr.scale(0.6, 0.6, 0.6)
#     scaledGrayCircleNode.childs = [grayCircleNode]

#     # Nodo de una rueda, escalado
#     wheelNode = sg.SceneGraphNode("wheel")
#     wheelNode.transform = tr.scale(0.22, 0.22, 0.22)
#     wheelNode.childs = [blackCircleNode, scaledGrayCircleNode]

#     # Nodo de la ventana, quad celeste escalado
#     windowNode = sg.SceneGraphNode("window")
#     windowNode.transform = tr.scale(0.22, 0.15, 1)
#     windowNode.childs = [blueQuadNode]
     
#     # Rueda izquierda posicionada
#     leftWheel = sg.SceneGraphNode("lWheel")
#     leftWheel.transform = tr.translate(-0.3, -0.2, 0)
#     leftWheel.childs = [wheelNode]

#     # Rueda derecha posicionada
#     rightWheel = sg.SceneGraphNode("rWheel")
#     rightWheel.transform = tr.translate(0.26, -0.2, 0)
#     rightWheel.childs = [wheelNode]

#     # Ventana posicionada
#     translateWindow = sg.SceneGraphNode("tlWindow")
#     translateWindow.transform = tr.translate(-0.08, 0.06, 0.0)
#     translateWindow.childs = [windowNode]

#     # Nodo padre auto
#     carNode = sg.SceneGraphNode("car")
#     carNode.childs = [redChasisNode, translateWindow, leftWheel, rightWheel]

#     return carNode

def createCar(pipeline):
    # Se crea la escena del auto de la pregunta 1

    # Se crean las shapes en GPU
    gpuGrayCircle =  createGPUShape(createColorCircle(20, 0.4, 0.4, 0.4), pipeline) # Shape del circulo gris
    gpuBlackCircle =  createGPUShape(createColorCircle(20, 0, 0, 0), pipeline) # Shape del circulo negro
    gpuBlueQuad = createGPUShape(bs.createColorQuad(0.2, 0.2, 1), pipeline) # Shape de quad azul

    # Nodo del quad celeste
    blueQuadNode = sg.SceneGraphNode("blueQuad")
    blueQuadNode.childs = [gpuBlueQuad]

    # Nodo de la ventana, quad celeste escalado
    windowNode = sg.SceneGraphNode("window")
    windowNode.transform = tr.scale(0.22, 0.15, 1)
    windowNode.childs = [blueQuadNode]

    # Ventana posicionada
    translateWindow = sg.SceneGraphNode("tlWindow")
    translateWindow.transform = tr.translate(-0.08, 0.06, 0.0)
    translateWindow.childs = [windowNode]

    # Nodo padre auto
    carNode = sg.SceneGraphNode("car")
    carNode.childs = [translateWindow]

    return carNode

def createScene(pipeline):
    # Funcion que crea la escena de la pregunta 2

    # Se crean las shapes en GPU
    # gpuGreenTriangle = createGPUShape(createColorTriangle(0.125, 0.705, 0.094), pipeline) # Shape del triangulo verde
    # gpuGrayQuad = createGPUShape(bs.createColorQuad(0.6, 0.6, 0.6), pipeline) # Shape del quad gris
    # gpuBrownTriangle = createGPUShape(createColorTriangle(0.592, 0.329, 0.090), pipeline) # Shape del triangulo cafe
    # gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del quad blanco
    # gpuYellowCircle = createGPUShape(createColorCircle(20, 1, 1, 0), pipeline) # Shape del circulo amarillo
    gpuBlueQuad =  createGPUShape(bs.createColorQuad(0.4, 0.972, 1), pipeline) # Shape del quad azul

    # Nodo del cielo, quad celeste escalado
    skyNode = sg.SceneGraphNode("sky")
    skyNode.transform = tr.scale(2, 2, 1)
    skyNode.childs = [gpuBlueQuad]

    # # Nodo del sol, circulo amarillo escalado y posicionado
    # sunNode = sg.SceneGraphNode("sun")
    # sunNode.transform = tr.matmul([tr.translate(0.7, 0.6, 0), tr.scale(0.3, 0.3, 1)])
    # sunNode.childs = [gpuYellowCircle]

    # # Nodo de la montaña 1, triangulo verde escalado y posicionado
    # mountain1Node = sg.SceneGraphNode("mountain1")
    # mountain1Node.transform = tr.matmul([tr.translate(-0.5, -0.0, 0), tr.scale(2.4, 1, 1)])
    # mountain1Node.childs = [gpuGreenTriangle]

    # # Nodo de la montaña 2, triangulo verde escalado y posicionado
    # mountain2Node = sg.SceneGraphNode("mountain2")
    # mountain2Node.transform = tr.matmul([tr.translate(-0.1, 0, 0), tr.scale(2.2, 1.5, 1)])
    # mountain2Node.childs = [gpuGreenTriangle]

    # # Nodo de la montaña 3, triangulo verde escalado y posicionado
    # mountain3Node = sg.SceneGraphNode("mountain3")
    # mountain3Node.transform = tr.matmul([tr.translate(0.6, -0.28, 0), tr.scale(4, 1.3, 1)])
    # mountain3Node.childs = [gpuGreenTriangle]

    # # Nodo que agrupa a las montañas, posicionado
    # mountainsNode = sg.SceneGraphNode("mountains")
    # mountainsNode.transform = tr.matmul([tr.translate(0, -0.3, 0), tr.scale(1, 1, 1)])
    # mountainsNode.childs = [mountain1Node, mountain2Node, mountain3Node]

    # # Nodo2 que agrupa a las montañas, posicionado
    # mountainsNode2 = sg.SceneGraphNode("mountains2")
    # mountainsNode2.transform = tr.matmul([tr.translate(0, -0.3, 0), tr.scale(1, 1, 1)])
    # mountainsNode2.childs = [mountain1Node, mountain2Node, mountain3Node]

    # # Nodo3 que agrupa a las montañas, posicionado
    # mountainsNode3 = sg.SceneGraphNode("mountains3")
    # mountainsNode3.transform = tr.matmul([tr.translate(0, -0.3, 0), tr.scale(1, 1, 1)])
    # mountainsNode3.childs = [mountain1Node, mountain2Node, mountain3Node]

    # # Nodo de la carretera, quad gris escalado y posicionado
    # highwayNode = sg.SceneGraphNode("highway")
    # highwayNode.transform = tr.matmul([tr.translate(0, -0.65, 0), tr.scale(2.0, 0.4, 1)])
    # highwayNode.childs = [gpuGrayQuad]

    # # Nodo del triangulo cafe escalado y posicionado
    # scaledTriangleNode = sg.SceneGraphNode("slTriangle")
    # scaledTriangleNode.transform = tr.matmul([tr.translate(0, 0.25, 0), tr.scale(0.2, 0.5, 1)])
    # scaledTriangleNode.childs = [gpuBrownTriangle]

    # # Nodo del triangulo rotado
    # rotatedTriangleNode = sg.SceneGraphNode("rtTriangle")
    # rotatedTriangleNode.transform = tr.rotationZ(math.pi)
    # rotatedTriangleNode.childs = [scaledTriangleNode]

    # # Nodo que junta los tringulos para hacer un aspa, luego se posiciona
    # bladeNode = sg.SceneGraphNode("blade")
    # bladeNode.transform = tr.translate(0, 0.5, 0)
    # bladeNode.childs = [scaledTriangleNode, rotatedTriangleNode]

    # # Nodo con un aspa rotada a la izquierda
    # rotatedBlade1Node = sg.SceneGraphNode("rtBlade1")
    # rotatedBlade1Node.transform = tr.rotationZ(2*math.pi/3)
    # rotatedBlade1Node.childs = [bladeNode]

    # # Nodo con un aspa rotada a la derecha
    # rotatedBlade2Node = sg.SceneGraphNode("rtBlade2")
    # rotatedBlade2Node.transform = tr.rotationZ(4*math.pi/3)
    # rotatedBlade2Node.childs = [bladeNode]

    # # Nodo rotor que juntas las aspas
    # scaleRotorNode = sg.SceneGraphNode("slRotor")
    # scaleRotorNode.transform = tr.scale(1,1,1)
    # scaleRotorNode.childs = [bladeNode, rotatedBlade1Node, rotatedBlade2Node]

    # # Nodo que contiene la rotacion del rotor
    # rotateRotorNode = sg.SceneGraphNode("rtRotor")
    # rotateRotorNode.transform = tr.rotationZ(0.5)
    # rotateRotorNode.childs = [scaleRotorNode]
    
    # # Nodo con el rotor posicionado
    # translateRotorNode = sg.SceneGraphNode("tlRotor")
    # translateRotorNode.transform = tr.translate(0, 0.5, 0)
    # translateRotorNode.childs = [rotateRotorNode]

    # # Nodo torre, quad gris escalado y posicionado
    # towerNode = sg.SceneGraphNode("tower")
    # towerNode.transform = tr.matmul([tr.translate(0, -0.7, 0), tr.scale(0.15, 2.4, 1)])
    # towerNode.childs = [gpuGrayQuad]

    # # Nodo del molino de viento escalado
    # windMillNode = sg.SceneGraphNode("windMill")
    # windMillNode.transform = tr.scale(0.2, 0.2, 1)
    # windMillNode.childs = [towerNode, translateRotorNode]
    
    # # Molino de viento 1 escalado y posicionado
    # translateWindMill1Node = sg.SceneGraphNode("windMill1")
    # translateWindMill1Node.transform = tr.matmul([tr.translate(-0.7,0.2,0), tr.scale(1.2, 1.2, 1.2)])
    # translateWindMill1Node.childs = [windMillNode]

    # # Molino de viento 2 escalado y posicionado
    # translateWindMill2Node = sg.SceneGraphNode("windMill2")
    # translateWindMill2Node.transform = tr.matmul([tr.translate(-0.3, 0.3, 0), tr.scale(0.7, 0.7, 0.7)])
    # translateWindMill2Node.childs = [windMillNode]

    # # Molino de viento 3 escalado y posicionado
    # translateWindMill3Node = sg.SceneGraphNode("windMill3")
    # translateWindMill3Node.transform = tr.matmul([tr.translate(0.2,0.3,0), tr.scale(1.8, 1.8, 1)])
    # translateWindMill3Node.childs = [windMillNode]

    # # Nodo que junta los molinos de la escena
    # windMillGroupNode = sg.SceneGraphNode("windMills")
    # windMillGroupNode.childs = [translateWindMill1Node, translateWindMill2Node, translateWindMill3Node]
    
    # # nodo de la linea de pista, quad blanco escalado y posicionado
    # lineNode = sg.SceneGraphNode("line")
    # lineNode.transform = tr.matmul([tr.translate(0, -0.65, 0), tr.scale(2, 0.02, 1)])
    # lineNode.childs = [gpuWhiteQuad]

    # # Nodo del background con todos los nodos anteriores
    # backGroundNode = sg.SceneGraphNode("background")
    # backGroundNode.childs = [skyNode, sunNode, mountainsNode, mountainsNode2, mountainsNode3, highwayNode, windMillGroupNode, lineNode]

    # Nodo del background con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [skyNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode



