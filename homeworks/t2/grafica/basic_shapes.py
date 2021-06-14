
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

import math

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName



def createTextureNormalsCubeX(image_filename, x0, x1, up):

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    x0, up,      0,0,1,
         0.5, -0.5,  0.5,    x1, up,      0,0,1,
         0.5,  0.5,  0.5,    x1, 0,        0,0,1,
        -0.5,  0.5,  0.5,    x0, 0,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    x0, up,      0,0,-1,
         0.5, -0.5, -0.5,    x1, up,      0,0,-1,
         0.5,  0.5, -0.5,    x1, 0,        0,0,-1,
        -0.5,  0.5, -0.5,    x0, 0,        0,0,-1,
       
    # X+          
         0.5, -0.5, -0.5,    x0, 1,        1,0,0,
         0.5,  0.5, -0.5,    x1, 1,        1,0,0,
         0.5,  0.5,  0.5,    x1, 0,        1,0,0,
         0.5, -0.5,  0.5,    x0, 0,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    x0, 1,        -1,0,0,
        -0.5,  0.5, -0.5,    x1, 1,        -1,0,0,
        -0.5,  0.5,  0.5,    x1, 0,        -1,0,0,
        -0.5, -0.5,  0.5,    x0, 0,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    x0, 1,        0,1,0,
         0.5,  0.5, -0.5,    x1, 1,        0,1,0,
         0.5,  0.5,  0.5,    x1, 0,        0,1,0,
        -0.5,  0.5,  0.5,    x0, 0,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    x0, 1,        0,-1,0,
         0.5, -0.5, -0.5,    x1, 1,        0,-1,0,
         0.5, -0.5,  0.5,    x1, 0,        0,-1,0,
        -0.5, -0.5,  0.5,    x0, 0,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices, image_filename)