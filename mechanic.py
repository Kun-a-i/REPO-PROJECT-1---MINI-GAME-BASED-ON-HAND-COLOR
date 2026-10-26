import pygame
import os
import cv2
import random
import threading

CUR_PATH = os.getcwd()
print(CUR_PATH)
PLAYER_SPRITE = os.path.join(CUR_PATH, 'assets/2D_TOPDOWN_PIXELART_CARS.png')
ROAD_SPRITE = os.path.join(CUR_PATH, 'assets/background-1.png')
STEER_SPRITE = os.path.join(CUR_PATH, 'assets/steering-wheel.png')

def set_orientation(image, angle, center_position):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center_position)
    return rotated_image, new_rect

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.original_image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
        self.original_steer = pygame.image.load(STEER_SPRITE).convert_alpha()
        self.original_steer = pygame.transform.scale_by(self.original_steer, 0.4)
        
        steer_crop = pygame.Rect(0, 0, 1280, 640)
        crop_area = pygame.Rect(0, 0, 26, 60)
        self.original_image = self.original_image.subsurface(crop_area)
        
        # Scaling calculation for player
        temp_rect = self.original_image.get_rect()
        target_scale = (15.11111111111111, 4.0625)
        scale = (screen_width / temp_rect.width, screen_height / temp_rect.height)
        final_scale = min(scale[0] / target_scale[0], scale[1] / target_scale[1])
        
        self.original_image = pygame.transform.scale_by(self.original_image, final_scale)
        self.image = self.original_image.copy()
        
        # Initialize steer image copy
        self.steer_image = self.original_steer.copy()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width / 2 + self.rect.width, 
                             screen_height / 2 + self.rect.height)
        
        # Create strict hitbox matching the unrotated image dimensions
        hb_width = int(self.image.get_width() * 0.6)
        hb_height = int(self.image.get_height() * 0.9)
        self.hitbox = pygame.Rect(0, 0, hb_width, hb_height)
        self.hitbox.center = self.rect.center

        self.original_hitbox = self.hitbox.copy()

        self.small_hitbox = pygame.Rect(0, 0, hb_width, 0.45*hb_height)
        self.small_hitbox.center = self.rect.center

        self.speed = 5
        self.lean_angle = 20
        self.velocity_x = 0
        self.is_hit = False
        self.hit_timer = 0

    def draw(self, surface):
        # Draw player car
        surface.blit(self.image, self.rect)
        
        # Debug hitbox
        # pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 2)

    def draw_steer(self, surface):
        # Draw steering wheel centered at (320, 480)
        cam_rect = pygame.Rect(0, 0, 640, 480)
        surface.set_clip(cam_rect)
        steer_rect = self.steer_image.get_rect(center=(320, 380))
        surface.blit(self.steer_image, steer_rect)
        surface.set_clip(None)

    def handle_input(self, steer):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        target_angle = 0 
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or steer == -1:
            self.velocity_x = -self.speed
            target_angle = self.lean_angle
            self.hitbox = self.small_hitbox
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or steer == 1:
            self.velocity_x = self.speed
            target_angle = -self.lean_angle
            self.hitbox = self.small_hitbox
        else :
            self.hitbox = self.original_hitbox

        if self.is_hit:
            red_image = self.original_image.copy()
            red_image.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.image = pygame.transform.rotate(red_image, target_angle)
            self.steer_image = pygame.transform.rotate(self.original_steer, target_angle)

            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False
        else:
            self.image = pygame.transform.rotate(self.original_image, target_angle)
            self.steer_image = pygame.transform.rotate(self.original_steer, target_angle)
            
        # Keep the visual rect cleanly centered on the hitbox
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self, steer):
        self.handle_input(steer)
        self.hitbox.x += self.velocity_x
        self.original_hitbox.center = self.hitbox.center
        self.small_hitbox.center = self.hitbox.center
        self.rect.center = self.hitbox.center


class Road(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(ROAD_SPRITE).convert_alpha()
        self.rect = self.image.get_rect()
        
        target_scale = (1.1428571428571428, 0.8307692307692308) 
        scale = (screen_width/self.rect.width, screen_height/self.rect.height)
        final_scale = min(scale[0]/target_scale[0], scale[1]/target_scale[1])
        self.image = pygame.transform.scale_by(self.image, final_scale)
        self.rect = self.image.get_rect()
        self.rects = [
            pygame.Rect((screen_width - self.rect.width) / 2, 0, self.rect.width, self.rect.height),
            pygame.Rect((screen_width - self.rect.width) / 2, self.rect.height, self.rect.width, self.rect.height),
            pygame.Rect((screen_width - self.rect.width) / 2, 2 * self.rect.height, self.rect.width, self.rect.height)
        ]
        self.speed = 25
        self.screen_height = screen_height

    def update(self):
        for rect in self.rects:
            rect.y += self.speed
            if rect.y >= self.screen_height:
                rect.y = -self.rect.height + 100

    def draw(self, surface):
        for rect in self.rects:
            surface.blit(self.image, rect)


class NPC(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
        crop_area = pygame.Rect(0, 0, 26, 64)
        ex_image = self.image.subsurface(crop_area)
        self.rect = ex_image.get_rect()

        self.screen_height = screen_height
        self.screen_width = screen_width
        
        target_scale=(15.11111111111111, 4.0625)
        scale = (screen_width/self.rect.width, screen_height/self.rect.height)
        self.final_scale = min(scale[0]/target_scale[0], scale[1]/target_scale[1])
        self.npcs = []
        sprite_width = 120
        
        # Fixed syntax error and multiplier formatting
        self.lanes = [i * sprite_width + 0.175 * screen_width for i in range(int(0.65*screen_width/sprite_width))]
        self.available_lanes = []
        
        # Define vertical offsets pool for spawning staggered above screen
        self.cols = [-700*(i + 1) for i in range(5)]
        self.available_cols = []

        self.speed = 20
        
        for _ in range(4):
            crop_area = pygame.Rect(0, random.randint(0, 3)*92, 26, 70)
            image = self.image.subsurface(crop_area)
            image = pygame.transform.scale_by(image, self.final_scale)

            
            rect = image.get_rect()
            rect.x = self.get_safe_lane()  # Now uses unique lane pooling!
            rect.y = self.get_next_cols()
            
            if rect.x <= (self.screen_width/2 - self.rect.width):
                    image = pygame.transform.rotate(image, 180)
                    speed = 2*self.speed + 10
            else :
                speed = self.speed
            
            self.npcs.append({"image": image, "rect": rect, "speed":speed})

    def get_next_cols(self):
        if not self.available_cols:
            self.available_cols = self.cols.copy()
            random.shuffle(self.available_cols)
        return self.available_cols.pop(0)
    
    def get_safe_lane(self):
        # Check where existing NPCs are parked/driving
        occupied_lanes = [npc["rect"].x for npc in self.npcs]
        free_lanes = [lane for lane in self.lanes if lane not in occupied_lanes]
        
        if not free_lanes:
            return random.choice(self.lanes)
        return random.choice(free_lanes)
    
    def update(self):
        for npc in self.npcs:
            npc["rect"].y += npc["speed"]
            
            # If it goes off the bottom, reset it to the top using pools
            if npc["rect"].y >= self.screen_height:
                crop_area = pygame.Rect(0, random.randint(0, 3)*92, 26, 70)
                npc["image"] = pygame.transform.scale_by(self.image.subsurface(crop_area), self.final_scale)
                
                npc["rect"].y = self.get_next_cols()
                npc["rect"].x = self.get_safe_lane()  # Prevents horizontal overlap
                if npc["rect"].x <= (self.screen_width/2 - npc["rect"].width):
                    npc["image"] = pygame.transform.rotate(npc["image"], 180)
                    npc["speed"] = 2*self.speed + 10
                else :
                    npc["speed"] = self.speed
        

    def draw(self, surface):
        for npc in self.npcs:
            surface.blit(npc["image"], npc["rect"])

    def check_hit(self, player):
        for npc in self.npcs:
            # colliderect automatically checks all 4 sides (X and Y overlap)
            if player.hitbox.colliderect(npc["rect"]):
                player.is_hit = True
                player.hit_timer = 1
                return 'hit'