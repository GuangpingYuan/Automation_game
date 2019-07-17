# Automation_game
Implementation of an automation game "Fill the bottle" using Pygame.
In this work, the automation system “Fill the bottle” is implemented based on Pygame.

The automation system consists of a tank, a valve and bottles transferred by a conveyor belt. The tank is filled with a liquid and controlled by an automatic valve which has three levels of opening. The goal of this system is to fill the bottles as fast as possible without overflowing them. Rapid and correct positioning is the key to influencing the scores. We want to fill the bottle with the largest possible flow and as little foam as possible. The conveyor speed has five levels in total. The score is calculated by the accumulation of liquid volume inside each bottle. It is punished by -1 point when it overflows. The game ends only when the player operates 300 times. 

The game screen is  set to 600x300. A rectangle to represent the bottle was used in order to simplify the implementation. The three green bars represent the left number of operations, the valve opening level, and the conveyor speed level respectively. The length of these bars will change through corresponding actions.

It has two versions:human mode and random action. Random action mode can be used to train a reinforcement learning agent.

Set the mode in game_settings.py as 'human' or 'auto'.

Run 'random_action.py' or 'human_mode.py'. 
