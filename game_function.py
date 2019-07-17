import sys
import pygame
from pygame.sprite import Sprite

def check_event(bottle,screen,tank,waterflow,conveyor,game_state,settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state.version == 1:
                if event.key == pygame.K_RIGHT:
                    bottle.moving_right = True
                    game_state.reward_fill = 0
                if event.key == pygame.K_LEFT:
                    bottle.moving_left = True
                    game_state.reward_fill = 0
            else:
                if event.key == pygame.K_RIGHT:
                    if settings.conveyor_speed <= 5:
                        settings.conveyor_speed += 1
                        game_state.reward_fill = 0
                if event.key == pygame.K_LEFT:
                    if settings.conveyor_speed > 0:
                        settings.conveyor_speed -= 1
                        game_state.reward_fill = 0
        elif event.type == pygame.KEYUP:
            if game_state.version == 1:
                if event.key == pygame.K_RIGHT:
                    bottle.moving_right = False
                    game_state.reward_fill = 0
                if event.key == pygame.K_LEFT:
                    bottle.moving_left = False
                    game_state.reward_fill = 0
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if pygame.key.get_pressed()[pygame.K_UP]:
                if tank.valve < 3:
                    tank.valve += 1
                game_state.reward_fill = 0
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if tank.valve > 1:
                    tank.valve -= 1
                game_state.reward_fill = 0
            waterflow_width, tank.fill_speed, tank.foam_speed = control_valve(tank.valve,settings)
            #print('Value is opening in level %d' %tank.valve)
            #print('Fill speed is %d' %tank.fill_speed)
            fill_water(screen, tank, waterflow, conveyor, bottle, tank.fill_speed,waterflow_width,tank.foam_speed,game_state)
        game_state.reward = settings.conveyor_speed + game_state.reward_fill


class Conveyor_belt():
    def __init__(self,screen,settings):
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('Conveyor_belt.png')
        #self.image = pygame.transform.scale(self.image,(1000,62))
        self.image = pygame.transform.rotozoom(self.image,0,self.settings.zoomrate)
        self.rect = self.image.get_rect()
        self.screen_rect  = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = 0.9*self.screen_rect.height

    def blitme(self):
        """draw a conveyor belt"""
        self.screen.blit(self.image,self.rect)

class Bottle():
    def __init__(self,screen,conveyor,tank,water_color,game_state):
        self.screen = screen
        self.conveyor = conveyor
        self.tank = tank
        self.rect = pygame.Rect(0,0,50,100)
        self.color_line = (0,0,0)
        self.rect_fill = pygame.Rect(0,0,50,0)
        self.color_fill = water_color
        self.foam = pygame.Rect(0,0,50,0)
        self.color_foam = (133,126,101)
        self.rect.bottomleft = self.conveyor.rect.topleft
        self.rect_fill.bottomleft = self.conveyor.rect.topleft
        self.foam.midbottom = self.rect_fill.midtop
        self.score = 0
        self.game_state = game_state
        if self.game_state.version == 1:
            self.moving_right = False
            self.moving_left = False
        else:
            self.moving_right = True
            self.moving_left = False


    def update(self,moving_speed):
        if self.moving_right and self.rect.right <= self.conveyor.rect.right:
            self.rect.centerx += moving_speed
            self.rect_fill.centerx += moving_speed
            self.foam.centerx += moving_speed
        if self.moving_left and self.rect.left >= self.conveyor.rect.left:
            self.rect.centerx -= moving_speed
            self.rect_fill.centerx -= moving_speed
            self.foam.centerx -= moving_speed

    def draw(self):
        pygame.draw.rect(self.screen,self.color_line,self.rect,5)
        pygame.draw.rect(self.screen,self.color_fill,self.rect_fill)
        pygame.draw.rect(self.screen,self.color_foam,self.foam)


class Tank():
    def __init__(self,screen,settings):
        self.screen = screen
        self.image = pygame.image.load('Tank.png')
        self.image = pygame.transform.rotozoom(self.image, 0, settings.zoomrate)
        self.rect = self.image.get_rect()
        self.screen_rect  = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = 0.25*self.screen_rect.height
        self.valve = 1


    def blitme(self):
        self.screen.blit(self.image,self.rect)

class Water(Sprite):
    def __init__(self,screen, tank, conveyor):
        super().__init__()
        self.tank = tank
        self.radius = 5
        self.screen = screen
        self.conveyor = conveyor
        self.rect = pygame.Rect(0,0,5,30)
        self.rect.centerx = self.tank.rect.centerx
        self.rect.top = self.tank.rect.bottom
        self.y = self.rect.y
        self.valve = 1
    def draw(self,color):
        pygame.draw.rect(self.screen,color,self.rect)
    def update(self):
         self.y +=1
         self.rect.y = self.y

class Scoreboard():
    """show the scores"""
    def __init__(self,screen,settings):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        #self.bottle = bottle

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None,48)

        #self.prep_score(bottle)
    def prep_score(self,game_state):
        #put score in right position
        self.score_str = str(sum(game_state.score_record[:]))
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = 20

    def show_score(self,game_state):
        self.prep_score(game_state)
        self.screen.blit(self.score_image,self.score_rect)


class Timeline():
    def __init__(self,screen,settings):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(25,25,125,25)
        self.color_line = (0,0,0)
        self.rect_fill = pygame.Rect(25,25,125,25)
        self.color_fill = self.settings.color_fill

    def update(self,game_state) if self.settings.mode == 'auto'#seconds
        if self.settings.mode == 'human':
            self.rect_fill.width = (self.settings.time_limit - seconds)/self.settings.time_limit * 125 #self.rect_fill.width
        else:
            self.rect_fill.width = (self.settings.action_limit - game_state.action_num)/self.settings.action_limit *125
    def draw(self):
        pygame.draw.rect(self.screen,self.color_line,self.rect,5)
        pygame.draw.rect(self.screen, self.color_fill, self.rect_fill)

class Speedline():
    def __init__(self,screen,settings):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.rect = pygame.Rect(0,0,125,25)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = 0.99*self.screen_rect.height
        self.color = self.settings.color_fill
    def update(self):
        self.rect.width = self.settings.conveyor_speed/5 *125
    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

class Valveangle():
    def __init__(self,screen,settings,tank):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.tank = tank
        self.settings = settings
        self.rect = pygame.Rect(0,0,25,90)
        self.rect.top = self.tank.rect.top
        self.rect.centerx = 0.6*self.screen_rect.width
        self.color = self.settings.color_fill
    def update(self):
        self.rect.height = self.tank.valve/3 *90
    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)


def fill_water(screen,tank,waterflow,conveyor,bottle,fill_speed,waterflow_width,foam_speed,game_state):
    if len(waterflow)< 10:
        drop = Water(screen,tank,conveyor)
        waterflow.add(drop)
        drop.rect.width = waterflow_width
        #game_state.score_record[-1] = bottle.score
        if tank.rect.centerx>= bottle.rect.left and tank.rect.centerx <= bottle.rect.right:
           if bottle.rect_fill.height + bottle.foam.height < bottle.rect.height:
               bottle.rect_fill.y -= fill_speed
               bottle.rect_fill.height += fill_speed
               bottle.foam.bottom = bottle.rect_fill.top
               bottle.foam.height += foam_speed
               bottle.draw()
               bottle.score = bottle.rect_fill.height
               game_state.reward_fill = fill_speed #+1
           #todo:try to find a way to differ full bottle and not full bottle, and give them different scores
           # elif bottle.rect_fill.height + bottle.foam.height == bottle.rect.height:
           #     game_state.score_record[-1] += 100
           #     print('Perfect!')
           else:
               print('Overflow!!!')
               bottle.score -= 1
               game_state.reward_fill = -0.3*fill_speed

        else:
            #give some punishment when it opens the valve while bottle is not under the valve
            #bottle.score -= 1
            game_state.reward_fill = -0.3
        game_state.score_record[-1] = bottle.score

def update_water(waterflow,conveyor):
    waterflow.update()
    for drop in waterflow.copy():
        if drop.rect.bottom >= conveyor.rect.top:
            waterflow.remove(drop)

def control_valve(valve,settings):
    waterflow_width = settings.waterflow_width*valve
    fill_speed = settings.fill_rate*valve
    foam_speed = settings.foam_rate*valve

    return waterflow_width, fill_speed,foam_speed

def add_bottle(screen,conveyor,tank,color,bottles,game_state):
    if len(bottles)== 0:
        bottle = Bottle(screen,conveyor,tank,color,game_state)
        bottles.append(bottle)
        game_state.score_record.append(bottle.score)
    elif bottles[-1].rect.right >= conveyor.rect.right:
        #print(game_state.score_record)
        print('Score is %d'%game_state.score_record[-1])
        print('Added a bottle!')
        bottle = Bottle(screen,conveyor,tank,color,game_state)
        game_state.score_record.append(bottle.score)

        bottles.append(bottle)
    return bottles[-1]

def reset(bottles, waterflow,game_state,tank,settings):
    #empty bottles list
    bottles[:] = []
    waterflow.empty()
    game_state.score_record = []
    tank.valve = 1
    game_state.done = False
    game_state.reward = 0
    game_state.reward_fill = 0
    game_state.action_num = 0
    if game_state.version == 2:
        settings.conveyor_speed = 1




