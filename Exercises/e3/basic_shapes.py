
# coding=utf-8
"""vertices and indices for a variety of simple shapes"""

import math

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]


def applyOffset(shape, stride, offset):

    numberOfVertices = len(shape.vertices)//stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):

    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]


def createAxis(length=1.0):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions        colors
        -length,  0.0,  0.0, 0.0, 0.0, 0.0,
         length,  0.0,  0.0, 1.0, 0.0, 0.0,

         0.0, -length,  0.0, 0.0, 0.0, 0.0,
         0.0,  length,  0.0, 0.0, 1.0, 0.0,

         0.0,  0.0, -length, 0.0, 0.0, 0.0,
         0.0,  0.0,  length, 0.0, 0.0, 1.0]

    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
         0, 1,
         2, 3,
         4, 5]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)
    
    
def createExpansiveGrayQuad(r, g, b, e):

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
         0.0,  0.0, 0.0,  r, g, b,
        -1.0, -1.0, 0.0,  e, e, e,
         1.0, -1.0, 0.0,  e, e, e,
         1.0,  1.0, 0.0,  e, e, e,
        -1.0,  1.0, 0.0,  e, e, e]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 2, 3,
         0, 3, 4,
         0, 4, 1]

    return Shape(vertices, indices)



def createRGBCircle(N, rad,r,g,b):

    # First vertex at the center
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            rad * math.cos(theta), rad * math.sin(theta), 0, r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)
    

def createRGBCircle2(N, rad,r,g,b):

    # First vertex at the center
    # vertices = [rad* math.cos(N), rad* math.cos(N), 0, r, g, b]
    vertices = []
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            rad * math.cos(theta), rad * math.sin(theta), 0, r, g, b]

        # A triangle is created using the center, this and the next vertex
        if(i):
            indices += [i-1, i]

    # The final triangle connects back to the second vertex
    indices += [N-1, 0]

    return Shape(vertices, indices)
    
    
def createRGBCircle3(N, rad,r,g,b):
    if(N%2==1):
        N-=1
    # First vertex at the center
    # vertices = [rad* math.cos(N), rad* math.cos(N), 0, r, g, b]
    vertices = []
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        if(i%2==0):
            theta = i * dtheta
            
            vertices += [
                # vertex coordinates
                rad * math.cos(theta), rad * math.sin(theta), 0, r, g, b]
            
            # Index
            if(i):
                indices += [i-2, i-1]

    # The final 
    # indices += [N-2, 0]

    return Shape(vertices, indices)

