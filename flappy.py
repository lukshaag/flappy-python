import pygame
import os
import random
import neat


ai_playing = True
generation = 0

#WINDOW AND ASSETS CONFIG
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 500

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\pipe.png'))
IMG_BASE = pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\base.png'))
IMG_BG = pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\bg.png'))
IMG_BIRD = [
    pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\bird1.png')),
    pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\bird2.png')),
    pygame.transform.scale2x(pygame.image.load(r'D:\CURSOS\PYTHON\PYTHON GAMES\FLAPPY BIRD\imgs\bird3.png'))
]

pygame.font.init()
SCORE_FONT = pygame.font.SysFont('Arial', 50)

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
        img_rotated = pygame.transform.rotate(self.img, self.angle)
        pos_img_center = self.img.get_rect(topleft=(self.x, self.y)).center
        rect = img_rotated.get_rect(center=pos_img_center)
        screen.blit(img_rotated, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    
class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.posTOP = 0
        self.posBASE = 0
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
        self.PIPE_BASE = IMG_PIPE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.posTOP = self.height - self.PIPE_TOP.get_height()
        self.posBASE = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.posTOP))
        screen.blit(self.PIPE_BASE, (self.x, self.posBASE))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        distance_top = (self.x - bird.x, round(self.posTOP) - round(bird.y))
        distance_base = (self.x - bird.x, round(self.posBASE) - round(bird.y))

        point_top = bird_mask.overlap(top_mask, distance_base)
        point_base = bird_mask.overlap(base_mask, distance_base)

        if point_base or point_top:
            return True
        else:
            return False


class Base:
    SPEED = 5
    WIDTH = IMG_BASE.get_width()
    IMG = IMG_BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH <0:
            self.x2 = self.x1  + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))

def screen_draw(screen, birds, pipes, base, score):
    screen.blit(IMG_BG, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = SCORE_FONT.render(f'SCORE: {score}', 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    if ai_playing:
        text = SCORE_FONT.render(f'GEN: {generation}', 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    base.draw(screen)
    pygame.display.update()

def main():
    birds = [Bird(230, 350)]
    base = Base(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    timer = pygame.time.Clock()

    running = True
    while running:
        timer.tick(30)

        #user interact
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
        #move bird and base
        for bird in birds:
            bird.move()
        base.move()

        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)
        
        for i, bird in enumerate(birds):
            if (bird.y + bird.img.get_height()) > base.y or bird.y < 0:
                birds.pop(i)


        screen_draw(screen, birds, pipes, base, score)

if __name__ == '__main__':
    main()