
import sys,os,time,pygame

from game_stats import GameStats
from setting import Settings
from button import Button
from scoreboard import Sorceboard
from sound import Audio
from ship import Ship
from bullet import Bullet
from alien import Alien

os.chdir( os.path.dirname(os.path.abspath(__file__)) )
os.system('cls' if os.name == 'nt' else 'clear')

#    pyinstaller --windowed --icon=Alien_Fleet_Invasion.ico --add-data="images;images" --add-data="sounds;sounds" Alien_Fleet_Invasion.py


"""日志系统"""
if os.path.exists("print_log"):
    print_log=True
else:
    print_log=False

#初始化日志
if print_log:
    global game_log,load_time
    game_log=[]
    load_time=str( time.strftime("%y%m%d_%H%M%S",time.localtime()) )
    os.makedirs("log", exist_ok=True)
    with open(f"log/{load_time}.txt","w",encoding="utf-8") as f:    pass

#日志打印
def print_in(log_str):
    if not print_log:
        print(log_str)
    else:
        log_str+="\n"
        game_log.append(log_str)
        if len(game_log)>=100:
            flush_logs()

#刷新缓存
def flush_logs():
    with open(f"log/{load_time}.txt","a",encoding="utf-8") as f:
        f.write("".join(game_log))
    game_log.clear()

#退出逻辑
def exit_game():
    if print_log:    flush_logs()
    sys.exit()



#主程序运行
class AlienInvasion:
    #初始化游戏
    def __init__(self):
        pygame.init() #初始化
        self.clock=pygame.time.Clock() #设置时钟
        self.settings=Settings() #设置设置

        #窗口设置
        if not self.settings.full_screen:
            self.screen=pygame.display.set_mode(self.settings.screen) #创建窗口
            self.settings.screen_width=self.screen.get_rect().width
            self.settings.screen_height=self.screen.get_rect().height
        else:
            self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN) #创建窗口
            self.settings.screen_width=self.screen.get_rect().width
            self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Fleet Invasion") #设置标题

        #初始化模块对象
        self.stats=GameStats(self)
        self.score_board=Sorceboard(self)
        self.play_button=Button(self,"Play")
        self.sounds=Audio()
        self.game_active=False
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        #初始化游戏
        self._创建舰队()



    #用于事件主循环
    def run_game(self):
        self.start_time=time.time()
        print_in(f"[{self.start_time}] 杂鱼进入了游戏")
        while True:
            self._检查事件()
            if self.game_active:
                self._子弹移动() #移动和出界处理
                self._更新外星人位置() #外星人移动和转向
                self.ship.update() #飞船移动
            self._更新屏幕() #按顺序绘图



    """事件控制"""
    def _检查事件(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                print_in(self.获取运行时间()+f" 呐,游戏结束了,杂鱼~")
                exit_game()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                self._check_play_button(pygame.mouse.get_pos())    #按下开始按钮检测
            elif event.type==pygame.KEYDOWN:    self._按下按键(event)
            elif event.type==pygame.KEYUP:    self._松开按键(event)

    def _按下按键(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
            print_in(self.获取运行时间()+"     杂鱼 正在右移...")
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
            print_in(self.获取运行时间()+"     杂鱼 正在左移...")
        elif event.key==pygame.K_q:
            print_in(self.获取运行时间()+" 嘿嘿,杂鱼退出了游戏")
            exit_game()
        elif event.key==pygame.K_SPACE:
            self._开火()    #开火

    def _松开按键(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
            print_in(self.获取运行时间()+"     杂鱼 停止右移...")
        if event.key==pygame.K_LEFT:
            self.ship.moving_left=False
            print_in(self.获取运行时间()+"     杂鱼 停止左移...")

    #游戏激活: 按下开始按钮(重置并激活游戏)
    def _check_play_button(self,mouse_pos):
        if not self.game_active and self.play_button.rect.collidepoint(mouse_pos):
            #重置状态
            self.stats._init_stats()
            self.settings._init_level()
            #self.settings.jump_to_level(36);    self.score_board.prep_level()    #跳级
            self.score_board.prep_score()
            self.score_board.prep_ships()
            self.sounds.replay_bgsounds()
            self.sounds.play_sound("boom")
            #清空对象
            self.bullets.empty()
            self.aliens.empty()
            #重新初始化
            self._创建舰队()
            self.ship.飞船中置()
            print_in(f"[{self.start_time}] 杂鱼开始了游戏")
            pygame.mouse.set_visible(False)
            self.game_active=True



    def _更新屏幕(self):
        self.screen.fill(self.settings.bg_color)
        self.aliens.draw(self.screen) #遍历外星人列表,绘制其图像到屏幕上
        for bullet in self.bullets.sprites():
            #绘制飞船前绘制子弹，保证子弹位于飞船下方
            bullet.draw_bullet()
        self.ship.blitme()

        if not self.game_active:    self.play_button.draw_button()
        else:    self.score_board.show_score()
        pygame.display.flip() #显示新屏幕
        self.clock.tick(60) #帧率控制



    """子弹代码"""
    def _开火(self):
        if len(self.bullets)<self.settings.bullet_allowed:
            if self.settings.get_level_layer()==1:    print_in(self.获取运行时间()+"     开火了！好小哦~")
            elif self.settings.get_level_layer()==2:    print_in(self.获取运行时间()+"     唔...开火了!")
            elif self.settings.get_level_layer()==3:    print_in(self.获取运行时间()+"     啊哈❤ ,开火！")
            self.bullets.add(Bullet(self))
            if self.settings.get_level_layer()==1:    self.sounds.play_sound("shoot_bullet")
            elif self.settings.get_level_layer()==2:    self.sounds.play_sound("shoot_wave")
            else:    self.sounds.play_sound("shoot_laser")
            
        else:
            print_in(self.获取运行时间()+"     杂鱼~❤ 杂鱼~ 射不出的杂鱼~")

    def _子弹移动(self):
        self.bullets.update()
        #使用副本检测出界的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:    self.bullets.remove(bullet)
        self._子弹击中检测()

    def _子弹击中检测(self):
        #重叠检测并删除
        if self.settings.bullet_pass:    collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)
        else:    collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collisions:
            alien_killed=sum(len(hit_aliens) for hit_aliens in collisions.values())
            get_score=self.settings.alien_points*alien_killed

            if alien_killed==1:    print_in(self.获取运行时间()+f"     杂鱼只击中了 {alien_killed} 个外星人,只拿到 {get_score}分 捏~")
            elif get_score<=100:    print_in(self.获取运行时间()+f"     杂鱼击中了 {alien_killed} 个外星人,只拿到 {get_score}分 捏~")
            elif get_score<=200:    print_in(self.获取运行时间()+f"     杂鱼击中了 {alien_killed} 个外星人,拿到了 {get_score}分呢")
            elif get_score<=300:    print_in(self.获取运行时间()+f"     ... 居然击中了 {alien_killed} 个外星人,拿到了 {get_score}分, 呜呜~")
            else:    print_in(self.获取运行时间()+f"     呀啊啊啊啊啊啊啊啊啊啊啊啊❤ ! {alien_killed} 个外星人! 拿到{get_score}分! ")

            self.stats.score+=get_score
            self.sounds.play_sound("crash")
            self.score_board.prep_score()
            self.score_board.检查最高分()



        #创建新舰队
        if not self.aliens:
            time.sleep(0.5)
            self.bullets.empty()
            self.settings.level_up()
            self.score_board.prep_level()
            self.score_board.prep_ships()
            print_in(self.获取运行时间()+f" 竟然进入 level.{self.settings.level} 了呢")
            print_in(self.获取运行时间()+f" 这次有 {self.settings.alien_fleet_height} 支舰队.")
            self.sounds.play_sound('boom')
            self._创建舰队()



    """外星舰队代码"""
    def _创建舰队(self):
        #以单个外星人为基准和基准位置创建整个舰队
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        new_x,new_y=alien.rect.size

        #根据模式创建舰队
        if self.settings.alien_fleet_hieght_new_model:
            for times in range(self.settings.alien_fleet_height):
                while new_x<(self.settings.screen_width-2*alien_width):
                    self._创建外星人(new_x,new_y)
                    new_x+=2*alien_width
                new_x=alien_width
                new_y+=-2*alien_height
        else:
            while new_y<(self.settings.screen_height-3*alien_height):
                while new_x<(self.settings.screen_width-2*alien_width):
                    self._创建外星人(new_x,new_y)
                    new_x+=2*alien_width
                new_x=alien_width
                new_y+=2*alien_height

    def _创建外星人(self,x,y):
        alien=Alien(self)
        alien.x=x
        alien.rect.x=x
        alien.rect.y=y
        self.aliens.add(alien)

    def _更新外星人位置(self):
        self._check_fleet_edges()
        self.aliens.update()
 
        #遍历aliens返回第一个碰撞的外星人
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._游戏失败()
        self._check_aliens_bottom() #检查是否越界

    def _check_fleet_edges(self): 
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for aliens in self.aliens.sprites():
                    aliens.rect.y+=self.settings.alien_down_speed
                self.settings.fleet_direction*=-1
                self.sounds.play_sound("fleet_turn")
                break
    
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                self._游戏失败()
                break



    """飞船代码"""
    def _游戏失败(self):
        self._更新屏幕()
        self.settings.ship_limit+=-1
        self.sounds.play_sound("boom")

        if self.settings.ship_limit>=0:
            print_in(self.获取运行时间()+f" 杂鱼寄喽,只剩下 {self.settings.ship_limit} 次机会喽~")
            print_in(self.获取运行时间()+f" 进入 {self.settings.level} 了呢")
            self.score_board.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._创建舰队()
            self.ship.飞船中置() #实际上ship属性只有一个飞船
        else:
            print_in(self.获取运行时间()+f" 呐,游戏结束了呢,杂鱼❤ ,杂鱼❤ ~")
            self.game_active=False
            pygame.mouse.set_visible(True)
        time.sleep(0.5) #休眠代码在该函数无所谓位置,因为没有覆盖绘图



    def 获取运行时间(self):    return f"[{time.time()-self.start_time:.3f}]"



#运行程序实例
if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()





