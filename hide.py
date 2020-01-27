from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import *
import time
import numpy as np
import copy
import csv


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

FIELD_WIDTH = 30

dirc = 0.1
r = 0.0
ex = 5.0
ez = 5.0
P2 = [0.0, 0.0]
V = [0.0, 0.0]

point = [[0 for i in range(2)] for j in range (100)]
pointnum = 0
rubberband = 0

t = 2
lightpos = [0.0, 50.0, 0.0, 1.0]

red = [ 0.8, 0.2, 0.2, 1.0 ]
green = [ 0.2, 0.8, 0.2, 1.0 ]
blue = [ 0.2, 0.2, 0.8, 1.0 ]
yellow = [ 0.8, 0.8, 0.2, 1.0 ]
white = [0.8, 0.8, 0.8, 1.0]

ground = [
    [ 0.6, 0.6, 0.6, 1.0 ],
    [ 0.3, 0.3, 0.3, 1.0 ]
]

class Sphere():
    def __init__(self, pos=None, rad=None):
        self.pos = pos
        self.radius = rad 
        



class TCube():
    def __init__(self, pos=None, rad=None, rot=None, ):
        self.pos = pos 
        self.radius = rad 
        self.rot = rot 
        self.axisX = np.array([[1.0], [0.0], [0.0]])
        self.axisY = np.array([[0.0], [1.0], [0.0]])
        self.axisZ = np.array([[0.0], [0.0], [1.0]])
    def getMinVec3(self):
        return self.pos - self.radius

    def getMaxVec3(self):
        return self.pos + self.radius
"""
                  z
                  ^
                  |
                  |
                  |
                  |
                  |
                  |
x<-----------------


"""
ey = 0
blockList = []
sphList = []
blockPos = [
    [[5.0],  [0.0], [5.0]],
    [[6.0],  [0.0], [5.0]],
    [[7.0],  [0.0], [5.0]],
    [[8.0],  [0.0], [5.0]],
    [[9.0],  [0.0], [5.0]],
    [[5.0],  [0.0], [6.0]],
    [[7.0],  [0.0], [6.0]],
    [[8.0],  [0.0], [6.0]],
    [[9.0],  [0.0], [6.0]],
    [[5.0],  [0.0], [7.0]],
    [[7.0],  [0.0], [7.0]],
    [[8.0],  [0.0], [7.0]],
    [[9.0],  [0.0], [7.0]],
    [[5.0],  [0.0], [8.0]],
    [[5.0],  [0.0], [9.0]],
    [[6.0],  [0.0], [9.0]],
    [[7.0],  [0.0], [9.0]],
    [[8.0],  [0.0], [9.0]],
    [[9.0],  [0.0], [9.0]],
    [[-5.0],  [0.0], [5.0]], #
    [[-6.0],  [0.0], [5.0]],
    [[-7.0],  [0.0], [5.0]],
    [[-8.0],  [0.0], [5.0]],
    [[-9.0],  [0.0], [5.0]],
    [[-5.0],  [0.0], [6.0]],
    [[-6.0],  [0.0], [6.0]],
    [[-7.0],  [0.0], [6.0]],
    [[-8.0],  [0.0], [6.0]],
    [[-9.0],  [0.0], [6.0]],
    [[-9.0],  [0.0], [7.0]],
    [[-5.0],  [0.0], [8.0]],
    [[-6.0],  [0.0], [8.0]],
    [[-7.0],  [0.0], [8.0]],
    [[-8.0],  [0.0], [8.0]],
    [[-9.0],  [0.0], [8.0]],
    [[-5.0],  [0.0], [9.0]],
    [[-6.0],  [0.0], [9.0]],
    [[-7.0],  [0.0], [9.0]],
    [[-8.0],  [0.0], [9.0]],
    [[-9.0],  [0.0], [9.0]],
    [[ 5.0],  [0.0], [-5.0]], #
    [[ 6.0],  [0.0], [-5.0]],
    [[ 7.0],  [0.0], [-5.0]],
    [[ 9.0],  [0.0], [-5.0]],
    [[ 5.0],  [0.0], [-6.0]],
    [[ 7.0],  [0.0], [-6.0]],
    [[ 9.0],  [0.0], [-6.0]],
    [[ 5.0],  [0.0], [-7.0]],
    [[ 7.0],  [0.0], [-7.0]],
    [[ 8.0],  [0.0], [-7.0]],
    [[ 9.0],  [0.0], [-7.0]],
    [[ 5.0],  [0.0], [-8.0]],
    [[ 5.0],  [0.0], [-9.0]],
    [[ 6.0],  [0.0], [-9.0]],
    [[ 7.0],  [0.0], [-9.0]],
    [[ 8.0],  [0.0], [-9.0]],
    [[ 9.0],  [0.0], [-9.0]],
    [[ -5.0],  [0.0], [-5.0]], #
    [[ -6.0],  [0.0], [-5.0]],
    [[ -7.0],  [0.0], [-5.0]],
    [[ -8.0],  [0.0], [-5.0]],
    [[ -9.0],  [0.0], [-5.0]],
    [[ -5.0],  [0.0], [-6.0]],
    [[ -6.0],  [0.0], [-6.0]],
    [[ -8.0],  [0.0], [-6.0]],
    [[ -9.0],  [0.0], [-6.0]],
    [[ -5.0],  [0.0], [-7.0]],
    [[ -6.0],  [0.0], [-7.0]],
    [[ -8.0],  [0.0], [-7.0]],
    [[ -9.0],  [0.0], [-7.0]],
    [[ -9.0],  [0.0], [-8.0]],
    [[ -5.0],  [0.0], [-9.0]],
    [[ -6.0],  [0.0], [-9.0]],
    [[ -7.0],  [0.0], [-9.0]],
    [[ -8.0],  [0.0], [-9.0]],
    [[ -9.0],  [0.0], [-9.0]]
]

for  pos in blockPos:
    blockList.append(TCube(np.array(pos), np.array([[0.5], [0.5], [0.5]]), np.array([[0.0], [0.0], [0.0]])))
myP = Sphere(np.array([[ex], [ey], [ez]]), 0.5)

bHit = False
    


       

def DegToRad(deg):
    return deg*pi/180


def DrawCube(pos, radius, rot, color):
    global red, green, white
    if color == 0:
        c = red 
    elif color == 1:
        c = green 
    else:
        c = white 
    
    glPushMatrix()
    glTranslatef(pos[0,0], pos[1,0], pos[2,0])
    glRotatef(rot[2,0], 0, 0, 1)
    glRotatef(rot[0,0], 1, 0, 0)
    glRotatef(rot[1,0], 0, 1, 0)
    glScaled(radius[0,0]*2, radius[1,0]*2, radius[2,0]*2)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, c)
    glutSolidCube(1)
    glPopMatrix()

dis = 0    
colCube =  None

    

def main():
    global t
    #t = time.time()
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow(b"walk through")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(SpaceDown)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def resize(w, h):
    glViewport(0, 0, w, h)
    
    glMatrixMode(GL_PROJECTION)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, float(w)/h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

def display():
    global dirc, r, ex, ez, lightpos
    global K, L, preX, preY, x0, y0
    global P2, e, V, savepoint, t
    global myP, colCube
    global bHit, dis

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    gluLookAt(0.0, 40.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    #gluLookAt(10.0, 10.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)

    scene()
    glutSwapBuffers()


    if r >= 360:
        r = 0


def scene():
    global red, green, blue, yellow, ground
    global FIELD_WIDTH
    global bHit , blockList, sphList

    if bHit is True:
        color = 0
    else:
        color = 2
    

    for cube in  blockList:
        DrawCube(cube.pos, cube.radius, cube.rot, color)
    for sph in sphList:
        DrawSphere(sph)

    glBegin(GL_QUADS) 
    glNormal3d(0.0, 1.0, 0.0) 
    for j in range(-FIELD_WIDTH, FIELD_WIDTH):
        for i in range(-FIELD_WIDTH, FIELD_WIDTH):
            glMaterialfv(GL_FRONT, GL_DIFFUSE, ground[(i + j) & 1]) 
            glVertex3d(i, -0.5, j) 
            glVertex3d(i, -0.5, j + 1) 
            glVertex3d(i + 1, -0.5, j + 1) 
            glVertex3d(i + 1, -0.5, j) 
    glEnd()


def DrawSphere(sph):
    global red, green, white
    
    glPushMatrix()
    glTranslatef(sph.pos[0,0], sph.pos[1,0], sph.pos[2,0])
    glScaled(sph.radius, sph.radius, sph.radius)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, green)
    glutSolidSphere(1, 10, 10)
    glPopMatrix()



preX = 0.1
preY = 0.1
x0 = 0
y0 = 0

def mouse(button, state, x, y):
    global K, L, preX, preY, x0, y0
    global P2, e, V, savepoint, t
    global ex, ez, r, dirc, sphList
    X = 2*(x / WINDOW_WIDTH - 0.5)
    Y = -2*(y / WINDOW_HEIGHT - 0.5)


    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if len(sphList) >= 3:
                pass
            else:
                modul = [0]*16
                proj = [0]*16
                view = [0]*4

                glGetDoublev(GL_MODELVIEW_MATRIX, modul)
                glGetDoublev(GL_PROJECTION_MATRIX, proj)
                glGetIntegerv(GL_VIEWPORT, view)
                cood = 0.4*np.array(gluUnProject(x, WINDOW_HEIGHT-y, 1, glGetDoublev(GL_MODELVIEW_MATRIX, modul),\
                    glGetDoublev(GL_PROJECTION_MATRIX, proj), glGetIntegerv(GL_VIEWPORT, view), ))
                
                cood[1] = 0.0
                cood = cood.reshape(-1,1)
                sphList.append(Sphere(cood, 0.2))

            x0 = X
            y0 = Y
            savepoint[0] = X
            savepoint[1] = Y
            glutIdleFunc(idle)
            display()
        
        elif state == GLUT_UP:
            savepoint[0] = X
            savepoint[1] = Y
            #r = 0
            preX = X
            rubberband = 0
            glutIdleFunc(0)

savepoint = [0, 0]
def SpaceDown(key, x, y):
    global X, Y, V, savepoint, x0, y0
    global bHit, myP,blockList, sphList
    v = 0.3

    if key == b'b':
        if sphList:
            sphList.pop()
    elif key == b' ':
        saveList = []
        print(sphList)
        for sph in sphList:
            saveList.append(np.ravel(sph.pos).tolist())
        print(saveList)
        with open('sphPt.csv', 'w') as f:
            pass
        with open('sphPt.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(saveList)
            print(saveList)

    else:
        print(key)
    
    glutIdleFunc(idle)
    

if __name__ == "__main__": main()
