from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

r = 0
THETA = 25

THETA2 = 45
THETA3 = 165
THETA4 = 75

R = 0.8
K = 0
L = 0.5

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutCreateWindow(b"tree")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(SpaceDown)
    glutKeyboardUpFunc(SpaceUp)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLineWidth(2.0)

    glEnable(GL_DEPTH_TEST)

def resize(w, h):
    glViewport(0, 0, w, h)
    
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(30.0, float(w)/h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()


def v(k, l):
    def v1(rotation, preRot):
        global K, R
        nonlocal k, l
        glPushMatrix()
        glTranslated(0, l, 0)

        glRotated(preRot, 0, 1, 0)    
        glRotated(rotation, 1, 0, 0)
        drawBranch(l)
       
        v(k+1, l*R)
    
    if(K < k or k == 0):
        return
    else:
        v1(-THETA, THETA2)
        glPopMatrix()

        v1(-THETA, THETA3)
        glPopMatrix()

        v1(-THETA, -THETA4)
        glPopMatrix()

def drawBranch(l):
    glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2d(0, 0)
    glVertex2d(0, l)
    glEnd()
    

def display():
    global r
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5.0, 5.0, 5.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0)

    glRotated(float(r), 0.0, 1.0, 0.0)
    glTranslated(0, 2, 0)

    drawBranch(L)

    v(1, L)
    glutSwapBuffers()

    r += 1

    if r >= 360:
        r = 0

def mouse(button, state, x, y):
    global K, L
    if state == GLUT_DOWN :
        if button == GLUT_LEFT_BUTTON:
            K += 1
        elif button == GLUT_RIGHT_BUTTON:
            K = 0
            init()

def SpaceDown(key, x, y):
    if(key == b' '):
        glutIdleFunc(idle)
    else: 
        print(str(key))

def SpaceUp(key, x, y):
    if(key == b' '):
        glutIdleFunc(0)



if __name__ == "__main__": main()
