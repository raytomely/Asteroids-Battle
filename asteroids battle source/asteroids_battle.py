import pygame,sys,math,random,os,pickle
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
BLUE=pygame.color.THECOLORS["blue"]
LIGHTBLUE=pygame.color.THECOLORS["lightblue"]
GREEN=pygame.color.THECOLORS["green"]
GREY=pygame.color.THECOLORS["grey"]
YELLOW=pygame.color.THECOLORS["yellow"]
CLOCK=pygame.time.Clock()
SCREEN_WIDTH=640
SCREEN_HEIGHT=480


def get_directions():
    directions=[]
    for angle in range(0,360,1):
        move_speed=random.randint(2,5)
        x=math.cos(math.radians(angle))*move_speed
        y=math.sin(math.radians(angle))*move_speed
        directions.append((x,-y))
    return directions


def get_sounds():
  path="asteroids_battle_data/"
  sounds={}
  for file in os.listdir("asteroids_battle_data"):
      if file[-3:]=="wav" or file[-3:]=="ogg":
         sounds[file]=pygame.mixer.Sound(path+file)
  return sounds

    
def make_asteroids(number):
    for i in range(number):
        size=random.randint(60,100)
        x=random.randint(0,540)
        y=-100
        asteroid=Asteroid([x,y],size)
        if  int(asteroid.yvel)==0:
            x=asteroid.xvel
            y=asteroid.yvel
            asteroid.xvel=y
            asteroid.yvel=x


def make_background():
    background=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)).convert()
    background.fill(WHITE)
    for i in range(100):
        radius=random.randint(2,6)
        x=random.randint(0,SCREEN_WIDTH)
        y=random.randint(0,SCREEN_HEIGHT)
        pygame.draw.circle(background,GREY,(x,y),radius)
    return background


def start_stage():
    pygame.mixer.stop()
    sounds["fanfare1.wav"].play()
    screen.fill(WHITE)
    font=pygame.font.SysFont('Arial',29)
    text=font.render(("battle "+str(battle)),True,BLACK)
    screen.blit(text,(255,200))
    pygame.display.flip()
    t1=pygame.time.get_ticks()
    while True:
        CLOCK.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        t2=pygame.time.get_ticks()
        if(t2-t1)/1000>2:
           break


def title_screen():
    path="asteroids_battle_data/Mortal Kombat.mid"
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    font=pygame.font.SysFont('Arial',55)
    font2=pygame.font.SysFont('Arial',30)
    font3=pygame.font.SysFont('Arial',28)
    blit_text=True
    timer=0
    done=False
    while not done:
        CLOCK.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_F4:
                  load_game()
                  pygame.mixer.music.stop()
                  done=True
               else:
                  pygame.mixer.music.stop()
                  done=True
            if event.type == JOYBUTTONDOWN:
               pygame.mixer.music.stop()
               done=True                
        screen.fill(BLACK)
        text=font.render(("Asteroids   Battle"),True,RED)
        screen.blit(text,(100,150))
        timer+=1
        if timer==15:
           timer=0
           if blit_text:
              blit_text=False
           elif not blit_text:
              blit_text=True           
        if blit_text:
           text=font2.render(("press any key"),True,YELLOW)
           screen.blit(text,(210,260))
        text=font3.render(("best score "+str(best_score)),True,WHITE)
        screen.blit(text,(230,350))
        pygame.display.flip()

        
def init_game(start_game=False,next_battle=False,lose_life=False):
    global battle, num_asteroids, score, best_score, player, background
    if start_game:
       player=Player([280,220])
       if score>best_score:
          best_score=score
       score=0
       battle=1
       num_asteroids=3
       Asteroid.group.clear()
       make_asteroids(num_asteroids)
       background=make_background()
       title_screen()
       start_stage()
    if next_battle:
       lives=player.lives
       missiles=player.missiles
       bombs=player.bombs
       player.__init__([280,220])
       player.lives=lives
       player.missiles=missiles
       player.bombs=bombs
       player.missiles+=5
       player.bombs+=1
       battle+=1
       num_asteroids+=2
       make_asteroids(num_asteroids)
       background=make_background()
       start_stage()
    if lose_life:
       lives=player.lives
       player.__init__([280,220])
       player.lives=lives
       Asteroid.group.clear()
       make_asteroids(num_asteroids)
       start_stage()

       
def pause_game():
    font=pygame.font.SysFont('Arial',29)
    text=font.render(("Pause"),True,BLACK)
    screen.blit(text,(260,230))
    pygame.display.flip()
    done=False
    while not done:
        CLOCK.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_p: 
                  done=True
            if event.type == JOYBUTTONDOWN:
               if event.button == 9:
                  done=True


def save_image(image):
    return pygame.image.tostring(image,'RGBA')


def load_image(saved_image,size,alpha=False):
    image=pygame.image.fromstring(saved_image,size,'RGBA')
    if alpha:
       image.convert_alpha()
    else:
        image.convert()
    return image


def save_game():  
    with open('asteroids.save', 'wb') as file:
         file_saver=pickle.Pickler(file)
         data={'player':player,
               'asteroids':asteroids,
               'num_asteroids':num_asteroids,
               'battle':battle,
               'score':score,
               'best_score':best_score,
               'background':save_image(background)}
         file_saver.dump(data)
    font=pygame.font.SysFont('Arial',28)
    text=font.render(('game saved'),True,BLUE)
    screen.blit(text,(230,230))
    pygame.display.flip()
    time1=pygame.time.get_ticks()
    time2=pygame.time.get_ticks()
    while time2-time1<500:
          time2=pygame.time.get_ticks()


def load_game():
    global player,asteroids,num_asteroids,battle,score,best_score,background
    try:
        with open('asteroids.save', 'rb') as file:
             file_loader=pickle.Unpickler(file)
             data=file_loader.load()
             player=data['player']
             player.get_images()
             player.rot_image=pygame.transform.rotate(player.image,player.angle)
             for shot in player.shots:
                 shot.image=pygame.Surface((10,10)).convert()
                 shot.image.set_colorkey(shot.image.get_at((0,0)))
                 pygame.draw.circle(shot.image,BLUE,(5,5),5)
             for particle in player.explosion.particles:
                 size=particle.size[0]
                 particle.image=pygame.Surface(particle.size).convert()
                 particle.image.set_colorkey(particle.image.get_at((0,0)))
                 pygame.draw.circle(particle.image,RED,(int(size/2),int(size/2)),int(size/2))
             player.sheild.get_images()
             player.missile.get_images()
             Asteroid.group=asteroids=data['asteroids']
             for asteroid in asteroids:
                 asteroid.get_images()
                 for particle in asteroid.explosion.particles:
                     size=particle.size[0]
                     particle.image=pygame.Surface(particle.size).convert()
                     particle.image.set_colorkey(particle.image.get_at((0,0)))
                     pygame.draw.circle(particle.image,RED,(int(size/2),int(size/2)),int(size/2))
             num_asteroids=data['num_asteroids']
             battle=data['battle']
             score=data['score']
             best_score=data['best_score']
             background=load_image(data['background'],(640,480),alpha=False)
             message="game loaded"
    except FileNotFoundError:
           message="unable to load"
    font=pygame.font.SysFont('Arial',28)
    text=font.render((message),True,BLUE)
    screen.blit(text,(230,230))
    pygame.display.flip()
    time1=pygame.time.get_ticks()
    time2=pygame.time.get_ticks()
    while time2-time1<500:
          time2=pygame.time.get_ticks()

                              
def collide(point,rect):
    collided=0
    if point[0]>=rect[0] and point[0]<rect[0]+rect[2] \
    and point[1]>=rect[1] and point[1]<rect[1]+rect[3]:
        collided=1
    return collided


def rect_collision(rect1,rect2):
    collision=0
    point1=(rect1[0],rect1[1])
    point2=(rect1[0]+rect1[2],rect1[1])
    point3=(rect1[0],rect1[1]+rect1[3])
    point4=(rect1[0]+rect1[2],rect1[1]+rect1[3])
    if collide(point1,rect2) or collide(point2,rect2) \
    or collide(point3,rect2) or collide(point4,rect2):
       collision=1
    return collision


def rect_collision2(rect1,rect2):
    #http://www.jeffreythompson.org/collision-detection/rect-rect.php
    collision=0
    if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
    and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
        collision=1
    return collision


def circle_collision(circle1,circle2):
    collision=0
    c1=circle1.center
    c2=circle2.center
    lenght=math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    if circle1.radius+circle2.radius>lenght:
       collision=1
    return collision


def circle_collision2(circle1,circle2):
    #optimized circle collision detection
    #that doesn't rely on the too costly square root function        
    collision=0
    dx=circle1.center[0]-circle2.center[0]
    dy=circle1.center[1]-circle2.center[1]
    if (circle1.radius+circle2.radius)**2>dx**2+dy**2:
       collision=1
    return collision


def circle_collision3(circle1,circle2):
    #optimized circle collision detection
    #that doesn't rely on the too costly square root function    
    collision=0
    xdist=circle1.center[0]-circle2.center[0]
    ydist=circle1.center[1]-circle2.center[1]
    radius_sum=circle1.radius+circle2.radius
    if xdist<0:
       xdist*=-1
    if ydist<0:
       ydist*=-1       
    if radius_sum>xdist and radius_sum>ydist:
       collision=1
    return collision


def orbital_rotation(sphere_pos,orbit_pos,angle):
    """x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    x=sphere_pos[0]
    y=sphere_pos[1]    
    sphere_pos[0]=x*math.cos(math.radians(angle))-y*math.sin(math.radians(angle))
    sphere_pos[1]=x*math.sin(math.radians(angle))+y*math.cos(math.radians(angle))
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

    
def dot_product(vector1,vector2):
    #http://www.sunshine2k.de/articles/Derivation_DotProduct_R2.pdf
    #vector1.x*vector2.x*+vector1.y*vector2.y==vector1.length*vector2.length*cos(radians(alpha))
    #where 'alpha' is angle between vector1 and vector2
    return vector1[0]*vector2[0]+vector1[1]*vector2[1]


def Project_point_to_line(vector1,vector2):
    #https://stackoverflow.com/questions/49061521/projection-of-a-point-to-a-line-segment-python-shapely
    #project vector1 onto vector2 and get the projected point
    #length_vector1=math.sqrt(vector1[0]**2+vector1[1]**2)
    length_vector2=math.sqrt(vector2[0]**2+vector2[1]**2)
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
    vector2_length=math.sqrt(vector2[0]**2+vector2[1]**2)
    dot=(vector1[0]*vector2[0]+vector1[1]*vector2[1])/vector2_length**2
    closest_point=[line_start[0]+dot*vector2[0],line_start[1]+dot*vector2[1]]
    #test to see if the closest point is on the line segment
    if int(math.sqrt((closest_point[0]-line_start[0])**2+(closest_point[1]-line_start[1])**2)+ \
    math.sqrt((closest_point[0]-line_end[0])**2+(closest_point[1]-line_end[1])**2))==int(vector2_length):
        #test collision with that point
        if(circle_center[0]-closest_point[0])**2+(circle_center[1]-closest_point[1])**2<radius_sum:
           collision=1       
    return collision


class Player:
   
   def __init__(self,pos):
       self.pos=pos
       self.get_images()
       self.size=50
       self.rot_pos=[pos[0],pos[1]]
       self.width=self.image.get_width()
       self.height=self.image.get_height()
       self.half_width=int(self.width/2)
       self.half_height=int(self.height/2)
       self.move_speed=10
       self.angle=90
       self.radius=15
       self.vitality=50
       self.lives=3
       self.get_velocity()
       self.center=[self.pos[0]+self.half_width,self.pos[1]+self.half_height]
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       self.rot_rect=self.rot_image.get_rect(topleft=pos)
       self.shots=[Shot(),Shot(),Shot()]
       self.shot_index=0
       self.shot=self.shots[self.shot_index]
       self.shot_interval=0
       self.shoted=False
       self.shooting=False
       self.charge_shot=ChargeShot()
       self.up=self.down=self.right=self.left=False
       self.hited=False
       self.choc_velocity=[0,0]
       self.choc_angle=20
       self.explosion=Explosion(self.center,self)
       self.dead=False
       self.wave=False
       self.wave_radius=10       
       self.hited_count=0
       self.sheild=Sheild(self.center)
       self.lazer_beam=Lazer_Beam()
       self.missile=Missile()
       self.bomb=Bomb()
       self.missiles=15
       self.bombs=1
    
   def rotate_center(self,angle):
       self.angle+=angle
       self.fix_angle()
       self.get_velocity()
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       self.rot_rect=self.rot_image.get_rect(center=self.rot_rect.center)
       self.rot_pos=[self.rot_rect.x,self.rot_rect.y]

   def rotate_center2(self,angle):
       self.angle+=angle
       self.fix_angle()
       self.get_velocity()
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       dx=self.half_width-int(self.rot_image.get_width()/2)
       dy=self.half_height-int(self.rot_image.get_height()/2)
       self.rot_pos[0]=self.pos[0]+dx
       self.rot_pos[1]=self.pos[1]+dy
              
   def move(self,xvel,yvel):
       self.pos[0]+=xvel
       self.pos[1]+=yvel
       self.center[0]+=xvel
       self.center[1]+=yvel              
       self.rot_pos[0]+=xvel
       self.rot_pos[1]+=yvel
       self.rot_rect.center=self.center

   def get_velocity(self):
       x=math.cos(math.radians(self.angle))*self.move_speed
       y=math.sin(math.radians(self.angle))*self.move_speed
       self.xvel=x
       self.yvel=y
                  
   def fix_angle(self):
       if self.angle>360:
          self.angle-=360
       elif self.angle<0:
          self.angle+=360
   
   def fire(self):
       if not self.shot.active and not self.hited and not self.shoted:
          sounds["shot1.wav"].play()
          self.shot=self.shots[self.shot_index]
          self.shot.active=True
          self.shoted=True
          self.shot.rect.centerx=self.pos[0]+self.half_width
          self.shot.rect.centery=self.pos[1]+self.half_height
          self.shot.direction[0]=self.xvel*2
          self.shot.direction[1]=-self.yvel*2
          self.shot_index+=1
          if self.shot_index>=len(self.shots):
             self.shot_index=0
          self.shot=self.shots[self.shot_index]
 
   def fire_missile(self):
       if not self.missile.active and not self.hited:
          if self.missiles>0:
             self.missile.activate(self.center,self.angle)
             self.missiles-=1
             sounds["dive.wav"].play()
             
   def launch_bomb(self):
       if not self.bomb.active and not self.hited:
          if self.bombs>0:
             self.bomb.active=True
             self.bomb.center=[self.center[0],self.center[1]]
             self.bombs-=1
             sounds["wave.wav"].play(2)
             
   def init_charge_shot(self):
       if not self.charge_shot.active and not self.hited:
          self.charge_shot.active=True
          self.charge_shot.charging=True
          normal_xvel=self.xvel/self.move_speed
          normal_yvel=self.yvel/self.move_speed
          radius=self.charge_shot.radius
          self.charge_shot.center[0]=self.center[0]+(normal_xvel*(self.half_width+radius))
          self.charge_shot.center[1]=self.center[1]+(-normal_yvel*(self.half_width+radius))
          self.charge_shot.direction[0]=self.xvel
          self.charge_shot.direction[1]=-self.yvel
          self.charge_shot.normalized_direction[0]=normal_xvel
          self.charge_shot.normalized_direction[1]=-normal_yvel

   def shoot_lazer_beam(self):
       if not self.lazer_beam.active and not self.hited and self.charge_shot.energy>25:
          self.charge_shot.energy-=25 
          self.lazer_beam.active=True
          self.lazer_beam.length=2
          self.lazer_beam.time=0          
          normal_xvel=self.xvel/self.move_speed
          normal_yvel=self.yvel/self.move_speed
          radius=self.lazer_beam.radius*2
          self.lazer_beam.start[0]=self.center[0]+(normal_xvel*(self.half_width+radius))
          self.lazer_beam.start[1]=self.center[1]+-(normal_yvel*(self.half_width+radius))
          self.lazer_beam.end[0]=self.lazer_beam.start[0]+(normal_xvel*self.lazer_beam.length)
          self.lazer_beam.end[1]=self.lazer_beam.start[1]-(normal_yvel*self.lazer_beam.length)     
          self.lazer_beam.vilocity[0]=normal_xvel*self.lazer_beam.move_speed
          self.lazer_beam.vilocity[1]=-normal_yvel*self.lazer_beam.move_speed

    
   def update(self,asteroids):
       if not self.dead:
          if not self.hited:
             if self.up:
                self.move(self.xvel,-self.yvel)
                self.offscreen_update()
             elif self.down:
                self.move(-self.xvel,self.yvel)
                self.offscreen_update()
             if self.right:
                self.rotate_center2(-10)
             elif self.left:
                self.rotate_center2(10)
             if self.shooting:
                self.fire()
             self.update_charge_shot()
             self.update_lazer_beam()
          else:
             if self.vitality>0:
                self.take_hit()
             else:
                self.wave=True 
                self.wave_radius+=20
                if self.wave_radius>=self.radius*15:
                   self.wave=False
                   self.dead=True
                   self.explosion.active=True
                   self.explosion.init_particles()
                   sounds["explosion2.wav"].play()
       for asteroid in asteroids:
           for shot in self.shots:
               shot.asteroid_collision(asteroid)
           self.asteroid_collision(asteroid)      
           self.sheild.asteroid_collision(asteroid)
           self.missile.asteroid_collision(asteroid)
           self.lazer_beam.asteroid_collision(asteroid)
           self.bomb.asteroid_collision(asteroid)
           self.charge_shot.asteroid_collision(asteroid)
       for shot in self.shots:
           shot.update()
       if self.shoted:
          self.shot_interval+=1
          if self.shot_interval==10:
             self.shot_interval=0
             self.shoted=False           
       self.sheild.update()
       self.missile.update()
       self.lazer_beam.update()
       self.bomb.update()
       self.charge_shot.update()
       self.explosion.update()
       
   def kill(self):
       self.lives-=1
       if self.lives<0:
          self.lives=0
          global game_over
          game_over=True
          sounds["lose1.wav"].play()
       else:
          init_game(lose_life=True)
          
   def offscreen_update(self):       
       if self.pos[0]<-self.width:
          x=self.width+SCREEN_WIDTH
          self.move(x,0)
          self.charge_shot.charging=False
       elif self.pos[0]>SCREEN_WIDTH:
          x=-self.width-SCREEN_WIDTH
          self.move(x,0)
          self.charge_shot.charging=False
       if self.pos[1]<-self.height:
          y=self.height+SCREEN_HEIGHT
          self.move(0,y)
          self.charge_shot.charging=False
       elif self.pos[1]>SCREEN_HEIGHT:
          y=-self.height-SCREEN_HEIGHT
          self.move(0,y)
          self.charge_shot.charging=False
          
   def update_charge_shot(self):
       if self.charge_shot.charging:
          if self.up:
             self.charge_shot.center[0]+=self.xvel
             self.charge_shot.center[1]+=-self.yvel
          elif self.down:
             self.charge_shot.center[0]+=-self.xvel
             self.charge_shot.center[1]+=self.yvel
          if self.right or self.left:
             self.charge_shot.active=False
             self.init_charge_shot()

   def update_lazer_beam(self):
       if self.lazer_beam.active:           
          if self.right:
             orbital_rotation(self.lazer_beam.start,self.center,10)
             orbital_rotation(self.lazer_beam.end,self.center,10)
             normal_xvel=self.xvel/self.move_speed
             normal_yvel=self.yvel/self.move_speed
             self.lazer_beam.vilocity[0]=normal_xvel*self.lazer_beam.move_speed
             self.lazer_beam.vilocity[1]=-normal_yvel*self.lazer_beam.move_speed
          elif self.left:
             orbital_rotation(self.lazer_beam.start,self.center,-10)
             orbital_rotation(self.lazer_beam.end,self.center,-10)
             normal_xvel=self.xvel/self.move_speed
             normal_yvel=self.yvel/self.move_speed
             self.lazer_beam.vilocity[0]=normal_xvel*self.lazer_beam.move_speed
             self.lazer_beam.vilocity[1]=-normal_yvel*self.lazer_beam.move_speed           
          if self.up:
             self.lazer_beam.start[0]+=self.xvel
             self.lazer_beam.start[1]+=-self.yvel
             self.lazer_beam.end[0]+=self.xvel
             self.lazer_beam.end[1]+=-self.yvel             
          elif self.down:
             self.lazer_beam.start[0]+=-self.xvel
             self.lazer_beam.start[1]+=self.yvel
             self.lazer_beam.end[0]+=-self.xvel
             self.lazer_beam.end[1]+=self.yvel         

   def asteroid_collision(self,asteroid):
       if not asteroid.dead and not self.hited:
          rect=[self.pos[0],self.pos[1],self.width,self.height]
          if rect_collision(rect,asteroid.rect):
             c1=self.center
             c2=asteroid.rect.center
             dx=c1[0]-c2[0]
             dy=c1[1]-c2[1]
             lenght=math.sqrt(dx**2+dy**2)
             if self.radius+asteroid.radius>lenght:
                sounds["choc3.wav"].play()
                angle=math.degrees(math.atan2(dy,dx))
                xvel=math.cos(math.radians(angle))*(asteroid.size/10)
                yvel=math.sin(math.radians(angle))*(asteroid.size/10)
                self.choc_velocity=[xvel,yvel]
                self.hited=True
                self.vitality-=asteroid.power
                self.image=self.hited_image
                self.rotate_center2(0)
                self.sheild.active=False
                if self.charge_shot.charging:
                   sounds["charging.wav"].stop() 
                   self.charge_shot.charging=False
                   self.charge_shot.active=False
                   self.charge_shot.radius=5
                   self.charge_shot.power=5
                if self.lazer_beam.active:
                   sounds["beam.wav"].stop()
                   self.lazer_beam.active=False
                   self.lazer_beam.length=2
                   self.lazer_beam.time=0
                if c2[0]>c1[0]:
                   self.choc_angle=20
                else:
                   self.choc_angle=-20
      
   def take_hit(self):
       self.move(self.choc_velocity[0],self.choc_velocity[1])
       self.rotate_center2(self.choc_angle)
       self.offscreen_update()
       self.hited_count+=1
       if self.hited_count==7:
          self.image=self.normal_image
       if not int(self.choc_velocity[0])==0:
          if self.choc_velocity[0]>0:
             self.choc_velocity[0]-=0.1
          else:
             self.choc_velocity[0]+=0.1
       if not int(self.choc_velocity[1])==0:
          if self.choc_velocity[1]>0:
             self.choc_velocity[1]-=0.1
          else:
             self.choc_velocity[1]+=0.1
       if int(self.choc_velocity[0])==0 \
       and int(self.choc_velocity[1])==0:
           self.hited=False
           self.hited_count=0
           
   def get_images(self):
       self.normal_image=pygame.Surface((50,50)).convert()
       self.normal_image.set_colorkey(self.normal_image.get_at((0,0)))
       self.hited_image=self.normal_image.copy()
       points=[[0,0],[50,25],[0,50]]
       pygame.draw.polygon(self.normal_image,RED,points,0)
       pygame.draw.circle(self.normal_image,YELLOW,(30,25),8)
       pygame.draw.circle(self.normal_image,WHITE,(30,27),3)
       pygame.draw.polygon(self.hited_image,YELLOW,points,0)
       self.image=self.normal_image
         
   def draw(self,surface):
       for shot in self.shots:
           shot.draw(surface)
       self.missile.draw(surface)
       self.lazer_beam.draw(surface)
       self.bomb.draw(surface)
       if not self.dead:
          surface.blit(self.rot_image,self.rot_pos)
          if self.wave:
             x=int(self.center[0])
             y=int(self.center[1])
             pygame.draw.circle(surface,YELLOW,(x,y),self.wave_radius,5)
       self.explosion.draw(surface)
       self.charge_shot.draw(surface)
       self.sheild.draw(surface)
       if self.vitality>0:
          pygame.draw.rect(surface,GREEN,[20,12,self.vitality,5],0)


class Shot:
   
   def __init__(self):
       self.image=pygame.Surface((10,10)).convert()
       self.image.set_colorkey(self.image.get_at((0,0)))
       pygame.draw.circle(self.image,BLUE,(5,5),5)
       self.rect=self.image.get_rect()
       self.radius=5
       self.center=self.rect.center
       self.direction=[0,0]
       self.active=False
       
   def update(self):
       if self.active:
          self.rect.centerx+=self.direction[0]
          self.rect.centery+=self.direction[1]
          if self.rect.x<-10 or self.rect.x>SCREEN_WIDTH \
          or self.rect.y<-10 or self.rect.y>SCREEN_HEIGHT:
             self.active=False
             
   def asteroid_collision(self,asteroid):
       if not asteroid.dead and self.active:
          if collide(self.rect.center,asteroid.rect):
             self.center=self.rect.center
             asteroid.center=asteroid.rect.center
             if circle_collision(self,asteroid):
                self.active=False
                asteroid.hited=True
                asteroid.vitality-=1
                asteroid.image=asteroid.hited_image
                asteroid.show_bar_time=30
                   
   def draw(self,surface):
       if self.active:
          surface.blit(self.image,self.rect)


class ChargeShot:

   def __init__(self):
       self.radius=5
       self.power=self.radius
       self.energy=50
       self.reload_time=0
       self.center=[0,0]
       self.direction=[0,0]
       self.normalized_direction=[0,0]
       self.active=False
       self.charging=False
       self.wave_radius=10
       self.wave=False

   def update(self):
       if self.energy<50:
          self.reload_time+=1
          if self.reload_time==50:
             self.reload_time=0
             self.energy+=1
       if self.active:
          if self.charging and self.energy>0:
             sounds["charging.wav"].stop()
             sounds["charging.wav"].play()
             self.radius+=1
             self.power+=1
             self.energy-=1
             self.center[0]+=self.normalized_direction[0]
             self.center[1]+=self.normalized_direction[1]
             if self.energy<=0:
                self.charging=False
                sounds["charging.wav"].stop()
                sounds["shot2.wav"].play()
          else:
             self.center[0]+=self.direction[0]
             self.center[1]+=self.direction[1]
             if self.center[0]+self.radius<0 or self.center[0]-self.radius>SCREEN_WIDTH \
             or self.center[1]+self.radius<0 or self.center[1]-self.radius>SCREEN_HEIGHT:
                self.active=False
                self.radius=5
                self.power=self.radius
          if self.wave: 
             self.wave_radius+=20
             if self.wave_radius>=self.radius*4:
                self.active=False
                self.wave=False
                self.wave_radius=10
                self.radius=5
                self.power=self.radius
                
   def asteroid_collision(self,asteroid):
       if not asteroid.dead and not self.wave and self.active:
          asteroid.center=asteroid.rect.center
          if circle_collision(self,asteroid):
             sounds["charging.wav"].stop()
             sounds["choc2.wav"].play()
             self.charging=False
             self.direction=[0,0]
             self.wave=True
             asteroid.hited=True
             asteroid.vitality-=self.power
             asteroid.image=asteroid.hited_image
             asteroid.show_bar_time=30
      
   def draw(self,surface):
       if self.active:
          x=int(self.center[0])
          y=int(self.center[1])
          pygame.draw.circle(surface,BLUE,(x,y),self.radius)
          if self.wave:
             pygame.draw.circle(surface,BLUE,(x,y),self.wave_radius,5)
       pygame.draw.rect(surface,BLUE,[20,20,self.energy,5],0)


class Sheild:

   def __init__(self,center):
       self.get_images()
       self.center=center
       self.radius=50
       self.vitality=50
       self.hited_count=0
       self.hited=False
       self.active=False

   def asteroid_collision(self,asteroid):     
       if not asteroid.dead and self.active:
          rect=[self.center[0]-50,self.center[1]-50,100,100]
          if rect_collision(asteroid.rect,rect):
             c1=self.center
             c2=asteroid.rect.center
             dy=c2[1]-c1[1]
             dx=c2[0]-c1[0]
             lenght=math.sqrt(dx**2+dy**2)
             if self.radius+asteroid.radius>lenght:
                angle=math.degrees(math.atan2(dy,dx))
                asteroid.xvel=math.cos(math.radians(angle))*asteroid.speed
                asteroid.yvel=math.sin(math.radians(angle))*asteroid.speed
                asteroid.choc_velocity=[asteroid.xvel*5,asteroid.yvel*5]
                asteroid.choc=True
                asteroid.hited=True
                asteroid.vitality-=asteroid.power
                asteroid.image=asteroid.hited_image
                asteroid.show_bar_time=30
                self.hited=True
                self.image=self.hited_image
                self.vitality-=asteroid.power
                sounds["choc1.wav"].play()
                if self.vitality<=0:
                   self.active=False
                      
   def get_images(self):
       self.normal_image=pygame.Surface((100,100)).convert()
       self.normal_image.set_colorkey(self.normal_image.get_at((0,0)))
       self.normal_image.set_alpha(100)
       self.hited_image=self.normal_image.copy()
       pygame.draw.circle(self.normal_image,BLUE,(50,50),50)
       pygame.draw.circle(self.hited_image,RED,(50,50),50)
       self.image=self.normal_image

   def update(self):
       if self.active:
          if self.hited:
             if self.hited_count>=3:
                self.image=self.normal_image
                self.hited_count=0
                self.hited=False
             self.hited_count+=1
          
   def draw(self,surface):
     if self.vitality>0:
        pygame.draw.rect(surface,LIGHTBLUE,[20,28,self.vitality,5],0)
        if self.active :
           x=self.center[0]-50
           y=self.center[1]-50
           surface.blit(self.image,(x,y))

       
class Missile:

   def __init__(self):
       self.angle=0
       self.get_images()
       self.center=[0,0]
       self.pos=[0,0]
       self.rot_pos=[0,0]
       self.center=[0,0]
       self.radius=5
       self.power=10
       self.move_speed=10
       self.moved_distance=0
       self.target=0
       self.target_angle=0
       self.rotangle=0
       self.wave_radius=5
       self.wave=False
       self.active=False

   def get_images(self):
       self.image=pygame.Surface((30,10)).convert()
       self.image.set_colorkey(self.image.get_at((0,0)))
       pygame.draw.circle(self.image,RED,(25,5),5)
       pygame.draw.rect(self.image,RED,[0,0,25,10],0)
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       self.rot_rect=self.rot_image.get_rect()
       self.width=self.image.get_width()
       self.height=self.image.get_height()
       self.half_width=int(self.width/2)
       self.half_height=int(self.height/2)       
       
   def rotate_center(self,angle):
       self.angle+=angle
       self.fix_angle()
       self.get_velocity()
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       self.rot_rect=self.rot_image.get_rect(center=self.rot_rect.center)
       self.rot_pos=[self.rot_rect.x,self.rot_rect.y]

   def rotate_center2(self,angle):
       self.angle+=angle
       self.fix_angle()
       self.get_velocity()
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       dx=self.half_width-int(self.rot_image.get_width()/2)
       dy=self.half_height-int(self.rot_image.get_height()/2)
       self.rot_pos[0]=self.pos[0]+dx
       self.rot_pos[1]=self.pos[1]+dy
       
   def move(self,xvel,yvel):
       self.pos[0]+=xvel
       self.pos[1]+=yvel
       self.center[0]+=xvel
       self.center[1]+=yvel              
       self.rot_pos[0]+=xvel
       self.rot_pos[1]+=yvel
       self.rot_rect.center=self.center
       
   def fix_angle(self):
       if self.angle>360:
          self.angle-=360
       elif self.angle<0:
          self.angle+=360
          
   def get_velocity(self):
       x=math.cos(math.radians(self.angle))*self.move_speed
       y=math.sin(math.radians(self.angle))*self.move_speed
       self.xvel=x
       self.yvel=y
       
   def offscreen_update(self):       
       if self.pos[0]<-self.width \
       or self.pos[0]>SCREEN_WIDTH \
       or self.pos[1]<-self.height \
       or self.pos[1]>SCREEN_HEIGHT:
          self.active=False
          
   def activate(self,pos,angle):
       self.active=True
       self.pos=[pos[0],pos[1]]
       self.rot_pos=[pos[0],pos[1]]
       self.angle=0
       self.center=[self.pos[0]+self.half_width,self.pos[1]+self.half_height]
       self.rot_image=pygame.transform.rotate(self.image,self.angle)
       self.rot_rect=self.rot_image.get_rect(topleft=pos)
       dx=pos[0]-self.center[0]
       dy=pos[1]-self.center[1]
       self.move(dx,dy)
       self.rotate_center2(angle)
       self.target=0
       self.moved_distance=0
       self.get_velocity()

   def get_target(self,target):
       if not target.dead:
          self.target=target
          
   def hunt_target(self):
       c1=self.center
       c2=self.target.rect.center
       dx=c2[0]-c1[0]
       dy=c2[1]-c1[1]
       angle=math.degrees(math.atan2(-dy,dx))
       if angle<0:
          angle+=360
       difangle=self.angle-angle
       if difangle>0 and difangle<180 or difangle<-180:
          self.rotangle=-5
       else:
          self.rotangle=5
       self.rotate_center2(self.rotangle)
       self.get_velocity()
       
   def asteroid_collision(self,asteroid):     
       if self.active and not self.wave:
          if self.target:
             if collide(self.center,self.target.rect):
                self.target.center=self.target.rect.center
                if circle_collision(self,self.target):
                   self.wave=True
                   self.target.hited=True
                   self.target.vitality-=self.power
                   self.target.image=asteroid.hited_image
                   self.target.show_bar_time=30
                   sounds["explosion1.wav"].play()
          if not asteroid.dead:
             if collide(self.center,asteroid.rect):
                asteroid.center=asteroid.rect.center
                if circle_collision(self,asteroid):
                   self.wave=True
                   asteroid.hited=True
                   asteroid.vitality-=self.power
                   asteroid.image=asteroid.hited_image
                   asteroid.show_bar_time=30
                   sounds["explosion1.wav"].play()
                   
   def update(self):
       if self.active:
          if not self.wave:
             self.move(self.xvel,-self.yvel)
             self.offscreen_update()
             self.moved_distance+=1
             if self.moved_distance>10:
                if self.target and not self.target.dead:
                   self.hunt_target()
                else:
                   self.get_target(asteroid)
          else:
            self.wave_radius+=10
            if self.wave_radius>=70:
               self.wave=False
               self.active=False
               self.wave_radius=5
                 
   def draw(self,surface):
       if self.active:
          if not self.wave:
             surface.blit(self.rot_image,self.rot_pos)
          else:
             pygame.draw.circle(surface,YELLOW,self.rot_rect.center,20)
             pygame.draw.circle(surface,YELLOW,self.rot_rect.center,self.wave_radius,5)


class Lazer_Beam:

   def __init__(self):
       self.start=[0,0]
       self.end=[0,0]
       self.vilocity=[0,0]
       self.diameter=10
       self.radius=5
       self.length=2
       self.move_speed=20
       self.time=0
       self.power=2
       self.color=BLUE
       self.color_time=0
       self.active=False
       
   def update(self):
       if self.active:
          if self.length<1000:
             self.end[0]+=self.vilocity[0]
             self.end[1]+=self.vilocity[1]
             self.length+=self.move_speed
          if self.time<100:
             self.time+=1
             sounds["beam.wav"].stop()
             sounds["beam.wav"].play()
          else:
             self.time=0
             self.length=2
             self.active=False
             sounds["beam.wav"].stop()
          if self.color_time<2:
             self.color_time+=1
          else:
             self.color_time=0
             if self.color==BLUE:
                self.color=LIGHTBLUE
             elif self.color==LIGHTBLUE:
                self.color=BLUE             
   
   def asteroid_collision(self,asteroid):      
       if not asteroid.dead and self.active:
          asteroid.center=asteroid.rect.center
          if line_circle_collision(asteroid.center,asteroid.radius,self.start,self.end,self.radius):
             asteroid.hited=True
             asteroid.vitality-=self.power
             asteroid.image=asteroid.hited_image
             asteroid.show_bar_time=30
                          
   def draw(self,surface):
       if self.active:
          x=int(self.end[0])
          y=int(self.end[1])
          pygame.draw.line(screen,self.color,self.start,self.end,self.diameter)
          pygame.draw.circle(surface,self.color,(int(self.start[0]),int(self.start[1])),self.diameter)
          pygame.draw.circle(surface,self.color,(int(self.end[0]),int(self.end[1])),self.radius)


class Bomb:

   def __init__(self):
       self.center=[0,0]
       self.radius=5
       self.power=5
       self.active=False
       
   def update(self):
       if self.active:
          self.radius+=10
          if self.radius>500:
             self.radius=5
             self.active=False
             
   def asteroid_collision(self,asteroid):      
       if not asteroid.dead and self.active:
          asteroid.center=asteroid.rect.center
          c1=self.center
          c2=asteroid.center
          lenght=math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
          if self.radius+asteroid.radius>lenght \
          and lenght>self.radius-asteroid.radius:
             asteroid.hited=True
             asteroid.vitality-=self.power
             asteroid.image=asteroid.hited_image
             asteroid.show_bar_time=30
             
   def draw(self,surface):
       if self.active:
          x=int(self.center[0])
          y=int(self.center[1])
          pygame.draw.circle(surface,BLUE,(x,y),self.radius,5)    

              
class Asteroid:
    
   group=[]
   
   def __init__(self,pos,size):
       if not self in Asteroid.group:
          Asteroid.group.append(self)
       self.size=size
       self.radius=int(size/2)
       self.vitality=int(size/2)
       self.power=int(size/10)
       self.get_images()
       self.rect=self.image.get_rect(topleft=pos)
       self.center=self.rect.center
       self.explosion=Explosion(self.rect.center,self)
       self.dead=False
       self.hited=False
       self.wave=False
       self.wave_radius=10
       self.show_bar_time=0
       self.on_hit=0
       self.get_velocity()
       self.choc_velocity=[0,0]
       self.choc=False
       self.on_choc=0
       
   def update(self):
       if not self.dead:
          self.rect.x+=self.xvel
          self.rect.y+=self.yvel
          if self.rect.x<-self.size:
             self.rect.x=SCREEN_WIDTH
          elif self.rect.x>SCREEN_WIDTH:
               self.rect.x=-self.size
          if self.rect.y<-self.size:
             self.rect.y=SCREEN_HEIGHT
          elif self.rect.y>SCREEN_HEIGHT:
               self.rect.y=-self.size
          if self.hited:
             if self.vitality>0:
                if self.on_hit>=3:
                   self.image=self.normal_image
                   self.on_hit=0
                   self.hited=False
                self.on_hit+=1
             else:
                self.xvel=0
                self.yvel=0
                self.wave=True
                self.wave_radius+=20
                if self.wave_radius>=self.radius*5:
                   self.dead=True
                   self.explosion.active=True
                   self.center=self.rect.center
                   self.explosion.init_particles()
                   global score
                   score+=self.size
                   sounds["explosion2.wav"].play()
          if self.choc and not self.wave:
             self.take_choc()
       self.explosion.update()

   def kill(self):
       asteroid.group.remove(self)
       if len(Asteroid.group)==0:
          init_game(next_battle=True)

   def draw(self,surface):
       if not self.dead:
          surface.blit(self.image,self.rect)
          if self.wave:
             pygame.draw.circle(surface,YELLOW,(self.rect.center),self.wave_radius,5)
          if self.show_bar_time>0 and self.vitality>0:
             self.show_bar_time-=1
             x=self.rect.center[0]-25
             y=self.rect.center[1]-self.radius-10
             pygame.draw.rect(surface,GREEN,[x,y,self.vitality,5],0)
       self.explosion.draw(surface)

   def get_velocity(self):
       index=random.randint(0,len(directions)-1)
       self.xvel=directions[index][0]
       self.yvel=directions[index][1]
       self.speed=math.hypot(self.xvel,self.yvel)
       
   def get_images(self):
       self.normal_image=pygame.Surface((self.size,self.size)).convert()
       self.normal_image.set_colorkey(self.normal_image.get_at((0,0)))
       self.hited_image=self.normal_image.copy()
       pygame.draw.circle(self.normal_image,RED,(self.radius,self.radius),self.radius)
       pygame.draw.circle(self.hited_image,YELLOW,(self.radius,self.radius),self.radius)
       self.image=self.normal_image
       
   def take_choc(self):
       self.rect.x+=self.choc_velocity[0]
       self.rect.y+=self.choc_velocity[1]
       self.on_choc+=1
       if not int(self.choc_velocity[0])==0:
          if self.choc_velocity[0]>0:
             self.choc_velocity[0]-=1
          else:
             self.choc_velocity[0]+=1
       if not int(self.choc_velocity[1])==0:
          if self.choc_velocity[1]>0:
             self.choc_velocity[1]-=1
          else:
             self.choc_velocity[1]+=1
       if int(self.choc_velocity[0])==0 \
       and int(self.choc_velocity[1])==0:
           self.choc=False
           self.on_choc=0
        
       
class Particle:

   def __init__(self,pos,size):
       self.pos=pos
       self.size=(size,size)
       self.image=pygame.Surface(self.size).convert()
       self.image.set_colorkey(self.image.get_at((0,0)))
       self.rect=self.image.get_rect(center=pos)
       pygame.draw.circle(self.image,RED,(int(size/2),int(size/2)),int(size/2))
       self.origin=[0,0]
       self.dead=False
       self.time=0
       self.max_time=1
       self.xvel=0
       self.yvel=0
       
   def move(self):
       self.pos[0]+=self.xvel
       self.pos[1]+=self.yvel
       self.time+=1
       if self.time>=self.max_time:
          self.dead=True


class Explosion:

   def __init__(self,pos,parent):
       self.pos=pos
       self.parent=parent
       self.get_prticles()
       self.init_particles()
       self.particles_to_move=10
       self.time=0
       self.active=False
       
   def get_prticles(self):
       self.particles=[]
       for i in range(30):
           pos=[self.pos[0],self.pos[1]]
           size=int((self.parent.size/100)*20)
           self.particles.append(Particle(pos,size))

   def init_particles(self):
       counter=0
       multiplier=int(self.parent.radius/10)
       self.pos=self.parent.center
       for particle in self.particles:
           particle.pos=[self.pos[0],self.pos[1]]
           index=random.randint(0,len(directions)-1)
           particle.xvel=directions[index][0]*2
           particle.yvel=directions[index][1]*2
           particle.pos[0]+=particle.xvel*multiplier
           particle.pos[1]+=particle.yvel*multiplier
           particle.max_time*=multiplier
           if multiplier<3:
              counter+=1
              if counter==10:
                 counter=0
                 multiplier+=10
           
   def update(self):
       if self.active:
          for i in range(self.particles_to_move-1,-1,-1):
              particle=self.particles[i]
              if not particle.dead:
                 particle.move()
              else:
                 self.particles.remove(particle)
                 self.particles_to_move-=1
          if len(self.particles)==0:
             self.active=False
             self.parent.kill()
          if self.particles_to_move<len(self.particles):
             self.time+=1
             if self.time==1:
                self.time=0
                self.particles_to_move+=10
   
   def draw(self,surface):
       if self.active:
          for particle in self.particles:
              surface.blit(particle.image,particle.pos)



pygame.init()

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add  RESIZABLE or FULLSCREEN
#Title
pygame.display.set_caption("asteroids battle")
#icon
icone = pygame.image.load("asteroids_battle_data/rocket.png")
pygame.display.set_icon(icone)


axis_up=-0.00784325693533128
axis_center=-0.007843017578125
num_joysticks = pygame.joystick.get_count()
if num_joysticks > 0:
   joystick = pygame.joystick.Joystick(0)
   joystick.init()
   for event in pygame.event.get():
       if event.type == JOYAXISMOTION:
          axis_up=event.value
          axis_center=joystick.get_axis(0)
          
font=pygame.font.SysFont('Arial',18)
font2=pygame.font.SysFont('Arial',28)
fullscreen=False
sounds=get_sounds()
score=0
best_score=0
battle=1
game_over=False
game_over_timer=0
num_asteroids=3
asteroids=Asteroid.group
directions=get_directions()
player=Player([280,220])
make_asteroids(num_asteroids)
background=make_background()
title_screen()
start_stage()


#pygame.key.set_repeat(400, 30)

while True:
    
    #loop speed limitation
    #30 frames per second is enought
    CLOCK.tick(30)
    
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
           
           
        if event.type == KEYDOWN:
           if event.key == K_F2:
              if not fullscreen:
                 screen = pygame.display.set_mode((640, 480),FULLSCREEN)
                 fullscreen=True
              elif fullscreen:
                 screen = pygame.display.set_mode((640, 480),)
                 fullscreen=False
           elif event.key == K_F3:
              if not game_over:
                 save_game()
           elif event.key == K_F4:
              load_game()
           if event.key == K_UP:
              player.up=True
           elif event.key == K_DOWN:
              player.down=True
           if event.key == K_RIGHT:
              player.right=True
           elif event.key == K_LEFT:
              player.left=True
           if event.key == K_s:
              player.shooting=True
           elif event.key == K_SPACE:
              player.init_charge_shot()
           elif event.key == K_l:
              player.shoot_lazer_beam()
           if event.key == K_f:
              player.fire_missile()
           if event.key == K_g:
              player.launch_bomb()
           if event.key == K_p:
              pause_game()              
           if event.key == K_d:
              if not player.dead \
              and not player.wave:
                if player.sheild.vitality>0:
                   if not player.sheild.active:
                      player.sheild.active=True
                   else:
                      player.sheild.active=False
        if event.type == KEYUP:
           if event.key == K_UP:
              player.up=False
           elif event.key == K_DOWN:
              player.down=False
           if event.key == K_RIGHT:
              player.right=False
           elif event.key == K_LEFT:
              player.left=False
           if event.key == K_s:
              player.shooting=False
           if event.key == K_SPACE:
              if player.charge_shot.charging:
                 player.charge_shot.charging=False
                 sounds["charging.wav"].stop()
                 sounds["shot2.wav"].play()
                 
        if num_joysticks > 0:      
           if event.type == JOYAXISMOTION:
              if event.axis == 1 and event.value < 0:
                 player.up=True
              elif event.axis == 1 and event.value > 0:
                 player.down=True
              if event.axis == 0 and event.value > 0:
                 player.right=True
              elif event.axis == 0 and event.value < 0:
                 player.left=True
              if event.axis == 1 and event.value == axis_up:
                 player.up=False
                 player.down=False
              if event.axis == 0 and event.value == axis_up:
                 player.right=False
                 player.left=False                  
           if event.type == JOYBUTTONDOWN:
              if event.button == 2:
                 player.shooting=True
              elif event.button == 3:
                 player.init_charge_shot()
              if event.button == 0:
                 player.fire_missile()
              if event.button == 1:
                 player.launch_bomb()
              if event.button == 9:
                 pause_game()
              if event.button == 7:
                 player.shoot_lazer_beam()                               
              if event.button == 5:
                 if not player.dead \
                 and not player.wave:
                   if player.sheild.vitality>0:
                      if not player.sheild.active:
                         player.sheild.active=True
                      else:
                         player.sheild.active=False
           if event.type == JOYBUTTONUP:
              if event.button == 2:
                 player.shooting=False
              if event.button == 3:
                 if player.charge_shot.charging:
                    player.charge_shot.charging=False
                    sounds["charging.wav"].stop()
                    sounds["shot2.wav"].play()
                                              
    player.update(asteroids)
    for asteroid in asteroids:
        asteroid.update()
    
    screen.blit(background,(0,0))
    for asteroid in asteroids:
        asteroid.draw(screen)
    player.draw(screen)
    text=font.render(("missiles:"+str(player.missiles)),True,BLACK)
    screen.blit(text,(100,5))
    text=font.render(("bombs:"+str(player.bombs)),True,BLACK)
    screen.blit(text,(100,20))
    text=font.render(("lives:"+str(player.lives)),True,BLACK)
    screen.blit(text,(205,5))    
    text=font.render(("score:"+str(score)),True,BLACK)
    screen.blit(text,(500,5))
    text=font.render(("asteroids:"+str(len(asteroids))),True,BLACK)
    screen.blit(text,(380,5))
    text=font.render(("battle:"+str(battle)),True,BLACK)
    screen.blit(text,(285,5))
    if game_over:
       text=font2.render(("Game  Over"),True,RED)
       screen.blit(text,(230,230))
       game_over_timer+=1
       if game_over_timer>50:
          game_over_timer=0
          game_over=False
          init_game(start_game=True)
    pygame.display.flip()
    
