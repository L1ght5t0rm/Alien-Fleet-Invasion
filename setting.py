
import time

#设置选项
class Settings:
    def __init__(self):
        #屏幕设置
        self.screen=(1200,800)
        self.bg_color=(200,200,200)
        self.full_screen=False

        self._init_level()



        #敌人选项
        self.alien_fleet_hieght_new_model=True
        self.fleet_direction=1




    """游戏难度等级控制"""
    def _init_level(self):
        self.level=1
        self.ship_speed=12

        #飞船选项
        self.ship_limit=3

        #子弹选项
        self.bullet_pass=False
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(10,10,10)
        self.bullet_speed=5.0
        self.bullet_allowed=6

        #敌人选项
        self.alien_points=30
        self.alien_fleet_height=2
        self.alien_speed=4
        self.alien_down_speed=14

        self.chek_SuperFire()


    def level_up(self):
        #等级上升
        self.level+=1
        #飞船增强
        if self.level<=10:    self.ship_speed+=2
        elif self.level<=20:    self.ship_speed+=1
        if self.level%10==0:    self.ship_limit+=1

        """子弹增强"""
        self.bullet_allowed+=1    #默认子弹数+1
        #layer1子弹--bullet
        if self.level<=10:
            self.bullet_color=(self.level*20,self.level*20,self.level*20)
        #layer2子弹--wave
        elif self.level==11:
            time.sleep(4)
            #新子弹样式
            self.bullet_color=(220,100,100)
            self.bullet_width=200
            self.bullet_height=5
            #子弹性质
            self.bullet_speed=6
            self.bullet_allowed=4
        elif self.level<=20:
            self.bullet_speed+=1
            self.bullet_width+=20
            if self.level%2:    self.bullet_allowed+=-1    #子弹数每2级+1
        #layer3子弹--laser
        elif self.level==21:
            time.sleep(4)
            #新子弹样式
            self.bullet_color=(150,150,240)
            self.bullet_height=150
            self.bullet_width=15
            #子弹性质
            self.bullet_pass=True
            self.bullet_allowed=4
        elif self.level<30:
            self.bullet_color=(150-self.level*2,150+self.level*2,240+self.level-20)
            self.bullet_height+=20
            self.bullet_width+=2
            self.bullet_speed+=-1
        else:
            self.bullet_color=(0,255,255)


        """敌人增强"""
        self.alien_points=33+self.level
        #舰队数控制
        if self.level<10:    self.alien_fleet_height+=1
        elif self.level%2:    self.alien_fleet_height+=1    #舰队数缓慢增加
        #速度控制
        if self.level<5:    self.alien_down_speed+=3
        elif self.level<8:    self.alien_down_speed+=1
        elif self.level<14:
            self.alien_down_speed+=-2
            self.alien_speed+=1
        #elif self.level<16:    self.alien_speed+=1
        elif self.level==21:
            self.alien_down_speed=30
            self.alien_speed=25
        elif self.level<=30:
            self.alien_speed+=-2
            self.alien_down_speed+=3

        if self.level<=32:    self.alien_speed+=1    #默认移速+1
        else:
            if self.level%4==1:    self.alien_speed+=1

        self.chek_SuperFire()

    def get_level_layer(self):
        if 0<self.level<=10:    return 1
        elif 10<self.level<=20:    return 2
        elif self.level==0:    return 0
        else:    return 3



    """开发控制"""
    def jump_to_level(self,level):
        self._init_level()
        for i in range(level-1):
            self.level_up()

    def chek_SuperFire(self):
        superfire=False
        if superfire:
            self.bullet_width=3000
            self.bullet_height=100
            self.bullet_pass=True
            self.alien_down_speed=80
            self.alien_speed=20


