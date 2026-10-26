import pygame
def start_menu(screen):
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