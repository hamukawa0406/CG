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

class mat44():
    """
    ret = np.matrix((
        [
            [1.0,0.0,0.0,0.0],
            [0.0,1.0,0.0,0.0],
            [0.0,0.0,1.0,0.0],
            [0.0,0.0,0.0,1.0]
        ]
    ))
    """
    def __init__(self):
        self.ret = np.matrix((
            [
                [1.0,0.0,0.0,0.0],
                [0.0,1.0,0.0,0.0],
                [0.0,0.0,1.0,0.0],
                [0.0,0.0,0.0,1.0]
            ]
        ))
    def rotate(self, axis, rad):
        sinA = sin(rad)
        cosA = cos(rad)
        if(axis == "X" or axis == "x"):
            self.ret[0,0] = 1.0
            self.ret[0,1] = 0.0
            self.ret[0,2] = 0.0
            self.ret[1,0] = 0.0
            self.ret[1,1] = cosA
            self.ret[1,2] = -sinA
            self.ret[2,0] = 0.0
            self.ret[2,1] = sinA
            self.ret[2,2] = cosA
        elif(axis == "Y" or axis == "y"):
            self.ret[0,0] = cosA 
            self.ret[0,1] = 0.0
            self.ret[0,2] = sinA
            self.ret[1,0] = 0.0
            self.ret[1,1] = 1.0
            self.ret[1,2] = 0.0
            self.ret[2,0] = -sinA
            self.ret[2,1] = 0.0
            self.ret[2,2] = cosA
        elif(axis == "Z" or axis == "z"):
            self.ret[0,0] = cosA 
            self.ret[0,1] = -sinA
            self.ret[0,2] = 0.0
            self.ret[1,0] = sinA
            self.ret[1,1] = cosA
            self.ret[1,2] = 0.0
            self.ret[2,0] = 0.0
            self.ret[2,1] = 0.0
            self.ret[2,2] = 1.0
        
        self.ret[3, 0:3] = 0.0
        self.ret[0:3, 3] = 0.0
        self.ret[3, 3] = 1.0
        return self.ret
        
    def YawPitchRoll(self, y, x, z):
        mY = copy.copy(self.rotate('y', y))
        mX = copy.copy(self.rotate('x', x))
        mZ = copy.copy(self.rotate('z', z))
        mM = mZ*mX
        mat = mM*mY
        return mat
        

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

    def updateAxisAll(self):
        mRot = mat44()
        mRot.ret = mRot.YawPitchRoll(DegToRad(self.rot[0,0]), DegToRad(self.rot[1,0]), DegToRad(self.rot[2,0]))
        self.axisX = mRot.ret*np.matrix([[1], [0], [0], [1]])
        self.axisX = self.axisX[0:3]
        self.axisY = mRot.ret*np.matrix([[0], [1], [0], [1]])
        self.axisY = self.axisY[0:3]
        self.axisZ = mRot.ret*np.matrix([[0], [0], [1], [1]])
        self.axisZ = self.axisZ[0:3]

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


def IsCollideBoxOBB(cA, cB):
    vDistance = cB.pos - cA.pos

    cA.updateAxisAll()
    cB.updateAxisAll()

    if not CompareLengthOBB(cA, cB, cA.axisX, vDistance):
        return False
    if not CompareLengthOBB(cA, cB, cA.axisY, vDistance):
        return False

    if not CompareLengthOBB(cA, cB, cA.axisZ, vDistance):
        return False

    if not CompareLengthOBB(cA, cB, cB.axisX, vDistance):
        return False

    if not CompareLengthOBB(cA, cB, cB.axisY, vDistance):
        return False

    if not CompareLengthOBB(cA, cB, cB.axisZ, vDistance):
        return False

    vSep = np.array([0, 0, 0])
    vSep = np.cross(cA.axisX.T.flatten(), cB.axisX.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False
    vSep = np.cross(cA.axisX.T.flatten(), cB.axisY.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisX.T.flatten(), cB.axisZ.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisY.T.flatten(), cB.axisX.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisY.T.flatten(), cB.axisY.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisY.T.flatten(), cB.axisZ.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisZ.T.flatten(), cB.axisX.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisZ.T.flatten(), cB.axisY.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False

    vSep = np.cross(cA.axisZ.T.flatten(), cB.axisZ.T.flatten())
    if not CompareLengthOBB(cA, cB, vSep, vDistance):
        return False
    
    return True



def CompareLengthOBB(cA, cB, vSep, vDistance):
    dotVal = np.dot(np.ravel(vSep), vDistance.T.flatten())
    length = fabs(dotVal)

    dotValX = np.dot(np.ravel(cA.axisX), np.ravel(vSep))
    dotValY = np.dot(np.ravel(cA.axisY), np.ravel(vSep))
    dotValZ = np.dot(np.ravel(cA.axisZ), np.ravel(vSep))

    lenA = fabs(dotValX*cA.radius[0,0]) \
         + fabs(dotValY*cA.radius[1,0]) \
         + fabs(dotValZ*cA.radius[2,0])
    
    dotValX = np.dot(np.ravel(cB.axisX), np.ravel(vSep))
    dotValY = np.dot(np.ravel(cB.axisY), np.ravel(vSep))
    dotValZ = np.dot(np.ravel(cB.axisZ), np.ravel(vSep))

    lenB = fabs(dotValX*cB.radius[0,0]) \
         + fabs(dotValY*cB.radius[1,0]) \
         + fabs(dotValZ*cB.radius[2,0])

 
    if length > lenA + lenB:
        return False
    return True

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

def isCollideOBB2Sph(sph, obb):
    global dis, colCube
    dis = calcLenOBB2Pt(obb, sph.pos)
    if dis <= sph.radius:
        dis = sph.radius - dis
        colCube = obb
        return True
    else:
        return False

dis = 0    
colCube =  None

def calcLenOBB2Pt(obb, pos):
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
    glutKeyboardUpFunc(SpaceUp)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
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

    #t = time.time() - t

    V = [savepoint[0] - x0, savepoint[1] - y0]

    r = 10*V[0]*t+r
    
    gluLookAt(0.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

    #glRotated(float(r), 0.0, 1.0, 0.0)
    for block in blockList:
        if isCollideOBB2Sph(myP, block) is True:
            bHit = True
            break
    else:
        bHit = False

    vec = np.array([V[1]*sin(r*pi/180)*t, 0, V[1]*cos(r*pi/180)*t])

    if(bHit is True):
        dirct = np.dot(vec, np.ravel(colCube.pos))
        if dirct >= 0:
            ez += -1.1*dis*cos(r*pi/180)*t
            ex += 1.1*dis*cos(r*pi/180)*t
        else:
            ez += 1.1*dis*cos(r*pi/180)*t
            ex += -1.1*dis*cos(r*pi/180)*t
    else:
        ez = V[1]*cos(r*pi/180)*t + ez
        ex = V[1]*sin(r*pi/180)*t + ex
    
    myP.pos[0,0] = ex
    myP.pos[2,0] = -ez

    #glTranslated(-ex, 0.0, ez)

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
    
    DrawQuadrangle()

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

def DrawQuadrangle():
    depth = 10
    glBegin(GL_POLYGON)
    glColor4f(1.0, 0.0, 1.0, 1.0)
    glVertex3d(10 , depth, 0)
    glColor4f(1.0, 0.0, 1.0, 1.0)
    glVertex3d(-10 , depth, 0)
    glColor4f(1.0, 0.0, 1.0, 1.0)
    glVertex3d(-10 , depth, 10)
    glColor4f(1.0, 0.0, 1.0, 1.0)
    glVertex3d(10 , depth, 10)
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
                cood = 0.5*np.array(gluUnProject(x, WINDOW_HEIGHT-y, 1, glGetDoublev(GL_MODELVIEW_MATRIX, modul),\
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
def motion(x, y):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global V, P2, savepoint, x0, y0
    global t, ex, ez, dirc, preX
    X = 2*(x / WINDOW_WIDTH - 0.5)
    Y = -2*(y / WINDOW_HEIGHT - 0.5)

    savepoint[0] = X
    savepoint[1] = Y

    glEnable(GL_COLOR_LOGIC_OP)
    glLogicOp(GL_INVERT)

    if preX*X < 0:
        dirc = -dirc
    preX = X

    glLogicOp(GL_COPY)
    glDisable(GL_COLOR_LOGIC_OP)


    rubberband = 1
    

def SpaceDown(key, x, y):
    global X, Y, V, savepoint, x0, y0
    global bHit, myP,blockList, sphList
    v = 0.3
    if(key == b'w'):
        y0 = 0
        if bHit is True:
            savepoint[1] = 0.0
        else:
            savepoint[1] = v
    elif key == b'a':
        x0 = 0
        savepoint[0] = -v
    elif key == b's':
        y0 = 0
        savepoint[1] = -v
    elif key == b'd':
        x0 = 0
        savepoint[0] = v
    elif key == b'b':
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
    


def SpaceUp(key, x, y):
    global V
    if key == b'w' or key == b's':
        savepoint[1] = 0.0
    elif key == b'a' or key == b'd':
        savepoint[0] = 0.0
    glutIdleFunc(0)



if __name__ == "__main__": main()
