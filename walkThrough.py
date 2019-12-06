from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

r = 0.0
ex = 0.0
ez = 0.0
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

    glLoadIdentity()
    gluPerspective(30.0, float(w)/h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

def display():
    global r, ex, ez, lightpos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    glRotated(float(r), 0.0, 1.0, 0.0)
    glTranslated(ex, 0.0, ez)

    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)

    scene()

    glutSwapBuffers()

    r += 1

    if r >= 360:
        r = 0


def scene():
    global red, green, blue, yellow, ground

    glPushMatrix() 
    glTranslated(0.0, 0.0, -3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, red) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(0.0, 0.0, 3.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, green) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(-3.0, 0.0, 0.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, blue) 
    glutSolidCube(1.0) 
    glPopMatrix() 

    glPushMatrix() 
    glTranslated(3.0, 0.0, 0.0) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, yellow) 
    glutSolidCube(1.0) 
    glPopMatrix() 

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




def mouse(button, state, x, y):
    global K, L
    print("(x, y)= ", x, " ", y)
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            glutIdleFunc(idle)
        
        elif state == GLUT_UP:
            glutIdleFunc(0)

def SpaceDown(key, x, y):
    if(key == b' '):
        glutIdleFunc(idle)

def SpaceUp(key, x, y):
    if(key == b' '):
        glutIdleFunc(0)



if __name__ == "__main__": main()
