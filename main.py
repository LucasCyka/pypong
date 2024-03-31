"""
    Simple pong game with pygame.

"""

import math
import pygame as py
import os


class Vector2D():
    x = 0
    y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __add__(v1,v2):
        return Vector2D(v1.x + v2.x, v1.y + v2.y)

    def __sub__(v1,v2):
        return Vector2D(v1.x - v2.x, v1.y - v2.y)

    def __mul__(v1,v2):
        return Vector2D(v1.x * v2,v1.y * v2)

    def normalized(self):
        mag = math.sqrt(self.x**2 + self.y**2)
        return Vector2D(self.x/mag,self.y/mag)
    
    def get(self):
        return (self.x,self.y)


class Player(py.sprite.Sprite):
    position = Vector2D(0,0)
    velocity = Vector2D(0,0)
    _SPEED = 4
    _PAD_SIZE = Vector2D(30,100)

    def __init__(self,position):
        py.sprite.Sprite.__init__(self)
        self.position = position
        self.image = load_image("pad.png")
        self.rect = self.image.get_rect()

        self.rect.top = position.y
        self.rect.right = position.x

    def update(self):
        self.rect.move_ip(self.velocity.x,self.velocity.y)

        self.velocity = Vector2D(0,0)
        self.position.x = self.rect.right 
        self.position.y = self.rect.top 

    def move(self,dir):
        _newDir = dir

        _newDir.y = int(not(self.position.y > screenSize.y - self._PAD_SIZE.y and _newDir.y >= 1)) * _newDir.y
        _newDir.y = int(not(self.position.y < 0 and _newDir.y <= 0)) * _newDir.y

        self.velocity = _newDir * self._SPEED

class Ball(py.sprite.Sprite):
    position = Vector2D(0,0)
    velocity = Vector2D(1,0)
    padLastCollision = ""
    _speed = 2.0
    _colliders = []

    def __init__(self,position, colliders = []):
        py.sprite.Sprite.__init__(self)
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.position = position

        self.rect.right = position.x
        self.rect.top = position.y
        self._colliders = colliders

        
    def update(self):
        self.rect.move_ip(self.velocity.x * self._speed,self.velocity.y * self._speed)

        self.position.x = self.rect.right
        self.position.y = self.rect.top

        self.detect_collisions()

    def detect_collisions(self):
        for collider in self._colliders:
            if self.rect.colliderect(collider.rect) and self.padLastCollision != collider:
                self._change_velocity(collider)
                break

    def _change_velocity(self,pad):
        if isinstance(pad,Wall):
            self.velocity.y *= -1
            self._speed =  max(min(self._speed+0.5,10),0)
            return

        self.padLastCollision = pad

        _dirY =  (pad.position.y+50) - (self.position.y+8)
        #print(pad.position.y+50)
        #print(self.position.y+16)

        _dirY = _dirY / 50 #normalization
        
        _dirY = _dirY * math.radians(55) #maximum angle
        

        self.velocity.x *= -1
        self.velocity.y = -math.sin(_dirY)

        self._speed =  max(min(self._speed+0.5,10),0)

class Wall(py.sprite.Sprite):

    position = Vector2D(0,0)

    def __init__(self,img,position):
        py.sprite.Sprite.__init__(self)
        self.image = load_image(img)
        self.rect = self.image.get_rect()
        self.position = position

        self.rect.left = self.position.x
        self.rect.top = self.position.y

    def update(self):
        pass


mainDir = "assets/"
screenSize = Vector2D(800,600)
screenSurface = None
running = True
backgroundColor = "black"

def load_image(name):
    img = py.image.load(os.path.join(mainDir,name))
    img = img.convert_alpha()

    return img


def init_screen():
    global screenSurface
    py.init()
    screenSurface = py.display.set_mode(screenSize.get())
    py.display.set_caption("PONG")

def main():
    init_screen()
    global running
    global screenSurface
    wall1 = Wall("wall.png",Vector2D(100,0))
    wall2 = Wall("wall.png",Vector2D(100,590))
    player1 = Player(Vector2D(30+100,(screenSize.y/2)-50))
    player2 = Player(Vector2D(screenSize.x-100,(screenSize.y/2)-50))
    ball = Ball(Vector2D(screenSize.x/2+8,screenSize.y/2-8),[player1,player2,wall1,wall2])
    sprites = py.sprite.RenderPlain([player1,player2,ball,wall1,wall2])
    clock = py.time.Clock()

    while running:
        clock.tick(60)

        for sprite in sprites:
            sprite.update()

        #events
        for event in py.event.get():
            if event.type == py.QUIT: 
                running = False
                return

        #player movement
        keys = py.key.get_pressed()
        up = keys[py.K_UP]
        down = keys[py.K_DOWN]
        w = keys[py.K_w]
        s = keys[py.K_s]

        if up or down and not (up and down):
            if up: player1.move(Vector2D(0,-1))
            else: player1.move(Vector2D(0,1))

        if w or s and not (w and s):
            if w: player2.move(Vector2D(0,-1))
            else: player2.move(Vector2D(0,1))
        
        screenSurface.fill(backgroundColor)
        sprites.draw(screenSurface)
        py.display.flip()




if __name__ == "__main__":
    main()