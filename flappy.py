import pygame as pg
import os
import random


#WINDOW AND ASSETS CONFIG
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 500

IMG_PIPE = pg.transform.scale2x(pg.image.load(os.path.join('imgs','pipe.png')))
IMG_BASE = pg.transform.scale2x(pg.image.load(os.path.join('imgs','base.png')))
IMG_BG = pg.transform.scale2x(pg.image.load(os.path.join('imgs','bg.png')))
IMG_BIRD = [
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird1.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird2.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird3.png')))
]

pg.font.init()
SCORE_FONT = pg.font.SysFont('Arial', 50)

#GAME LOGIC
class Bird:
    IMGS = IMG_BIRD
    #rotate animation
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        #calculate displacement
        self.time += 1
        displacemnt = 1.5 * (self.time**2) + self.speed * self.time
        #restrinct desplacement
        if displacemnt > 16:
            displacemnt = 16
        elif displacemnt < 0:
            displacemnt -= 2
        
        self.y += displacemnt

        #bird angle
        if displacemnt < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATION

    def draw(self, screen):
        #define which sprite will use
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #if the bird is falling I won't flap

        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        #draw img
        img_rotated = pg.transform.rotate(self.img, self.angle)
        pos_img_center = self.img.get_rect(topleft=(self.x, self.y)).center
        rect = img_rotated.get_rect(center=pos_img_center)
        screen.blit(img_rotated, rect.topleft)

    def get_mask(self):
        pg.mask.from_surface(self.img)

class Base:
    pass

class Pipe:
    pass
