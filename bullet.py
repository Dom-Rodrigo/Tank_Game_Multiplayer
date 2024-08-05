import pygame
from tank import Tank


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.turn = tank.turn
        self.speed = tank.speed * 3
        if self.turn in [0, 4, -4]: #Tank is poiting to the top
            self.rect.center = (tank.rect.x+38, tank.rect.y-20)
        if self.turn in [-2, 2]: #Tank is pointing down
            self.rect.center = (tank.rect.x+38, tank.rect.y+100)

        if self.turn in [-1, 3]: #Tank is poiting to the right
            self.rect.center = (tank.rect.x+85, tank.rect.y+35)

        if self.turn in [1, -3]: #Tank is poiting to the left
            self.rect.center = (tank.rect.x-38, tank.rect.y+35)
        self.tank = tank

        #adjusted to the tip


    def update(self, width, height):
        print(f"Bullet at ({self.rect.x}, {self.rect.y}) moving in direction {self.turn}")
        if self.turn in [0, 4, -4]: #Tank is poiting to the top
            self.rect.y -= self.speed
        if self.turn in [-2, 2]: #Tank is pointing down
            self.rect.y += self.speed
        if self.turn in [-1, 3]: #Tank is poiting to the right
            self.rect.x += self.speed
        if self.turn in [1, -3]: #Tank is poiting to the left
            self.rect.x -= self.speed
        if self.rect.top < 0:
            self.kill()
        if self.rect.top > height:
            self.kill()
        if self.rect.right > width:
            self.kill()
        if self.rect.right < 0:
            self.kill()
