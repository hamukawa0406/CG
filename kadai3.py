from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

THETA = 25
THETA2 = 30
R = 0.8

K = 0
L = 0.3

r = 0
red = [0.8, 0.2, 0.2, 1.0]
green = [0.0, 1.0, 0.0, 1.0]

count = 0
           

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)# | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"kadai3")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
#    glEnable(GL_DEPTH_TEST)
    glLineWidth(3.0)

def resize(w, h):
    glViewport(0, 0, w, h)
    
    glLoadIdentity()
#    gluPerspective(30.0, w / h, 1.0, 100.0)
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)


def display():
    global K, L
    glClear(GL_COLOR_BUFFER_BIT)# | GL_DEPTH_BUFFER_BIT)
    glColor3d(0.0, 1.0, 0.0)
#    gluLookAt(3.0, 4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
#    v(K, L)

def v(k, l):
    global THETA, THETA2
    global R, count
    def v1(rotation, preRot):
        nonlocal k
        global count
        glPushMatrix()
        if preRot == 0:
            glRotated(rotation, 0, 0, 1)
        elif preRot == THETA2:
            glRotated(preRot, 0, 1, 0)
            glRotated(rotation, 0, 0, 1)
        elif preRot == -THETA2:
            glRotated(preRot, 0, 1, 0)
            glRotated(rotation, 1, 0, 0)
        glColor3d(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex2d(0,0)
        glVertex2d(0,l)
        glEnd()
        glFlush()
        glTranslated(0, l, 0)
        if(count == k):
            print("even count k ", count, " ",k)
            glPopMatrix()
        else:
            count += 1
            v1(THETA, 0)
            v1(-THETA, THETA2)
            v1(-THETA, -THETA2)
  
    count += 1
    glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2d(0,0)
    glVertex2d(0,l)
    glEnd()
    glFlush()
    glTranslated(0, l, 0)    
    v1(THETA, 0)
    v1(-THETA, THETA2)
    v1(-THETA, -THETA2)
    l = l*R
    '''
    if(count == k):
        print("even count k ", k)
        glPopMatrix()
        return
    else:
        glPushMatrix()
    '''    
    #v(k, l)

 

def mouse(button, state, x, y):
    global K, L, count
    count = 0
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
           K += 1
           v(K, L)
        if button == GLUT_RIGHT_BUTTON:
           K = 0
    
 
            


if __name__ == "__main__": main()


