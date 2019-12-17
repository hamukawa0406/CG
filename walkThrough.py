from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from math import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

dirc = 0.1
r = 0.0
ex = 0.0
ez = 0.0
P2 = [0.0, 0.0]
V = [0.0, 0.0]

point = [[0 for i in range(2)] for j in range (100)]
pointnum = 0
rubberband = 0

t = 0.05
lightpos = [3.0, 4.0, 5.0, 1.0]

red = [ 0.8, 0.2, 0.2, 1.0 ]
green = [ 0.2, 0.8, 0.2, 1.0 ]
blue = [ 0.2, 0.2, 0.8, 1.0 ]
yellow = [ 0.8, 0.8, 0.2, 1.0 ]

ground = [
    [ 0.6, 0.6, 0.6, 1.0 ],
    [ 0.3, 0.3, 0.3, 1.0 ]
]

def main():
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
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    V = [savepoint[0] - x0, savepoint[1] - y0]
    P2 = [V[0]*t + ex, V[1]*t + ez]
    r = P2[0]
    print("x0 =", x0)
    print("P2[0] ", P2[0])

    glRotated(float(r), 0.0, 1.0, 0.0)
    ez = P2[1]
    ex = P2[0]
    glTranslated(-ex, 0.0, ez)

    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)

    scene()
    glutSwapBuffers()


    if r >= 360:
        r = 0


def scene():
    global red, green, blue, yellow, ground

    glPushMatrix() 
    glTranslated(-1.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, green) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(0.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, red) 
    glutSolidCube(1.0) 
    glPopMatrix() 

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

    '''
    glPushMatrix()
    glTranslated(0.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, yellow)
    glutSolidSphere(0.3, 20, 20)
    glPopMatrix()

    '''
    glBegin(GL_QUADS) 
    glNormal3d(0.0, 1.0, 0.0) 
    for j in range(-5, 5):
        for i in range(-5, 5):
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
    
    print("(ex, ez)= ", ex, " ", ez)
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            print(" ")
            x0 = X
            y0 = Y
            #savepoint[0] = X
            savepoint[1] = Y
            glutIdleFunc(idle)
            display()
        
        elif state == GLUT_UP:
            print("savePoint", savepoint[1])
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
    print("(X, Y) = ", X, " ", Y)
    

def SpaceDown(key, x, y):
    if(key == b' '):
        glutIdleFunc(idle)

def SpaceUp(key, x, y):
    if(key == b' '):
        glutIdleFunc(0)



if __name__ == "__main__": main()
