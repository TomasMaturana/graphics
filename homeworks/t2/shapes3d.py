"""Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import openmesh as om

# Convenience function to ease initialization
def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path, glMode=GL_CLAMP_TO_EDGE):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, glMode, glMode, GL_LINEAR, GL_LINEAR)
    return gpuShape

def createScene(pipeline):

    gpuRedCube = createGPUShape(pipeline, bs.createColorNormalsCube(1, 0, 0))
    gpuGreenCube = createGPUShape(pipeline, bs.createColorNormalsCube(0, 1, 0))
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.7, 0.7, 0.7))
    gpuWhiteCube = createGPUShape(pipeline, bs.createColorNormalsCube(1, 1, 1))

    redCubeNode = sg.SceneGraphNode("redCube")
    redCubeNode.childs = [gpuRedCube]

    greenCubeNode = sg.SceneGraphNode("greenCube")
    greenCubeNode.childs = [gpuGreenCube]

    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    whiteCubeNode = sg.SceneGraphNode("whiteCube")
    whiteCubeNode.childs = [gpuWhiteCube]

    rightWallNode = sg.SceneGraphNode("rightWall")
    rightWallNode.transform = tr.translate(1, 0, 0)
    rightWallNode.childs = [redCubeNode]

    leftWallNode = sg.SceneGraphNode("leftWall")
    leftWallNode.transform = tr.translate(-1, 0, 0)
    leftWallNode.childs = [greenCubeNode]

    backWallNode = sg.SceneGraphNode("backWall")
    backWallNode.transform = tr.translate(0,-1, 0)
    backWallNode.childs = [grayCubeNode]

    lightNode = sg.SceneGraphNode("lightSource")
    lightNode.transform = tr.matmul([tr.translate(0, 0, -0.4), tr.scale(0.12, 0.12, 0.12)])
    lightNode.childs = [grayCubeNode]

    ceilNode = sg.SceneGraphNode("ceil")
    ceilNode.transform = tr.translate(0, 0, 1)
    ceilNode.childs = [grayCubeNode, lightNode]

    floorNode = sg.SceneGraphNode("floor")
    floorNode.transform = tr.translate(0, 0, -1)
    floorNode.childs = [grayCubeNode]

    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(5, 5, 5)])
    sceneNode.childs = [rightWallNode, leftWallNode, backWallNode, ceilNode, floorNode]

    trSceneNode = sg.SceneGraphNode("tr_scene")
    trSceneNode.childs = [sceneNode]

    return trSceneNode

def createCube1(pipeline):
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5))

    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(0.25,-0.15,-0.25),
        tr.rotationZ(np.pi*0.15),
        tr.scale(0.2,0.2,0.5)
    ])
    objectNode.childs = [grayCubeNode]

    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createCube2(pipeline):
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.5, 0.5, 0.5))

    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    objectNode = sg.SceneGraphNode("object1")
    objectNode.transform = tr.matmul([
        tr.translate(-0.25,-0.15,-0.35),
        tr.rotationZ(np.pi*-0.2),
        tr.scale(0.3,0.3,0.3)
    ])
    objectNode.childs = [grayCubeNode]

    scaledObject = sg.SceneGraphNode("object1")
    scaledObject.transform = tr.scale(5, 5, 5)
    scaledObject.childs = [objectNode]

    return scaledObject

def createColorNormalSphere(N, r, g, b):

    vertices = []
    indices = []
    dTheta = 2 * np.pi /N
    dPhi = 2 * np.pi /N
    r = 0.5
    c = 0

    for i in range(N - 1):
        theta = i * dTheta
        theta1 = (i + 1) * dTheta
        for j in range(N):
            phi = j*dPhi
            phi1 = (j+1)*dPhi
            v0 = [r*np.sin(theta)*np.cos(phi), r*np.sin(theta)*np.sin(phi), r*np.cos(theta)]
            v1 = [r*np.sin(theta1)*np.cos(phi), r*np.sin(theta1)*np.sin(phi), r*np.cos(theta1)]
            v2 = [r*np.sin(theta1)*np.cos(phi1), r*np.sin(theta1)*np.sin(phi1), r*np.cos(theta1)]
            v3 = [r*np.sin(theta)*np.cos(phi1), r*np.sin(theta)*np.sin(phi1), r*np.cos(theta)]
            n0 = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
            n1 = [np.sin(theta1)*np.cos(phi), np.sin(theta1)*np.sin(phi), np.cos(theta1)]
            n2 = [np.sin(theta1)*np.cos(phi1), np.sin(theta1)*np.sin(phi1), np.cos(theta1)]
            n3 = [np.sin(theta)*np.cos(phi1), np.sin(theta)*np.sin(phi1), np.cos(theta)]


            # Creamos los quad superiores
            if i == 0:
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], r, g, b, n2[0], n2[1], n2[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            # Creamos los quads inferiores
            elif i == (N-2):
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v3[0], v3[1], v3[2], r, g, b, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            
            # Creamos los quads intermedios
            else: 
                vertices += [v0[0], v0[1], v0[2], r, g, b, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], r, g, b, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], r, g, b, n2[0], n2[1], n2[2]]
                vertices += [v3[0], v3[1], v3[2], r, g, b, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                indices += [ c + 2, c + 3, c + 0 ]
                c += 4
    return bs.Shape(vertices, indices)

def createTextureNormalSphere(N):
    vertices = []
    indices = []
    dTheta = 2 * np.pi /N
    dPhi = 2 * np.pi /N
    r = 0.5
    c = 0

    for i in range(N - 1):
        theta = i * dTheta
        theta1 = (i + 1) * dTheta
        for j in range(N):
            phi = j*dPhi
            phi1 = (j+1)*dPhi
            v0 = [r*np.sin(theta)*np.cos(phi), r*np.sin(theta)*np.sin(phi), r*np.cos(theta)]
            v1 = [r*np.sin(theta1)*np.cos(phi), r*np.sin(theta1)*np.sin(phi), r*np.cos(theta1)]
            v2 = [r*np.sin(theta1)*np.cos(phi1), r*np.sin(theta1)*np.sin(phi1), r*np.cos(theta1)]
            v3 = [r*np.sin(theta)*np.cos(phi1), r*np.sin(theta)*np.sin(phi1), r*np.cos(theta)]
            n0 = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
            n1 = [np.sin(theta1)*np.cos(phi), np.sin(theta1)*np.sin(phi), np.cos(theta1)]
            n2 = [np.sin(theta1)*np.cos(phi1), np.sin(theta1)*np.sin(phi1), np.cos(theta1)]
            n3 = [np.sin(theta)*np.cos(phi1), np.sin(theta)*np.sin(phi1), np.cos(theta)]


            # Creamos los quad superiores
            if i == 0:
                vertices += [v0[0], v0[1], v0[2], 0, 1, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], 1, 1, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], 0.5, 0, n2[0], n2[1], n2[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            # Creamos los quads inferiores
            elif i == (N-2):
                vertices += [v0[0], v0[1], v0[2], 0, 0, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], 0.5, 1, n1[0], n1[1], n1[2]]
                vertices += [v3[0], v3[1], v3[2], 1, 0, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            
            # Creamos los quads intermedios
            else: 
                vertices += [v0[0], v0[1], v0[2], 0, 0, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], 0, 1, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], 1, 1, n2[0], n2[1], n2[2]]
                vertices += [v3[0], v3[1], v3[2], 0, 1, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                indices += [ c + 2, c + 3, c + 0 ]
                c += 4
    return bs.Shape(vertices, indices)

def createSphereNode(r, g, b, pipeline):
    sphere = createGPUShape(pipeline, createColorNormalSphere(20, r,g,b))

    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(0.25,0.15,-0.35),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [sphere]

    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere

def createTexSphereNode(pipeline):
    sphere = createTextureGPUShape(createTextureNormalSphere(20), pipeline, "img/stone.png")

    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(-0.25,0.25,-0.35),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [sphere]

    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere

######################################################################################################

def createTextureMesh(npyZMesh, npyTexIndex, N):
    # Creamos una malla de triangulos
    texMesh = om.TriMesh()
    nh=int(N/2)
    texNum = 1/12

    # Generamos un vertice para cada x,y,z
    for i in range(N):
        for j in range(N):
            z = npyZMesh[i, j]
            
            # Agregamos el vertice a la malla
            texMesh.add_vertex(np.array([i-nh, j-nh, z]))

    # Podemos calcular el indice de cada punto (i,j) de la siguiente manera
    index = lambda i, j: i*N + j 
    
    # Obtenemos los vertices, y agregamos las caras
    vertexs = list(texMesh.vertices())

    # Creamos caras para cada cuadrado de la malla
    for i in range(N-1):
        for j in range(N-1):

            # Conseguimos los indices por cada cuadrado
            v0 = index(i,j)
            v1 = index(i+1,j)
            v2 = index(i+1,j+1)
            v3 = index(i,j+1)

            texMesh.add_face(vertexs[v0], vertexs[v1], vertexs[v2])
            texMesh.add_face(vertexs[v2], vertexs[v3], vertexs[v0])
            texMesh.set_texcoord2D(vertexs[v0], [texNum*npyTexIndex[i,j], 0.0])
            texMesh.set_texcoord2D(vertexs[v1], [texNum*npyTexIndex[i,j]+texNum, 0.0])
            texMesh.set_texcoord2D(vertexs[v2], [texNum*npyTexIndex[i,j]+texNum, 1.1])
            texMesh.set_texcoord2D(vertexs[v3], [texNum*npyTexIndex[i,j], 1.1])

    return texMesh


def createTexNodes(pipeline, npyMesh, N, texture_path):
    groundMesh = createTextureMesh(npyMesh[0], npyMesh[2], N)
    skyMesh = createTextureMesh(npyMesh[1], npyMesh[3], N)
    groundMeshShape = createTextureGPUShape(meshToShape(groundMesh, textured=True), pipeline, texture_path, glMode=GL_REPEAT)
    skyMeshShape = createTextureGPUShape(meshToShape(skyMesh, textured=True), pipeline, texture_path, glMode=GL_REPEAT)

    groundNode = sg.SceneGraphNode("ground")
    groundNode.transform =tr.matmul([
        tr.translate(0,0,0),
        tr.scale(1,1,1)
    ])
    groundNode.childs = [groundMeshShape]

    skyNode = sg.SceneGraphNode("sky")
    skyNode.transform =tr.matmul([
        tr.translate(0,0,0),
        tr.scale(1,1,1)
    ])
    skyNode.childs = [skyMeshShape]

    caveNode = sg.SceneGraphNode("cave")
    caveNode.transform = tr.scale(1, 1, 1)
    caveNode.childs = [groundNode, skyNode]

    return caveNode, groundMesh, skyMesh


def meshToShape(mesh, color=None, textured=False, verbose=False):
    assert isinstance(mesh, om.TriMesh)
    assert (color != None) != textured, "The mesh will be colored or textured, only one of these need to be specified."

    # Requesting normals per face
    mesh.request_face_normals()

    # Requesting normals per vertex
    mesh.request_vertex_normals()

    # Computing all requested normals
    mesh.update_normals()

    # You can also update specific normals
    #mesh.update_face_normals()
    #mesh.update_vertex_normals()
    #mesh.update_halfedge_normals()

    # At this point, we are sure we have normals computed for each face.
    assert mesh.has_face_normals()

    vertices = []
    indices = []

    # To understand how iteraors and circulators works in OpenMesh, check the documentation at:
    # https://www.graphics.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/blob/master/docs/iterators.rst

    def extractCoordinates(numpyVector3):
        assert len(numpyVector3) == 3
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]
        return [x,y,z]

    # This is inefficient, but it works!
    # You can always optimize it further :)

    # Checking each face
    for faceIt in mesh.faces():
        faceId = faceIt.idx()
        if verbose: print("face: ", faceId)

        # Checking each vertex of the face
        for faceVertexIt in mesh.fv(faceIt):
            faceVertexId = faceVertexIt.idx()

            # Obtaining the position and normal of each vertex
            vertex = mesh.point(faceVertexIt)
            normal = mesh.normal(faceVertexIt)
            if verbose: print("vertex ", faceVertexId, "-> position: ", vertex, " normal: ", normal)

            x, y, z = extractCoordinates(vertex)
            nx, ny, nz = extractCoordinates(normal)

            if textured:
                assert mesh.has_vertex_texcoords2D()

                texcoords = mesh.texcoord2D(faceVertexIt)
                tx = texcoords[0]
                ty = texcoords[1]
                
                vertices += [x, y, z, tx, ty, nx, ny, nz]
                indices += [len(vertices)//8 - 1]
            else:
                assert color != None

                r = color[0]
                g = color[1]
                b = color[2]

                vertices += [x, y, z, r, g, b, nx, ny, nz]
                indices += [len(vertices)//9 - 1]
        
        if verbose: print()

    return bs.Shape(vertices, indices)

def get_vertexs_and_indexes(mesh):
    # Obtenemos las caras de la malla
    faces = mesh.faces()

    # Creamos una lista para los vertices e indices
    vertexs = []

    # Obtenemos los vertices y los recorremos
    for vertex in mesh.points():
        vertexs += vertex.tolist()
        # Agregamos un color al azar
        vertexs += [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]

    indexes = []

    for face in faces:
        # Obtenemos los vertices de la cara
        face_indexes = mesh.fv(face)
        for vertex in face_indexes:
            # Obtenemos el numero de indice y lo agregamos a la lista
            indexes += [vertex.idx()]

    return vertexs, indexes

def z_in_pos(mesh, x, y, N=100):
    index = lambda i, j: i*N + j 
    nh = int(N/2)
    vertexs = list(mesh.vertices())
    if (-nh < int(x) <nh) and (-nh < int(y) <nh):
        i=index((int(x)+nh), (int(y)+nh))
        v = vertexs[i]
        z = mesh.point(v)[2]
        print([x,y,z])
        return z+1
    else:
        return False

    # mesh_faces = mesh.faces()

    # for face in mesh_faces:
    #     # Obtenemos los vertices de la cara
    #     face_vertexes = list(mesh.fv(face))

    #     # Obtenemos las posiciones de los 3 vertices
    #     first_vertex = mesh.point(face_vertexes[0]).tolist()
    #     second_vertex = mesh.point(face_vertexes[1]).tolist()
    #     third_vertex = mesh.point(face_vertexes[2]).tolist()

    #     # Revisamos si alguno de los vertices esta en el rango buscado, devolvemos face si esta dentro del rango
    #     if (first_vertex[0] <= x <= second_vertex[0]) or (first_vertex[0] <= second_vertex[axis] <= first_vertex[0]) or (
    #             first_vertex[0] <= third_vertex[axis] <= first_vertex[0]):
    #             return face
    
    # return False

def createNPYTextureShape(npyMesh, N):
    #mesh = createTextureMesh(npyMesh, N)
    #vertexs, indexes = get_vertexs_and_indexes(mesh)
    vertices = []
    indices = []
    # dTheta = 2 * np.pi /N
    # dPhi = 2 * np.pi /N
    # r = 0.5
    c = 0
    nh=int(N/2)

    for i in range(N-1):
        # theta = i * dTheta
        # theta1 = (i + 1) * dTheta
        for j in range(N-1):
            # phi = j*dPhi
            # phi1 = (j+1)*dPhi
            v0 = np.array([i-nh, j-nh, npyMesh[i, j]])
            v1 = np.array([i-nh+1, j-nh, npyMesh[i+1, j]])
            v2 = np.array([i-nh+1, j-nh+1, npyMesh[i+1, j+1]])
            v3 = np.array([i-nh, j-nh+1, npyMesh[i, j+1]])
            n1=np.cross((v1-v0),(v2-v0))/np.linalg.norm(np.cross((v1-v0),(v2-v0)))
            #n2=np.cross((v2-v1),(v3-v1))/np.linalg.norm(np.cross((v2-p1),(v3-v1)))

            
            vertices += [v0[0], v0[1], v0[2], 0, 0, n1[0], n1[1], n1[2]]
            vertices += [v1[0], v1[1], v1[2], 0, 1, n1[0], n1[1], n1[2]]
            vertices += [v2[0], v2[1], v2[2], 1, 1, n1[0], n1[1], n1[2]]
            vertices += [v3[0], v3[1], v3[2], 0, 1, n1[0], n1[1], n1[2]]
            indices += [ c + 0, c + 1, c +2 ]
            indices += [ c + 2, c + 3, c + 0 ]
            c += 4
    return bs.Shape(vertices, indices)

def createNPYTexNodes(pipeline, npyMesh, N, texture_path1, texture_path2):
    groundMeshShape = createTextureGPUShape(createNPYTextureShape(npyMesh[0], N), pipeline, texture_path1)
    skyMeshShape = createTextureGPUShape(createNPYTextureShape(npyMesh[1], N), pipeline, texture_path2)

    groundNode = sg.SceneGraphNode("ground")
    groundNode.transform =tr.matmul([
        tr.translate(0,0,-5),
        tr.scale(0.3,0.3,0.3)
    ])
    groundNode.childs = [groundMeshShape]

    skyNode = sg.SceneGraphNode("sky")
    skyNode.transform =tr.matmul([
        tr.translate(0,0,-5),
        tr.scale(0.3,0.3,0.3)
    ])
    skyNode.childs = [skyMeshShape]

    caveNode = sg.SceneGraphNode("cave")
    caveNode.transform = tr.scale(1, 1, 1)
    caveNode.childs = [groundNode, skyNode]

    return caveNode

