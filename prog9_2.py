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
            [ 0, 1, 2, 3 ],
            [ 1, 5, 6, 2 ],
            [ 5, 4, 7, 6 ],
            [ 4, 0, 3, 7 ],
            [ 4, 5, 1, 0 ],
            [ 3, 2, 6, 7 ]
        ]
        self.COLOR = [
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, 1.0, 0.0 ],
            [ 0.0, 0.0, 1.0 ],
            [ 1.0, 1.0, 0.0 ],
            [ 1.0, 0.0, 1.0 ],
            [ 0.0, 1.0, 1.0 ] 
        ]

        self.VERTEX = [
            [0.0, 0.0, 0.0],   # A
            [1.0, 0.0, 0.0],   # B
            [1.0, 1.0, 0.0],   # C
            [0.0, 1.0, 0.0],   # D
            [0.0, 0.0, 1.0],   # E
            [1.0, 0.0, 1.0],   # F
            [1.0, 1.0, 1.0],   # G
            [0.0, 1.0, 1.0]    # H
        ]

        self.EDGE = [
            [0, 1], # a (A-B)
            [1, 2], # i (B-C)
            [2, 3], # u (C-D)
            [3, 0], # e (D-A)
            [4, 5], # o (E-F)
            [5, 6], # ka (F-G)
            [6, 7], # ki (G-H)
            [7, 4], # ku (H-E)
            [0, 4], # ke (A-E)
            [1, 5], # ko (B-F)
            [2, 6], # sa (C-G)
            [3, 7]  # shi (D-H)
        ]
        
        self.NORMAL = [
            [ 0.0, 0.0,-1.0 ],
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 1.0 ],
            [-1.0, 0.0, 0.0 ],
            [ 0.0,-1.0, 0.0 ],
            [ 0.0, 1.0, 0.0 ]
        ]

        self.light0pos = [0.0, 3.0, 5.0, 1.0]
        self.light1pos = [5.0, 3.0, 0.0, 1.0]


            

def main():
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"GLUT prog1")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    init()
    glutMainLoop()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(2.0)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, green)
    glLightfv(GL_LIGHT1, GL_SPECULAR, green)

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
    gluLookAt(3.0, 4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glLightfv(GL_LIGHT0, GL_POSITION, surface.light0pos)
    glLightfv(GL_LIGHT1, GL_POSITION, surface.light1pos)

    glRotated(float(r), 0.0, 1.0, 0.0)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, red)

    glColor3d(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    for j in range(6):
        glNormal3dv(surface.NORMAL[j])
        for i in range(4):
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

def keyboard(key, x, y):
    if key == 'q' or key == 'Q'or key == '\033':  # '\033' は ESC の ASCII コード */
        exit()

if __name__ == "__main__": main()


