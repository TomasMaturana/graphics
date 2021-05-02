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

def createTextureGPUShape(shape, pipeline, path, sWrapMode=GL_CLAMP_TO_EDGE, tWrapMode=GL_CLAMP_TO_EDGE, minFilterMode=GL_NEAREST, maxFilterMode=GL_NEAREST, fillusage=GL_STATIC_DRAW):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, fillusage)
    gpuShape.texture = es.textureSimpleSetup(
        path, sWrapMode, tWrapMode, minFilterMode, maxFilterMode)
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

def createSpriteShapes(quadTexX, quadTexY, pipeline, path, ximgs, yimgs):
    # Creamos una lista para guardar todas las gpu shapes necesarias
    shapes = []
    # Creamos una gpushape por cada frame de textura
    for j in range(yimgs):
        shapesY = []
        for i in range(ximgs):
            gpuPlayer = es.GPUShape().initBuffers()
            pipeline.setupVAO(gpuPlayer)

            shapePlayer = bs.createTextureQuadXY(quadTexX, quadTexY, i/ximgs, (i + 1)/ximgs, j/yimgs,(j + 1)/yimgs)

            gpuPlayer.fillBuffers(shapePlayer.vertices, shapePlayer.indices, GL_STATIC_DRAW)

            gpuPlayer.texture = es.textureSimpleSetup(path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

            shapesY.append(gpuPlayer)
        shapes.append(shapesY)
    return shapes


def createCar(pipeline):
    # Se crea la escena del auto de la pregunta 1

    # Se crean las shapes en GPU
    gpuChasis = createGPUShape(createColorChasis(0.7, 0, 0), pipeline) # Shape del chasis 
    gpuGrayCircle =  createGPUShape(createColorCircle(20, 0.4, 0.4, 0.4), pipeline) # Shape del circulo gris
    gpuBlackCircle =  createGPUShape(createColorCircle(20, 0, 0, 0), pipeline) # Shape del circulo negro
    gpuBlueQuad = createGPUShape(bs.createColorQuad(0.2, 0.2, 1), pipeline) # Shape de quad azul

    # Nodo del chasis rojo
    redChasisNode = sg.SceneGraphNode("redChasis")
    redChasisNode.childs = [gpuChasis]

    # Nodo del circulo gris
    grayCircleNode = sg.SceneGraphNode("grayCircleNode")
    grayCircleNode.childs = [gpuGrayCircle]
    
    # Nodo del circulo negro
    blackCircleNode = sg.SceneGraphNode("blackCircle")
    blackCircleNode.childs = [gpuBlackCircle]

    # Nodo del quad celeste
    blueQuadNode = sg.SceneGraphNode("blueQuad")
    blueQuadNode.childs = [gpuBlueQuad]

    # Nodo del circulo gris escalado
    scaledGrayCircleNode = sg.SceneGraphNode("slGrayCircle")
    scaledGrayCircleNode.transform = tr.scale(0.6, 0.6, 0.6)
    scaledGrayCircleNode.childs = [grayCircleNode]

    # Nodo de una rueda, escalado
    wheelNode = sg.SceneGraphNode("wheel")
    wheelNode.transform = tr.scale(0.22, 0.22, 0.22)
    wheelNode.childs = [blackCircleNode, scaledGrayCircleNode]

    # Nodo de la ventana, quad celeste escalado
    windowNode = sg.SceneGraphNode("window")
    windowNode.transform = tr.scale(0.22, 0.15, 1)
    windowNode.childs = [blueQuadNode]
     
    # Rueda izquierda posicionada
    leftWheel = sg.SceneGraphNode("lWheel")
    leftWheel.transform = tr.translate(-0.3, -0.2, 0)
    leftWheel.childs = [wheelNode]

    # Rueda derecha posicionada
    rightWheel = sg.SceneGraphNode("rWheel")
    rightWheel.transform = tr.translate(0.26, -0.2, 0)
    rightWheel.childs = [wheelNode]

    # Ventana posicionada
    translateWindow = sg.SceneGraphNode("tlWindow")
    translateWindow.transform = tr.translate(-0.08, 0.06, 0.0)
    translateWindow.childs = [windowNode]

    # Nodo padre auto
    carNode = sg.SceneGraphNode("car")
    carNode.childs = [redChasisNode, translateWindow, leftWheel, rightWheel]

    return carNode


def createScene(pipeline):
    # Funcion que crea la escena de la pregunta 2

    # Se crean las shapes en GPU
    gpuGrayQuad = createGPUShape(bs.createColorQuadXY(0.6, 0.6, 0.6), pipeline) # gray street shape
    gpuWhiteQuad = createGPUShape(bs.createColorQuadXY(1,1,1), pipeline) # white paint for street shape, 
    gpuBrownQuad = createGPUShape(bs.createColorQuadXY(0.5,0.3,0.1), pipeline) # tree trunk shape, roof store shape
    gpuGreenCircle = createGPUShape(createColorCircle(30, 0.4, 0.8, 0.1), pipeline) # green three leaves shape
    gpuLightBlueQuad = createGPUShape(bs.createColorQuadXY(0.65,0.9,1), pipeline) # window and door store shape 
    gpuApricotQuad = createGPUShape(bs.createColorQuadXY(1,0.7,0.4), pipeline) # store wall shape 
    gpuLightGrayQuad = createGPUShape(bs.createColorQuadXY(0.8, 0.8, 0.8), pipeline) # gray metal shape
    gpuGreenQuad = createGPUShape(bs.createColorQuadXY(0.4, 1, 0.4), pipeline) # green quad shape

    # TREE ###########################################################################################################
    # tree leaves node 1
    leavesNode1 = sg.SceneGraphNode("leaves1")
    leavesNode1.transform = tr.matmul([tr.translate(0, 0.4, 0), tr.scale(0.5, 0.5, 1)])
    leavesNode1.childs = [gpuGreenCircle]

    # tree leaves node 2
    leavesNode2 = sg.SceneGraphNode("leaves2")
    leavesNode2.transform = tr.matmul([tr.translate(-0.2, 0.05, 0), tr.scale(0.5, 0.5, 1)])
    leavesNode2.childs = [gpuGreenCircle]

    # tree leaves node 3
    leavesNode3 = sg.SceneGraphNode("leaves3")
    leavesNode3.transform = tr.matmul([tr.translate(0.2, 0.05, 0), tr.scale(0.5, 0.5, 1)])
    leavesNode3.childs = [gpuGreenCircle]

    # tree trunk node
    trunkNode = sg.SceneGraphNode("trunk")
    trunkNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.3, 1, 1)])
    trunkNode.childs = [gpuBrownQuad]

    # tree node
    treeNode = sg.SceneGraphNode("tree")
    treeNode.transform = tr.matmul([tr.translate(0.9, 0.8, 0), tr.scale(0.2, 0.4, 1)])
    treeNode.childs = [trunkNode, leavesNode1, leavesNode2, leavesNode3]   

    # STREET ##########################################################################################################
    # asphalt node
    asphaltNode = sg.SceneGraphNode("asphalt")
    asphaltNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.5, 2, 1)])
    asphaltNode.childs = [gpuGrayQuad]

    # street center paint node 1
    asphaltPaintNode1 = sg.SceneGraphNode("asphaltPaint1")
    asphaltPaintNode1.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.01, 0.7, 1)])
    asphaltPaintNode1.childs = [gpuWhiteQuad]

    # street center paint node 2
    asphaltPaintNode2 = sg.SceneGraphNode("asphaltPaint2")
    asphaltPaintNode2.transform = tr.matmul([tr.translate(0, 0.8, 0), tr.scale(0.01, 0.7, 1)])
    asphaltPaintNode2.childs = [gpuWhiteQuad]

    # street center paint node 3
    asphaltPaintNode3 = sg.SceneGraphNode("asphaltPaint3")
    asphaltPaintNode3.transform = tr.matmul([tr.translate(0, -0.8, 0), tr.scale(0.01, 0.7, 1)])
    asphaltPaintNode3.childs = [gpuWhiteQuad]

    # street limit paint node 1
    asphaltLimitNode1 = sg.SceneGraphNode("asphaltLimit1")
    asphaltLimitNode1.transform = tr.matmul([tr.translate(0.25, 0, 0), tr.scale(0.015, 2, 1)])
    asphaltLimitNode1.childs = [gpuWhiteQuad]

    # street limit paint node 2
    asphaltLimitNode2 = sg.SceneGraphNode("asphaltLimit2")
    asphaltLimitNode2.transform = tr.matmul([tr.translate(-0.25, 0, 0), tr.scale(0.015, 2, 1)])
    asphaltLimitNode2.childs = [gpuWhiteQuad]

    # street node 1
    streetNode1 = sg.SceneGraphNode("street")
    streetNode1.transform = tr.matmul([tr.translate(0.5, 0, 0), tr.scale(1.2, 1, 1)])
    streetNode1.childs = [asphaltNode, asphaltPaintNode1, asphaltPaintNode2, asphaltPaintNode3, asphaltLimitNode1, asphaltLimitNode2]

    # street node 2
    streetNode2 = sg.SceneGraphNode("street")
    streetNode2.transform = tr.matmul([tr.translate(-0.4, 0, 0), tr.scale(1.2, 1, 1)])
    streetNode2.childs = [asphaltNode, asphaltPaintNode1, asphaltPaintNode2, asphaltPaintNode3, asphaltLimitNode1, asphaltLimitNode2]

    # STORE ################################################################################################
    # store window node
    windowNode = sg.SceneGraphNode("window")
    windowNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.5, 0.65, 1)])
    windowNode.childs = [gpuLightBlueQuad]

    # store metal structure node 1
    metalStructureNode1 = sg.SceneGraphNode("metalStructure1")
    metalStructureNode1.transform = tr.matmul([tr.translate(0, 0.2, 0), tr.scale(0.5, 0.02, 1)])
    metalStructureNode1.childs = [gpuLightGrayQuad]

    # store metal structure node 2
    metalStructureNode2 = sg.SceneGraphNode("metalStructure2")
    metalStructureNode2.transform = tr.matmul([tr.translate(0, -0.2, 0), tr.scale(0.5, 0.02, 1)])
    metalStructureNode2.childs = [gpuLightGrayQuad]

    # store metal structure node 3
    metalStructureNode3 = sg.SceneGraphNode("metalStructure3")
    metalStructureNode3.transform = tr.matmul([tr.translate(0.1, 0, 0), tr.scale(0.3, 0.02, 1)])
    metalStructureNode3.childs = [gpuLightGrayQuad]

    # store metal structure node 4
    metalStructureNode4 = sg.SceneGraphNode("metalStructure4")
    metalStructureNode4.transform = tr.matmul([tr.translate(-0.05, 0, 0), tr.scale(0.02, 0.4, 1)])
    metalStructureNode4.childs = [gpuLightGrayQuad]

    # store metal structure node 5
    metalStructureNode5 = sg.SceneGraphNode("metalStructure5")
    metalStructureNode5.transform = tr.matmul([tr.translate(0.25, 0, 0), tr.scale(0.02, 1, 1)])
    metalStructureNode5.childs = [gpuLightGrayQuad]
    
    # store wall node
    wallNode = sg.SceneGraphNode("wall")
    wallNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.5, 1, 1)])
    wallNode.childs = [gpuApricotQuad]

    # store facade
    facadeNode = sg.SceneGraphNode("facade")
    facadeNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(1, 1, 1)])
    facadeNode.childs = [wallNode, windowNode, metalStructureNode1, metalStructureNode2, metalStructureNode3, metalStructureNode4, metalStructureNode5]

    # store roof node 1
    roofNode1 = sg.SceneGraphNode("roof1")
    roofNode1.transform = tr.matmul([tr.translate(-0.25, 0.1, 0), tr.scale(0.2, 1, 1), tr.shearing(0, 0.2, 0, 0, 0, 0)])
    roofNode1.childs = [gpuBrownQuad]

    # store roof node 2
    roofNode2 = sg.SceneGraphNode("roof2")
    roofNode2.transform = tr.matmul([tr.translate(-0.25, -0.1, 0), tr.scale(0.2, 1, 1), tr.shearing(0, -0.2, 0, 0, 0, 0)])
    roofNode2.childs = [gpuBrownQuad]

    # store name back node
    nameBackNode = sg.SceneGraphNode("nameBack")
    nameBackNode.transform = tr.matmul([tr.translate(-0.25, 0, 0), tr.scale(0.15, 0.9, 1)])
    nameBackNode.childs = [gpuWhiteQuad]

    # store name back green node
    greenNameBackNode = sg.SceneGraphNode("greenNameBack")
    greenNameBackNode.transform = tr.matmul([tr.translate(-0.3, 0, 0), tr.scale(0.05, 0.9, 1)])
    greenNameBackNode.childs = [gpuGreenQuad]

    # roof node
    roofNode = sg.SceneGraphNode("roof")
    roofNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(1, 1, 1)])
    roofNode.childs = [roofNode1, roofNode2, nameBackNode, greenNameBackNode]

    # store node
    storeNode = sg.SceneGraphNode("store")
    storeNode.transform = tr.matmul([tr.translate(-0.83, 0.3, 0), tr.scale(0.5, 1, 1)])
    storeNode.childs = [facadeNode, roofNode]

    # Nodo del cielo, quad celeste escalado
    # skyNode = sg.SceneGraphNode("sky")
    # skyNode.transform = tr.scale(2, 2, 1)
    # skyNode.childs = [gpuBlueQuad]

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
    # backGroundNode = sg.SceneGraphNode("background")
    # backGroundNode.childs = [skyNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [streetNode1, streetNode2, treeNode, storeNode]

    return sceneNode



