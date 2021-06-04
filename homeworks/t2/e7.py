
# coding=utf-8
"""plotting a 2d function as a surface"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


def fun1(x, y, a, b):
    return np.cos(x)-15

def fun2(x, y, a, b):
    return np.cos(y)

def fun3(x, y, a, b):
    return (np.cos(y/10)+np.cos(x/10))*15


def fun(x, y, a, b):
    if abs(y)>40:
        return np.sin(y/20)*15
    else:
        return np.cos(y*np.sin(x/50))+np.cos(x/50)+5




def generateMesh(xs, ys, function, color):

    vertices = []
    indices = []

    # We generate a vertex for each sample x,y,z
    for i in range(len(xs)):
        for j in range(len(ys)):
            x = xs[i]
            y = ys[j]
            z = function(x, y)
            p1=np.array([x,y,z])

            x0 = xs[i-1]
            y0 = ys[j-1]
            z0 = function(x0, y0)
            p0=np.array([x0,y0,z0])

            x2 = xs[(i+1)%len(xs)]
            y2 = ys[(j+1)%len(ys)]
            z2 = function(x2, y2)
            p2=np.array([x2,y2,z2])
            
            #N=np.cross((p1-p0),(p2-p0))/np.linalg.norm(np.cross((p1-p0),(p2-p0)))

            vertices += [x, y, z] + [z*color[0]/35,z*color[1]/35,z*color[2]/35] #+ [N[0],N[1],N[2]]

    # The previous loops generates full columns j-y and then move to
    # the next i-x. Hence, the index for each vertex i,j can be computed as
    index = lambda i, j: i*len(ys) + j 
    
    # We generate quads for each cell connecting 4 neighbor vertices
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):

            # Getting indices for all vertices in this quad
            isw = index(i,j)
            ise = index(i+1,j)
            ine = index(i+1,j+1)
            inw = index(i,j+1)

            # adding this cell's quad as 2 triangles
            indices += [
                isw, ise, ine,
                ine, inw, isw
            ]

    return bs.Shape(vertices, indices)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 900
    height = 900
    title = "Height Plotter"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    flatPipeline = es.SimpleModelViewProjectionShaderProgram()    #ls.SimpleFlatShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(flatPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    flatPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    meshCurve = lambda x, y: fun(x, y, 1.0, 1.0)

    # generate a numpy array with 40 samples between -10 and 10
    xs = np.ogrid[-50:50:1]
    ys = np.ogrid[-50:50:1]
    cpuSurface = generateMesh(xs, ys, meshCurve, [1,1,0])
    gpuSurface = es.GPUShape().initBuffers()
    flatPipeline.setupVAO(gpuSurface)
    gpuSurface.fillBuffers(cpuSurface.vertices, cpuSurface.indices, GL_STATIC_DRAW)

    t0 = glfw.get_time()
    camera_theta = np.pi/7

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        # Setting up the view transform

        camX = 40 * np.sin(camera_theta)
        camY = 40 * np.cos(camera_theta)

        viewPos = np.array([camX, camY, 40])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,5]),
            np.array([0,0,1])
        )

        # Setting all uniform shader variables

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "lightPosition"), 10, 10, 2)
        glUniform3f(glGetUniformLocation(flatPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(flatPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(flatPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(flatPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(flatPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(flatPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
        glUniformMatrix4fv(glGetUniformLocation(flatPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniformMatrix4fv(glGetUniformLocation(flatPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        pipeline.drawCall(gpuAxis, GL_LINES)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing shapes with different model transformations
        glUniformMatrix4fv(glGetUniformLocation(flatPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(0.5))
        pipeline.drawCall(gpuSurface)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuSurface.clear()
    gpuAxis.clear()

    glfw.terminate()
