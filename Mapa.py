# ************************************************
#   Instancia.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from math import floor
from random import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *

""" Classe Instancia """
class Mapa:   
    def __init__(self, numero):
        self.position = Point (0,0,0) 
        self.escala = Point (0,0,0)
        self.max = Point (0,0,0)
        self.min = Point (0,0,0)
        self.columnsOffset = 0
        self.colors = [random(),random(),random()]
        self.rua = False
        self.instance = self.criaMapa(numero)
        
    
    def desenha(self):
        pos = self.position
        glColor3f(0.0,0.0,0.0) # Preto
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        self.DesenhaMapa()
        glTranslatef(0, self.escala.y/2, 0)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        glColor3f(self.colors[0], self.colors[1], self.colors[2])
        glutSolidCube(1)
        glPopMatrix()
        
    def DesenhaMapa(self):
        glColor3f(self.colors[0], self.colors[1], self.colors[2])
        glBegin ( GL_QUADS )
        glNormal3f(0,1,0)
        glVertex3f(-0.5,  0.0, -0.5)
        glVertex3f(-0.5,  0.0,  0.5)
        glVertex3f( 0.5,  0.0,  0.5)
        glVertex3f( 0.5,  0.0, -0.5)
        glEnd()
        
        glColor3f(1,1,1) # desenha a borda da QUAD 
        glBegin ( GL_LINE_STRIP )
        glNormal3f(0,1,0)
        glVertex3f(-0.5,  0.0, -0.5)
        glVertex3f(-0.5,  0.0,  0.5)
        glVertex3f( 0.5,  0.0,  0.5)
        glVertex3f( 0.5,  0.0, -0.5)
        glEnd()
        
        
        #TODO: PARA USO DA TEXTURA
        
        # glDisable (GL_TEXTURE_2D)
        # glEnable (GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, Texturas[NroDaTextura])
        
        # glColor3f(1,1,1) # desenha QUAD em branco, pois vai usa textura
        # glBegin ( GL_QUADS )
        # glNormal3f(0,1,0)
        # glTexCoord(0,0)
        # glVertex3f(-0.5,  0.0, -0.5)
        # glTexCoord(0,1)
        # glVertex3f(-0.5,  0.0,  0.5)
        # glTexCoord(1,1)
        # glVertex3f( 0.5,  0.0,  0.5)
        # glTexCoord(1,0)
        # glVertex3f( 0.5,  0.0, -0.5)
        # glEnd()
        
    
    def criaMapa(self, num):
        # Rua - 0
        # quadra - 1
        # Prédios - 2 até 8
        # Personagem - 9
        if num == 0 or num == 9:
            #rua
            self.rua = True
            self.colors = [0.3,0.3,0.3]
        elif num == 1:
            #quadra
            self.colors = [1,0,0]
        elif num > 1:
            self.escala = Point(1,num,1)
            #predio
            pass
        pass