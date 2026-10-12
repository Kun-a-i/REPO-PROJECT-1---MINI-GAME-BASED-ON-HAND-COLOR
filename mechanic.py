import pygame
import os
import cv2
CUR_PATH = os.getcwd()
PLAYER_SPRITE = os.path.join(CUR_PATH, 'PCV_Game/assets/2D_TOPDOWN_PIXELART_CARS.png')
ROAD_SPRITE = os.path.join(CUR_PATH, 'PCV_Game/assets/background-1.png')
def set_orientation(image, angle, center_position):
    # Rotate the original surface
    rotated_image = pygame.transform.rotate(image, angle)
    
    # Generate the new bounding rect and lock the center
    new_rect = rotated_image.get_rect(center=center_position)
    
    return rotated_image, new_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
        crop_area = pygame.Rect(0, 0, 30, 64)
        self.original_image = self.original_image.subsurface(crop_area)
        self.original_image = pygame.transform.scale_by(self.original_image, 3) 

        self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.speed = 5
        self.lean_angle = 20

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        self.velocity_x = 0
        self.velocity_y = 0
        target_angle = 0 
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            target_angle = self.lean_angle  # Lean left
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            target_angle = -self.lean_angle # Lean right

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, target_angle)
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.handle_input()
        self.rect.x += self.velocity_x

import pygame

class Road(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(ROAD_SPRITE).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1.25)
        self.rect = self.image.get_rect()
        
        # Create two road segments to loop seamlessly
        self.rects = [
            pygame.Rect((screen_width-self.rect.width)/2, 0               , self.rect.width, self.rect.height-50),
            pygame.Rect((screen_width-self.rect.width)/2, self.rect.height, self.rect.width, self.rect.height-50),
            pygame.Rect((screen_width-self.rect.width)/2, 2*self.rect.height,self.rect.width, self.rect.height-50)
        ]
        self.speed = 15
        self.screen_height = screen_height

    def update(self):
        for rect in self.rects:
            rect.y += self.speed
            if rect.y >= self.screen_height:
                rect.y = -rect.height

    def draw(self, surface):
        for rect in self.rects:
            surface.blit(self.image, rect)

        
    

        