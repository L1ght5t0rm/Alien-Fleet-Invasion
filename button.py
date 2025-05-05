
import pygame.font

class Button:
    def __init__(self,main_game,msg):
        self.screen=main_game.screen
        self.screen_rect=self.screen.get_rect()

        #按钮样式
        self.width,self.height=200,50
        self.button_color=(0,120,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        #创建对象,居中放置
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        #渲染图像
        self._prep_msg(msg)


    #文本放置
    def _prep_msg(self,msg):
        #(标签,反锯齿,文本色,按钮色)
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center


    #绘制按钮
    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)












