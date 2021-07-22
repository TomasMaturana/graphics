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

import imgui
from imgui.integrations.glfw import GlfwRenderer


def transformGuiOverlay(locationZ, la, ld, ls, cte_at, lnr_at, qud_at, shininess, rot3, pos3):
    # Funcion para actualizar el menu

    # start new frame context
    imgui.new_frame()

    # open new window context
    imgui.begin("Light control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

    # draw text label inside of current window
    imgui.text("Configuration sliders")

    # Posicion z de la fuente de luz
    edited, locationZ = imgui.slider_float("location Z", locationZ, -1.0, 2.3)
    # Rotacion de la esfera
    edited, rot3[0] = imgui.slider_float("Rot x", rot3[0], 0.0, np.pi*2)
    edited, rot3[1] = imgui.slider_float("Rot Y", rot3[1], 0, np.pi*2)
    edited, rot3[2] = imgui.slider_float("Rot Z", rot3[2], 0, np.pi*2)

    # Rotacion de la esfera
    edited, pos3[0] = imgui.slider_float("Pos x", pos3[0], -6.55, 6.55)
    edited, pos3[1] = imgui.slider_float("Pos Y", pos3[1], -3.05, 3.05)

    # Coeficiente de iluminacion ambiental
    edited, la = imgui.color_edit3("la", la[0], la[1], la[2])
    # Boton para reiniciar la iluminacion ambiental
    if imgui.button("clean la"):
        la = (1.0, 1.0, 1.0)
    
    # Coeficiente de iluminacion difusa
    edited, ld = imgui.color_edit3("ld", ld[0], ld[1], ld[2])
    # Boton para reiniciar la iluminacion difusa
    if imgui.button("clean ld"):
        ld = (1.0, 1.0, 1.0)

    # Coeficiente de iluminacion especular
    edited, ls = imgui.color_edit3("ls", ls[0], ls[1], ls[2])
    # Boton para reiniciar la iluminacion especular
    if imgui.button("clean ls"):
        ls = (1.0, 1.0, 1.0)
    # Coeficientes de atenuacion y shininess
    edited, cte_at = imgui.slider_float("constant Att.", cte_at, 0.0001, 0.2)
    edited, lnr_at = imgui.slider_float("linear Att.", lnr_at, 0.01, 0.1)
    edited, qud_at = imgui.slider_float("quadratic Att.", qud_at, 0.005, 0.1)
    edited, shininess = imgui.slider_float("shininess", shininess, 0.1, 200)

    # close current window context
    imgui.end()

    # pass all drawing comands to the rendering pipeline
    # and close frame context
    imgui.render()
    imgui.end_frame()

    return locationZ, la, ld, ls, cte_at, lnr_at, qud_at, shininess, rot3, pos3


if __name__ == "__main__":

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

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    # gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(4))

    scene = createScene(phongPipeline)
    balls=[]
    white_ball = Ball(phongTexPipeline, [0,0], [0,0])
    balls.append(white_ball)
    ball1 = Ball(phongTexPipeline, [2,0], [0,0], str(1))
    balls.append(ball1)
    ball2 = Ball(phongTexPipeline, [2.35,-0.2], [0,0], str(2))
    balls.append(ball2)
    ball3 = Ball(phongTexPipeline, [2.35,0.2], [0,0], str(3))
    balls.append(ball3)
    ball4 = Ball(phongTexPipeline, [2.7,-0.4], [0,0], str(4))
    balls.append(ball4)
    ball5 = Ball(phongTexPipeline, [3.05,-0.2], [0,0], str(5))
    balls.append(ball5)
    ball6 = Ball(phongTexPipeline, [2.7,0.4], [0,0], str(6))
    balls.append(ball6)
    ball7 = Ball(phongTexPipeline, [3.05,-0.6], [0,0], str(7))
    balls.append(ball7)
    ball8 = Ball(phongTexPipeline, [2.7,0], [0,0], str(8))
    balls.append(ball8)
    ball9 = Ball(phongTexPipeline, [3.05,0.2], [0,0], str(9))
    balls.append(ball9)
    ball10 = Ball(phongTexPipeline, [3.05,0.6], [0,0], str(10))
    balls.append(ball10)
    ball11 = Ball(phongTexPipeline, [3.4,-0.8], [0,0], str(11))
    balls.append(ball11)
    ball12 = Ball(phongTexPipeline, [3.4,-0.4], [0,0], str(12))
    balls.append(ball12)
    ball13 = Ball(phongTexPipeline, [3.4,0], [0,0], str(13))
    balls.append(ball13)
    ball14 = Ball(phongTexPipeline, [3.4,0.4], [0,0], str(14))
    balls.append(ball14)
    ball15 = Ball(phongTexPipeline, [3.4,0.8], [0,0], str(15))
    balls.append(ball15)


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # initilize imgui context (see documentation)
    imgui.create_context()
    impl = GlfwRenderer(window)
    
    # IMPORTANTE!! si usa imgui debe conectar los input con on_key despues de inicializar imgui, de lo contrario no funcionan los input 
    # Se instancia un controller
    controller = Controller()
    actualBall=0
    controller.set_target_ball(balls[actualBall])
    # Se conecta el metodo on_key del controller para manejar el input del teclado
    glfw.set_key_callback(window, controller.on_key)

    # valores que controla el menu de imgui
    locationZ = 2.3 
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

        
        impl.process_inputs()
        # Using GLFW to check for input events
        glfw.poll_events()

        if controller.is_q_pressed:        
            actualBall=(actualBall-1)%len(balls)
            controller.set_target_ball(balls[actualBall], 1)
            
        if controller.is_w_pressed:        
            actualBall=(actualBall+1)%len(balls)
            controller.set_target_ball(balls[actualBall], 2)

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

         # imgui function

        locationZ, la, ld, ls, cte_at, lnr_at, qud_at, shininess, rot, pos = \
            transformGuiOverlay(locationZ, la, ld, ls, cte_at, lnr_at, qud_at, shininess, rot, pos)


##############################################################################
        if controller.is_z_pressed:
            controller.update_ball_velocity([center[0]-eye[0], center[1]-eye[1]])

        # Physics!
        coef=0.2
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

        # checking and processing collisions among balls
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                if areColliding(balls[i], balls[j]):
                    collide(balls[i], balls[j])
                    print("colliding:" + str(i) + "->" + str(j))
##############################################################################



        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # # The axis is drawn without lighting effects
        # if controller.showAxis:
        #     glUseProgram(mvpPipeline.shaderProgram)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        #     glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #     mvpPipeline.drawCall(gpuAxis, GL_LINES)

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
        #sg.drawSceneGraphNode(cube1, lightingPipeline, "model")
        #sg.drawSceneGraphNode(cube2, lightingPipeline, "model")
        # sg.drawSceneGraphNode(sphere, lightingPipeline, "model")
        
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

        # sg.findNode(white_ball.gpuNode, "rot").transform = tr.matmul([tr.rotationZ(rot[2]),tr.rotationY(rot[1]),tr.rotationX(rot[0])])
        # sg.findNode(white_ball.gpuNode, "sphere").transform = tr.matmul([tr.translate(pos[0], pos[1], pos[2]), tr.scale(0.4,0.4,0.4)])
        # sg.drawSceneGraphNode(white_ball.gpuNode, phongTexPipeline, "model")

        for b in balls:
            b.update()
            sg.drawSceneGraphNode(b.gpuNode, phongTexPipeline, "model")
        
        # Drawing the imgui texture over our drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        impl.render(imgui.get_draw_data())

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    #gpuAxis.clear()
    impl.shutdown()
    scene.clear()
    #white_ball.clear()
    for b in balls:
        b.gpuNode.clear()

    glfw.terminate()