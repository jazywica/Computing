# -*- encoding: utf-8 -*-
""" SPACESHIP - First part of the game - Week 3 """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_cjpi0KNasX_1.py

import math
import random
try:
    import simplegui  # access to drawing operations for interactive applications
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  # CodeSkulptor GUI module stand alone version


# 1. Globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

angle_vel_inc = 0.05  # these two variables are put here as 'global' to make them easy to adjust
pos_vel_inc = 0.1
c = 0.01  # this is a component for the friction


# 2. Class definition
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

    def change_direction(self, angle_vel_inc):  # this is an internal method that changes the ship's velocity
        self.angle_vel += angle_vel_inc

    def thrusters_on_off(self, thrusting):
        if thrusting:
            self.thrust = True
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        forward_vector = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0] + (forward_vector[0] * 35), self.pos[1] + (forward_vector[1] * 35)],
                           [self.vel[0] + forward_vector[0] * 5, self.vel[1] + forward_vector[1] * 5], 0, 0, missile_image, missile_info, missile_sound)

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel  # this class is designed to update ship's heading via an internal field 'angle_vel'
        forward_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] = self.vel[0] + (forward_vector[0] * pos_vel_inc)  # this takes care of the acceleration, which is present only when the 'up' arrow is pressed
            self.vel[1] = self.vel[1] + (forward_vector[1] * pos_vel_inc)
        self.vel[0] *= (1 - c)  # this takes care of the friction, the smallest value will always be 0 (it will never go negative)
        self.vel[1] *= (1 - c)
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
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

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel  # for all the motions we are simply updating the position with velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


# 3. Helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# 4. Define key handlers to control firing_angle
def keydown(key):
    global a_bubble, firing_angle_vel, bubble_stuck
    if simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()
    elif simplegui.KEY_MAP["left"] == key:  # what we do here, we just increment the velocity by a fixed amount stored in 'firing_angle_vel_inc'
        my_ship.change_direction(-angle_vel_inc)
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.change_direction(angle_vel_inc)
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_on_off(True)

def keyup(key):
    global firing_angle_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.change_direction(angle_vel_inc)  # and here we subtract the same amount so we go back to zero again
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.change_direction(-angle_vel_inc)
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_on_off(False)


# 5. Define the draw handler
def draw(canvas): # remember that this procedure is called by the frame 60 times per second
    global time

    # animate background - we draw the background first as we want this to be below all the other images
    time += 1  # this is a primitive timer, it will increase by 60 every second
    wtime = (time / 4) % WIDTH  # this represents a horizontal shift of 20 pixels per second (40sec to pass across the 800px screen), which we are going to need for the dynamic debris
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],[WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))  # by using 'wtime - WIDTH / 2' we use two dynamic images and move them glued across the screen
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))  # we need two images to have the full coverage
    canvas.draw_text('Lives:', [40, 40], 28, 'White')
    canvas.draw_text(str(lives), [40, 70], 28, 'White')
    canvas.draw_text('Score:', [690, 40], 28, 'White')
    canvas.draw_text(str(score), [690, 70], 28, 'White')

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


# 6. Timer handler that spawns a rock
def rock_spawner():
    global a_rock
    range = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    a_rock = Sprite([random.randrange(45, WIDTH - 45), random.randrange(45, HEIGHT - 45)], [random.choice(range), random.choice(range)], 0, random.choice(range) * 0.1, asteroid_image, asteroid_info)


# 7. Images and sounds
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")  # alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# 8. Initialize frame and register handlers
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# 9. Initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
timer = simplegui.create_timer(1000.0, rock_spawner)


# 10. Get things rolling
timer.start()
frame.start()
