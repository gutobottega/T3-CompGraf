# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe uma curva de Bezier em OpenGL
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from math import degrees, floor, cos, radians, sin, sqrt
import math
from random import random
from time import sleep
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Instance import *
from Point import *

# ***********************************************************************************

# Vida do jogador
lifes = 3
hearts = []
dead = Instance('personagens/c0.txt')

#Enemy quantity
amtEnemies = 5

#shots
amtShots = 10
amtEnemyShots = 5
characterFireRate = 0.1
enemyFireRate = 3


characterFireRateCounter = time.time()
enemyFireRateCounter = time.time()



modelos = [
    "personagens/p1.txt",
    "personagens/p2.txt",
    "personagens/p3.txt",
    "personagens/p4.txt",
    "personagens/p5.txt",
    "personagens/p6.txt",
    "personagens/p7.txt",
    "personagens/p8.txt"
    ]

# ***********************************************************************************

# Limites da Janela de Seleção
Min = Point()
Max = Point()

# Quantidade de inimigos no universo

character = Instance('personagens/personagem.txt')

# lista de instancias do universo
enemies = [] 

# lista de instancias do universo
characterShots = [] 
enemyShots = [] 

# **************************************************************
def CalculeBezier3(PC, t:float):
    P = Point()
    UmMenosT:float = 1-t;
    P =  PC[0] * UmMenosT * UmMenosT + PC[1] * 2 * UmMenosT * t + PC[2] * t*t;
    #P.imprime()
    return P

# ***********************************************************************************
# def TracaBezier3Points():
    
#     t=1.0
#     DeltaT = 1.0/50
#     P = Point;
#     glBegin(GL_LINE_STRIP);
    
#     while(t<1.0):
#         P = CalculaBezier3(Curva1, t)
#         glVertex2f(P.x, P.y)
#         t += DeltaT
#     P = CalculaBezier3(Curva1, 1.0) #faz o acabamento da curva
#     glVertex2f(P.x, P.y)
    
#     glEnd()

# ***********************************************************************************
def reshape(w,h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
def DrawInstances():
    [x.Draw() for x in enemies]
    [x.Draw() for x in characterShots]
    [x.Draw() for x in enemyShots]
    character.Draw()
    [x.Draw() for x in hearts]
    
def rotaciona(V:Point, angulo:float):
    angulo = radians(angulo)
    x = V.x * cos(angulo) - V.y * sin(angulo)
    y = V.x * sin(angulo) + V.y * cos(angulo)
    return Point(x, y)

def distance(A,B):
    xA = A.x
    yA = A.y
    xB = B.x
    yB = B.y
    return sqrt((xA-xB)**2) + ((yA-yB)**2)

def curveLength(curva):
    DeltaT = 1.0/50;
    t=DeltaT;
    curveLength = 0;
    P1 = CalculeBezier3(curva,0.0)
    while(t<1.0):
        P2 = CalculeBezier3(curva, t)
        curveLength += distance(P1,P2);
        P1 = P2;
        t += DeltaT;
        
    P2 = CalculeBezier3(curva, 1.0)
    curveLength += distance(P1,P2);
    return curveLength


# **************************************************************
def DesenhaEixos():
    global Min, Max

    Meio = Point(); 
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
    glEnd()
    
def asHit(p1:Instance,p2:Instance):
    if(abs(p1.position.x - p2.position.x) > (p1.columnsOffset + p2.columnsOffset)):
        return False
    if(abs(p1.position.y - p2.position.y) > (p1.linesOffset + p2.linesOffset)):
        return False
    return True

def checkEnemyHitBox():
    removeS = []
    removeE = []
    for s in range(len(characterShots)):
        for e in range(len(enemies)):
            if(asHit(characterShots[s], enemies[e])):
                if s not in removeS: removeS += [s]
                if e not in removeE: removeE += [e]
    removeS.sort(reverse=True)
    removeE.sort(reverse=True)
    [characterShots.pop(j) for j in removeS]
    [enemies.pop(j) for j in removeE]

def checkCharacterHitBox():
    global character, lifes
    removeS = []
    removeE = []
    hit = False
    for s in range(len(enemyShots)):
        if(asHit(enemyShots[s], character)):
            if s not in removeS: removeS += [s]
            hit = True
    for e in range(len(enemies)):
        if(asHit(enemies[e], character)):
            if e not in removeE: removeE += [e]
            hit = True
    removeS.sort(reverse=True)
    removeE.sort(reverse=True)
    [enemyShots.pop(j) for j in removeS]
    [enemies.pop(j) for j in removeE]
    if(hit):
        character.position = Point (0,-20,0)
        lifes -= 1
        updateHearts()


def isVisible(pos):
    if(pos.x < Max.x and pos.x > Min.x):
            if(pos.y < Max.y and pos.y > Min.y):
                return True
    return False
# ***********************************************************************************
def updateCharacterShots():
    remove = []
    for i in range(len(characterShots)):
        newPos = characterShots[i].position + rotaciona(characterShots[i].movement, characterShots[i].rotation) * characterShots[i].speed
        if(not isVisible(newPos)):
            remove += [i]
        else: characterShots[i].position = newPos
    remove.sort(reverse=True)
    [characterShots.pop(j) for j in remove]
    
def updateEnemyShots():
    remove = []
    for i in range(len(enemyShots)):
        newPos = enemyShots[i].position + rotaciona(enemyShots[i].movement, enemyShots[i].rotation) * enemyShots[i].speed
        if(not isVisible(newPos)):
            remove += [i]
        else: enemyShots[i].position = newPos
    remove.sort(reverse=True)
    [enemyShots.pop(j) for j in remove]
    

def dotproduct(v1, v2):
      return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    v1 = [v1.x,v1.y,v1.z]
    v2 = [v2.x,v2.y,v2.z]
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def updateEnemies():
    global enemies, Max, Min, counter, enemyFireRateCounter, enemyShots
    for enemy in enemies:
        if enemy.t>1.0:
            DeltaT = enemy.path()/curveLength(enemy.curva)
            
            end = Point()
            end.y = random() * (Max.y - Min.y) + Min.y 
            if (enemy.position.x < 0): 
                end.x = Max.x
            else: end.x = Min.x
            enemy.CreateCurve(character.position, end)
            enemy.t = 0.0
        else:
            DeltaT = enemy.path()/curveLength(enemy.curva)
            enemy.t = enemy.t + DeltaT
            if(random() > 0.2):
                now = time.time()
                if(now - enemyFireRateCounter > enemyFireRate):
                    enemyFireRateCounter = now
                    if(len(enemyShots) + 1 <= amtEnemyShots):
                        inst = Instance('personagens/tiro.txt')
                        inst.position = enemy.position
                        aux = character.position - inst.position
                        inst.rotation = degrees(angle(enemy.movement, aux))
                        if(aux.x > 0): inst.rotation = -inst.rotation
                        inst.speed = 1
                        enemyShots += [inst]
                        inst.Draw()
        P = CalculeBezier3(enemy.curva, enemy.t)
        enemy.position = P
        enemy.Draw()
    counter = time.time()
    
# ***********************************************************************************
def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(3)
    glColor3f(1,1,1) # R, G, B  [0..1]
    #DesenhaEixos()
    glColor3f(1,1,0)
    updateEnemies()
    updateCharacterShots()
    updateEnemyShots()
    checkEnemyHitBox()
    checkCharacterHitBox()
    if lifes == 0: 
        print('You lost D=')
        sleep(1)
        os._exit(0)
    elif len(enemies) == 0:
        print('You won =D')
        print("With", lifes, "life left.")
        sleep(1)
        os._exit(0)
    DrawInstances()
    glColor3f(1,0,0)

    glutSwapBuffers()
 
# ***********************************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global characterShots, characterFireRateCounter
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == b' ':
        now = time.time()
        if(now - characterFireRateCounter > characterFireRate):
            characterFireRateCounter = now
            if(len(characterShots) + 1 <= amtShots):
                inst = Instance('personagens/tiro.txt')
                inst.position = character.position
                inst.rotation = character.rotation
                characterShots += [inst]
    if args[0] == ESCAPE:
        os._exit(0)
    glutPostRedisplay()

# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global character
    character = character
    if a_keys == GLUT_KEY_UP:  
        newPos = character.position + rotaciona(character.movement, character.rotation) * character.speed
        if(isVisible(newPos)):
            character.position = newPos
            
    if a_keys == GLUT_KEY_DOWN:  
        newPos = character.position - rotaciona(character.movement, character.rotation) * character.speed
        if(isVisible(newPos)):
            character.position = newPos

    if a_keys == GLUT_KEY_LEFT:
        character.rotation += 15 
        
    if a_keys == GLUT_KEY_RIGHT:
        character.rotation -= 15
        pass

    glutPostRedisplay()

# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PointClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PointClicado = Point (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PointClicado.imprime("Point Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return

def updateHearts():
    if(lifes>2):return
    hearts[lifes].colors = dead.colors

def createHearts():
    global hearts
    hearts += [Instance('personagens/c1.txt')]
    hearts += [Instance('personagens/c1.txt')]
    hearts += [Instance('personagens/c1.txt')]
    
    hearts[0].position = Point(Min.x + 30, Min.y +10)
    hearts[1].position = Point(Min.x + 20, Min.y +10)
    hearts[2].position = Point(Min.x + 10, Min.y +10)

def CreateEnemies():
    global enemies, Max
    aux = [
        Point(-Max.x, 50, 0),
        Point(Max.x, -50, 0),
        Point(-20, 50, 0),
        Point(-70, 20, 0),
        Point(0, -50, 0),
        Point(20, 80, 0),
        Point(50, 0, 0),
        Point(70, -10, 0),
    ]
    for i in range(amtEnemies):
        enemy = Instance(modelos[int(random()*len(modelos))])
        enemy.position = aux[int(random()*len(aux))]
        end = Point()
        end.y = random() * (Max.y - Min.y) + Min.y 
        if (enemy.position.x < 0): 
            end.x = Max.x
        else: end.x = Min.x
        enemy.CreateCurve(Point(),end)
        enemies.append(enemy)  

# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela (PRETA)
    glClearColor(29/255, 41/255, 81/255, 1)
    d:int = 80
    Min = Point(-d,-d)
    Max = Point(d,d)
    CreateEnemies()
    createHearts()


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Animacao com Bezier")
glutDisplayFunc(display)
glutIdleFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutSpecialFunc(arrow_keys);
init()

try:
    glutMainLoop()
except SystemExit:
    pass
