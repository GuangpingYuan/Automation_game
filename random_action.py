from game import Fill_bottle
import matplotlib.pyplot as plt
from time import sleep
env = Fill_bottle()
#observation = env.reset_all()
#observation = env.getPresentFrame()
#step = 0

for i in range (10000):
    action = env.random_action()
    #print(action)
    obs,reward,done = env.getNextFrame(action)
    #sleep(0.5)
    #step += 1
    # print(obs.shape)
    # plt.imshow(obs)
    # plt.show()
    #print(reward)
    if done:
        #print(step)
        env.reset_all()
        #step = 0
