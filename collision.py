from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import *
import time
import numpy as np
import copy


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

FIELD_WIDTH = 30

dirc = 0.1
r = 0.0
ex = 0.0
ez = 0.0
P2 = [0.0, 0.0]
V = [0.0, 0.0]

point = [[0 for i in range(2)] for j in range (100)]
pointnum = 0
rubberband = 0

t = 2
lightpos = [0.0, 10.0, 0.0, 1.0]

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
        

 


class TCube():
    def __init__(self, pos=None, rad=None, rot=None, ):
        self.pos = pos 
        self.radius = rad 
        self.rot = rot 
        self.axisX = np.array([[0.0], [0.0], [0.0]])
        self.axisY = np.array([[0.0], [0.0], [0.0]])
        self.axisZ = np.array([[0.0], [0.0], [0.0]])
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


myC = TCube(np.array([[-1.0], [0.0], [-3.0]]), np.array([[0.6], [0.5], [0.4]]), np.array([[45.0], [0.0], [0.0]]))
tarC = TCube(np.array([[0.0], [0.0], [-3.0]]), np.array([[0.6], [0.5], [0.4]]), np.array([[0.0], [0.0], [0.0]]))
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
    print(np.ravel(vSep))
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

 
    #print(length, lenA, lenB)
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
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(rot[2], 0, 0, 1)
    glRotatef(rot[0], 1, 0, 0)
    glRotatef(rot[1], 0, 1, 0)
    glScaled(radius[0]*2, radius[1]*2, radius[2]*2)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, c)
    glutSolidCube(1)
    glPopMatrix()

    

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
    global myC, tarC
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



    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    #t = time.time() - t

    V = [savepoint[0] - x0, savepoint[1] - y0]
    P2 = [V[0]*t + ex, V[1]*t + ez]
    r = 10*V[0]*t+r

    glRotated(float(r), 0.0, 1.0, 0.0)
    ez = V[1]*cos(r*pi/180)*t + ez
    ex = V[1]*sin(r*pi/180)*t + ex

    glTranslated(-ex, 0.0, ez)


    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)

    scene()
    glutSwapBuffers()


    if r >= 360:
        r = 0


def scene():
    global red, green, blue, yellow, ground
    global FIELD_WIDTH
    global myC, tarC, bHit

    if bHit is True:
        color = 0
    else:
        color = 2

    """
    glPushMatrix() 
    glTranslated(-1.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, green) 
    glutSolidCube(1.0) 
    glPopMatrix() 
    """
    DrawCube(myC.pos, myC.radius, myC.rot, color)
    DrawCube(tarC.pos, tarC.radius, tarC.rot, color)

    """
    glPushMatrix() 
    glTranslated(0.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, red) 
    glutSolidCube(1.0) 
    glPopMatrix() 
    """

    """
    glPushMatrix() 
    glTranslated(1.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, yellow) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(1.0, 0.0, -2.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(1.0, 0.0, -1.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, red) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(1.0, 0.0, 0.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(1.0, 0.0, 1.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(1.0, 0.0, 2.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(0.0, 0.0, 2.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(-1.0, 0.0, 2.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 


    glPushMatrix() 
    glTranslated(1.0, 0.0, 3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 


    glPushMatrix() 
    glTranslated(2.0, 0.0, 0.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(3.0, 0.0, 0.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 
    """

    '''
    glPushMatrix()
    glTranslated(0.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, yellow)
    glutSolidSphere(0.3, 20, 20)
    glPopMatrix()

    '''

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


preX = 0.1
preY = 0.1
x0 = 0
y0 = 0

def mouse(button, state, x, y):
    global K, L, preX, preY, x0, y0
    global P2, e, V, savepoint, t
    global ex, ez, r, dirc
    X = 2*(x / WINDOW_WIDTH - 0.5)
    Y = -2*(y / WINDOW_HEIGHT - 0.5)
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            x0 = X
            y0 = Y
            #savepoint[0] = X
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
    global bHit, myC, tarC
    v = 0.3
    if(key == b'w'):
        y0 = 0
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
    
    if IsCollideBoxOBB(myC, tarC) is True:
        bHit = True
    else:
        bHit = False
    glutIdleFunc(idle)
    


def SpaceUp(key, x, y):
    global V
    if key == b'w' or key == b's':
        savepoint[1] = 0.0
    elif key == b'a' or key == b'd':
        savepoint[0] = 0.0
    glutIdleFunc(0)



if __name__ == "__main__": main()
