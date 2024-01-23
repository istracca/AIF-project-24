class Moving:
    def __init__(self, env):
        self.__env = env
    
    #Do next position to enviroment
    def Move(self, ActualPosition, NextPosition):
        
        DiffStep = (int(ActualPosition[0] - NextPosition[0]), int(ActualPosition[1] - NextPosition[1]))
        
        Moves = {
            (1, 0):   0, #Moving N
            (0, -1):  1, #Moving E
            (-1, 0):  2, #Moving S
            (0, 1):   3, #Moving W
            (1, -1):  4, #Moving NE
            (-1, -1): 5, #Moving SE
            (-1, 1):  6, #Moving SW
            (1, 1):   7, #Moving NW
            (0, 0):   46 #Rest
        }
        
        return self.__env.step(Moves[DiffStep])[0]