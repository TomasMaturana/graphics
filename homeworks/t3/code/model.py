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
# import random
# import grafica.transformations as tr
from shapes3d import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

# Example parameters

NUMBER_OF_CIRCLES = 10
CIRCLE_DISCRETIZATION = 20
RADIUS = 0.1999
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600


# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 5                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 0.5                        # altura fija de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
    
    # Añadir ángulo a la coordenada theta
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta

    def set_center(self, x, y, z):
        self.center = np.array([x, y, z])
    
    def set_eye(self, x, y, z):
        self.center = np.array([x, y, z])

    def set_height(self, h):
        self.height=h

    # Actualizar la matriz de vista
    def update_view(self):
        # Se calcula la posición de la camara con coordenadas poleras relativas al centro
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        return viewMatrix

# Clase para manejar el controlador y la camara polar
class Controller:
    def __init__(self):
        self.fillPolygon = True

        # Variables para controlar la camara
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False

        self.is_z_pressed = False
        self.is_q_pressed = False
        self.is_w_pressed = False
        self.is_1_pressed = False
        self.upCam = False
        self.targetBall = None
        self.mooving = False

        # Se crea instancia de la camara
        self.polar_camera = PolarCamera()

    # Entregar la referencia a la camara
    def get_camera(self):
        return self.polar_camera

    # Metodo para ller el input del teclado
    def on_key(self, window, key, scancode, action, mods):

        # Caso de detectar la tecla [UP], actualiza estado de variable
        if key == glfw.KEY_UP and not self.upCam:
            if action == glfw.PRESS:
                self.is_up_pressed = True
            elif action == glfw.RELEASE:
                self.is_up_pressed = False

        # Caso de detectar la tecla [DOWN], actualiza estado de variable
        if key == glfw.KEY_DOWN and not self.upCam:
            if action == glfw.PRESS:
                self.is_down_pressed = True
            elif action == glfw.RELEASE:
                self.is_down_pressed = False

        # Caso de detectar la tecla [RIGHT], actualiza estado de variable
        if key == glfw.KEY_RIGHT and not self.upCam:
            if action == glfw.PRESS:
                self.is_right_pressed = True
            elif action == glfw.RELEASE:
                self.is_right_pressed = False

        # Caso de detectar la tecla [LEFT], actualiza estado de variable
        if key == glfw.KEY_LEFT and not self.upCam:
            if action == glfw.PRESS:
                self.is_left_pressed = True
            elif action == glfw.RELEASE:
                self.is_left_pressed = False

        # Caso de detectar la tecla 1, cambia a camara desde arriba
        if key == glfw.KEY_1:
            if action == glfw.PRESS:
                self.is_1_pressed = True

        # Caso de detectar la tecla q, retrocede targetBall
        if key == glfw.KEY_Q:
            if action == glfw.PRESS:
                self.is_q_pressed = True

        # Caso de detectar la tecla w, avanza targetBall
        if key == glfw.KEY_W:
            if action == glfw.PRESS:
                self.is_w_pressed = True
            
        # Caso de detectar la tecla z, se ejecuta el golpe a la bola
        if key == glfw.KEY_Z and not self.upCam and not self.mooving:
            if action == glfw.PRESS:
                self.is_z_pressed = True
        
        # Caso de detectar la barra espaciadora, se cambia el metodo de dibujo
        if key == glfw.KEY_SPACE:
            if action == glfw.PRESS:
                self.fillPolygon = not self.fillPolygon

        # Caso en que se cierra la ventana
        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)
                
    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera(self, delta):
        # Camara rota a la izquierda
        if self.is_left_pressed:
            self.polar_camera.set_theta(-2 * delta)

        # Camara rota a la derecha
        if self.is_right_pressed:
            self.polar_camera.set_theta( 2 * delta)
        
        # Camara se acerca al centro
        if self.is_up_pressed:
            self.polar_camera.set_rho(-5 * delta)

        # Camara se aleja del centro
        if self.is_down_pressed:
            self.polar_camera.set_rho(5 * delta)
        
        if self.is_1_pressed:
            if self.upCam:
                self.polar_camera.set_height(0.5)
                self.upCam = False
                self.is_1_pressed = False
                self.polar_camera.rho=5
            else:
                self.polar_camera.set_height(6)
                self.upCam = True
                self.is_1_pressed = False
                self.polar_camera.rho=0.1
                self.polar_camera.theta=0

    def update_center(self, pos):
        self.polar_camera.set_center(pos[0], pos[1], self.polar_camera.center[2])

    #Golpe a bola
    def update_ball_velocity(self, vel):
        if self.is_z_pressed and not self.mooving:
            self.targetBall.velocity=vel
            self.is_z_pressed = False
            self.mooving = True

    # target ball setter
    def set_target_ball(self, ball, qOrW=0):
        self.targetBall=ball
        if qOrW==1:
            self.is_q_pressed = False
        elif qOrW==2:
            self.is_w_pressed = False



class Ball:
    def __init__(self, pipeline, pipeline2, position, velocity, num=""):
        self.pipeline = pipeline
        self.gpuNode = createTexSphereNode(pipeline, num)
        self.shadow = createShadowNode(pipeline2)
        self.position = position
        self.radius = RADIUS
        self.velocity = velocity
        self.state = True
        self.thetaX = np.pi
        self.thetaY = np.pi

    def action(self, aceleration, deltaTime):
        # Euler integration
        self.velocity += deltaTime * aceleration
        self.position += self.velocity * deltaTime

    def update(self, zPos=-1.8):
        self.thetaX = (self.thetaX - self.velocity[1]*0.02) % (2*np.pi)
        self.thetaY = (self.thetaY - self.velocity[0]*0.02) % (2*np.pi)
        sg.findNode(self.gpuNode, "sphere").transform = tr.matmul([tr.translate(self.position[0], self.position[1], zPos), tr.scale(0.4,0.4,0.4), tr.rotationX(self.thetaX), tr.rotationY(self.thetaY)])
        self.shadow.transform = tr.matmul([tr.translate(self.position[0], self.position[1], zPos-self.radius), tr.scale(0.4,0.4,1)])

    def delete(self):
        self.state=False
    

def rotate2D(vector, theta):
    """
    Direct application of a 2D rotation
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        cos_theta * vector[0] - sin_theta * vector[1],
        sin_theta * vector[0] + cos_theta * vector[1]
    ], dtype = np.float32)


def collide(ball1, ball2, restCoef=1):
    """
    If there are a collision between the balls, it modifies the velocity of
    both balls in a way that preserves energy and momentum.
    """
    
    assert isinstance(ball1, Ball)
    assert isinstance(ball2, Ball)

    normal = ball2.position - ball1.position
    normal /= np.linalg.norm(normal)

    ball1MovingToNormal = np.dot(ball2.velocity, normal) > 0.0
    ball2MovingToNormal = np.dot(ball1.velocity, normal) < 0.0

    if not (ball1MovingToNormal and ball2MovingToNormal):

        # obtaining the tangent direction
        tangent = rotate2D(normal, np.pi/2.0)

        # Projecting the velocity vector over the normal and tangent directions
        # for both balls, 1 and 2.
        v1n = np.dot(ball1.velocity, normal) * normal
        v1t = np.dot(ball1.velocity, tangent) * tangent

        v2n = np.dot(ball2.velocity, normal) * normal
        v2t = np.dot(ball2.velocity, tangent) * tangent

        # swaping the normal components...
        # this means that we applying energy and momentum conservation
        ball1.velocity = restCoef*(v2n + v1t)
        ball2.velocity = restCoef*(v1n + v2t)


def areColliding(ball1, ball2):
    assert isinstance(ball1, Ball)
    assert isinstance(ball2, Ball)

    difference = ball2.position - ball1.position
    distance = np.linalg.norm(difference)
    collisionDistance = ball2.radius + ball1.radius
    return distance < collisionDistance


def collideWithBorder(ball):
    if abs(ball.position[0]) < 0.15 and abs(ball.position[1]) >= 3.1:
        if abs(ball.position[1]) >= 3.25:
            ball.delete()
        return True

    if 6.5 <= abs(ball.position[0])  and abs(ball.position[1]) >= 3:
        if abs(ball.position[1]) >= 3.2:
            ball.delete()
        return True

    # Right
    if ball.position[0] + ball.radius > 6.76:
        ball.velocity[0] = -abs(ball.velocity[0])

    # Left
    if ball.position[0] < -6.76 + ball.radius:
        ball.velocity[0] = abs(ball.velocity[0])

    # Top
    if ball.position[1] > 3.3 - ball.radius:
        ball.velocity[1] = -abs(ball.velocity[1])

    # Bottom
    if ball.position[1] < -3.3 + ball.radius:
        ball.velocity[1] = abs(ball.velocity[1])


