

from pygame import mixer


class Audio:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "bg_sound": mixer.Sound("sounds/bg_sound.mp3"),
            "boom": mixer.Sound("sounds/boom.mp3"),
            "crash": mixer.Sound("sounds/crash.mp3"),
            "shoot_bullet": mixer.Sound("sounds/shoot_bullet_1.mp3"),
            "shoot_wave": mixer.Sound("sounds/shoot_wave_1.mp3"),
            "shoot_laser": mixer.Sound("sounds/shoot_laser_1.mp3"),
            "fleet_turn": mixer.Sound("sounds/fleet_turn_1.mp3"),
        }

    #播放音效
    def play_sound(self,name):
        self.sounds[name].play()

    #播放背景音乐
    def replay_bgsounds(self):
        self.sounds["bg_sound"].stop()
        self.sounds["bg_sound"].play(loops=-1)


