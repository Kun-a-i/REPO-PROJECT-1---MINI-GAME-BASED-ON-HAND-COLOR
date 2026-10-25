import pygame
import mechanic
import sys
import control


SCREEN_WIDTH  = 1920
SCRREN_HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCRREN_HEIGHT))
player = mechanic.Player(SCREEN_WIDTH, SCRREN_HEIGHT)
all_sprites = pygame.sprite.Group()
road = mechanic.Road(SCREEN_WIDTH,SCRREN_HEIGHT)
npc = mechanic.NPC(SCREEN_WIDTH, SCRREN_HEIGHT)
all_sprites.add(player)
clock = pygame.time.Clock()

cam_worker = control.CameraProcessor(4)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
    
            print(f"Cursor position: X={x}, Y={y}")
            
    screen.fill((0, 255, 0))
    road.update()
    road.draw(screen)
    npc.update()
    npc.draw(screen)
    if npc.check_hit(player) == 'hit' :
        pygame.time.delay(100)
    player.update()
    player.draw(screen)
    cam_worker.update(screen)


    

    clock.tick(60)
    
    pygame.display.flip()

cam_worker.stop()
pygame.quit()