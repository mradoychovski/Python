# program template for Spaceship
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
 
 
class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        
    def get_center(self):
        return self.center
 
    def get_size(self):
        return self.size
 
    def get_radius(self):
        return self.radius
 
    def get_lifespan(self):
        return self.lifespan
 
    def get_animated(self):
        return self.animated
 
 
# art assets created by Kim Lathrop, may be freely re-used in
# non-commercial projects, please credit Kim
 
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
# debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png,
# debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "https://www.dropbox.com/s/yno5lc731x34b4k/debris.png?dl=1")
 
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "https://www.dropbox.com/s/0e015b0pfk3p0e6/nebula.jpg?dl=1")
 
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "https://www.dropbox.com/s/8cgid4m470njdfb/asteroids_blue_tee.jpg?dl=1")
 
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "https://www.dropbox.com/s/n0p6q91huhlltxz/spaceship%2Bboost.png?dl=1")
 
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image(
    "https://www.dropbox.com/s/ufdkgd9botze6f7/missile.png?dl=1")
 
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "https://www.dropbox.com/s/o39bneyp9bh00w6/asteroids4.png?dl=1")
 
# animated explosion - explosion_orange.png, explosion_blue.png,
# explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "https://www.dropbox.com/s/h6bmj8cysa7a5vv/explosion.png?dl=1")
 
# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound(
    "https://www.dropbox.com/s/47tvpr88kt2p3oj/powerUp.ogg?dl=1")
#soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound(
    "http://rpg.hamsterrepublic.com/wiki-images/2/21/Collision8-Bit.ogg")
ship_thrust_sound = simplegui.load_sound(
    "http://rpg.hamsterrepublic.com/wiki-images/a/a2/ThunderMagic.ogg")
explosion_sound = simplegui.load_sound(
    "http://rpg.hamsterrepublic.com/wiki-images/0/0c/TornadoMagic.ogg")
explosion_sound.set_volume(.5)
 
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
  
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) 
 
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
 
    def draw(self, canvas):
        center = list(self.image_center)
        if self.thrust:
            center[1] = self.image_center[1] + self.image_size[1]
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
 
    def update(self):
        # update angle
        self.angle += self.angle_vel
 
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .2
            self.vel[1] += acc[1] * .2
 
        self.vel[0] *= .99
        self.vel[1] *= .99
 
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def keydown(self,key):
        ang_vel = .09
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel = - ang_vel
        elif key == simplegui.KEY_MAP['right']:
            self.angle_vel = ang_vel
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = True
            if self.thrust:
                ship_thrust_sound.play()
        elif key == simplegui.KEY_MAP['space']:
            self.shoot()
            
    def keyup(self,key):
        angle_vel = 0
        if key == simplegui.KEY_MAP['right']:
            my_ship.angle_vel = angle_vel
        elif key == simplegui.KEY_MAP['left']:
            my_ship.angle_vel = angle_vel
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = False
            if not self.thrust:
                self.forward = [0,0]
                ship_thrust_sound.pause()
 
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0],
                       self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0],
                       self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                 missile_image, missile_info, missile_sound))
  
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.init_vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def get_vel(self):
        return self.vel
 
    def draw(self, canvas):
        center = list(self.image_center)
        if self.animated:
            center[0] = self.image_center[0] + (self.image_size[0] * self.age)
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
 
    def update(self):
        # update angle
        self.angle += self.angle_vel
 
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        self.age += 1
        return self.age > self.lifespan
 
    def collide(self, other_object):
        return dist(self.pos, other_object.pos) <= self.radius + other_object.radius
  
# mouseclick handlers that reset UI and conditions whether splash image is
# drawn
def click(pos):
    global started, lives, score, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        timer.start()
 
def draw(canvas):
    global time, started, score, lives, rock_group, my_ships
 
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]],
                      [size[0] - 2 * wtime, size[1]],
                      [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2],
                      [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]],
                      [2 * wtime, size[1]], [1.25 * wtime, HEIGHT / 2],
                      [2.5 * wtime, HEIGHT])

    # soundrack
    soundtrack.play()
    
    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
 
    # process collisions
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(missile_group, rock_group) * 10
 
    # end of game handling
    if lives == 0:
        started = False
        rock_group = set()
        timer.stop()
        soundtrack.rewind()
 
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("Score", [680, 50], 22, "White", "sans-serif")
    canvas.draw_text(str(lives), [50, 80], 22, "White", "sans-serif")
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")
 
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

# feeds draw handler for sprite groups
def process_sprite_group(group, canvas):
    for obj in set(group):
        obj.draw(canvas)
        if obj.update():
            group.discard(obj)
        
# removes sprites upon collision with ship
def group_collide(group, other_object):
    global explosion_group
    for obj in set(group):
        if obj.collide(other_object):
            group.discard(obj)
            explosion_group.add(Sprite(obj.pos, [0, 0], 0, 0, explosion_image,
                                       explosion_info, explosion_sound))
            return True
    return False

# handles collisions between missiles and rocks
def group_group_collide(group, other_group):
    counter = 0
    for obj in set(group):
        if group_collide(other_group, obj):
            group.discard(obj)
            counter += 1
    return counter
        
# timer handler that spawns rock sprites
def rock_spawner():
    global rock_group, time
    rock_pos = [WIDTH * random.random(), HEIGHT * random.random()]
    rock_vel = [random.random() * 3 - 1.5,random.random() * 3 - 1.5]
    distance = dist(rock_pos, my_ship.get_pos())
    if started and len(rock_group) < 12 and distance > my_ship.get_radius() + asteroid_info.get_radius() + 100:
        rock_group.add(Sprite(rock_pos, rock_vel, 0, (random.random() - 0.5) / 8, asteroid_image, asteroid_info))
    
def key_down(key):
    my_ship.keydown(key)
    
def key_up(key):
    my_ship.keyup(key)

def kill():
    global lives
    lives = 0
 
 
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
 
# initialize ship and sprites groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 1.5 * math.pi, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()
 
 
# register handlers
frame.set_keyup_handler(key_up)
frame.set_keydown_handler(key_down)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("Kill yourself", kill, 100)
 
timer = simplegui.create_timer(1000.0, rock_spawner)
 
# get things rolling
timer.start()
frame.start()
