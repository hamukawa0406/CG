#!/usr/bin/python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


vertex = [
    [ 0.0, 0.0, 0.0 ],
    [ 1.0, 0.0, 0.0 ],
    [ 1.0, 1.0, 0.0 ],
    [ 0.0, 1.0, 0.0 ],
    [ 0.0, 0.0, 1.0 ],
    [ 1.0, 0.0, 1.0 ],
    [ 1.0, 1.0, 1.0 ],
    [ 0.0, 1.0, 1.0 ]]

face = [
    [ 0, 1, 2, 3 ],
    [ 1, 5, 6, 2 ],
    [ 5, 4, 7, 6 ],
    [ 4, 0, 3, 7 ],
    [ 4, 5, 1, 0 ],
    [ 3, 2, 6, 7 ]]

color = [
    [ 0.3, 0.3, 0.3 ],
    [ 0.4, 0.4, 0.4 ],
    [ 0.5, 0.5, 0.5 ],
    [ 0.6, 0.6, 0.6 ],
    [ 0.7, 0.7, 0.7 ],
    [ 0.8, 0.8, 0.8 ]]

angleX = 0.0
angleY = 0.0


def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)


def drawObjs(name=False):
    global angleX, angleY

    glLoadIdentity()
    gluLookAt(3.0, 4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotated(angleX, 1.0, 0.0, 0.0);
    glRotated(angleY, 0.0, 1.0, 0.0);

    for j in range(0, 6):
        if name:
            glLoadName(j)
        glBegin(GL_QUADS)
        glColor3dv(color[j])
        for i in range(0, 4):
            glVertex(vertex[face[j][i]])
        glEnd()


def draw():
    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawObjs()

    glFlush()
    glutSwapBuffers()


def mouse(button, state, x, y):
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            sel = glSelectBuffer(8)
            glRenderMode(GL_SELECT)
            glInitNames()
            glPushName(0)
            glMatrixMode(GL_PROJECTION)

            glPushMatrix()
            glLoadIdentity()
            vp = glGetIntegerv(GL_VIEWPORT)
            gluPickMatrix(x, vp[3] - y -1, 1, 1, vp)
            gluPerspective(30.0, vp[2]/vp[3], 1.0, 100.0)
            glMatrixMode(GL_MODELVIEW)
            drawObjs(name=True)
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()

            hits = glRenderMode(GL_RENDER)
            for n in hits:
                h = n.names[0]
                color[h] = [1.0, 0, 0]
            glMatrixMode(GL_MODELVIEW)
            glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(320, 320)
glutCreateWindow(b"PyOpenGL 17")
glutDisplayFunc(draw)
glutReshapeFunc(resize)
glutMouseFunc(mouse)

glClearColor(0.0, 0.0, 1.0, 0.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

glutMainLoop()