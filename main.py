import pygame, sys
from settings import *
from random import choice, randint
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('graphics/main/map.png').convert()
        self.fg = pygame.image.load('graphics/main/overlay.png').convert_alpha()

    def customize_draw(self):

        # Change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2


        # blit the bg
        display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)
    
        # blit the fg
        display_surface.blit(self.fg, -self.offset)


# Basic Setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger Like')
clock = pygame.time.Clock()


# Sprite Groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# Sprite Creation
player = Player(pos = (2062,3274), groups = all_sprites, collision_sprites = obstacle_sprites)

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

# font
font = pygame.font.Font(None, 50)
text_surf = font.render('You Win!', True, 'white')
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

game_over_surf = font.render('Game Over!', True, 'white')
game_over_rect = game_over_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# music
music = pygame.mixer.Sound('audio/music.mp3')
music.play(loops = -1)

# Simple Sprite Setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

# Long Sprite Setup
for file_name, pos_list in LONG_OBJECTS.items():
    path = f'graphics/objects/long/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])

# Game Loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(pos, [all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # delta time
    dt = clock.tick() / 1000

    # Background
    display_surface.fill('black')

    if player.pos.y >= 1180:
        # update
        all_sprites.update(dt)
        # draw
        all_sprites.customize_draw()
    else:
        display_surface.fill('teal')
        display_surface.blit(text_surf, text_rect)


    # Update the display surface -> Draw the frame
    pygame.display.update()