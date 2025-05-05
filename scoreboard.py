
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Sorceboard:
    #初始化
    def __init__(self,main_game):
        #显示得分需要用的属性
        self.main_game=main_game
        self.screen=main_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=main_game.settings
        self.stats=main_game.stats

        #初始化字体属性
        self.text_color=(20,20,20)
        self.font=pygame.font.SysFont(None,48)

        #初始化得分图像
        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()

    #初始化图像
    def prep_score(self):
        score_str=f"{self.stats.score:,}"
        self.score_imgae=self.font.render(score_str,True,self.text_color,None)

        self.score_rect=self.score_imgae.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def prep_highest_score(self):
        highest_socre_str=f"{self.stats.highest_score:,}"
        self.highest_score_image=self.font.render(highest_socre_str,True,self.text_color,None)

        self.highest_score_rect=self.highest_score_image.get_rect()
        self.highest_score_rect.centerx=self.screen_rect.centerx
        self.highest_score_rect.top=self.score_rect.top-10    #保持与计分板同一水平高度

    def prep_level(self):
        level_str=f"level.{self.settings.level}"
        self.level_image=self.font.render(level_str,True,self.text_color,None)

        self.level_rect=self.level_image.get_rect()
        self.level_rect.left=self.screen_rect.left+20
        self.level_rect.top=self.score_rect.top

    def prep_ships(self):
        self.ships=Group()
        for ship_number in range(self.main_game.settings.ship_limit):
            ship=Ship(self.main_game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10+self.score_rect.bottom
            self.ships.add(ship)



    #显示得分
    def show_score(self):
        self.screen.blit(self.score_imgae,self.score_rect)
        self.screen.blit(self.highest_score_image,self.highest_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)


    #检查最高分
    def 检查最高分(self):
        if self.stats.score>self.stats.highest_score:
            self.stats.highest_score=self.stats.score
            with open("record.txt", "w", encoding='utf-8') as f:
                f.write(str(self.stats.highest_score))
            self.prep_highest_score()



