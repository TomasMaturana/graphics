
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

import math

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def createColorQuadXY(r, g, b, x=1, y=1):
    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -x/2, -y/2, 0.0,  r, g, b,
         x/2, -y/2, 0.0,  r, g, b,
         x/2,  y/2, 0.0,  r, g, b,
        -x/2,  y/2, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuadXY(x, y, xi, xf, yi, yf):
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -x, -y, 0.0, xi, yf,
         x, -y, 0.0, xf, yf,
         x,  y, 0.0, xf, yi,
        -x,  y, 0.0, xi, yi]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)

def createColorTriangle(r, g, b):
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

    return Shape(vertices, indices)

def createColorCircle2(N, r,g,b, rad=0.5):
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

        # A triangle is created using this and the next vertex
        if(i):
            indices += [i-1, i]

    # The final connects back to the second vertex
    indices += [N-1, 0]

    return Shape(vertices, indices)