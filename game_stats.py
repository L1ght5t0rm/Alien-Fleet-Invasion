

class GameStats:
    def __init__(self,main_game):
        self.settings=main_game.settings
        try:
            with open("record.txt", "r",encoding="utf-8") as f:
                self.highest_score=int(f.read())
        except:    self.highest_score=0
        self._init_stats()

    def _init_stats(self):
        self.score=0




