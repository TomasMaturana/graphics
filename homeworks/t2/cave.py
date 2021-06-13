import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import grafica.scene_graph as sg
from shapes3d import *
from shapes import *
from model import *
import grafica.newLightShaders as nl
import sys

class Camera:
    def __init__(self):
        self.theta = np.pi
        self.eye = [0, 0, 0]
        self.at = [0, 0, 0]
        self.up = [0, 0, 1]
        self.viewMatrix = None

    def set_eye_at_simple(self, eye, at):
        self.eye=eye
        self.at=at

    def set_eye(self, delta, mesh, skyMesh):
        atEyeDiff = self.at - self.eye
        newEye = self.eye + (atEyeDiff * delta)
        newEye[2] = z_in_pos(mesh, int(newEye[0]), int(newEye[1]))

        # if sky - ground < lara height
        newSkyZ=z_in_pos(skyMesh, int(newEye[0]), int(newEye[1]))
        if (newSkyZ-newEye[2])<1:
           return False

        # if next z >> actual z
        if abs(newEye[2]-self.eye[2]) >1:
            return False

        newEye[2] = newEye[2] +0.5
        self.eye = newEye


    def set_at(self, delta, mesh):
        atEyeDiff = self.at - self.eye
        self.at += atEyeDiff * delta
        #self.at[1] += 0.001
        self.at[2] = z_in_pos(mesh, int(self.at[0]), int(self.at[1]))

    
    def set_up(self, up):
        self.up = up

    def set_theta(self, deltaT):
        self.theta += np.pi*deltaT


    def update_view(self):
        at_x = self.eye[0] + np.cos(self.theta)
        at_y = self.eye[1] + np.sin(self.theta)
        self.at = np.array([at_x, at_y, self.eye[2]])

        viewMatrix = tr.lookAt(
            self.eye,
            self.at,
            self.up
        )
        return viewMatrix

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True

        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False

        self.leftClickOn = False
        self.rightClickOn = False

        self.torch_lvl= 4

        self.camera = Camera()

        self.mousePos = (0.0, 0.0)

    def get_camera(self):
        return self.camera

    def on_key(self, window, key, scancode, action, mods):

        if key == glfw.KEY_UP:
            if action == glfw.PRESS:
                self.is_up_pressed = True
            elif action == glfw.RELEASE:
                self.is_up_pressed = False

        if key == glfw.KEY_DOWN:
            if action == glfw.PRESS:
                self.is_down_pressed = True
            elif action == glfw.RELEASE:
                self.is_down_pressed = False

        if key == glfw.KEY_RIGHT:
            if action == glfw.PRESS:
                self.is_right_pressed = True
            elif action == glfw.RELEASE:
                self.is_right_pressed = False

        if key == glfw.KEY_LEFT:
            if action == glfw.PRESS:
                self.is_left_pressed = True
            elif action == glfw.RELEASE:
                self.is_left_pressed = False
        
        if key == glfw.KEY_SPACE:
            if action == glfw.PRESS:
                self.fillPolygon = not self.fillPolygon

        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_LEFT_CONTROL:
            if action == glfw.PRESS:
                self.showAxis = not self.showAxis

        elif key == glfw.KEY_1:
            if action == glfw.PRESS:
                self.torch_lvl = 4

        elif key == glfw.KEY_2:
            if action == glfw.PRESS:
                self.torch_lvl = 2
        
        elif key == glfw.KEY_3:
            if action == glfw.PRESS:
                self.torch_lvl = 1

        elif key == glfw.KEY_0:
            if action == glfw.PRESS:
                self.torch_lvl = 15


    #Funcion que recibe el input para manejar la camara
    def update_camera(self, delta, mesh, skyMesh, doit=False):
        
        if self.mousePos[0]<750:
            self.camera.set_theta(0.4 * delta)
        if self.mousePos[0]<650:
            self.camera.set_theta(0.8 * delta)
        elif self.is_left_pressed or self.mousePos[0]<550:
            self.camera.set_theta(1.5 * delta)

        if self.mousePos[0]>850:
            self.camera.set_theta(-0.4 * delta)
        if self.mousePos[0]>950:
            self.camera.set_theta(-0.8 * delta)
        if self.is_right_pressed or self.mousePos[0]>1050:
            self.camera.set_theta(-1.5 * delta)

        if self.is_up_pressed or self.leftClickOn or doit:
            resEye=self.camera.set_eye(4 * delta, mesh, skyMesh)
            if resEye:
                self.camera.set_at(4 * delta, mesh)

        if self.is_down_pressed or self.rightClickOn:
            resEye=self.camera.set_eye(-4 * delta, mesh, skyMesh)
            if resEye:
                self.camera.set_at(-4 * delta, mesh)

def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)

def mouse_button_callback(window, button, action, mods):

    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    """

    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = True
            print("Mouse click - button 1")

        if (button == glfw.MOUSE_BUTTON_2):
            controller.rightClickOn = True
            print("Mouse click - button 2:")

    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = False
        if (button == glfw.MOUSE_BUTTON_2):
            controller.rightClickOn = False


if __name__ == "__main__":

    # save system arguments 
    map = np.load(sys.argv[1])
    texture_path = "img/"+sys.argv[2]
    N = int(sys.argv[3])

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1600
    height = 800
    title = "T2 A: Lara Jones"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

     # Different shader programs for different lighting strategies
    phongPipeline = nl.MultiplePhongShaderProgram()
    phongTexPipeline = nl.SimplePhongTextureDirectionalShaderProgram()

    ##############################################################################
    # tex_pipeline = es.SimpleTextureTransformShaderProgram()
    # player_shapes= createSpriteShapes(0.5, 0.5, tex_pipeline, "img/walk.png", 7, 1)
    # playerNode = sg.SceneGraphNode("player")
    # # player model instance
    # player = Player(1)
    # # Se indican las referencias del nodo y el controller al modelo
    # player.set_model(playerNode, player_shapes)
    # player.set_controller(controller)
    ##############################################################################


    # This shader program does not consider lighting
    #mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    #gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(4))

    # # gpuRedCube = createGPUShape(phongPipeline, bs.createColorNormalsCube(1,0,0))

    # # scene = createScene(phongPipeline)
    # # cube1 = createCube1(phongPipeline)
    # # cube2 = createCube2(phongPipeline)
    # # sphere = createSphereNode(0.3, 0.3, 0.3, phongPipeline)
    playerNode = createPlayerCube(phongTexPipeline, "img/walk.png")

    caveScene, groundMesh, skyMesh = createTexNodes(phongTexPipeline, map, N, texture_path)
    

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()
    r = 0.5
    g = 0
    b = 0.25
    print(sys.argv[1])
    camera=controller.get_camera()
    if sys.argv[1] == "map1.npy":
        controller.camera.set_eye_at_simple([10, -40, 7], [10, -40, 7])
    elif sys.argv[1] == "map2.npy":
        controller.camera.set_eye_at_simple([0, 0, 7], [0, 0, 7])

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        normalizedMousePos = (
            controller.mousePos[0] / width,
            controller.mousePos[1] / height
        )

        controller.update_camera(delta, groundMesh, skyMesh)
        camera = controller.get_camera()

        viewMatrix = camera.update_view()

        playerNode.transform = tr.matmul([
            tr.translate(camera.at[0], camera.at[1], camera.eye[2]),
            #tr.rotationZ(np.pi*0.15),
            tr.scale(1,1,1)
        ])

        # Setting up the projection transform
        projection = tr.perspective(90, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # The axis is drawn without lighting effects
        # if controller.showAxis:
        #     glUseProgram(mvpPipeline.shaderProgram)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #     mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #lightingPipeline = phongPipeline
        
        lightposition = np.array([camera.at[0], camera.at[1], camera.eye[2]])
        lightPoint = lightposition + 1*(lightposition - camera.eye)

        #r = np.abs(((0.5*t1+0.00) % 2)-1)
        #g = np.abs(((0.5*t1+0.33) % 2)-1)
        #b = np.abs(((0.5*t1+0.66) % 2)-1)

        # Setting all uniform shader variables
        
        # glUseProgram(lightingPipeline.shaderProgram)
        # # White light in all components: ambient, diffuse and specular.
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        # glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        # glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.01)
        # glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        # glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.05)

        # glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        # glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        # glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        # Drawing
        #sg.drawSceneGraphNode(scene, lightingPipeline, "model")
        #sg.drawSceneGraphNode(cube1, lightingPipeline, "model")
        #sg.drawSceneGraphNode(cube2, lightingPipeline, "model")
        #sg.drawSceneGraphNode(sphere, lightingPipeline, "model")
        
        glUseProgram(phongTexPipeline.shaderProgram)
        torch=controller.torch_lvl

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "La"), 1.0/torch, 1.0/torch, 1.0/torch)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "viewPosition"), lightPoint[0], lightPoint[1], lightposition[2])
        
        glUniform1ui(glGetUniformLocation(phongTexPipeline.shaderProgram, "shininess"), int(100/torch))
        
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        #sg.drawSceneGraphNode(tex_sphere, phongTexPipeline, "model")
        sg.drawSceneGraphNode(caveScene, phongTexPipeline, "model")

        # glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(playerNode, phongTexPipeline, "model")
        
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    #gpuAxis.clear()
    # gpuRedCube.clear()

    glfw.terminate()