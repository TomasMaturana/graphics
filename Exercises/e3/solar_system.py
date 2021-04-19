# coding=utf-8
"""Drawing solar system"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import basic_shapes as bs
import easy_shaders as es
import transformations as tr
import math

__author__ = "Daniel Calderon"
__license__ = "MIT"


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Solar System", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0, 0, 0, 1.0)

    # Creating shapes on GPU memory

    shapeSpace = bs.createExpansiveGrayQuad(0.5, 0.3, 0, 0.01)
    gpuSpace = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSpace)
    gpuSpace.fillBuffers(shapeSpace.vertices, shapeSpace.indices, GL_STATIC_DRAW)
    
    shapeSunShadow = bs.createRGBCircle2(100, 0.6, 1, 1, 1)
    gpuSunShadow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSunShadow)
    gpuSunShadow.fillBuffers(shapeSunShadow.vertices, shapeSunShadow.indices, GL_STATIC_DRAW)
    
    shapeSun = bs.createRGBCircle(100, 0.6, 0.9, 0.9, 0)
    gpuSun = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSun)
    gpuSun.fillBuffers(shapeSun.vertices, shapeSun.indices, GL_STATIC_DRAW)
    
    shapeSunFlames = bs.createRGBCircle(200, 0.6, 0.8, 0.4, 0)
    gpuSunFlames = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSunFlames)
    gpuSunFlames.fillBuffers(shapeSunFlames.vertices, shapeSunFlames.indices, GL_STATIC_DRAW)
    
    shapeEarthShadow = bs.createRGBCircle2(100, 0.3, 0, 0.8, 0)
    gpuEarthShadow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEarthShadow)
    gpuEarthShadow.fillBuffers(shapeEarthShadow.vertices, shapeEarthShadow.indices, GL_STATIC_DRAW)
    
    shapeEarth = bs.createRGBCircle(100, 0.3, 0, 0.1, 0.9)
    gpuEarth = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEarth)
    gpuEarth.fillBuffers(shapeEarth.vertices, shapeEarth.indices, GL_STATIC_DRAW)
    
    shapeEarthOrbit = bs.createRGBCircle3(200, 1.4, 1, 1, 1)
    gpuEarthOrbit = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuEarthOrbit)
    gpuEarthOrbit.fillBuffers(shapeEarthOrbit.vertices, shapeEarthOrbit.indices, GL_STATIC_DRAW)
    
    shapeMoonShadow = bs.createRGBCircle2(15, 0.1, 0.3, 0.3, 0.3)
    gpuMoonShadow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMoonShadow)
    gpuMoonShadow.fillBuffers(shapeMoonShadow.vertices, shapeMoonShadow.indices, GL_STATIC_DRAW)
    
    shapeMoon = bs.createRGBCircle(15, 0.1, 0.8, 0.8, 0.8)
    gpuMoon = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMoon)
    gpuMoon.fillBuffers(shapeMoon.vertices, shapeMoon.indices, GL_STATIC_DRAW)
    
    shapeMoonOrbit = bs.createRGBCircle3(200, 0.6, 1, 1, 1)
    gpuMoonOrbit = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMoonOrbit)
    gpuMoonOrbit.fillBuffers(shapeMoonOrbit.vertices, shapeMoonOrbit.indices, GL_STATIC_DRAW)

    # shapeQuad = bs.createRainbowQuad()
    # gpuQuad = es.GPUShape().initBuffers()
    # pipeline.setupVAO(gpuQuad)
    # gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Using the time as the theta parameter
        theta = glfw.get_time()
        
        
        # Space
        triangleTransform = tr.matmul([
            tr.uniformScale(1)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuSpace)
        
        
        # EarthOrbit
        triangleTransform = tr.matmul([
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuEarthOrbit, mode=GL_LINES)
        
        
        # MoonOrbit
        triangleTransform = tr.matmul([
            tr.translate(0.7 * math.cos(theta), 0.7 * math.sin(theta), 0),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuMoonOrbit, mode=GL_LINES)


        # Sun
        triangleTransform = tr.matmul([
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuSun)
        
        
        # SunFlames
        triangleTransform = tr.matmul([
            tr.rotationZ(0.3 * theta),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuSunFlames, mode=GL_LINES)
        
        
        # SunShadow
        triangleTransform = tr.matmul([
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuSunShadow, mode=GL_LINES)
        
        
        # Earth
        triangleTransform = tr.matmul([
            tr.translate(0.7 * math.cos(theta), 0.7 * math.sin(theta), 0),
            tr.rotationZ(2 * theta),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuEarth)
        
        
        # EarthShadow
        triangleTransform = tr.matmul([
            tr.translate(0.7 * math.cos(theta), 0.7 * math.sin(theta), 0),
            tr.rotationZ(2 * theta),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuEarthShadow, mode=GL_LINES)
        
        
        # Moon
        triangleTransform = tr.matmul([
            tr.translate(0.7 * math.cos(theta), 0.7 * math.sin(theta), 0),
            tr.translate(0.3 * math.cos(theta*2.718), 0.3 * math.sin(theta*2.718), 0),
            tr.rotationZ(2 * theta),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuMoon)
        
        
        # MoonShadow
        triangleTransform = tr.matmul([
            tr.translate(0.7 * math.cos(theta), 0.7 * math.sin(theta), 0),
            tr.translate(0.3 * math.cos(theta*2.718), 0.3 * math.sin(theta*2.718), 0),
            tr.rotationZ(2 * theta),
            tr.uniformScale(0.5)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        # drawing function
        pipeline.drawCall(gpuMoonShadow, mode=GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuSpace.clear()
    gpuSun.clear()
    gpuSunShadow.clear()
    gpuSunFlames.clear()
    gpuEarth.clear()
    gpuEarthShadow.clear()
    gpuEarthOrbit.clear()
    gpuMoon.clear()
    gpuMoonShadow.clear()
    gpuMoonOrbit.clear()
    
    glfw.terminate()