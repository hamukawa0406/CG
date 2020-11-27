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

r = 0.0
ex = 0.0
ez = 0.0
V = [0.0, 0.0]

rubberband = 0

t = 2
lightpos = [0.0, 100.0, 0.0, 1.0]
lightpos2 = [15.0, 10.0, 15.0, 1.0]
lightpos3 = [-15.0, 10.0, 15.0, 1.0]
lightpos4 = [15.0, 10.0, -15.0, 1.0]
lightpos5 = [-15.0, 10.0, -15.0, 1.0]


red = [ 0.8, 0.0, 0.0, 1.0 ]
green = [ 0.0, 0.8, 0.0, 1.0 ]
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
        
class Seek():
    def __init__(self, sph=None):
        self.sph = sph
        self.hit = False



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
ey = 0
blockList = []
sphPtList = []
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
    blockList.append(TCube(np.array(pos), np.array([[0.5], [5.0], [0.5]]), np.array([[0.0], [0.0], [0.0]])))
myP = Sphere(np.array([[ex], [ey], [ez]]), 0.1)
preP = myP


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
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, c)
    glutSolidCube(1)
    glPopMatrix()

def isCollideOBB2Sph(sph, obb):
    global dis
    dis = calcLenOBB2Pt(obb, sph.pos)
    if dis <= sph.radius:
        dis = sph.radius - dis
        return True
    else:
        return False

dis = 0    


def calcLenOBB2Pt(obb, pos):
    cVec = pos - obb.pos
    Vec = np.array([[0],[0],[0]])
    lit = np.array([obb.axisX, obb.axisY, obb.axisZ])
    for i in range(3):
        L = obb.radius[i,0]
        if( L <= 0 ):
             continue
        s = np.dot( np.ravel(pos-obb.pos), np.ravel(lit[i])) / L

        s = abs(s)
        if( s > 1):
            Vec = Vec + (1-s)*L*lit[i] 
        
    return np.linalg.norm(Vec)  

def isCollideSph2Sph(sphA, sphB):
    global dis
    length = np.linalg.norm(np.ravel(sphB.pos-sphA.pos))

    if length <= sphA.radius + sphB.radius:
        dis = sphA.radius + sphB.radius - length
        return True
    else:
        return False

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow(b"walk through")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(KeyDown)
    glutKeyboardUpFunc(KeyUp)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    init()
    glutMainLoop()

startTime = 0
def init():
    global startTime
    global sphPtList
    startTime = time.time()
    with open('sphPt.csv', 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            if not len(row):
                pass
            else:
                ar = np.array(row)
                ar = ar.reshape(-1,1)
                sp = Sphere(ar, 0.2)
                sk = Seek(sp)
                sphPtList.append(sk)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)


def resize(w, h):
    glViewport(0, 0, w, h)
    
    glMatrixMode(GL_PROJECTION)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, float(w)/h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

vx = 0

def display():
    global r, ex, ez, lightpos
    global x0, y0
    global e, V, savepoint
    global myP, preP
    global bHit, dis
    global vx, startTime

    if time.time() - startTime >= 60:
        print("GAME OVER")
        exit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    V = [savepoint[0] - x0, savepoint[1] - y0]


    r += 5*V[0]*t
    
    gluLookAt(0.0, 0.5, 2.0, 0.0, 0.2, 0.0, 0.0, 1.0, 0.0)
    glRotated(float(r), 0.0, 5.0, 0.0)


    myP.pos[0,0] = V[1]*sin(r*pi/180)*t + ex + vx*sin(DegToRad(90+r))
    myP.pos[2,0] = -(V[1]*cos(r*pi/180)*t + ez + vx*cos(DegToRad(90+r)))

    for block in blockList:
        if isCollideOBB2Sph(myP, block) is True:
            bHit = True
            break
    else:
        hitNum = 0
        for sphs in sphPtList:
            if isCollideSph2Sph(myP, sphs.sph):
                hitNum += sphs.hit
                bHit = True
                sphs.hit = True
                break
        else:
            bHit = False
    
    for sphs in sphPtList:
        if sphs.hit is False:
            break
    else:
        print("CLEAR!!!!")
        print("Congraturations!!!")
        exit()
    
 

    if(bHit is True):
        pass
    else:
        ex = myP.pos[0,0]
        ez = -myP.pos[2,0]
    

    if bHit is False:
        preP = myP


    glTranslated(-ex, 0.0, ez)


    lightpos[0] = myP.pos[0,0]
    lightpos[2] = myP.pos[2,0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    glLightfv(GL_LIGHT1, GL_POSITION, lightpos2)
    glLightfv(GL_LIGHT2, GL_POSITION, lightpos3)
    glLightfv(GL_LIGHT3, GL_POSITION, lightpos4)
    glLightfv(GL_LIGHT4, GL_POSITION, lightpos5)

    scene()
    glutSwapBuffers()


    if r >= 360:
        r = 0


def scene():
    global red, green, blue, yellow, ground
    global FIELD_WIDTH
    global bHit , blockList, sphPtList, myP

    if bHit is True:
        color = 0
    else:
        color = 2

    DrawSphere(myP, True)
    for cube in  blockList:
        DrawCube(cube.pos, cube.radius, cube.rot, color)
    for sphs in sphPtList:
        DrawSphere(sphs.sph, sphs.hit)
    

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

def DrawSphere(sph, hit):
    global red, green, yellow, white
    if hit is True:
        color = green
    else:
        color = red
    
    glPushMatrix()
    glTranslatef(sph.pos[0,0], sph.pos[1,0], sph.pos[2,0])
    glScaled(sph.radius, sph.radius, sph.radius)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
    glutSolidSphere(1, 100, 100)
    glPopMatrix()


x0 = 0
y0 = 0

def mouse(button, state, x, y):
    global x0, y0
    global savepoint
    X = 2*(x / WINDOW_WIDTH - 0.5)
    Y = -2*(y / WINDOW_HEIGHT - 0.5)
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            x0 = X
            savepoint[0] = X
            glutIdleFunc(idle)
            display()
        
        elif state == GLUT_UP:
            x0 = 0
            savepoint[0] = 0
            rubberband = 0
            glutIdleFunc(0)

savepoint = [0, 0]
def motion(x, y):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global savepoint
    global ex, ez
    X = 2*(x / WINDOW_WIDTH - 0.5)
    Y = -2*(y / WINDOW_HEIGHT - 0.5)

    savepoint[0] =  X

    glEnable(GL_COLOR_LOGIC_OP)
    glLogicOp(GL_INVERT)

    glLogicOp(GL_COPY)
    glDisable(GL_COLOR_LOGIC_OP)

    rubberband = 1
    glutIdleFunc(idle)
    

def KeyDown(key, x, y):
    global savepoint, x0, y0
    global bHit, vx
    v = 0.3
    if(key == b'w'):
        y0 = 0
        if bHit is True:
            savepoint[1] = 0.0
        else:
            savepoint[1] = v
    elif key == b'a':
        vx = -v
    elif key == b's':
        y0 = 0
        savepoint[1] = -v
    elif key == b'd':
        vx = v
    
    glutIdleFunc(idle)
    


def KeyUp(key, x, y):
    global vx
    global savepoint
    if key == b'w' or key == b's':
        savepoint[1] = 0.0
    elif key == b'a' or key == b'd':
        vx = 0
    glutIdleFunc(idle)



if __name__ == "__main__": main()
