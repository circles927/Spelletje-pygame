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

    
    screen = pygame.display.set_mode((1024, 1024))
    pygame.display.set_caption("Adjusted Game (diff graphics)")
    clock = pygame.time.Clock()
    

    backgroundImage = pygame.image.load("images/new graphics/plain-background-new(for_adding).png")
    # backgroundAddition = pygame.image.load("images/background_addition.png")
    treeNrOneImage = pygame.image.load("images/new graphics/tree-1-new.png")
    treeNrTwoImage = pygame.image.load("images/new graphics/tree-2-new.png")
    shrubberyImage = pygame.image.load("images/new graphics/shrubbery-new.png")
    stoneImage = pygame.image.load("images/new graphics/stone-new.png")

    music8bit = pygame.mixer.Sound("sound/arcade_heroes.ogg")
    laserSound = pygame.mixer.Sound("sound/laser_soundeffect.mp3")

    music8bit.play(loops=-1)

    SPRITESHEET_PATH = "images/new graphics/sprite 2-new.png"
    JSON_PATH = "images/new graphics/sprite 2-new.json"

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
    elevation = "none"
    jump = "none"
    fired = "none"
    laserDirection = "none"
    slowmo = False
    obstructed = False

    backgroundAnchorX = 0

    posX = 150
    posY = 700

    laserX = 0
    laserY = 0

    running = True

    treeOneLoc = [330, 100]
    shrubbLoc = [1060, 480]
    stoneLoc = [1800, 700]
    treeTwoLoc = [2700, 420]

    # Testing collision on stone sprite:

    while running:
        dt = clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                button = event.button

        originalCoordinates = (posX, posY)

        keys = pygame.key.get_pressed()
        mouseButtons = pygame.mouse.get_pressed()

        # Maar 1 achtergrond op dit moment:
        screen.blit(backgroundImage, (backgroundAnchorX, 0))
        # screen.blit(backgroundAddition, (backgroundAnchorX + 704, 0))

        # Update animation on pressing button, and blitting left or right
        # Bewegen naar rechts:         
        if keys[pygame.K_d]:
            if posX < 580:
                posX += 12
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif posX >= 580 and backgroundAnchorX >= -3060:
                backgroundAnchorX -= 12
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif posX <= 790 and backgroundAnchorX <= -3060:
                posX += 12
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"
            elif posX >= 790:
                frame_index = (frame_index + 1) % len(framesRight)
                direction = "right"

        if keys[pygame.K_a]:
            if posX >= 320 and backgroundAnchorX <= 0:    
                posX -= 12
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif posX < 320 and backgroundAnchorX < 0:
                backgroundAnchorX += 12
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif posX >= -24 and backgroundAnchorX >= 0:
                posX -= 12
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
            elif posX < -24:
                frame_index = (frame_index + 1) % len(framesLeft)
                direction = "left"
                
        # -----------------------------------------
        # if keys[pygame.K_d]:
        #     if posX < 450:
        #         posX += 4
        #         frame_index = (frame_index + 1) % len(framesRight)
        #         direction = "right"
        #     elif posX >= 450 and backgroundAnchorX > -704:
        #         backgroundAnchorX -= 4
        #         frame_index = (frame_index + 1) % len(framesRight)
        #         direction = "right"
        #     elif backgroundAnchorX <= -704 and posX < 685:
        #         posX += 4source venv/bin/activate
        #         frame_index = (frame_index + 1) % len(framesRight)
        #         direction = "right"
        #     elif posX >= 685:
        #         frame_index = (frame_index + 1) % len(framesRight)
        #         direction = "right"
        # -----------------------------------------

        # Deze afwisseling naar links is moeizamer.
        # Bewegen naar links:



        # -----------------------------------------
        # if keys[pygame.K_a]:
        #     # Vanaf het midden, achtergrond naar rechts, tenzij achtergrond het verst naar rechts staat.
        #     if posX <= 275 and backgroundAnchorX <= -4:
        #         backgroundAnchorX += 4
        #         frame_index = (frame_index + 1) % len(framesLeft)
        #         direction = "left"
        #     # Als achtergrond verst rechts is, dus de meest linker rand, dan moet de Sprite het laatste deel zelf lopen, vanaf het midden naar de meest linker rand 
        #     elif (posX <= 275 and posX >= 0) and backgroundAnchorX > -4:
        #         posX -= 4
        #         frame_index = (frame_index + 1) % len(framesLeft)
        #         direction = "left"
        #     # Als sprite voorbij het midden is (mag ie niet voorbij de 800, want dat betekent dat ie van het scherm loopt als de meest rechter rand in beeld is geschoven), moet ie eerst een stuk naar links lopen, voordat ie stopt en de achtergrond weer naar rechts gaat.
        #     elif (posX > 275 and posX < 800):
        #         posX -= 4
        #         frame_index = (frame_index + 1) % len(framesLeft)
        #         direction = "left"
        # ------------------------------------------

        if keys[pygame.K_w]:
            if posY >= 425:
                posY -= 12
                elevation = "up"
        if keys[pygame.K_s]:
            if posY <= 785:
                posY += 12
                elevation = "down"

        if keys[pygame.K_SPACE]:
            jump = "begin_1"

        if direction == "right":
            if jump == "none":
                screen.blit(framesRight[frame_index], (posX, posY))
            elif jump == "begin_1":
                screen.blit(framesJumpRight[0], (posX, posY))
                jump = "begin_2"
            if fired == "none" and direction == "right":
                laserX = posX + 145
            elif jump == "begin_2":
                posY -= 20
                screen.blit(framesJumpRight[1], (posX, posY))
                jump = "begin_3"
            elif jump == "begin_3":
                posY -= 40
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_4"
            elif jump == "begin_4":
                posY -= 20
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_5"
            elif jump == "begin_5":
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_6"
            elif jump == "begin_6":
                posY += 20
                screen.blit(framesJumpRight[2], (posX, posY))
                jump = "begin_7"
            elif jump == "begin_7":
                posY += 40
                screen.blit(framesJumpRight[1], (posX, posY))
                jump = "begin_8"
            elif jump == "begin_8":
                posY += 20
                screen.blit(framesJumpRight[0], (posX, posY))
                jump = "none"

        elif direction == "left":
            if jump == "none":
                screen.blit(framesLeft[frame_index], (posX, posY))
            elif jump == "begin_1":
                screen.blit(framesJumpLeft[0], (posX, posY))
                jump = "begin_2"
            elif jump == "begin_2":
                posY -= 20
                screen.blit(framesJumpLeft[1], (posX, posY))
                jump = "begin_3"
            elif jump == "begin_3":
                posY -= 40
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_4"
            elif jump == "begin_4":
                posY -= 20
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_5"
            elif jump == "begin_5":
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_6"
            elif jump == "begin_6":
                posY += 20
                screen.blit(framesJumpLeft[2], (posX, posY))
                jump = "begin_7"
            elif jump == "begin_7":
                posY += 40
                screen.blit(framesJumpLeft[1], (posX, posY))
                jump = "begin_8"
            elif jump == "begin_8":
                posY += 20
                screen.blit(framesJumpLeft[0], (posX, posY))
                jump = "none"
        else:
            print("something went wrong tracking direction")

        if mouseButtons[0] == True:
            if fired == "none" and direction == "right":
                laserX = posX + 145
                laserY = posY + 70
                screen.blit(laserFramesRight[0], (laserX, laserY))
                fired = "started"
                laserDirection = "right"
                laserSound.play(loops=0)
                
            elif fired == "none" and direction == "left":
                laserX = posX + 70
                laserY = posY + 70
                screen.blit(laserFramesLeft[0], (laserX, laserY))
                fired = "started"
                laserDirection = "left"
                laserSound.play(loops=0)

        if fired != "none" and laserDirection == "right":
            if fired == "started":
                laserX += 6
                screen.blit(laserFramesRight[1], (laserX, laserY))
                fired = "halfway"
            elif fired == "halfway":
                laserX += 18
                screen.blit(laserFramesRight[2], (laserX, laserY))
                fired = "full"
            elif fired == "full":
                laserX += 18
                screen.blit(laserFramesRight[2], (laserX, laserY))
                if laserX > screen.get_width():
                    fired = "none"
        elif fired != "none" and laserDirection == "left":
            if fired == "started":
                laserX -= 6
                screen.blit(laserFramesRight[1], (laserX, laserY))
                fired = "halfway"
            elif fired == "halfway":
                laserX -= 18
                screen.blit(laserFramesRight[2], (laserX, laserY))
                fired = "full"
            elif fired == "full":
                laserX -= 18
                screen.blit(laserFramesRight[2], (laserX, laserY))
                if laserX < -5:
                    fired = "none"  

        # unnecessary for now
        screen.blit(treeNrOneImage, (backgroundAnchorX + 330, 100))
        screen.blit(shrubberyImage, (backgroundAnchorX + 1060, 480))
        screen.blit(stoneImage, (backgroundAnchorX + 1800, 700))
        screen.blit(treeNrTwoImage, (backgroundAnchorX + 2700, 420))

        # alienRect = pygame.Rect(posX + 40, posY + 80, 60, 28)
        # stoneRect = pygame.Rect(stoneLoc[0] + backgroundAnchorX + 46, stoneLoc[1] + 36, 128, 87)

        alienRect = pygame.Rect(posX + 80, posY + 168, 119, 47)
        stoneRect = pygame.Rect(stoneLoc[0] + backgroundAnchorX + 46, stoneLoc[1] + 36, 128, 87)

        if alienRect.colliderect(stoneRect):
            obstructed = True
        elif not alienRect.colliderect(stoneRect):
            obstructed = False
        else:
            print("something went wrong with collision detection")

        if obstructed == True:
            posX = originalCoordinates[0]
            posY = originalCoordinates[1]
        elif obstructed == False:
            pass

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()