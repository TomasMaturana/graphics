""" Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg

def createGPUShape(pipeline, shape):
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

def createTaco(pipeline):
    quad = createTextureGPUShape(bs.createTextureQuad(1 ,1), pipeline, "sprites/wood.jpg")
    quadNode = sg.SceneGraphNode("quad")
    quadNode.transform =tr.matmul([
        tr.translate(0.005,-0.9,0.0),
        tr.scale(0.02,0.8,0.4),
        tr.shearing(-0.5, 0, 0, 0, 0, 0)
    ])
    quadNode.childs = [quad]

    quadNode2 = sg.SceneGraphNode("quad")
    quadNode2.transform =tr.matmul([
        tr.translate(-0.005,-0.9,0.0),
        tr.scale(0.02,0.8,0.4),
        tr.shearing(0.5, 0, 0, 0, 0, 0)
    ])
    quadNode2.childs = [quad]

    # Nodo del objeto escalado con el mismo valor de la escena base
    scaledQuad = sg.SceneGraphNode("sc_quad")
    scaledQuad.childs = [quadNode, quadNode2]

    return scaledQuad

def createShadowNode(pipeline):
    # Funcion para crear Grafo de una esfera texturizada de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    gpuBlackCircle = createGPUShape(pipeline, bs.createRGBCircle(50, 0.5, 0.5, 0.5)) 

    blackCircleNode = sg.SceneGraphNode("blackCircle")
    blackCircleNode.childs = [gpuBlackCircle]

    shadowNode = sg.SceneGraphNode("shadow")
    shadowNode.childs = [blackCircleNode]

    return shadowNode

def createScene(pipeline):
    # Se crea la escena base

    # Se crean las shapes en GPU
    gpuRedCube = createGPUShape(pipeline, bs.createColorNormalsCube(1, 0, 0)) # Shape del cubo rojo
    gpuGreenCube = createGPUShape(pipeline, bs.createColorNormalsCube(0, 1, 0)) # Shape del cubo verde
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.7, 0.7, 0.7)) # Shape del cubo gris
    gpuBrownCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.6, 0.2, 0.2)) # Shape del cubo café
    gpuBlackCircle = createGPUShape(pipeline, bs.createRGBCircle(50, 0.0, 0.0, 0.0)) 

    # Nodo del cubo rojo
    redCubeNode = sg.SceneGraphNode("redCube")
    redCubeNode.childs = [gpuRedCube]

    # Nodo del cubo verde
    greenCubeNode = sg.SceneGraphNode("greenCube")
    greenCubeNode.childs = [gpuGreenCube]

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del círculo negro
    blackCircleNode = sg.SceneGraphNode("blackCircle")
    blackCircleNode.childs = [gpuBlackCircle]

    # Nodo del cubo café
    brownCubeNode = sg.SceneGraphNode("brownCube")
    brownCubeNode.childs = [gpuBrownCube]
    
    # Nodo de la pared derecha de color rojo
    rightWallNode = sg.SceneGraphNode("rightWall")
    rightWallNode.transform = tr.matmul([tr.translate(3, 0, 0), tr.scale(3, 3, 3)])
    rightWallNode.childs = [redCubeNode]

    # Nodo de la pared izquierda de color rojo
    leftWallNode = sg.SceneGraphNode("leftWall")
    leftWallNode.transform = tr.matmul([tr.translate(-3, 0, 0), tr.scale(3, 3, 3)])
    leftWallNode.childs = [redCubeNode]

    # Nodo de la pared de fondo de color rojo
    backWallNode = sg.SceneGraphNode("backWall")
    backWallNode.transform = tr.matmul([tr.translate(0, -3, 0), tr.scale(3, 3, 3)])
    backWallNode.childs = [redCubeNode]

    # Nodo de la pared de frente de color rojo
    frontWallNode = sg.SceneGraphNode("frontWall")
    frontWallNode.transform = tr.matmul([tr.translate(0, 3, 0), tr.scale(3, 3, 3)])
    frontWallNode.childs = [redCubeNode]

    # Nodo del cubo que representa la fuente de luz (no genera la iluminacion)
    lightNode = sg.SceneGraphNode("lightSource")
    lightNode.transform = tr.matmul([tr.translate(0, 0, 0.4), tr.scale(0.12, 0.12, 0.12)])
    lightNode.childs = [grayCubeNode]

    # Nodo del cielo del techo de color gris
    ceilNode = sg.SceneGraphNode("ceil")
    ceilNode.transform = tr.matmul([tr.translate(0, 0, 3), tr.scale(3, 3, 3)])
    ceilNode.childs = [grayCubeNode, lightNode]

    # Nodo del suelo de color café
    floorNode = sg.SceneGraphNode("floor")
    floorNode.transform = tr.matmul([tr.translate(0, 0, -2), tr.scale(3, 3, 3)])
    floorNode.childs = [brownCubeNode]

    # Nodo de hoyo 1
    holeNode1 = sg.SceneGraphNode("hole1")
    holeNode1.transform = tr.matmul([tr.translate(0.445, 0.44, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode1.childs = [blackCircleNode]

    # Nodo de hoyo 2
    holeNode2 = sg.SceneGraphNode("hole2")
    holeNode2.transform = tr.matmul([tr.translate(0, 0.45, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode2.childs = [blackCircleNode]

    # Nodo de hoyo 3
    holeNode3 = sg.SceneGraphNode("hole3")
    holeNode3.transform = tr.matmul([tr.translate(0, -0.45, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode3.childs = [blackCircleNode]

    # Nodo de hoyo 4
    holeNode4 = sg.SceneGraphNode("hole4")
    holeNode4.transform = tr.matmul([tr.translate(0.445, -0.44, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode4.childs = [blackCircleNode]

    # Nodo de hoyo 5
    holeNode5 = sg.SceneGraphNode("hole5")
    holeNode5.transform = tr.matmul([tr.translate(-0.445, 0.44, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode5.childs = [blackCircleNode]

    # Nodo de hoyo 6
    holeNode6 = sg.SceneGraphNode("hole6")
    holeNode6.transform = tr.matmul([tr.translate(-0.445, -0.44, 0.51), tr.scale(0.04, 0.08, 1)])
    holeNode6.childs = [blackCircleNode]

    # Nodo de la superficie de pool verde
    fieldNode = sg.SceneGraphNode("field")
    fieldNode.transform = tr.matmul([tr.translate(0, 0, -0.25), tr.scale(1.5, 0.75, 0.1)])
    fieldNode.childs = [greenCubeNode, holeNode1, holeNode2, holeNode3, holeNode4, holeNode5, holeNode6]

    # Nodo de amortiguador1
    am1Node = sg.SceneGraphNode("am1")
    am1Node.transform = tr.matmul([tr.translate(0.33, 0.35, -0.2), tr.scale(0.6, 0.05, 0.05)])
    am1Node.childs = [greenCubeNode]

    # Nodo de amortiguador2
    am2Node = sg.SceneGraphNode("am2")
    am2Node.transform = tr.matmul([tr.translate(0.33, -0.35, -0.2), tr.scale(0.6, 0.05, 0.05)])
    am2Node.childs = [greenCubeNode]

    # Nodo de amortiguador3
    am3Node = sg.SceneGraphNode("am3")
    am3Node.transform = tr.matmul([tr.translate(-0.33, 0.35, -0.2), tr.scale(0.6, 0.05, 0.05)])
    am3Node.childs = [greenCubeNode]

    # Nodo de amortiguador4
    am4Node = sg.SceneGraphNode("am4")
    am4Node.transform = tr.matmul([tr.translate(-0.33, -0.35, -0.2), tr.scale(0.6, 0.05, 0.05)])
    am4Node.childs = [greenCubeNode]

    # Nodo de amortiguador5
    am5Node = sg.SceneGraphNode("am5")
    am5Node.transform = tr.matmul([tr.translate(0.7, 0, -0.2), tr.scale(0.05, 0.6, 0.05)])
    am5Node.childs = [greenCubeNode]

    # Nodo de amortiguador6
    am6Node = sg.SceneGraphNode("am6")
    am6Node.transform = tr.matmul([tr.translate(-0.7, 0, -0.2), tr.scale(0.05, 0.6, 0.05)])
    am6Node.childs = [greenCubeNode]

    # Nodo de borde1
    edge1Node = sg.SceneGraphNode("edge1")
    edge1Node.transform = tr.matmul([tr.translate(0, 0.4, -0.25), tr.scale(1.6, 0.1, 0.2)])
    edge1Node.childs = [brownCubeNode]

    # Nodo de borde2
    edge2Node = sg.SceneGraphNode("edge2")
    edge2Node.transform = tr.matmul([tr.translate(0, -0.4, -0.25), tr.scale(1.6, 0.1, 0.2)])
    edge2Node.childs = [brownCubeNode]

    # Nodo de borde3
    edge3Node = sg.SceneGraphNode("edge3")
    edge3Node.transform = tr.matmul([tr.translate(0.75, 0, -0.25), tr.scale(0.1, 0.9, 0.2)])
    edge3Node.childs = [brownCubeNode]

    # Nodo de borde4
    edge4Node = sg.SceneGraphNode("edge4")
    edge4Node.transform = tr.matmul([tr.translate(-0.75, 0, -0.25), tr.scale(0.1, 0.9, 0.2)])
    edge4Node.childs = [brownCubeNode]

    # Nodo de la mesa de pool 
    tableNode = sg.SceneGraphNode("table")
    tableNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(1, 1, 1)])
    tableNode.childs = [fieldNode, am1Node, am2Node, am3Node, am4Node, am5Node, am6Node, edge1Node, edge2Node, edge3Node, edge4Node]

    # Nodo de la escena para realizar un escalamiento
    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(10, 10, 10)])
    sceneNode.childs = [rightWallNode, leftWallNode, frontWallNode, backWallNode, ceilNode, floorNode, tableNode]

    # Nodo final de la escena 
    trSceneNode = sg.SceneGraphNode("tr_scene")
    trSceneNode.childs = [sceneNode]

    return trSceneNode

def createCube1(pipeline):
    # Funcion para crear Grafo de un objeto de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del cubo escalado 
    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(0.25,-0.15,-0.25),
        tr.rotationZ(np.pi*0.15),
        tr.scale(0.2,0.2,0.5)
    ])
    objectNode.childs = [grayCubeNode]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createCube2(pipeline):
    # Funcion para crear Grafo de un objeto de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5)) # Shape del cubo gris

    # Nodo del cubo gris
    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    # Nodo del cubo escalado 
    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(-0.25,-0.15,-0.35),
        tr.rotationZ(np.pi*-0.2),
        tr.scale(0.3,0.3,0.3)
    ])
    objectNode.childs = [grayCubeNode]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createColorNormalSphere(N, r, g, b):
    # Funcion para crear una esfera con normales

    vertices = []           # lista para almacenar los verices
    indices = []            # lista para almacenar los indices
    dTheta = 2 *np.pi /N   # angulo que hay entre cada iteracion de la coordenada theta
    dPhi = 2 * np.pi /N     # angulo que hay entre cada iteracion de la coordenada phi
    rho = 0.5               # radio de la esfera
    c = 0                   # contador de vertices, para ayudar a indicar los indices

    # Se recorre la coordenada theta
    for i in range(int(N/2)):
        theta = i * dTheta # angulo theta en esta iteracion
        theta1 = (i + 1) * dTheta # angulo theta en la iteracion siguiente
        # Se recorre la coordenada phi
        for j in range(N):
            phi = j*dPhi # angulo phi en esta iteracion
            phi1 = (j+1)*dPhi # angulo phi en la iteracion siguiente

            # Se crean los vertices necesarios son coordenadas esfericas para cada iteracion

            # Vertice para las iteraciones actuales de theta (i) y phi (j) 
            v0 = [rho*np.sin(theta)*np.cos(phi), rho*np.sin(theta)*np.sin(phi), rho*np.cos(theta)]
            # Vertice para las iteraciones siguiente de theta (i + 1) y actual de phi (j) 
            v1 = [rho*np.sin(theta1)*np.cos(phi), rho*np.sin(theta1)*np.sin(phi), rho*np.cos(theta1)]
            # Vertice para las iteraciones actual de theta (i) y siguiente de phi (j + 1) 
            v2 = [rho*np.sin(theta1)*np.cos(phi1), rho*np.sin(theta1)*np.sin(phi1), rho*np.cos(theta1)]
            # Vertice para las iteraciones siguientes de theta (i + 1) y phi (j + 1) 
            v3 = [rho*np.sin(theta)*np.cos(phi1), rho*np.sin(theta)*np.sin(phi1), rho*np.cos(theta)]
            
            # Se crean los vectores normales para cada vertice segun los valores de rho tongo 
            n0 = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
            n1 = [np.sin(theta1)*np.cos(phi), np.sin(theta1)*np.sin(phi), np.cos(theta1)]
            n2 = [np.sin(theta1)*np.cos(phi1), np.sin(theta1)*np.sin(phi1), np.cos(theta1)]
            n3 = [np.sin(theta)*np.cos(phi1), np.sin(theta)*np.sin(phi1), np.cos(theta)]


            # Creamos los triangulos superiores
            #        v0
            #       /  \
            #      /    \
            #     /      \
            #    /        \
            #   /          \
            # v1 ---------- v2
            if i == 0:
                #           vertices              color    normales
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], r, g, b, n2[0], n2[1], n2[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3

            # Creamos los triangulos inferiores
            # v0 ---------- v3
            #   \          /
            #    \        /
            #     \      /
            #      \    /
            #       \  /
            #        v1
            elif i == (N-1):
                #           vertices              color    normales
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v3[0], v3[1], v3[2], r, g, b, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            
            # Creamos los quads intermedios
            #  v0 -------------- v3
            #  | \                |
            #  |    \             |
            #  |       \          |
            #  |          \       |
            #  |             \    |
            #  |                \ |
            #  v1 -------------- v2
            else: 
                #           vertices              color    normales
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], r, g, b, n2[0], n2[1], n2[2]]
                vertices += [v3[0], v3[1], v3[2], r, g, b, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c + 2 ]
                indices += [ c + 2, c + 3, c + 0 ]
                c += 4
    return bs.Shape(vertices, indices)

def createTextureNormalSphere(N):
    # Funcion para crear una esfera con normales y texturizada

    vertices = []           # lista para almacenar los verices
    indices = []            # lista para almacenar los indices
    dTheta = 2*np.pi /N   # angulo que hay entre cada iteracion de la coordenada theta
    dPhi = 2 * np.pi /N     # angulo que hay entre cada iteracion de la coordenada phi
    rho = 0.5               # radio de la esfera
    c = 0                   # contador de vertices, para ayudar a indicar los indices

    # Se recorre la coordenada theta
    for i in range(int(N/2)):
        theta = i * dTheta # angulo theta en esta iteracion
        theta1 = (i + 1) * dTheta # angulo theta en la iteracion siguiente
         # Se recorre la coordenada phi
        for j in range(N):
            phi = j*dPhi # angulo phi en esta iteracion
            phi1 = (j+1)*dPhi # angulo phi en la iteracion siguiente

            # Se crean los vertices necesarios son coordenadas esfericas para cada iteracion

            # Vertice para las iteraciones actuales de theta (i) y phi (j) 
            v0 = [rho*np.sin(theta)*np.cos(phi), rho*np.sin(theta)*np.sin(phi), rho*np.cos(theta)]
            # Vertice para las iteraciones siguiente de theta (i + 1) y actual de phi (j) 
            v1 = [rho*np.sin(theta1)*np.cos(phi), rho*np.sin(theta1)*np.sin(phi), rho*np.cos(theta1)]
            # Vertice para las iteraciones actual de theta (i) y siguiente de phi (j + 1) 
            v2 = [rho*np.sin(theta1)*np.cos(phi1), rho*np.sin(theta1)*np.sin(phi1), rho*np.cos(theta1)]
            # Vertice para las iteraciones siguientes de theta (i + 1) y phi (j + 1) 
            v3 = [rho*np.sin(theta)*np.cos(phi1), rho*np.sin(theta)*np.sin(phi1), rho*np.cos(theta)]

            # Se crean los vectores normales para cada vertice segun los valores de rho tongo 
            n0 = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
            n1 = [np.sin(theta1)*np.cos(phi), np.sin(theta1)*np.sin(phi), np.cos(theta1)]
            n2 = [np.sin(theta1)*np.cos(phi1), np.sin(theta1)*np.sin(phi1), np.cos(theta1)]
            n3 = [np.sin(theta)*np.cos(phi1), np.sin(theta)*np.sin(phi1), np.cos(theta)]

            
            # Creamos los quads 
            #  v0 -------------- v3
            #  | \                |
            #  |    \             |
            #  |       \          |
            #  |          \       |
            #  |             \    |
            #  |                \ |
            #  v1 -------------- v2
                #           vertices           UV coord                      normales
            vertices += [v0[0], v0[1], v0[2], phi/(2*np.pi), theta/(np.pi), n0[0], n0[1], n0[2]]
            vertices += [v1[0], v1[1], v1[2], phi/(2*np.pi), theta1/(np.pi), n1[0], n1[1], n1[2]]
            vertices += [v2[0], v2[1], v2[2], phi1/(2*np.pi), theta1/(np.pi), n2[0], n2[1], n2[2]]
            vertices += [v3[0], v3[1], v3[2], phi1/(2*np.pi), theta/(np.pi), n3[0], n3[1], n3[2]]
            indices += [ c + 0, c + 1, c +2 ]
            indices += [ c + 2, c + 3, c + 0 ]
            c += 4

    return bs.Shape(vertices, indices)


def createSphereNode(r, g, b, pipeline):
    # Funcion para crear Grafo de una esfera de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    sphere = createGPUShape(pipeline, createColorNormalSphere(20, r,g,b)) # Shape de la esfera

    # Nodo de la esfera trasladado y escalado
    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(0.25,0.15,-0.35),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [sphere]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere

def createTexSphereNode(pipeline, num=""):
    # Funcion para crear Grafo de una esfera texturizada de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    sphere = createTextureGPUShape(createTextureNormalSphere(40), pipeline, "sprites/b" + num + ".png") # Shape de la esfera texturizada

    rotNode = sg.SceneGraphNode("rot")
    rotNode.childs = [sphere]
    # Nodo de la esfera trasladado y escalado
    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(-0.0,0.0,-0.0),
        tr.scale(0.4,0.4,0.4)
    ])
    sphereNode.childs = [rotNode]

    # Nodo del objeto escalado con el mismo valor de la escena base
    scaledSphere = sg.SceneGraphNode("sc_sphere"+num)
    scaledSphere.childs = [sphereNode]

    return scaledSphere