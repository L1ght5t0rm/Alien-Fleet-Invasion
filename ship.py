
import pygame
from pygame.sprite import Sprite

#飞船
class Ship(Sprite):
    #传入Alien_Invasion实例引用用于访问
    def __init__(self,main_game):
        super(Ship, self).__init__()
        self.screen=main_game.screen
        self.screen_rect=main_game.screen.get_rect()

        #加载图像，获取并储存外接矩形为rect属性
        self.image=pygame.image.load("images/ship.bmp")
        self.rect=self.image.get_rect()

        #设置rect对象属性(飞船默认初始位置)
        """
        center,centerx,centery
        midbottom,midtop,midright
        """
        self.rect.midbottom=(self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 20)
        self.settings=main_game.settings    #获取游戏主实例setting属性并储存为自身setting属性
        self.x=float(self.rect.x)
        self.width=self.rect.width

        #设置移动属性
        self.moving_right=False
        self.moving_left=False



    #调用时使所指飞船绘图显示
    def blitme(self):
        self.screen.blit(self.image,self.rect)


    #飞船移动
    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:    self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.right>self.width:    self.x+=-self.settings.ship_speed
        self.rect.x=self.x


    #飞船中置
    def 飞船中置(self):
        self.rect.midbottom=(self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 20)
        self.x=float(self.rect.x)


