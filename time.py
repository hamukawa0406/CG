from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import random
import sys

r = 0
lightPos0 = [0.0, -0.0, -4.5, 1]
lightPos1 = [0.0, 2.0, 0.0, 1.0]
night = [0.0, 1.0, 1.0, 1.0]
morning = [1.0, 1.0, 0.8, 1.0]
grass = [0.7, 1.0, 0.5]
star = [1.0, 1.0, 1.0]
building = [0.75, 0.75, 0.75]

SURFACE = []

VERTEX1 = [
    [0.0, 0.0, -0.3],   # A
    [0.3, 0.0, -0.3],   # B
    [0.3, 0.6, -0.3],   # C
    [0.0, 0.6, -0.3],   # D
    [0.0, 0.0, 0.0],   # E
    [0.3, 0.0, 0.0],   # F
    [0.3, 0.6, 0.0],   # G
    [0.0, 0.6, 0.0]    # H
]

VERTEX2 = [
    [0.0, 0.0, -0.3],   # A
    [0.3, 0.0, -0.3],   # B
    [0.3, 0.3, -0.3],   # C
    [0.0, 0.3, -0.3],   # D
    [0.0, 0.0, 0.0],   # E
    [0.3, 0.0, 0.0],   # F
    [0.3, 0.3, 0.0],   # G
    [0.0, 0.3, 0.0]    # H
]

VERTEX3 = [
    [0.0, 0.0, -0.3],   # A
    [0.3, 0.0, -0.3],   # B
    [0.3, 0.9, -0.3],   # C
    [0.0, 0.9, -0.3],   # D
    [0.0, 0.0, 0.0],   # E
    [0.3, 0.0, 0.0],   # F
    [0.3, 0.9, 0.0],   # G
    [0.0, 0.9, 0.0]    # H
]

FACE = [
    [0, 1, 2, 3],
    [1, 5, 6, 2],
    [5, 4, 7, 6],
    [4, 0, 3, 7],
    [4, 5, 1, 0],
    [3, 2, 6, 7]
]

NORMAL = [
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0],
    [0.0, -1.0, 0.0],
    [0.0, 1.0, 0.0]
]

for i in range(len(FACE)):
    s = []
    s.append(FACE[i])
    s.append(NORMAL[i])
    SURFACE.append(s)

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT0)

def display():
    global r, n
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #gluLookAt(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0)
    #glTranslated(0.0, -2.0, 0.0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, star)
    glRotated(r, 0.0, 1.0, 10.0)

    sky(100)
    ground()
    city()
    
    glFlush()
    glutSwapBuffers()
    
    r += 1
    if r >= 360:
        r = 0
    
def ground():
    glTranslated(0.0, 0.0, 0.0)
    glRotated(r, 0.0, 1.0, -10.0)
    glBegin(GL_QUADS)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, grass)
    #glColor3d(0.7, 1.0, 0.5)
    glNormal3d(0.0, 1.0, 0.0)
    glVertex3d(-10.0, 0.0, 0.0)
    glVertex3d(-10.0, -30.0, 10.0)
    glVertex3d(10.0, -30.0, 10.0)
    glVertex3d(10.0, 0.0, 0.0)
    glEnd()

def city():
	glPushMatrix()
	glTranslated(-1.0, 0.0, 0.0)
	glBegin(GL_QUADS)
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, building)
	for surface in SURFACE:
		glNormal3dv(surface[1])
		for f in surface[0]:
			glVertex3dv(VERTEX1[f])
	glEnd()
	glPopMatrix()

	glPushMatrix()
	glTranslated(-0.3, 0.0, -0.5)
	glBegin(GL_QUADS)
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, building)
	for surface in SURFACE:
	    glNormal3dv(surface[1])
	    for f in surface[0]:
	        glVertex3dv(VERTEX2[f])
	glEnd()
	glPopMatrix()

	glPushMatrix()
	glTranslated(0.3, 0.0, -0.2)
	glBegin(GL_QUADS)
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, building)
	for surface in SURFACE:
	    glNormal3dv(surface[1])
	    for f in surface[0]:
	        glVertex3dv(VERTEX3[f])
	glEnd()
	glPopMatrix()

def sky(n):
    r = 0.5
    #glPushMatrix()
    #glTranslated(0.0, -2.0, 0.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    for i in range(n):
        rate = i / n
        x = 10*r*cos(2.0*pi*rate)
        y = 10*r*sin(2.0*pi*rate)
        
        if i > 50:
            sx = random.uniform(0.0, x)
            sy = random.uniform(0.0, y)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, star)
            #glColor(1.0, 1.0, 1.0)
            glVertex3d(sx, sy, 0)
        
    glEnd()

    #glTranslated(0.0, -2.0, 0.0)
    glBegin(GL_POLYGON)
    for i in range(n):
        rate = i / n
        x = 10*r*cos(2.0*pi*rate)
        y = 10*r*sin(2.0*pi*rate)
        
        if i < 10:
        	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, night)
            #glColor(0.0, 0.0, 0.1)
                
        else:
        	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, morning)
            #glColor(0.26, 0.8, 0.94)
        
        glNormal3d(0.0, 1.0, 0.0)
        glVertex3d(x, y, 0)
        
    glEnd()

    #glPopMatrix()
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glLoadIdentity()
    gluPerspective(30.0, w / h, 1.0, 100.0)

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            glutIdleFunc(idle)
            
        else:
            glutIdleFunc(0)

def keyboard(key, x, y):
    if key == b'q' or key == b'Q' or key == b'\033':
        sys.exit()

def idle():
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutCreateWindow(b"GLUT prog1")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
init()
glutMainLoop()
