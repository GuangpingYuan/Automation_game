
class Settings():
    def __init__(self):
        """initialize game settings"""
        self.screen_width = 600#1200
        self.screen_height = 300#600
        self.zoomrate = 0.8
        self.bg_color = (255,255,255)

        #settings of conveyor belt
        self.conveyor_speed = 1

        #settings of waterflow
        self.water_color = (62,112,252)
        self.fill_rate = 5
        self.waterflow_width = 3.5

        #settings of time
        self.time_limit = 20
        #if actions are limited
        self.action_limit = 610

        self.color_fill = (37,239,37)

        #setting of foam generation
        self.foam_rate = 2

        """Mode 'human' is human mode, human can control the game through keyboard.
           Mode 'auto' is automation mode, system will generate random numbers to play the game."""
        self.mode = 'auto'


