# ************************************************
#   Instancia.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from math import floor
from random import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *

""" Classe Instancia """
class Mapa:
    
    def __init__(self):
        self.position = Point (0,0,0) 
        self.escala = Point (0,0,0)
        self.max = Point (0,0,0)
        self.min = Point (0,0,0)
        self.colors = [random(),random(),random()]
        self.rua = False
        
    def criaRua(self):
        self.rua = True     
    
    def desenha(self):
        pos = self.position
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        self.DesenhaMapa()
        glTranslatef(0, self.escala.y/2, 0)
        if not self.rua:
            glScalef(self.escala.x, self.escala.y, self.escala.z)
            glColor3f(self.colors[0], self.colors[1], self.colors[2])
            glutSolidCube(1)
        glPopMatrix()
        
    def DesenhaMapa(self):
        if(self.rua):
            glEnable (GL_TEXTURE_2D)
            glColor3f(1,1,1) # desenha QUAD em branco, pois vai usa textura
            glBegin ( GL_QUADS )
            glNormal3f(0,1,0)
            glTexCoord(0,0)
            glVertex3f(-0.5,  0.0, -0.5)
            glTexCoord(0,1)
            glVertex3f(-0.5,  0.0,  0.5)
            glTexCoord(1,1)
            glVertex3f( 0.5,  0.0,  0.5)
            glTexCoord(1,0)
            glVertex3f( 0.5,  0.0, -0.5)
            glEnd()
            #glDisable (GL_TEXTURE_2D)
        else:
            glColor3f(self.colors[0], self.colors[1], self.colors[2])
            glBegin ( GL_QUADS )
            glNormal3f(0,1,0)
            glVertex3f(-0.5,  0.0, -0.5)
            glVertex3f(-0.5,  0.0,  0.5)
            glVertex3f( 0.5,  0.0,  0.5)
            glVertex3f( 0.5,  0.0, -0.5)
            glEnd()