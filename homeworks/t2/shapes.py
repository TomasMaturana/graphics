"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
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


def createSpriteShapes(quadTexX, quadTexY, pipeline, path, ximgs, yimgs):
    # a list to save all needed gpushapes
    shapes = []
    # one gpushape per texture frame
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



