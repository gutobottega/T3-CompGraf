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
class Instance:   
    def __init__(self, nome):
        self.max = Point()
        self.min = Point()
        self.position = Point (0,-20,0) 
        self.escala = Point (1,1,1)
        self.rotation:float = 0.0
        self.movement = Point(0,1,0)
        self.speed = 2
        self.counter = time.time()
        self.colors = []
        self.max = Point (0,0,0)
        self.min = Point (0,0,0)
        self.columnsOffset = 0
        self.linesOffset = 0
        self.t = 0.0
        self.curva = []
        self.instance = self.createInstance(nome)
    
    def path(self):
        now = time.time()
        ret = self.speed * (now - self.counter) * 12
        self.counter = now
        return ret
    
    def Draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        self.DrawCharacter()
        glPopMatrix()
        
    def DrawPixel(self):
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(-1, 0)
        glVertex2f(0, 0)
        glVertex2f(0, -1)
        glEnd()
    
    def createInstance(self, nome):
        #TODO: get max and min valuesss
        Nome = nome
        infile = open(Nome)
        line = infile.readline()
        number = int(line)
        for i in range(number):
            self.colors += [infile.readline().split()[1:]]
        [lines, columns] = infile.readline().split()
        lines, columns = (int(lines), int(columns))
        self.linesOffset = floor(lines/2)
        self.columnsOffset = floor(columns/2)
        aux = infile.readlines()
        infile.close()
        return [x.split() for x in aux]

    def DrawCharacter(self):
        for line in range(len(self.instance)):
            for column in range(len(self.instance[line])):
                color = self.colors[int(self.instance[line][column]) - 1]
                glColor3f(int(color[0])/255, int(color[1])/255, int(color[2])/255)
                posX = self.columnsOffset - column
                posY = self.linesOffset - line
                glPushMatrix()
                glTranslatef(posX, posY, 0)
                self.DrawPixel()
                glPopMatrix()
    
    def CreateCurve(self, mid, end):
        self.curva = []
        self.curva += [self.position]
        self.curva += [mid]
        self.curva += [end]