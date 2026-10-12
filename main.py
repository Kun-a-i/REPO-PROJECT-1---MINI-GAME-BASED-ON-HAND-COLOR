import pygame
import mechanic
import sys


SCREEN_WIDTH  = 1920
SCRREN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCRREN_HEIGHT))
player = mechanic.Player(SCREEN_WIDTH/2 + 45, SCRREN_HEIGHT - 300)
all_sprites = pygame.sprite.Group()
road = mechanic.Road(SCREEN_WIDTH,SCRREN_HEIGHT)
all_sprites.add(player)
clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
            
    screen.fill((0, 255, 0))
    road.update()
    road.draw(screen)
    player.update()

    all_sprites.draw(screen)
    

    clock.tick(60)
    
    pygame.display.flip()

pygame.quit()