from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

THETA = 25
THETA2 = 30
R = 0.8
K = 0
L = 0.3

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutCreateWindow(b"GLUT prog1")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    global L
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLineWidth(2.0)



    glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2d(0, 0)
    glVertex2d(0, L)
    glEnd()
    glFlush()

def resize(w, h):
    glViewport(0, 0, w, h)
    
    glLoadIdentity()
    gluPerspective(30.0, float(w)/h, 1.0, 100.0)
    gluLookAt(5.0, 5.0, 5.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0)

#    glMatrixMode(GL_MODELVIEW)

def v(k, l):
    def v1(rotation, preRot):
        global K, R
        nonlocal k, l
        glPushMatrix()
        glColor3d(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex2d(0, 0)
        glVertex2d(0, l)
        glEnd()

        glTranslated(0, l, 0)

        if preRot == 0:
            glRotated(preRot, 0, 0, 1)
            glRotated(rotation, 0, 0, 1)
        elif preRot == THETA2:
            glRotated(preRot, 0, 1, 0)
            glRotated(rotation, 1, 0, 0)
        elif preRot == -THETA2:
            glRotated(preRot, 0, 1, 0)
            glRotated(rotation, 1, 0, 0)

        glColor3d(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex2d(0, 0)
        glVertex2d(0, l)
        glEnd()
        
        v(k+1, l*R)

    if(k == 0):
        return
    
    if(K < k):
        return
    else:
        v1(THETA, 0)
        glPopMatrix()
        v1(THETA, THETA2)
        glPopMatrix()
        v1(-THETA, -THETA2)
        glPopMatrix()
        glColor3d(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2d(-0.001, 0)
        glVertex2d(0.001, 0)
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def mouse(button, state, x, y):
    global K, L
    if state == GLUT_DOWN :
        if button == GLUT_LEFT_BUTTON:
            K += 1
            v(1, L)
        elif button == GLUT_RIGHT_BUTTON:
            K = 0
            glClear(GL_COLOR_BUFFER_BIT)
            glBegin(GL_LINES)
            glEnd()
        glFlush()


if __name__ == "__main__": main()
