import pygame,sys,math
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE ou FULLSCREEN
#title
pygame.display.set_caption("polygon collision")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
BLUE=pygame.color.THECOLORS["blue"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480


class Polygon:
    def __init__(self,vertices,color):
        self.vertices=vertices
        self.color=color
        self.move_speed=10
        self.rotation_speed=10
        self.angle=90
        self.get_centroid()
        self.get_velocity()
                
    def get_centroid(self):
       #https://stackoverflow.com/questions/2792443/finding-the-centroid-of-a-polygon
        sum_x=0
        sum_y=0
        len_vertices=len(self.vertices)
        for vertex in self.vertices:
            sum_x+=vertex[0]
            sum_y+=vertex[1]
        center_x=int(sum_x/len_vertices)
        center_y=int(sum_y/len_vertices)
        self.center=[center_x,center_y]
        
    def rotate(self,angle):
        self.angle-=angle
        self.fix_angle()
        self.get_velocity()
        for vertex in self.vertices:
            vertex[0]-=self.center[0]
            vertex[1]-=self.center[1]
            x=vertex[0]
            y=vertex[1]    
            vertex[0]=x*cos(radians(angle))-y*sin(radians(angle))
            vertex[1]=x*sin(radians(angle))+y*cos(radians(angle))
            vertex[0]+=self.center[0]
            vertex[1]+=self.center[1]
        
    def move(self,xvel,yvel):
        for vertex in self.vertices:
            vertex[0]+=xvel
            vertex[1]+=yvel
        self.center[0]+=xvel
        self.center[1]+=yvel              
        
    def get_velocity(self,):
        x=math.cos(math.radians(self.angle))*self.move_speed
        y=math.sin(math.radians(self.angle))*self.move_speed
        self.xvel=x
        self.yvel=y
       
    def fix_angle(self):
        if self.angle>360:
           self.angle-=360
        elif self.angle<0:
           self.angle+=360
    
    def draw(self,surface):
        x=int(self.center[0])
        y=int(self.center[1])
        pygame.draw.polygon(surface,self.color,self.vertices,2)
        pygame.draw.circle(surface,GREEN,(x,y),5)

        
def rect_collision(rect1,rect2):
    #http://www.jeffreythompson.org/collision-detection/rect-rect.php
    collision=0
    if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
    and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
        collision=1
    return collision


def polygon_collision(polygon1,polygon2):
    #polygons collision detection with the separating axis theorem (SAT) 
    #https://hackmd.io/@US4ofdv7Sq2GRdxti381_A/ryFmIZrsl?type=view
    '''
    Return True and the MPV (minimum push vector) if the shapes collide. Otherwise, return False and
    None.

    polygon1 and polygon2 are lists of ordered pairs, the vertices of the polygons in the
    counterclockwise direction.
    '''
    collision=False
    minimum_push_vector=None
    #get the vectors for the edges of the polygons.
    edges = []
    vertices=polygon1.vertices
    len_vertices = len(vertices)
    for i in range(len_vertices):
        v1=vertices[(i + 1)%len_vertices]
        v2=vertices[i]
        edge = [v1[0]-v2[0],v1[1]-v2[1]]
        edges.append(edge)
    vertices=polygon2.vertices    
    len_vertices = len(vertices)
    for i in range(len_vertices):
        v1=vertices[(i + 1)%len_vertices]
        v2=vertices[i]
        edge = [v1[0]-v2[0],v1[1]-v2[1]]
        edges.append(edge)

   #get a 90 degree clockwise rotation of the vectors.
    orthogonals=[]
    for edge in edges:
       orthogonals.append([-edge[1], edge[0]])
       
    push_vectors = []
    for orthogonal in orthogonals:
        #get True and the push vector if orthogonal is a separating axis of polygon1 and polygon2.
        #Otherwise, get False and None.
        is_separating_axis=False
        push_vector=None
        min1, max1 = float('+inf'), float('-inf')
        min2, max2 = float('+inf'), float('-inf')
        for vector in polygon1.vertices:
            projection = vector[0]*orthogonal[0]+vector[1]*orthogonal[1]
            min1 = min(min1, projection)
            max1 = max(max1, projection)
        for vector in polygon2.vertices:
            projection = vector[0]*orthogonal[0]+vector[1]*orthogonal[1]
            min2 = min(min2, projection)
            max2 = max(max2, projection)

        if max1 >= min2 and max2 >= min1:
            #push_vector_length(d)
            d = min(max2 - min1, max1 - min2)
            # push a bit more than needed so the shapes do not overlap in future
            # tests due to float precision
            d_over_orthogonal_squared = d/(orthogonal[0]*orthogonal[0]+orthogonal[1]*orthogonal[1]) + 1e-10
            push_vector = [d_over_orthogonal_squared*orthogonal[0],d_over_orthogonal_squared*orthogonal[1]]
            is_separating_axis = False
        else:
            is_separating_axis =  True
            push_vector = None
                                                           
        if is_separating_axis:
            # they do not collide and there is no push vector
            collision = False
            minimum_push_vector = None
            return collision, minimum_push_vector
        else:
            push_vectors.append(push_vector)
            
    #they do collide and the push_vector with the smallest length is the MPV (minimum push vector)
    minimum_push_vector =  min(push_vectors, key=(lambda v: v[0]*v[0]+v[1]*v[1]))
    collision=True
    #assert mpv pushes polygon1 away from polygon2
    #get the displacement between the geometric center of polygon1 and polygon2
    c1=polygon1.center
    c2=polygon2.center
    displacement = [c2[0]-c1[0],c2[1]-c1[1]]# direction from polygon1 to polygon2
    if displacement[0]*minimum_push_vector[0]+displacement[1]*minimum_push_vector[1] > 0: # if it's the same direction, then invert
        minimum_push_vector = [-minimum_push_vector[0],-minimum_push_vector[1]]
    return collision, minimum_push_vector


def rectangular_polygon_collision(polygon1,polygon2):
    #optimized polygons collision detection with the separating axis theorem (SAT)
    #for rectangular polygon only
    #useful for Oriented Bounding Box (OBB) collision detection
    #https://hackmd.io/@US4ofdv7Sq2GRdxti381_A/ryFmIZrsl?type=view
    collision=False
    #get the vectors for the edges of the polygons.
    edges = []
    vertices=polygon1.vertices
    #we only need two connected edges for rectangles the others two are parallel to them
    len_vertices = 2
    for i in range(len_vertices):
        v1=vertices[i + 1]
        v2=vertices[i]
        edge = [v1[0]-v2[0],v1[1]-v2[1]]
        edges.append(edge)
    vertices=polygon2.vertices    
    len_vertices = 2
    for i in range(len_vertices):
        v1=vertices[i + 1]
        v2=vertices[i]
        edge = [v1[0]-v2[0],v1[1]-v2[1]]
        edges.append(edge)
    
   #get a 90 degree clockwise rotation of the vectors.
    orthogonals=[]
    for edge in edges:
       orthogonals.append([-edge[1], edge[0]])
       
    for orthogonal in orthogonals:
        #get True if orthogonal is a separating axis of polygon1 and polygon2.
        #Otherwise, get False.
        is_separating_axis=False
        min1, max1 = float('+inf'), float('-inf')
        min2, max2 = float('+inf'), float('-inf')
        for vector in polygon1.vertices:
            projection = vector[0]*orthogonal[0]+vector[1]*orthogonal[1]
            min1 = min(min1, projection)
            max1 = max(max1, projection)
        for vector in polygon2.vertices:
            projection = vector[0]*orthogonal[0]+vector[1]*orthogonal[1]
            min2 = min(min2, projection)
            max2 = max(max2, projection)

        if max1 >= min2 and max2 >= min1:
            is_separating_axis = False
        else:
            is_separating_axis =  True
                                                              
        if is_separating_axis:
            #they do not collide 
            return collision
            
    #they do collide 
    collision=True
    
    return collision


polygon1=Polygon([[10,100],[110,100],[110,200],[10,200]],BLUE)
polygon2=Polygon([[400,200],[500,200],[500,300],[400,300]],RED)

pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enough
    CLOCK.tick(30)
    
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
           if event.key == K_UP:
              polygon1.move(polygon1.xvel,-polygon1.yvel)
              collision,mpv=polygon_collision(polygon1,polygon2)
              if collision:
                 polygon1.move(mpv[0],mpv[1])
           elif event.key == K_DOWN:
              polygon1.move(-polygon1.xvel,polygon1.yvel)
              collision,mpv=polygon_collision(polygon1,polygon2)
              if collision:
                 polygon1.move(mpv[0],mpv[1])
           if event.key == K_RIGHT:
              polygon1.rotate(polygon1.rotation_speed)
              if polygon_collision(polygon1,polygon2)[0]:
                 polygon1.rotate(-polygon1.rotation_speed)
           elif event.key == K_LEFT:
              polygon1.rotate(-polygon1.rotation_speed)
              if polygon_collision(polygon1,polygon2)[0]:
                 polygon1.rotate(polygon1.rotation_speed)
                            
           
    screen.fill(BLACK)
    polygon1.draw(screen)
    polygon2.draw(screen)
    pygame.display.flip()
