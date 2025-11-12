import pygame
import json
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
    pygame.mixer.init()

    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Spritesheet with JSON (SUCCES)")
    clock = pygame.time.Clock()
    
    backgroundImage = pygame.image.load("images/background_first_try.png")
    backgroundAddition = pygame.image.load("images/background_addition.png")
    shrubberyImage = pygame.image.load("images/shrubbery.png")
    stoneImage = pygame.image.load("images/stone.png")

    music8bit = pygame.mixer.Sound("sound/arcade_heroes.ogg")
    laserSound = pygame.mixer.Sound("sound/laser_soundeffect.mp3")

    music8bit.play(loops=-1)

    SPRITESHEET_PATH = "images/sprite 2.png"
    JSON_PATH = "images/sprite 2.json"

    LASERSPRITESHEET = "images/laser.png"
    LASERSPRITEJSON = "images/laser.json"

    sheet = SpriteSheet(SPRITESHEET_PATH, JSON_PATH)

    framesRight = [sheet.get_frame("sprite 2 0.aseprite"), sheet.get_frame("sprite 2 1.aseprite")]
    framesLeft = [pygame.transform.flip(framesRight[0], True, False), pygame.transform.flip(framesRight[1], True, False)]
    
    framesJumpRight = [sheet.get_frame("sprite 2 2.aseprite"), sheet.get_frame("sprite 2 3.aseprite"), sheet.get_frame("sprite 2 4.aseprite")]
    framesJumpLeft = [pygame.transform.flip(framesJumpRight[0], True, False), pygame.transform.flip(framesJumpRight[1], True, False), pygame.transform.flip(framesJumpRight[2], True, False)]

    laser = SpriteSheet(LASERSPRITESHEET, LASERSPRITEJSON)

    laserFramesRight = [laser.get_frame("laser 0.aseprite"), laser.get_frame("laser 1.aseprite"), laser.get_frame("laser 2.aseprite")]
    laserFramesLeft = [pygame.transform.flip(laserFramesRight[0], True, False), pygame.transform.flip(laserFramesRight[1], True, False), pygame.transform.flip(laserFramesRight[2], True, False)]

    frame_index = 0

    direction = "right"
    jump = "none"
    fired = "none"
    laserDirection = "none"

    backgroundAnchorX = 0

    posX = 150
    posY = 450

    laserX = 0
    laserY = 0

    running = True
    while running:
        dt = clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                button = event.button

        keys = pygame.key.get_pressed()
        mouseButtons = pygame.mouse.get_pressed()

        # Draw already starts here:
        screen.blit(backgroundImage, (backgroundAnchorX, 0))
        screen.blit(backgroundAddition, (backgroundAnchorX + 704, 0))
        

        # Update animation on pressing button, and blitting left or right
        # Deze afwisseling naar rechts ken ik goed, niet per sé comments nodig.
        if keys[pygame.K_d]:
            if posX < 450:
                posX += 4
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif posX >= 450 and backgroundAnchorX > -704:
                backgroundAnchorX -= 4
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif backgroundAnchorX <= -704 and posX < 685:
                posX += 4
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif posX >= 685:
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"

        # Deze afwisseling naar links is moeizamer.
        if keys[pygame.K_a]:
            # comments toevoegen aub, per stukje
            if backgroundAnchorX >= 0 and posX >= 0:
                posX -= 4
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif backgroundAnchorX >= -704 and posX > 300:
                posX -= 4
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif backgroundAnchorX <= 0 and posX <= 300:
                backgroundAnchorX += 4
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif backgroundAnchorX >= 0 and posX >= 0:
                posX -= 4
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif backgroundAnchorX >= 0 and posX <= 0:
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            

            # if posX > 0 and backgroundAnchorX < 0:
            #     backgroundAnchorX += 4
            #     frame_index = (frame_index + 1) % len(framesLeft)
            #     direction = "left"
            # elif posX > 450 and backgroundAnchorX >= 0:
            #     backgroundAnchorX -= 4
            #     frame_index = (frame_index + 1) % len(framesLeft)
            #     direction = "left"
            # elif posX >= 450 and backgroundAnchorX >= 0:
            #     posX -= 4                
            #     frame_index = (frame_index + 1) % len(framesLeft)
            #     direction = "left"
            # elif posX > 0 and posX <= 450:
            #     posX -= 4
            #     frame_index = (frame_index + 1) % len(framesLeft)
            #     direction = "left"

        if keys[pygame.K_w]:
            if posY >= 400:
                posY -= 4
        if keys[pygame.K_s]:
            if posY <= 489:
                posY += 4

        if keys[pygame.K_SPACE]:
            jump = "begin_1"

        if direction == "right":
            if jump == "none":
                screen.blit(framesRight[frame_index], (posX, posY))
            elif jump == "begin_1":
                screen.blit(framesJumpRight[0], (posX, posY))
                jump = "begin_2"
            elif jump == "begin_2":
                posY -= 10
                screen.blit(framesJumpRight[1], (posX, posY))
                jump = "begin_3"
            elif jump == "begin_3":
                posY -= 20
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_4"
            elif jump == "begin_4":
                posY -= 10
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_5"
            elif jump == "begin_5":
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_6"
            elif jump == "begin_6":
                posY += 10
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_7"
            elif jump == "begin_7":
                posY += 20
                screen.blit(framesJumpRight[1], (posX, posY))
                jump = "begin_8"
            elif jump == "begin_8":
                posY += 10
                screen.blit(framesJumpRight[0], (posX, posY))
                jump = "none"

        elif direction == "left":
            if jump == "none":
                screen.blit(framesLeft[frame_index], (posX, posY))
            elif jump == "begin_1":
                screen.blit(framesJumpLeft[0], (posX, posY))
                jump = "begin_2"
            elif jump == "begin_2":
                posY -= 10
                screen.blit(framesJumpLeft[1], (posX, posY))
                jump = "begin_3"
            elif jump == "begin_3":
                posY -= 20
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_4"
            elif jump == "begin_4":
                posY -= 10
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_5"
            elif jump == "begin_5":
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_6"
            elif jump == "begin_6":
                posY += 10
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_7"
            elif jump == "begin_7":
                posY += 20
                screen.blit(framesJumpLeft[1], (posX, posY))
                jump = "begin_8"
            elif jump == "begin_8":
                posY += 10
                screen.blit(framesJumpLeft[0], (posX, posY))
                jump = "none"
        else:
            print("something went wrong tracking direction")

        if mouseButtons[0] == True:
            if fired == "none" and direction == "right":
                laserX = posX + 50
                laserY = posY + 28
                screen.blit(laserFramesRight[0], (laserX, laserY))
                fired = "started"
                laserDirection = "right"
                laserSound.play(loops=0)
                
            elif fired == "none" and direction == "left":
                laserX = posX + 40
                laserY = posY + 28
                screen.blit(laserFramesLeft[0], (laserX, laserY))
                fired = "started"
                laserDirection = "left"
                laserSound.play(loops=0)

        if fired != "none" and laserDirection == "right":
            if fired == "started":
                laserX += 3
                screen.blit(laserFramesRight[1], (laserX, laserY))
                fired = "halfway"
            elif fired == "halfway":
                laserX += 9
                screen.blit(laserFramesRight[2], (laserX, laserY))
                fired = "full"
            elif fired == "full":
                laserX += 9
                screen.blit(laserFramesRight[2], (laserX, laserY))
                if laserX > screen.get_width():
                    fired = "none"
        elif fired != "none" and laserDirection == "left":
            if fired == "started":
                laserX -= 3
                screen.blit(laserFramesRight[1], (laserX, laserY))
                fired = "halfway"
            elif fired == "halfway":
                laserX -= 9
                screen.blit(laserFramesRight[2], (laserX, laserY))
                fired = "full"
            elif fired == "full":
                laserX -= 9
                screen.blit(laserFramesRight[2], (laserX, laserY))
                if laserX < -5:
                    fired = "none"  
        
        screen.blit(shrubberyImage, (backgroundAnchorX + 335, 455))
        screen.blit(stoneImage, (backgroundAnchorX + 650, 520))

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()