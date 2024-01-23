import gym
import minihack
from Map import Map

def CreateLevel1():

    new_level = minihack.LevelGenerator(w = 11, h = 11)
    new_level.set_start_pos((6, 5))

    new_level.fill_terrain(type='fillrect',flag='L', x1 = 1, y1 = 1, x2 = 4, y2 = 4)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 6, y1 = 1, x2 = 9, y2 = 4)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 1, y1 = 6, x2 = 4, y2 = 9)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 6, y1 = 6, x2 = 9, y2 = 9)

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 2, y1 = 2, x2 = 8, y2 = 8)

    new_level.add_monster(name='wolf',symbol='d', place=(3,3))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment

def CreateLevel2():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((7, 6))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    for i in range(1,w,2):
        for j in range (1,w,2):    
            new_level.fill_terrain(type='fillrect',flag='L', x1=i, y1=j, x2=i, y2=j)

    new_level.add_monster(name='wolf',symbol='d', place=(0,0))
    # new_level.add_monster(name='wolf',symbol='d', place=(10,10))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment

def CreateLevel3():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((6, 5))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    new_level.fill_terrain(type='fillrect',flag='L',x1=3,y1=4,x2=7,y2=4)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=3,y1=2,x2=3,y2=3)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=7,y1=2,x2=7,y2=3)   

    new_level.add_monster(name='wolf',symbol='d', place=(5,2))
    # new_level.add_monster(name='wolf',symbol='d', place=(10,10))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment

def CreateLevel4():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((10, 9))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    new_level.fill_terrain(type='fillrect',flag='L',x1=1,y1=7,x2=7,y2=7)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=7,y1=1,x2=7,y2=7)   

    new_level.add_monster(name='wolf',symbol='d', place=(3,3))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment

def CreateLevel5():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((10, 9))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    new_level.fill_terrain(type='fillrect',flag='L',x1=1,y1=1,x2=7,y2=1)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=1,y1=1,x2=1,y2=7)   

    new_level.add_monster(name='wolf',symbol='d', place=(0,0))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment

def CreateLevel6():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((10, 10))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    new_level.fill_terrain(type='fillrect',flag='L',x1=1,y1=3,x2=1,y2=5)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=1,y1=7,x2=1,y2=9)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=3,y1=1,x2=3,y2=4)
    new_level.fill_terrain(type='fillrect',flag='L',x1=3,y1=6,x2=3,y2=9)     
    new_level.fill_terrain(type='fillrect',flag='L',x1=5,y1=1,x2=5,y2=5)
    new_level.fill_terrain(type='fillrect',flag='L',x1=5,y1=7,x2=5,y2=9)    
    new_level.fill_terrain(type='fillrect',flag='L',x1=7,y1=1,x2=7,y2=9)   
    new_level.fill_terrain(type='fillrect',flag='L',x1=9,y1=1,x2=9,y2=9)   

    new_level.fill_terrain(type='fillrect',flag='L',x1=5,y1=1,x2=7,y2=1)

    new_level.fill_terrain(type='fillrect',flag='L',x1=3,y1=9,x2=5,y2=9)
    new_level.fill_terrain(type='fillrect',flag='L',x1=7,y1=9,x2=9,y2=9)




    new_level.add_monster(name='wolf',symbol='d', place=(0,0))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    
    return MapGame, Enviroment
