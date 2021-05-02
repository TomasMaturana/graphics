""" P3 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from model import *
import sys


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False
        self.glasses = 1
        self.humansOut = []
        self.zombiesOut = []
        self.humansIn = []
        self.zombiesIn = []
        self.gameover = 0  # -1: game over, 1: you won
        self.texScene = None


# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detectar la barra espaciadora, se activan las gafas detectoras
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.glasses = int((controller.glasses +1)%2)

    # Caso de detectar la barra espaciadora, se activan las gafas detectoras
    if key == glfw.KEY_ENTER and action ==glfw.PRESS:
        controller.gameover = "restarting"

    # Caso de detectar 0, se cambia el método de dibujo
    if key == glfw.KEY_0 and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 1800
    height = 900
    title = "T1A - Beauchefville"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # save system arguments 
    Z = int(sys.argv[1])
    H = int(sys.argv[2])
    T = int(sys.argv[3])
    P = float(sys.argv[4])

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    # principal scene graph
    mainScene = createScene(pipeline)

    # win scene graph
    youWin_shape= createTextureGPUShape(bs.createTextureQuadXY(1, 1, 0, 1, 0, 1), tex_pipeline, "sprites/trololo.png")
    youWinNode = sg.SceneGraphNode("win")
    youWinNode.childs = [youWin_shape]

    # game over scene graph
    gameOver_shape= createTextureGPUShape(bs.createTextureQuadXY(1, 1, 0, 1, 0, 1), tex_pipeline, "sprites/gameover.png")
    gameOverNode = sg.SceneGraphNode("over")
    gameOverNode.childs = [gameOver_shape]

    # player scene graph
    player_shapes= createSpriteShapes(0.5, 0.5, tex_pipeline, "sprites/hinata.png", 7, 4)
    playerNode = sg.SceneGraphNode("player")

    # player model instance
    player = Player(0.2, P)
    # Se indican las referencias del nodo y el controller al modelo
    player.set_model(playerNode, player_shapes)
    player.set_controller(controller)

    # game over scene graph
    aura_shape= createTextureGPUShape(bs.createTextureQuadXY(0.5, 0.5, 0, 1, 0, 1), tex_pipeline, "sprites/aura.png")
    auraNode = sg.SceneGraphNode("aura")
    auraNode.childs = [aura_shape]

    aura=Aura(-0.8, 0.3, 0.1)
    # Se indican las referencias del nodo y el controller al modelo
    aura.set_model(auraNode)
    aura.set_controller(controller)

    # Shape with background texture
    grass = createTextureGPUShape(bs.createTextureQuadXY(1, 1, 0, 4, 0, 5), tex_pipeline, "sprites/grass.jfif", sWrapMode=GL_REPEAT, tWrapMode=GL_REPEAT)

    # background node is created
    grassNode = sg.SceneGraphNode("grass")
    grassNode.childs = [grass]

    # # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [playerNode, auraNode]
    controller.texScene=tex_scene

    # set of human/zombies shapes
    human_shapes= createSpriteShapes(0.3, 0.5, tex_pipeline, "sprites/humanDown.png", 3, 1)
    human_shapes.append(createSpriteShapes(0.3, 0.5, tex_pipeline, "sprites/humanUp.png", 3, 1)[0])
    human_shapes.append(createSpriteShapes(0.3, 0.5, tex_pipeline, "sprites/zombieDown1.png", 4, 1)[0])
    human_shapes.append(createSpriteShapes(0.3, 0.5, tex_pipeline, "sprites/zombieUp1.png", 4, 1)[0])

    humanQuantity= int(20/T*H) +5
    zombieQuantity= int(25/T*Z) +5

    for i in range(humanQuantity):
        # human scene graph
        humanNode = sg.SceneGraphNode("human")
        # human model instance
        x=np.random.randint(800)/1000 * (-1 + np.random.randint(2)*(2))
        if np.random.randint(2):
            human = Human(x, -1, 0.2, 1, 1, P=P, isZombie=0)
        else:
            human = Human(x, 1, 0.2, 0, 1, P=P, isZombie=0)
        # controller reference
        human.set_controller(controller)
        # Se indican las referencias del nodo al modelo
        human.set_model(humanNode, human_shapes)
        controller.humansOut.append(human)
        #tex_scene.childs.append(humanNode)

    for i in range(zombieQuantity):
        # human scene graph
        zombieNode = sg.SceneGraphNode("zombie")
        # human model instance
        x=np.random.randint(800)/1000 * (-1 + np.random.randint(2)*(2))
        if np.random.randint(2):
            zombie = Human(x, -1, 0.2, 1, 0, isZombie=1)
        else:
            zombie = Human(x, 1, 0.2, 0, 0, isZombie=1)
        # controller reference
        zombie.set_controller(controller)
        # Se indican las referencias del nodo al modelo
        zombie.set_model(zombieNode, human_shapes)
        controller.zombiesOut.append(zombie)
        #tex_scene.childs.append(zombieNode)



    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()
    waveNum=0

    # Application loop
    while not glfw.window_should_close(window):
        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # texture background is drawed
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(grassNode, tex_pipeline, "transform")

        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        if controller.gameover==1:
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(youWinNode, tex_pipeline, "transform")

        elif controller.gameover==-1:
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(gameOverNode, tex_pipeline, "transform")
        
        elif controller.gameover=="restarting":
            for hum in controller.humansIn:
                hum.pos[1]=2*(-1 + 2*hum.actual_direction)
                #controller.humansOut.append(hum)
                #controller.humansIn.remove(hum)
                hum.update(delta)
            for zom in controller.zombiesIn:
                zom.pos[1]=2*(-1 + 2*zom.actual_direction)
                #controller.zombiesOut.append(zom)
                #controller.zombiesIn.remove(zom)   
                zom.update(delta) 
            player.pos=[0.9, -0.5]
            player.infected=0
            player.update(delta)
            # Se dibuja el grafo de escena con texturas
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")
            controller.gameover=0
        else:
            # Variables del tiempo
            t1 = glfw.get_time()
            delta = t1 -t0
            t0 = t1
            waveNum += delta
            if (waveNum - T)>0:
                waveNum -= T
                if len(controller.humansOut)>=H:
                    for i in range(H):
                        controller.humansOut[0].outOfScene=0
                        controller.humansOut[0].pos[1] = -(1+np.random.randint(50)/100)*(-1 + 2*controller.humansOut[0].actual_direction)
                        controller.humansOut[0].zombie=0
                        tex_scene.childs.append(controller.humansOut[0].model)
                        controller.humansIn.append(controller.humansOut[0])
                        controller.humansOut.pop(0)
                if len(controller.zombiesOut)>=Z:
                    for i in range(Z):
                        controller.zombiesOut[0].outOfScene=0
                        controller.zombiesOut[0].pos[1] = -(1+np.random.randint(50)/100)*(-1 + 2*controller.zombiesOut[0].actual_direction)
                        controller.zombiesOut[0].zombie=1
                        tex_scene.childs.append(controller.zombiesOut[0].model)
                        controller.zombiesIn.append(controller.zombiesOut[0])
                        controller.zombiesOut.pop(0)

            # Se llama al metodo del player para detectar colisiones
            player.collision(controller.humansIn)
            player.collision(controller.zombiesIn)
            # Se llama al metodo del player para actualizar su posicion
            player.update(delta)

            aura.update()
            aura.collision([player])

            # Se llama al metodo del human para actualizar su posicion
            for hum in controller.humansIn:
                hum.update(delta)
                if hum.zombie==0:
                    hum.collision(controller.humansIn)
                    hum.collision(controller.zombiesIn)

            # Se llama al metodo del zombie para actualizar su posicion
            for zom in controller.zombiesIn:
                zom.update(delta)

            # Se dibuja el grafo de escena con texturas
            glUseProgram(tex_pipeline.shaderProgram)
            sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # print(controller.humansOut)
    # print(controller.humansIn)
    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()