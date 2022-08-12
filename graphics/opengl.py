from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

def Square(midx):
    glBegin(GL_LINE_LOOP)
    glVertex3f(1, 1,0)
    glVertex3f(2, 1,0)
    glVertex3f(1.5, 1.5,midx)
    glVertex3f(1, 1,0)
    glVertex3f(1, 2, 0)
    glVertex3f(1.5, 1.5, midx)
    glVertex3f(2, 2, 0)
    glVertex3f(1, 2, 0)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(2, 1,0)
    glVertex3f(2, 2,0)
    glEnd()


def main():
    pygame.init()
    size = (800,600)
    video_flags = pygame.OPENGL | pygame.DOUBLEBUF    
    screen = pygame.display.set_mode(size, video_flags)

    gluPerspective(65, (size[0]/size[1]), 0.2, 30.0)

    glTranslatef(-1.8,-0.5, -5)
    glRotatef(90, 1, 0, 0)
    ii=0
    kk=0.05
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(1, 0.1, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Square(ii)
        ii = ii+kk
        if ii>1.5 or ii<(-1.5):
            kk=-kk
        pygame.display.flip()
        pygame.time.wait(10)

 
if __name__ == "__main__":
    main()