import sys
import os
import pygame
from pygame.sprite import Group

import game_function as gf
from game_settings import Settings
from game_state import GameStats
def run_game():
    pygame.init()
    #get start time
    start_time = pygame.time.get_ticks()
    settings = Settings()
    settings.mode = 'human'
    screen = pygame.display.set_mode((settings.screen_width,settings.screen_height))
    pygame.display.set_caption("Fill the bottle")
    conveyor_belt = gf.Conveyor_belt(screen,settings)
    tank = gf.Tank(screen,settings)
    #bottle = gf.Bottle(screen,conveyor_belt,tank,settings.color)
    #print(bottle)
    waterflow = Group()
    bottles = []
    scoreboard = gf.Scoreboard(screen,settings)
    game_state = GameStats(settings)
    timeline = gf.Timeline(screen,settings)
    while True:
        seconds = (pygame.time.get_ticks() - start_time) / 1000
        if seconds >= settings.time_limit:
        #if game_state.action_num >= settings.action_limit:
            print('Final score is %d'%sum(game_state.score_record[:]))
            if sum(game_state.score_record[:]) >= game_state.highest_score:
                game_state.highest_score = sum(game_state.score_record[:])
                print('New highest score reaches %d'%game_state.highest_score)
            #flag done and reward, that can be used in further training
            game_state.done = True
            game_state.reward = sum(game_state.score_record[:])
            #reset the game
            gf.reset(bottles,waterflow,game_state,tank,settings)
            game_state.round += 1
            print('New round!  round %d'%game_state.round)
            start_time = pygame.time.get_ticks()

        #update all components
        bottle = gf.add_bottle(screen,conveyor_belt,tank,settings.water_color,bottles,game_state)
        gf.check_event(bottle,screen,tank,waterflow,conveyor_belt,game_state,settings)
        gf.update_water(waterflow,conveyor_belt)
        timeline.update(game_state)
        #print('reward_fill is %f'%game_state.reward_fill)

        #show all components
        screen.fill(settings.bg_color)
        conveyor_belt.blitme()
        tank.blitme()
        scoreboard.show_score(game_state)
        timeline.draw()
        for bottle in bottles:
            bottle.update(settings.conveyor_speed)
            bottle.draw()
        for drop in waterflow.sprites():
            drop.draw(settings.water_color)


        pygame.display.flip()


if __name__=='__main__':
    run_game()