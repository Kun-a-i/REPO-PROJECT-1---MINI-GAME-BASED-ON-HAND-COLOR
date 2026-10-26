import pygame
import mechanic
import sys
import control

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080  # Fixed typo from SCRREN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()

# Fonts and UI Setup
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 100)

# Game State: can be "MENU" or "PLAYING"
game_state = "MENU"

player = mechanic.Player(SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites = pygame.sprite.Group()
road = mechanic.Road(SCREEN_WIDTH, SCREEN_HEIGHT)
npc = mechanic.NPC(SCREEN_WIDTH, SCREEN_HEIGHT)
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
            
            if game_state == "MENU":
                # Check if click is inside the start button
                if start_button_rect.collidepoint((x, y)):
                    game_state = "PLAYING"
            if game_state == "DEATH":
                if start_button_rect.collidepoint((x,y)):
                    player = mechanic.Player(SCREEN_WIDTH, SCREEN_HEIGHT)
                    all_sprites = pygame.sprite.Group()
                    road = mechanic.Road(SCREEN_WIDTH, SCREEN_HEIGHT)
                    npc = mechanic.NPC(SCREEN_WIDTH, SCREEN_HEIGHT)
                    all_sprites.add(player)
                    clock = pygame.time.Clock()
                    game_state = "PLAYING"
            else:
                # Color picker tool when playing
                pixel = screen.get_at((x, y))
                h, s, v, a = pixel.hsva
                print(f"H : {h/2}, S : {s/100 * 255}, V : {v/100 * 255}")

    if game_state == "MENU":
        # --- DRAW MENU ---
        screen.fill((30, 30, 30))  
        
        # Draw Title
        title_surf = font_large.render("PCV DRIVING GAME", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_surf, title_rect)
        
        # Draw Start Button
        pygame.draw.rect(screen, (0, 200, 0), start_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), start_button_rect, 4, border_radius=12) # Border
        
        # Draw Button Text
        text_surf = font_medium.render("START", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=start_button_rect.center)
        screen.blit(text_surf, text_rect)

    elif game_state == "PLAYING":
        screen.fill((0, 200, 0))
        road.update()
        road.draw(screen)
        npc.update()
        npc.draw(screen)
        
        if npc.check_hit(player) == 'hit' :
            game_state = "DEATH"

            
        player.update(steer=cam_worker.steering())
        player.draw(screen)
        cam_worker.update(screen)
    
        player.draw_steer(screen)

    elif game_state == "DEATH":
        screen.fill((30, 30, 30))  

        pygame.draw.rect(screen, (0, 200, 0), start_button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), start_button_rect, 4, border_radius=12) # Border
        
        # Draw Button Text
        text_surf = font_medium.render("PLAY AGAIN", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=start_button_rect.center)
        screen.blit(text_surf, text_rect)

        score_surf = font_large.render("GAME OVER", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(start_button_rect.centerx, start_button_rect.centery-300))
        screen.blit(score_surf, score_rect)

        score_surf = font_medium.render(f"YOUR SCORE WAS {player.score} !!!", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(start_button_rect.centerx, start_button_rect.centery-200))
        screen.blit(score_surf, score_rect)
        

    clock.tick(60)
    pygame.display.flip()

cam_worker.stop()
pygame.quit()
sys.exit()