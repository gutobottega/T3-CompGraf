# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
# 
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
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
# 
# ***********************************************************************************
from math import cos, radians, sin
from random import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from jogador import Jogador
from Point import Point
from PIL import Image
import numpy as np
#from PIL import Image
import time

from Mapa import Mapa

quadras = []
ruas = []
texturas = []
recargas = []

player = Jogador()
player.position = Point(0, 0.5, 0)
player.alvo = Point(0, 0, 1)
alvoCamera = Point(0, 0, 1)

#PARÂMETROS
velocidade = 1
combustivel = 100
textura = 1
#texturas
#0 Piso.jpg
#1 None.png
#2 CROSS.png
movimenta = False
terceiraPessoa = False
visaoSuperior = False

# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    global texturas
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    texturas += [carregaTextura('None.png')]
    texturas += [carregaTextura('CROSS.png')]
    criaMapa()

def carregaTextura(nome) -> int:
    # carrega a imagem
    image = Image.open(nome)
    image = image.convert('RGB')
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL 
    img_data = np.array(list(image.getdata()), np.uint8)

    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION: 
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()
    return texture
    
def criaMapa():
    global quadras, ruas, player, texturas, recargas
    infile = open('map.txt')
    lines = infile.readlines()
    infile.close()
    matriz = []
    
    glBindTexture(GL_TEXTURE_2D, texturas[textura])
    
    for line in lines:
        matriz.append(line.split('\t'))
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            newMapa = Mapa()
            newMapa.position.set(j,0,i)
            
            num = int(matriz[i][j])
            # Rua - 0
            # quadra - 1
            # Personagem - 2
            # Prédios - 3 até maior
            if num == 0 or num == 2:
                #rua
                newMapa.criaRua()
                if num == 2: player.position.set(j,player.position.y,i)
                ruas.append(newMapa)
                if random() < 0.1:
                    recargas.append(newMapa.position)
            elif num == 1:
                #quadra
                newMapa.colors = [1,0,0]
                quadras.append(newMapa)
            else:
                #predio
                newMapa.escala = Point(1,num,1)
                quadras.append(newMapa)
# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
	# Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
	# Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)
    
    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4] 
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0 ]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, Especularidade)
    return
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)
    
def dentro(p1:Point,p2:Point):
    if(p1.x + 0.5 > p2.x and p1.x - 0.5 < p2.x):
        if(p1.z + 0.5 > p2.z and p1.z - 0.5 < p2.z):
            return True
    return False
    
def estaDentroDasRuas(newPos):
    for s in range(len(ruas)):
        if(dentro(ruas[s].position, newPos)):
            return True
    return False
# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCubo(tamanho):
    glutSolidCube(tamanho)
    
def desenhaCombustivel():
    for pos in recargas:
        glPushMatrix()
        glTranslatef(pos.x, pos.y + 0.5, pos.z)
        glColor3f(1,1,0)
        glScalef(0.3, 0.3, 0.3)
        glutSolidCube(1)
        glPopMatrix()
        
def checaCombustivel():
    global recargas, combustivel
    remove = []
    for i in range(len(recargas)):
        pos = recargas[i]
        if(dentro(player.position, pos)):
            combustivel += 10
            remove += [i]
    for i in remove:
        recargas.pop(i)

def PosicUser():
    global player, combustivel
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    if movimenta and combustivel > 0:
        move = player.move(velocidade)
        newPos = player.position + player.movement * move
        if estaDentroDasRuas(newPos):
            combustivel -= move
            print(combustivel)
            player.position = newPos
    else: player.counter = time.time()
    gluPerspective(60,AspectRatio,0.01,50) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if terceiraPessoa:
        alvo = player.position
        pos = alvo - alvoCamera * 5
    else:
        pos = player.position
        alvo = alvoCamera + pos
    if not visaoSuperior:
        gluLookAt(pos.x, pos.y, pos.z, 
                alvo.x, alvo.y, alvo.z, 
                0,1.0,0)
    else:
        gluLookAt(pos.x, 20, pos.z, 
                alvo.x, 0, alvo.z, 
                0,1.0,0)
    
# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
       
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
    
    glColor3f(1,1,1) # desenha a borda da QUAD 
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()
     
# **********************************************************************
def DesenhaPisoOld():
    glPushMatrix()
    glTranslated(-20,-1,-10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()    
     
def DesenhaPiso():
    global quadras,ruas
    for m in ruas:
        m.desenha()
    for m in quadras:
        m.desenha()

def rotaciona(V:Point, angulo:float):
    angulo = radians(angulo)
    x = V.x * cos(angulo) + V.z * sin(angulo)
    z = -V.x * sin(angulo) + V.z * cos(angulo)
    return Point(x, V.y, z)


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    global Angulo
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    DefineLuz()
    player.desenha()
    PosicUser()

    glMatrixMode(GL_MODELVIEW)
    DesenhaPiso()
    
    checaCombustivel()
    desenhaCombustivel()
   

    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global movimenta, terceiraPessoa, alvoCamera, visaoSuperior, combustivel
    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada
    if args[0] == b' ':
        movimenta = not movimenta
    if args[0] == b'm':
        visaoSuperior = not visaoSuperior
    if args[0] == b'c':
        combustivel = 10
    if args[0] == b'v':
        terceiraPessoa = not terceiraPessoa
    if args[0] == b'a':
        player.rotation += 15
        player.movement = rotaciona(player.movement, 15)
        alvoCamera = rotaciona(alvoCamera, 15)
    if args[0] == b'd':
        player.rotation -= 15
        player.movement = rotaciona(player.movement, -15)
        alvoCamera = rotaciona(alvoCamera, -15)

    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global alvoCamera
    if a_keys == GLUT_KEY_LEFT:
        alvoCamera = rotaciona(alvoCamera, +15)
        
    if a_keys == GLUT_KEY_RIGHT:
        alvoCamera = rotaciona(alvoCamera, -15)
        
    if a_keys == GLUT_KEY_DOWN:
        alvoCamera.y -= 0.1
        
    if a_keys == GLUT_KEY_UP:
        alvoCamera.y += 0.1
    
    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL 3D")
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutSpecialFunc(arrow_keys);
# executa algumas inicializaÃ§Ãµes
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


gluLookAt(10, 2, 10, 
        10, 1, 11, 
        0,1.0,0) 
try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
