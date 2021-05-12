# coding=utf-8
"""A simple scene graph class and functionality"""

from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.gpu_shape as gs


class SceneGraphNode:
    """
    A simple class to handle a scene graph
    Each node represents a group of objects
    Each leaf represents a basic figure (GPUShape)
    To identify each node properly, it MUST have a unique name
    """
    def __init__(self, name):
        self.name = name
        self.transform = tr.identity()
        self.childs = []

    def clear(self):
        """Freeing GPU memory"""

        for child in self.childs:
            child.clear()

            

def drawSceneGraphNode(node, pipeline, transformName, parentTransform=tr.identity(), mode=GL_TRIANGLES):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf, mode=mode)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform, mode=mode)

