from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(320, 240)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutCreateWindow(b"GLUT prog1")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLineWidth(2.0)

def resize(w, h):
    glViewport(0, 0, w, h)
#    glLoadIdentity()
#    glOrtho(-0.5, w - 0.5, h - 0.5, -0.5, -1.0, 1.0)
#    glOrtho(-w / 200.0, w / 200.0, -h /200.0, h / 200.0, -1.0, 1.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3d(0.0, 1.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex2d(-0.9, -0.9)
    glVertex2d( 0.0, 0.9)
    glVertex2d( 0.9,  -0.9)
    glVertex2d(-0.9,  0.5)
    glVertex2d(0.9,  0.5)
    glEnd()
    glFlush()

def mouse(button, state, x, y):
    global x0, y0
    if state == GLUT_DOWN :
        if button == GLUT_LEFT_BUTTON:
            zoom(0.8)
        elif button == GLUT_RIGHT_BUTTON:
            zoom(1.2)

def zoom(r):
    glOrtho(-r, r, -r, r, -r, r)

if __name__ == "__main__": main()
