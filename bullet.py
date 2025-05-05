
import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    #创建子弹对象
    def __init__(self,main_game):
        super(Bullet, self).__init__()
        self.screen=main_game.screen
        self.settings=main_game.settings

        #创建矩形,并将其移动到飞船位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midbottom=main_game.ship.rect.midtop
        self.y=float(self.rect.y)    #浮点数储存当前位置


    def update(self):
        self.y+=-self.settings.bullet_speed
        self.rect.y=self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.settings.bullet_color,self.rect)



