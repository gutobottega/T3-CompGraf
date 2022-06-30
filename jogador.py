# ************************************************
#   Instancia.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from math import floor
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *

""" Classe Instancia """
class Jogador:   
    
    def __init__(self):
        self.max = Point()
        self.min = Point()
        self.position = Point (0,0.5,0) 
        self.escala = Point (1,1,1)
        self.rotation:float = 0.0
        self.movement = Point(0,0,1)
        self.speed = 1
        self.counter = time.time()
    
    def move(self,v):
        now = time.time()
        ret = self.speed * (now - self.counter) * v
        self.counter = now
        return ret
    
    def desenha(self):
        pos = self.position
        glColor3f(0.0,0.0,0.0) # Preto
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        glRotatef(self.rotation,0,1,0)
        glScalef(0.7, 0.3, 1 )
        glutSolidCube(1)
        glPopMatrix()