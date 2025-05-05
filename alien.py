
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,main_game):
        super(Alien, self).__init__()
        self.screen=main_game.screen

        #加载图像，获取并储存外接矩形为rect属性
        self.image=pygame.image.load("images/alien.bmp")
        self.rect=self.image.get_rect()

        #设置rect对象属性(外星人默认初始位置)
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x=float(self.rect.x)

        #读取settings设置
        self.settings=main_game.settings

    def update(self):
        self.x+=self.settings.fleet_direction*self.settings.alien_speed
        self.rect.x=self.x

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)




