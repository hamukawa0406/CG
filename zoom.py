from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA)
    glutCreateWindow(b"GLUT prog1")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    glutSpecialFunc(directionKey)
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
    winX = (x / WINDOW_WIDTH - 0.5) * 2
    winY = (y / WINDOW_HEIGHT - 0.5) * 2
    imag = 1.2
    print("(x, y) = ", winX, winY)
    if state == GLUT_DOWN :
        if button == GLUT_LEFT_BUTTON:
            zoom(0.8, winX, winY)
        elif button == GLUT_RIGHT_BUTTON:
            zoom(1.2, winX, winY) 

def directionKey(key, x, y):
    if key == GLUT_KEY_UP:
        zoom(1/imag, 0, 0)
    elif key == GLUT_KEY_DOWN:
        zoom(imag, 0, 0)


def zoom(r, x, y):
    #x, y is point of mouse(-1~1). view area transfer by one fifth of each value 
    glOrtho(-r+x/5, r+x/5, -r-y/5, r-y/5, -r, r)
    display()

if __name__ == "__main__": main()
