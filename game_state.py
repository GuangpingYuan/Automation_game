
class GameStats():
    """record the game state"""
    def __init__(self,settings):
        self.settings = settings
        self.score_record = []
        self.round = 0
        self.highest_score = 0
        self.done = False
        self.reward = 0
        self.reward_fill = 0
        self.final_score = 0
        self.action_num = 0
        """vision 1: left and right key control the movement.Bottle moves right when right key is pressed, bottle stops when right key is released. 
           Vision 2: left and right key control the acceleration. Bottle continuously moves right. It speeds up when right key is pressed, however it slows down or stops when left key is pressed.
                        The hightest moving speed is 5, it can not move towards left."""
        self.version = 2

