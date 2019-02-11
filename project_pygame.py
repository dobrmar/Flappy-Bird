import pygame 
import os
import random


pygame.init() 
screen = pygame.display.set_mode((840, 500)) 
pygame.display.set_caption('Flappy bird')
running = True
jump = 4.5
v = 4
g = 0.2

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Bird(pygame.sprite.Sprite):
    image = load_image("bird1.png")
 
    def __init__(self, group):
        super().__init__(group)
        self.image = Bird.image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.score = 0
        self.end = False
        self.rect.y = 200
        self.v = 0
        self.start = False
        self.mask = pygame.mask.from_surface(self.image)
                
    def update(self, up):
        if up:
            self.v = - jump
        self.v += g
        self.rect.y += self.v
        if self.rect.y <= -17:
            self.start = False
            self.end = True
        elif self.rect.y >= 448:
            self.start = False
            self.end = True
        

class Block(pygame.sprite.Sprite):
    image = load_image("block1.png")
 
    def __init__(self, group, x, y, next):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.top = True
        self.have_score = False
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        if next:
            self.top = False
            Block(game.blocks, x, y - 654, False)
        
    def update(self):
        if self.rect.x + 90 < 0:
            if self.top:
                Block(game.blocks, 840, random.randint(100, 400), True)
            self.kill()
        else:
            self.rect.x -= v
        if pygame.sprite.collide_mask(self, bird):
            bird.start = False
            bird.end = True
        if self.top and self.rect.x + 100 < 50 and not self.have_score:
            bird.score += 1
            self.have_score = True


class Game:
    def __init__(self):       
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.decoration_before = pygame.sprite.Group()
        self.decoration_after = pygame.sprite.Group()
        
    def start_new_game(self):    
        self.blocks = pygame.sprite.Group()
        
        Block(game.blocks, 840, random.randint(100, 400), True)
        Block(game.blocks, 1150, random.randint(100, 400), True)
        Block(game.blocks, 1460, random.randint(100, 400), True)
        
        bird.rect.y = 200
        bird.score = 0
        game.decoration_before.draw(screen)
        screen.blit(text, (50, 7))
        screen.blit(f.render(str(bird.score), 0, (0, 0, 250)), (120, 7))
        game.all_sprites.draw(screen)
        game.blocks.draw(screen)
        game.decoration_after.draw(screen)
        
        game.decoration_before.draw(screen)
        screen.blit(text, (50, 7))
        screen.blit(f.render(str(bird.score), 0, (0, 0, 250)), (120, 7))
        game.all_sprites.draw(screen)
        game.blocks.draw(screen)
        game.decoration_after.draw(screen)
        screen.blit(f.render("нажмите пробел", 0, (0, 0, 230)), (25, 280))
        

game = Game()
    
setting = pygame.sprite.Sprite(game.decoration_after)
setting.image = load_image("setting.png")
setting.rect = setting.image.get_rect()
setting.rect.x = 5
setting.rect.y = 5

background = pygame.sprite.Sprite(game.decoration_before)
background.image = load_image("background1.png")
background.rect = background.image.get_rect()
background.rect.x = 0
background.rect.y = 0

bird = Bird(game.all_sprites)
Block(game.blocks, 840, random.randint(100, 400), True)
Block(game.blocks, 1150, random.randint(100, 400), True)
Block(game.blocks, 1460, random.randint(100, 400), True)

f = pygame.font.SysFont('comic sans ms', 20)
text = f.render("score:", 0, (0, 0, 250))

game.decoration_before.draw(screen)
screen.blit(text, (50, 7))
screen.blit(f.render(str(bird.score), 0, (0, 0, 250)), (120, 7))
game.all_sprites.draw(screen)
game.blocks.draw(screen)
game.decoration_after.draw(screen)
screen.blit(f.render("нажмите пробел", 0, (0, 0, 230)), (25, 280))

clock = pygame.time.Clock()
running = True
up = False
first_start = True
while running:
    clock.tick(60)
    up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not bird.end:
                    bird.start = True
                else:
                    bird.end = False
                    game.start_new_game()
                up = True
    if bird.start:
        game.all_sprites.update(up)
        game.blocks.update()
        game.decoration_before.draw(screen)
        game.all_sprites.draw(screen)
        game.blocks.draw(screen)
        game.decoration_after.draw(screen)
        screen.blit(text, (50, 7))
        screen.blit(f.render(str(bird.score), 0, (0, 0, 250)), (120, 7))
    elif bird.end:
        screen.blit(load_image('game_over1.png'), (250, 100))
        screen.blit(f.render("нажмите пробел для продолжения", 0, (0, 0, 230)), (250, 330))
    pygame.display.flip()
    
pygame.quit()