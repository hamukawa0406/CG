from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

r = 0
red = [0.8, 0.2, 0.2, 1.0]
green = [0.0, 1.0, 0.0, 1.0]



class Cube:
    def __init__(self):
        self.FACE = [
            [ 0, 1, 2], #A-B-C
            [ 0, 2, 3], #A-C-D
            [ 0, 3, 1], #A-D-B
            [ 1, 2, 3], #B-C-D
        ]
        self.COLOR = [
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, 1.0, 0.0 ],
            [ 0.0, 0.0, 1.0 ],
            [ 1.0, 1.0, 0.0 ],
        ]

        self.VERTEX = [
            [0.0, 3.0, 0.0],   # A
            [2*sqrt(2), -1.0, 0.0],   # B
            [-1*sqrt(2), -1.0, -1*sqrt(6)],   # C
            [-1*sqrt(2), -1.0, sqrt(6)],   # D
        ]

        self.EDGE = [
            [0, 1], # a (A-B)
            [1, 2], # i (B-C)
            [2, 3], # u (C-D)
            [3, 0], # e (D-A)
            [2, 0], # o (C-A)
            [1, 3], # ka (B-D)
        ]

            

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"kadai2")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    init()
    glutMainLoop()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(2.0)

def resize(w, h):
    glViewport(0, 0, w, h)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w / h, 1.0, 100.0)

    # モデルビュー変換行列の設定 */
    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

def display():
    global r
    surface = Cube()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3.0, 4.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glRotated(float(r), 0.0, 1.0, 0.0)

    glBegin(GL_TRIANGLES)
    for j in range(4):
        glColor3dv(surface.COLOR[j])
        for i in range(3):
            glVertex3dv(surface.VERTEX[surface.FACE[j][i]])
    glEnd()

    glutSwapBuffers()

    glFlush()

    r += 1                      # 一周回ったら回転角を 0 に戻す */
if r >= 360:
         r = 0

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            glutIdleFunc(idle)
        else :
            glutIdleFunc(0)
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            glutPostRedisplay()


if __name__ == "__main__": main()


