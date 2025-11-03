import pgzrun
# import pygame
import time

alien = Actor('sprite2renewedright1')
alien.topright = 0, 10

WIDTH = 500
HEIGHT = alien.height + 20

def animatespritestepsright():
    if alien.image == 'sprite2renewedright1':
        time.sleep(0.1)
        alien.image = 'sprite2renewedright2'
    elif alien.image == 'sprite2renewedright2':
        time.sleep(0.1)
        alien.image = 'sprite2renewedright1'  
    else:
        time.sleep(0.1)
        alien.image = 'sprite2renewedright1'  

def animatespritestepsleft():
    if alien.image == 'sprite2renewedleft1':
        time.sleep(0.1)
        alien.image = 'sprite2renewedleft2'
    elif alien.image == 'sprite2renewedleft2':
        time.sleep(0.1)
        alien.image = 'sprite2renewedleft1'
    else:
        time.sleep(0.1)
        alien.image = 'sprite2renewedleft1'    

def draw():
    screen.clear()
    screen.fill((80, 0, 80))
    alien.draw()

def update():
    if keyboard.RIGHT:
        alien.left += 3
        animatespritestepsright()
        if alien.left > WIDTH:
            alien.right = 0
    if keyboard.LEFT:
        alien.left -= 3
        animatespritestepsleft()
        if alien.right < 0:
            alien.left = WIDTH

pgzrun.go()