import pygame
import json
import sys
import os
# import time

class SpriteSheet:
    def __init__(self, image_path, json_path):
        self.sheet_of_the_sprites = pygame.image.load(image_path)
        with open(json_path, "r") as f:    
            self.data_of_sprites = json.load(f)

    def get_frame(self, frame_name):
        frame_info = self.data_of_sprites["frames"][frame_name]["frame"]
        x, y, w, h = frame_info["x"], frame_info["y"], frame_info["w"], frame_info["h"]
        
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.blit(self.sheet_of_the_sprites, (0, 0), (x, y, w, h))
        
        return image
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Spritesheet with JSON vb.")
    clock = pygame.time.Clock()

    SPRITESHEET_PATH = "images/sprite 2.png"
    JSON_PATH = "images/sprite 2.json"

    sheet = SpriteSheet(SPRITESHEET_PATH, JSON_PATH)

    frames = [sheet.get_frame("sprite 2 0.aseprite"), sheet.get_frame("sprite 2 1.aseprite")]

    frame_index = 0
    frame_timer = 0
    frame_delay = 100

    posX = 150
    posY = 100

    running = True
    while running:
        dt = clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update animation
        # frame_timer += dt
        # if frame_timer >= frame_delay:
        #     frame_timer = 0
        #     frame_index = (frame_index + 1) % len(frames)

        # Update animation on pressing button
        if keys[pygame.K_RIGHT]:
            posX += 3
            frame_index = (frame_index + 1) % len(frames)
        if keys[pygame.K_LEFT]:
            posX -= 3
            frame_index = (frame_index + 1) % len(frames)

        # Draw
        screen.fill((30, 30, 30))
        screen.blit(frames[frame_index], (posX, posY))
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()