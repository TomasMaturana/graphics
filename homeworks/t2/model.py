""" Clases y objetos correspondiente al modelo"""

import glfw
import numpy as np
import grafica.transformations as tr

class Player():
    # Clase que contiene al modelo del player
    def __init__(self, size):
        self.pos = [0.0, 0.0, 7.2] # Posicion en el escenario
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # controller reference, to access to their variables
        self.size = size # Escala a aplicar al nodo 
        # self.radio = 0.02 # distancia para realiozar los calculos de colision
        self.actual_sprite = 1  # sprint number 
        self.sprite = None
        # self.actual_direction = 0 # 0:down  1:up  2:right  3:left
        # self.infected= 0
        # self.zombie= 0

    def set_model(self, new_model, sprite=None):
        # Se obtiene una referencia a uno nodo
        self.model = new_model
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], self.pos[2]), tr.scale(self.size/2, self.size, 1)])
        # if we use sprite, model will actualice after
        if(sprite):
            self.sprite=sprite
            

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def update(self):
        self.model.childs= [self.sprite[self.actual_sprite]]
        # self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], self.pos[2]), tr.scale(self.size/2, self.size, 1)])

        # # Si detecta la tecla [D] presionada se mueve hacia la derecha
        # if self.controller.is_d_pressed and self.pos[0] < 0.9:
        #     self.pos[0] += self.vel[0] * delta
        #     self.actual_sprite[2]=(self.actual_sprite[2] + 0.05)%7
        #     self.actual_direction = 2
        # # Si detecta la tecla [A] presionada se mueve hacia la izquierda
        # if self.controller.is_a_pressed and self.pos[0] > -0.9:
        #     self.pos[0] -= self.vel[0] * delta
        #     self.actual_sprite[3]=(self.actual_sprite[3] + 0.05)%7
        #     self.actual_direction = 3
        # # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        # if self.controller.is_w_pressed and self.pos[1] < 0.9:
        #     self.pos[1] += self.vel[1] * delta
        #     self.actual_sprite[1]=(self.actual_sprite[1] + 0.05)%7
        #     self.actual_direction = 1
        # # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        # if self.controller.is_s_pressed and self.pos[1] > -0.9:
        #     self.pos[1] -= self.vel[1] * delta
        #     self.actual_sprite[0]=(self.actual_sprite[0] + 0.05)%7
        #     self.actual_direction = 0
        # #print(self.pos[0], self.pos[1])

        # # Se le aplica la transformacion de traslado segun la posicion actual
        # self.model.childs= [self.sprite[self.actual_direction][int(self.actual_sprite[self.actual_direction])]]
        # self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size/2, self.size, 1)])

    # def collision(self, someonesList):
    #     for someone in someonesList:
    #         # if the distance to someone is minor than their radios summatory, then collision
    #         if ((self.radio+someone.radio)**2 > ((self.pos[0]- someone.pos[0])**2 + (self.pos[1]-someone.pos[1])**2)):
    #             if someone.zombie:
    #                 self.zombie=1
    #                 self.controller.gameover=-1
    #                 print("fatal collision")
    #             elif someone.infected and not self.infected:
    #                 self.infected=1 
    #     return

    # def infectedToZombie(self, P): # human infected is converted to zombie with P probability
    #     if self.infected and not self.zombie:
    #         self.zombie=np.random.choice([0, 1], p=[1-P, P])
    #     if self.zombie:
    #         self.controller.gameover=-1
    #         print("fatal infection")

        

# class Aura():
#     # class to contain the variables of an Aura object (checkpoint to win)
#     def __init__(self, posx, posy, size):
#         self.pos = [posx, posy]
#         self.radio = 0.05
#         self.model = None # scene graph asociated reference
#         self.size = size # scale to apply to the node
#         self.controller = None # controller reference, to access to their variables

#     def set_model(self, new_model):
#         self.model = new_model

#     def set_controller(self, new_controller):
#         self.controller = new_controller

#     def collision(self, someonesList):
#         # to detect collisions with players

#         for someone in someonesList:
#             # if the distance to someone is minor than their radios summatory, then collision
#             if ((self.radio+someone.radio)**2 > ((self.pos[0]- someone.pos[0])**2 + (self.pos[1]-someone.pos[1])**2)):
#                 self.controller.gameover=1
#                 return

#     def update(self, delta):
#             self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size/2, self.size, 1), tr.rotationZ(delta)])