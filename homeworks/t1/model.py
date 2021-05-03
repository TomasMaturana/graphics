""" Clases y objetos correspondiente al modelo"""

import glfw
import numpy as np
import grafica.transformations as tr

class Player():
    # Clase que contiene al modelo del player / auro
    def __init__(self, size, P):
        self.pos = [0.9, -0.5] # Posicion en el escenario
        self.vel = [0.5,1] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo 
        self.radio = 0.02 # distancia para realiozar los calculos de colision
        self.actual_sprite = [1, 1, 1, 1]  # sprint number --> [down, up, right, left]
        self.sprite = None
        self.actual_direction = 0 # 0:down  1:up  2:right  3:left
        self.infected= 0
        self.zombie= 0
        self.P = P

    def set_model(self, new_model, sprite=None):
        # Se obtiene una referencia a uno nodo
        self.model = new_model
        # if we use sprite, model will actualice after
        if(sprite):
            self.sprite=sprite
            

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def update(self, delta):
        # Se actualiza la posicion del auto

        # Si detecta la tecla [D] presionada se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] < 0.9:
            self.pos[0] += self.vel[0] * delta
            self.actual_sprite[2]=(self.actual_sprite[2] + 0.05)%7
            self.actual_direction = 2
        # Si detecta la tecla [A] presionada se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] > -0.9:
            self.pos[0] -= self.vel[0] * delta
            self.actual_sprite[3]=(self.actual_sprite[3] + 0.05)%7
            self.actual_direction = 3
        # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] < 0.9:
            self.pos[1] += self.vel[1] * delta
            self.actual_sprite[1]=(self.actual_sprite[1] + 0.05)%7
            self.actual_direction = 1
        # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] > -0.9:
            self.pos[1] -= self.vel[1] * delta
            self.actual_sprite[0]=(self.actual_sprite[0] + 0.05)%7
            self.actual_direction = 0
        #print(self.pos[0], self.pos[1])

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.childs= [self.sprite[self.actual_direction][int(self.actual_sprite[self.actual_direction])]]
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size/2, self.size, 1)])

    def collision(self, someonesList):
        for someone in someonesList:
            # si la distancia a la carga es menor que la suma de los radios ha ocurrido en la colision
            if ((self.radio+someone.radio)**2 > ((self.pos[0]- someone.pos[0])**2 + (self.pos[1]-someone.pos[1])**2)):
                if someone.zombie:
                    self.zombie=1
                    self.controller.gameover=-1
                elif someone.infected and not self.infected:
                    self.infected=1 
        return

    def infectedToZombie(self, P): # human infected is converted to zombie with P probability
        if self.infected and not self.zombie:
            self.zombie=np.random.choice([0, 1], p=[1-P, P])
        if self.zombie:
            self.controller.gameover=-1

    
class Human():
    # Clase para contener las caracteristicas de un objeto que representa una carga 
    def __init__(self, posx, posy, size, direction, wasHuman, infected=0, isZombie=0, velocity=[0.05,0.15]):
        self.pos = [posx, posy]
        self.radio = 0.02
        self.vel = velocity # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.size = size # Escala a aplicar al nodo 
        self.actual_sprite = 1  # sprint number --> [down, up]
        self.sprite = None # human and zombie sprites --> [humanDown, humanUp, zombieDown, zombieUp]
        self.actual_direction = direction # 0:down  1:up 
        self.stepsToWalk = 1 # number of iterations to change between left and right direction
        self.Xdirection = 0 # 0: left, 1: right
        self.outOfScene = 1 # 1 if the shape is out of the scene
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.zombie = isZombie # 1 if actually is a zombie (to change the sprint)
        self.wasHuman = wasHuman # 1 if at first was a human (to recicle object)
        if isZombie:
            self.infected = isZombie # 1 if is infected (zombie always is infected)
        else:
            self.infected = infected

    def set_model(self, new_model, sprite):
        # Se obtiene una referencia a uno nodo
        self.model = new_model
        self.sprite = sprite

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def update(self, delta):
        if self.actual_direction and self.pos[1] <1.3: # moving up
            self.pos[1] += self.vel[1] * delta / (1 + self.zombie*0.5)
            self.actual_sprite=(self.actual_sprite + 0.01)%4
        elif not self.actual_direction and self.pos[1] >-1.3: # moving down
            self.pos[1] -= self.vel[1] * delta / (1 + self.zombie*0.5)
            self.actual_sprite=(self.actual_sprite + 0.01)%4
        else:
            self.remove()

        if not self.outOfScene:
            if self.stepsToWalk<=0:
                self.stepsToWalk=np.random.randint(1000)
                self.Xdirection = np.random.randint(2)

            if (self.Xdirection==1): # 1: right, 0: left
                self.pos[0] += self.vel[0] * delta 
                if self.pos[0] >0.8:
                    self.Xdirection = 0
            else:
                self.pos[0] -= self.vel[0] * delta
                if self.pos[0] <-0.8:
                    self.Xdirection = 1
            
            self.stepsToWalk-=1

            # Se le aplica la transformacion de traslado segun la posicion actual
            # self.model.childs= [self.sprite[(self.actual_direction + (self.zombie * 2) - (self.zombie * 2 *self.wasHuman*self.controller.glasses))][int(self.actual_sprite - 1*self.wasHuman*self.controller.glasses)]]
            self.model.childs= [self.sprite[(self.actual_direction + (self.zombie * 2) )][int(self.actual_sprite)]]
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size/2, self.size, 1)])

    def remove(self):
        self.outOfScene = 1
        try:
            self.controller.texScene.childs.remove(self.model)
        except:
            pass
        if self.wasHuman:
            if self.model in self.controller.glassesScene.childs:
                self.controller.glassesScene.childs.remove(self.model)
            self.controller.humansOut.append(self)
            try:
                self.controller.humansIn.remove(self)
            except:
                pass
        else:
            self.controller.zombiesOut.append(self)
            try:
                self.controller.zombiesIn.remove(self)
            except:
                pass
    
    def collision(self, someonesList):
        # function to detect collisions between humans and zombies
        if not self.zombie: # if is a human
            for someone in someonesList:
                collision=((self.radio+someone.radio)**2 > ((self.pos[0]- someone.pos[0])**2 + (self.pos[1]-someone.pos[1])**2))
                # if the distance to someone is minor than their radios summatory, then collision
                if collision and someone.zombie:
                    self.zombie=1
                    if self.model in self.controller.glassesScene.childs:
                        self.controller.glassesScene.childs.remove(self.model)
                elif collision and someone.infected and not self.infected:
                    self.infected=1 
                    self.controller.glassesScene.childs.append(self.model)
            return

    def infectedToZombie(self, P): # human infected is converted to zombie with P probability
        if self.wasHuman and self.infected and not self.zombie:
            self.zombie=np.random.choice([0, 1], p=[1-P, P])
        if self.model in self.controller.glassesScene.childs and self.zombie:
            self.controller.glassesScene.childs.remove(self.model)

class Aura():
    # Clase para contener las caracteristicas de un objeto que representa una carga 
    def __init__(self, posx, posy, size):
        self.pos = [posx, posy]
        self.radio = 0.05
        self.model = None # Referencia al grafo de escena asociado
        self.size = size # Escala a aplicar al nodo 
        self.controller = None # Referencia del controlador, para acceder a sus variables

    def set_model(self, new_model):
        # Se obtiene una referencia a uno nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def collision(self, someonesList):
        # Funcion para detectar las colisiones con las cargas

        # Se recorren las cargas 
        for someone in someonesList:
            # si la distancia a la carga es menor que la suma de los radios ha ocurrido en la colision
            if ((self.radio+someone.radio)**2 > ((self.pos[0]- someone.pos[0])**2 + (self.pos[1]-someone.pos[1])**2)):
                self.controller.gameover=1
                return

    def update(self, delta):
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size/2, self.size, 1), tr.rotationZ(delta)])