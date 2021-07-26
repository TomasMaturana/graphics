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
from model import *
import sys
import json


if __name__ == "__main__":
    config = open(sys.argv[1],)
    data = json.load(config)
    coef=data["friccion"]
    restCoef=data["restitucion"]

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1600
    height = 800
    title = "Tarea 3B: Pool"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Different shader programs for different lighting strategies
    phongPipeline = ls.SimplePhongShaderProgram()
    phongTexPipeline = ls.SimpleTexturePhongShaderProgram() # Pipeline para dibujar texturas
    texPipeline = es.SimpleTextureTransformShaderProgram() # Pipeline para dibujar texturas
    

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    scene = createScene(phongPipeline)
    taco = createTaco(texPipeline)
    balls=[]
    white_ball = Ball(phongTexPipeline, phongPipeline, [0,0], [0,0])
    balls.append(white_ball)
    ball1 = Ball(phongTexPipeline, phongPipeline, [2,0], [0,0], str(1))
    balls.append(ball1)
    ball2 = Ball(phongTexPipeline, phongPipeline, [2.35,-0.2], [0,0], str(2))
    balls.append(ball2)
    ball3 = Ball(phongTexPipeline, phongPipeline, [2.35,0.2], [0,0], str(3))
    balls.append(ball3)
    ball4 = Ball(phongTexPipeline, phongPipeline, [2.7,-0.4], [0,0], str(4))
    balls.append(ball4)
    ball5 = Ball(phongTexPipeline, phongPipeline, [3.05,-0.2], [0,0], str(5))
    balls.append(ball5)
    ball6 = Ball(phongTexPipeline, phongPipeline, [2.7,0.4], [0,0], str(6))
    balls.append(ball6)
    ball7 = Ball(phongTexPipeline, phongPipeline, [3.05,-0.6], [0,0], str(7))
    balls.append(ball7)
    ball8 = Ball(phongTexPipeline, phongPipeline, [2.7,0], [0,0], str(8))
    balls.append(ball8)
    ball9 = Ball(phongTexPipeline, phongPipeline, [3.05,0.2], [0,0], str(9))
    balls.append(ball9)
    ball10 = Ball(phongTexPipeline, phongPipeline, [3.05,0.6], [0,0], str(10))
    balls.append(ball10)
    ball11 = Ball(phongTexPipeline, phongPipeline, [3.4,-0.8], [0,0], str(11))
    balls.append(ball11)
    ball12 = Ball(phongTexPipeline, phongPipeline, [3.4,-0.4], [0,0], str(12))
    balls.append(ball12)
    ball13 = Ball(phongTexPipeline, phongPipeline, [3.4,0], [0,0], str(13))
    balls.append(ball13)
    ball14 = Ball(phongTexPipeline, phongPipeline, [3.4,0.4], [0,0], str(14))
    balls.append(ball14)
    ball15 = Ball(phongTexPipeline, phongPipeline, [3.4,0.8], [0,0], str(15))
    balls.append(ball15)


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Se instancia un controller
    controller = Controller()
    actualBall=0
    controller.set_target_ball(balls[actualBall])
    # Se conecta el metodo on_key del controller para manejar el input del teclado
    glfw.set_key_callback(window, controller.on_key)

    # valores que controla el menu de imgui
    locationZ = 3
    la = [1.0, 1.0, 1.0] 
    ld = [1.0, 1.0, 1.0] 
    ls = [1.0, 1.0, 1.0]
    cte_at = 0.0001
    lnr_at= 0.03
    qud_at = 0.01
    shininess = 100
    rot = [0.0, 0.0, 0.0] 
    pos = [0.0, 0.0, -1.8] 

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        glfw.poll_events()

        if not controller.targetBall.state:
            actualBall=(actualBall)%len(balls)
            controller.set_target_ball(balls[actualBall])

        if controller.is_q_pressed:        
            actualBall=(actualBall-1)%len(balls)
            controller.set_target_ball(balls[actualBall], 1)
            
        if controller.is_w_pressed:        
            actualBall=(actualBall+1)%len(balls)
            controller.set_target_ball(balls[actualBall], 2)

        if controller.upCam:
            center_pos = [0, 0]
        else:
            center_pos = controller.targetBall.position
        controller.update_center(center_pos)

        controller.update_camera(delta)
        camera = controller.get_camera()
        viewMatrix = camera.update_view()
        eye = camera.eye
        center = camera.center

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        if controller.is_z_pressed:
            controller.update_ball_velocity([(center[0]-eye[0])*2, (center[1]-eye[1])*2])


        #
        acceleration = np.array([0.0, 0.0], dtype=np.float32)
        for b in balls:
            if abs(b.velocity[0])>0.05:
                if abs(b.velocity[1])>0.05:
                    acceleration = np.array([-b.velocity[0]*coef, -b.velocity[1]*coef], dtype=np.float32)
                else:
                    b.velocity[1]=0.0
                    acceleration = np.array([-b.velocity[0]*coef, 0.0], dtype=np.float32)
            else:
                if abs(b.velocity[1])>0.05:
                    b.velocity[0]=0.0
                    acceleration = np.array([0.0, -b.velocity[1]*coef], dtype=np.float32)
                else:
                    b.velocity[0]=0.0
                    b.velocity[1]=0.0
                    acceleration = np.array([0.0, 0.0], dtype=np.float32)

            b.action(acceleration, delta)

            # checking and processing collisions against the border
            collideWithBorder(b)
            if not b.state:
                b.gpuNode.clear()
                balls.remove(b)

        # checking and processing collisions among balls
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                if areColliding(balls[i], balls[j]):
                    collide(balls[i], balls[j], restCoef)
                    # print("colliding:" + str(i) + "->" + str(j))



        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        lightingPipeline = phongPipeline
        lightposition = [0, 0, locationZ]

        # Setting all uniform shader variables
        
        glUseProgram(lightingPipeline.shaderProgram)
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), la[0], la[1], la[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), ld[0], ld[1], ld[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), ls[0], ls[1], ls[2])

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), int(shininess))
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), cte_at)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), lnr_at)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), qud_at)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        # Drawing
        sg.drawSceneGraphNode(scene, lightingPipeline, "model")
        
        # Se cambia al pipeline para dibujar texturas

        glUseProgram(phongTexPipeline.shaderProgram)
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "La"), la[0], la[1], la[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ld"), ld[0], ld[1], ld[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ls"), ls[0], ls[1], ls[2])

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(phongTexPipeline.shaderProgram, "shininess"), int(shininess))

        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "constantAttenuation"), cte_at)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "linearAttenuation"), lnr_at)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "quadraticAttenuation"), qud_at)
        
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        
        count = 0
        for b in balls:
            b.update()
            sg.drawSceneGraphNode(b.gpuNode, phongTexPipeline, "model")
            if b.velocity[0] == 0 and b.velocity[1] == 0:
                count +=1
        
        if count == len(balls):
            controller.mooving = False

        glUseProgram(phongPipeline.shaderProgram)
        for b in balls:
            sg.drawSceneGraphNode(b.shadow, phongPipeline, "model")

        if not controller.upCam:
            glUseProgram(texPipeline.shaderProgram)
            sg.drawSceneGraphNode(taco, texPipeline, "transform")
        
        # Drawing the imgui texture over our drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    scene.clear()
    taco.clear()
    for b in balls:
        b.gpuNode.clear()
        b.shadow.clear()

    glfw.terminate()