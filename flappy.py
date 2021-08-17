import pygame as pg
import os
import random

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

IMG_CANO = pg.transform.scale2x(pg.image.load(os.path.join('imgs','pipe.png')))
IMG_BASE = pg.transform.scale2x(pg.image.load(os.path.join('imgs','base.png')))
IMG_BG = pg.transform.scale2x(pg.image.load(os.path.join('imgs','bg.png')))
IMG_BIRD = [
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird1.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird2.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs','bird3.png')))
]

pg.font.init()
SCORE_FONT = pg.font.SysFont('Arial', 50)

