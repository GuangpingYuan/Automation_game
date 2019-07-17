import pygame
from pygame.sprite import Group
import random
import os

from game_settings import Settings
import game_function as gf
from game_state import GameStats

#IF do not show the window
#os.environ['SDL_VIDEODRIVER']= "dummy"
class Fill_bottle():
    def __init__(self):
        self.name = 'Fill_bottle'
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Fill the bottle")
        self.conveyor_belt = gf.Conveyor_belt(self.screen,self.settings)
        self.tank = gf.Tank(self.screen,self.settings)
        self.waterflow = Group()
        self.bottles = []
        self.scoreboard = gf.Scoreboard(self.screen, self.settings)
        self.game_state = GameStats(self.settings)
        self.timeline = gf.Timeline(self.screen, self.settings)
        self.speedline = gf.Speedline(self.screen,self.settings)
        self.valveangle = gf.Valveangle(self.screen,self.settings,self.tank)

    def getPresentFrame(self):
        #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        #self.seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        self.bottle = gf.add_bottle(self.screen,self.conveyor_belt,self.tank,self.settings.water_color,self.bottles,self.game_state)
        #show all components
        self.screen.fill(self.settings.bg_color)
        self.conveyor_belt.blitme()
        self.tank.blitme()
        self.scoreboard.show_score(self.game_state)
        self.timeline.draw()
        self.speedline.draw()
        self.valveangle.draw()
        for bottle in self.bottles:
            bottle.update(self.settings.conveyor_speed)
            bottle.draw()
        for drop in self.waterflow.sprites():
            drop.draw(self.settings.water_color)

        #copies the pixedls from the surface to a 3D array. It will be used for RL.
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #swap two axes
        image_data = image_data.swapaxes(0,1)
        pygame.display.flip()
        #return the surface data
        return image_data

    def getNextFrame(self,action):
        pygame.event.pump()
        #self.seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        #if self.seconds >= self.settings.time_limit:
        if self.game_state.action_num >= self.settings.action_limit:
            self.game_state.final_score = sum(self.game_state.score_record[:])
            print('Final score is %d'%sum(self.game_state.score_record[:]))
            if sum(self.game_state.score_record[:]) >= self.game_state.highest_score:
                self.game_state.highest_score = sum(self.game_state.score_record[:])
                print('New highest score reaches %d'%self.game_state.highest_score)
            #flag done and reward, that can be used in further training
            self.game_state.done = True
            #self.start_time = pygame.time.get_ticks()
        #update all components
        self.bottle = gf.add_bottle(self.screen,self.conveyor_belt,self.tank,self.settings.water_color,self.bottles,self.game_state)
        #Do not check keyboard event
        #gf.check_event(bottle,self.screen,self.tank,self.waterflow,self.conveyor_belt,self.game_state,self.settings)
        self.get_action(action)
        self.game_state.action_num += 1
        gf.update_water(self.waterflow,self.conveyor_belt)
        self.timeline.update(self.game_state)
        self.speedline.update()
        self.valveangle.update()

        self.screen.fill(self.settings.bg_color)
        self.conveyor_belt.blitme()
        self.tank.blitme()
        self.scoreboard.show_score(self.game_state)
        self.timeline.draw()
        self.speedline.draw()
        self.valveangle.draw()
        for bottle in self.bottles:
            bottle.update(self.settings.conveyor_speed)
            bottle.draw()
        for drop in self.waterflow.sprites():
            drop.draw(self.settings.water_color)

        # copies the pixedls from the surface to a 3D array. It will be used for RL.
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #swap two axes
        image_data = image_data.swapaxes(0,1)
        pygame.display.flip()
        # return the surface data
        #print('action is %d'%action)
        # print('speed is %d'%self.settings.conveyor_speed)
        # print('reward fill is %d'%self.game_state.reward_fill)
        # print('score is %d'%self.game_state.score_record[-1])
        #print('reward is %f'%self.game_state.reward)
        return [image_data,self.game_state.reward,self.game_state.done]



    def reset_all(self):
        gf.reset(self.bottles, self.waterflow, self.game_state, self.tank, self.settings)
        self.game_state.round = 0
        #self.start_time = pygame.time.get_ticks()

    def get_action(self,action):
        #todo:assume action is a number, such as 3. Make one movement at a time
        if action == 0:
            self.game_state.reward_fill = 0
        if action == 4:
            if self.settings.conveyor_speed < 5:
                self.settings.conveyor_speed += 1
            self.game_state.reward_fill = 0
        if action ==5:
            if self.settings.conveyor_speed > 0:
                self.settings.conveyor_speed -= 1
            self.game_state.reward_fill = 0
        if action==2:
            if self.tank.valve < 3:
                self.tank.valve += 1
            self.game_state.reward_fill = 0
        if action==3:
            if self.tank.valve > 1:
                self.tank.valve -= 1
            self.game_state.reward_fill = 0
        if action == 1:
            waterflow_width,self.tank.fill_speed,self.tank.foam_speed = gf.control_valve(self.tank.valve,self.settings)
            gf.fill_water(self.screen,self.tank,self.waterflow,self.conveyor_belt,self.bottle,
                          self.tank.fill_speed,waterflow_width,self.tank.foam_speed,self.game_state)

        if self.bottle.rect.centerx <= 270 or self.bottle.rect.centerx > 330:
            speed_factor = 1
        elif self.bottle.rect.centerx > 270 and self.bottle.rect.centerx <= 300:
            speed_factor = max(-0.2*self.bottle.rect.centerx+55,-0.5)
        elif self.bottle.rect.centerx > 300 and self.bottle.rect.centerx <= 330:
            speed_factor = max(0.2*self.bottle.rect.centerx - 65, -0.5)

        self.game_state.reward = speed_factor*self.settings.conveyor_speed + self.game_state.reward_fill


    def random_action(self):
        # action = []
        # num1 = random.randint(0,1)
        # action.append(num1)
        # num2 = random.randint(2,3)
        # action.append(num2)
        # num3 = random.randint(4,5)
        # action.append(num3)
        # return action
        action =random.randint(0,5)
        return action

ACITON_MEANING= {
    0:"NOOP",
    1:"Fill water",
    2:"Increase valve opening angle",
    3:"Decrease valve opening angle",
    4:"Speed up" or "Move towards right",
    5:"Slow down" or "Move towards left",
}

Fill_bottle()