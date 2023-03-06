import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE ou FULLSCREEN
#title
pygame.display.set_caption("point projection")
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480

font=pygame.font.SysFont('Arial', 30)
message=''
sphere_pos=Vector2(420,340)
sphere_angle=sphere_pos.angle_to((0,0))
sphere_pos=[435,160]
orbit_pos=[320,240]
line_end=[500,240+100]
projection_line=[[0,0],[0,0]]
sphere_radius=50

def circle_collision(circle1_center,circle2_center,circle1_radius,circle2_radius):
    collision=0
    c1=circle1_center
    c2=circle2_center
    lenght=sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    if circle1_radius+circle2_radius>lenght:
       collision=1
    return collision

def point_line_collision(point,line_start,line_end,line_length):
    #http://www.jeffreythompson.org/collision-detection/line-point.php
    collision=0
    length1=sqrt((point[0]-line_start[0])**2+(point[1]-line_start[1])**2)
    length2=sqrt((point[0]-line_end[0])**2+(point[1]-line_end[1])**2)
    if int(length1+length2)==int(line_length):
       collision=1
    return collision       

def dot_product(vector1,vector2):
    #http://www.sunshine2k.de/articles/Derivation_DotProduct_R2.pdf
    #vector1.x*vector2.x*+vector1.y*vector2.y==vector1.length*vector2.length*cos(radians(alpha))
    #where 'alpha' is angle between vector1 and vector2
    return vector1[0]*vector2[0]+vector1[1]*vector2[1]

def Project_point_to_line(vector1,vector2):
    #https://stackoverflow.com/questions/49061521/projection-of-a-point-to-a-line-segment-python-shapely
    #project vector1 onto vector2 and get the projected point
    #length_vector1=math.sqrt(vector1[0]**2+vector1[1]**2)
    length_vector2=sqrt(vector2[0]**2+vector2[1]**2)
    dot_product_result=dot_product(vector1,vector2)
    #cos_alpha=dot_product_result/(length_vector1*length_vector2)
    #projected_vector_length=cos_alpha*length_vector1
    projected_vector_length=dot_product_result/length_vector2
    #projected_vector=projected_vector_length*(vector2/length_vector2)
    projected_vector=[0,0]
    projected_vector[0]=projected_vector_length*(vector2[0]/length_vector2)
    projected_vector[1]=projected_vector_length*(vector2[1]/length_vector2)
    #projected_point=vector2_start+projected_vector
    return projected_vector

def line_circle_collision(circle_center,circle_radius,line_start,line_end,half_line_thickness):
    #http://www.jeffreythompson.org/collision-detection/line-circle.php
    collision=0
    radius_sum=(circle_radius+half_line_thickness)**2
    #test to see if the circle collide with either ends of the line segment
    if (line_start[0]-circle_center[0])**2+(line_start[1]-circle_center[1])**2<radius_sum \
    or (line_end[0]-circle_center[0])**2+(line_end[1]-circle_center[1])**2<radius_sum:
       return 1
    #get the closest point to the line segment
    vector1=[circle_center[0]-line_start[0],circle_center[1]-line_start[1]]
    vector2=[line_end[0]-line_start[0],line_end[1]-line_start[1]]
    vector2_length=sqrt(vector2[0]**2+vector2[1]**2)
    dot=(vector1[0]*vector2[0]+vector1[1]*vector2[1])/vector2_length**2
    closest_point=[line_start[0]+dot*vector2[0],line_start[1]+dot*vector2[1]]
    #test to see if the closest point is on the line segment
    if int(sqrt((closest_point[0]-line_start[0])**2+(closest_point[1]-line_start[1])**2)+ \
    sqrt((closest_point[0]-line_end[0])**2+(closest_point[1]-line_end[1])**2))==int(vector2_length):
        #test collision with that point
        if(circle_center[0]-closest_point[0])**2+(circle_center[1]-closest_point[1])**2<radius_sum:
           collision=1         
    return collision

def dda(x1,y1,x2,y2): #Digital Differential Analyzer Algorithm
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
       steps = abs(dx)
    else:
       steps = abs(dy)  
    Xincrement = dx / steps
    Yincrement = dy / steps
    x=x1
    y=y1
    for i in range(steps):
        pygame.draw.rect(screen,(0,255,0), [x, y,5,5], 0)
        x = x + Xincrement
        y = y + Yincrement
    pygame.display.flip()

def orbital_rotation(angle):
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    sphere_pos.rotate_ip(angle)
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]
    
def orbital_rotation2(angle):
    """x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    x=sphere_pos[0]
    y=sphere_pos[1]    
    sphere_pos[0]=x*cos(radians(angle))-y*sin(radians(angle))
    sphere_pos[1]=x*sin(radians(angle))+y*cos(radians(angle))
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

def orbital_rotation3(angle):
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]    
    angle=degrees(atan2(sphere_pos[1],sphere_pos[0]))+angle
    magnitude=sqrt(sphere_pos[0]*sphere_pos[0]+sphere_pos[1]*sphere_pos[1])
    sphere_pos[0]=cos(radians(angle))*magnitude
    sphere_pos[1]=sin(radians(angle))*magnitude
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

    
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
           if event.key == K_RIGHT:
              orbital_rotation2(10)
           elif event.key == K_LEFT:
              orbital_rotation2(-10)

           vector1=[sphere_pos[0]-orbit_pos[0],sphere_pos[1]-orbit_pos[1]]
           vector2=[line_end[0]-orbit_pos[0],line_end[1]-orbit_pos[1]]
           projected_vector=Project_point_to_line(vector1,vector2)
           projected_point=[orbit_pos[0]+projected_vector[0],orbit_pos[1]+projected_vector[1]]
           projection_line=[sphere_pos,projected_point]
           vector2_length=sqrt(vector2[0]**2+vector2[1]**2)
           if point_line_collision(projected_point,orbit_pos,line_end,vector2_length) \
           or circle_collision(sphere_pos,line_end,sphere_radius,5):
              if circle_collision(sphere_pos,projected_point,sphere_radius,5):
                 message='collision'
              else:
                 message=''

                
    screen.fill(BLACK)    
    pygame.draw.circle(screen,(0,255,0),(int(sphere_pos[0]),int(sphere_pos[1])),10)
    pygame.draw.circle(screen,(0,0,255),(int(sphere_pos[0]),int(sphere_pos[1])),sphere_radius,5)
    pygame.draw.circle(screen,(0,0,255),orbit_pos,10)
    pygame.draw.line(screen,WHITE,orbit_pos,line_end,5)
    pygame.draw.line(screen,(255,0,0),projection_line[0],projection_line[1],5)
    text=font.render((message), True, (250,250,250))
    screen.blit(text,(20,20))
    pygame.display.flip()
