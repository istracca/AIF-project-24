from Map import *
from utils import *
from CreateVideo import *

def combination_1(MapGame, Joystick, Goal, SuccessorFunction, MakeVideo, video_path=None):
    moves = 0

    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
    WolfPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])
    frames = []
    if MakeVideo:
        frame = MapGame.get_map_image()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frames.append(frame_bgr)
    MapGame.view_map()

    while(1):
        if CharacterPosition==Goal:
            print("Target reached in", moves, "moves!")
            if MakeVideo:
                create_video(video_path, frames, frame_rate=4)
            return moves
        if CharacterPosition==WolfPosition:
            print("Wolf wins")
            if MakeVideo:
                create_video(video_path, frames, frame_rate=4)
            return False
        if moves > 200:
            print("Target not reached in 500 moves")
            if MakeVideo:
                create_video(video_path, frames, frame_rate=4)
            return False
        else:
            res = a_star_search_zero_risk(CharacterPosition,Goal,WolfPosition,SuccessorFunction)
            if res!=False:      # There is a risk-free path. Follow that until the end
                path = res
                print("I found a 100% safe path:", path)
                for step in path:
                    NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                    MapGame = Map(NewState)
                    moves += 1
                    if MakeVideo:
                        frame = MapGame.get_map_image()
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        frames.append(frame_bgr)
                    MapGame.view_map()
                    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
            else:
                 # Assuming the wolf moves as described in next_step_wolf, look for a safe path at least under that assumption
                path, wolf_path, cost = a_star_prev_monst(CharacterPosition,Goal,WolfPosition,SuccessorFunction)
                print(path, cost)
                if cost >= 10000:    # No safe path exists. Try to survive by waiting for the wolf to make a mistake
                    print("If the wolf plays well, it has won. I try to survive as long as possible hoping it makes a mistake")
                    step = trying_to_survive(CharacterPosition,WolfPosition,Goal,SuccessorFunction)
                    NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                    MapGame = Map(NewState)
                    moves += 1
                    if MakeVideo:
                        frame = MapGame.get_map_image()
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        frames.append(frame_bgr)
                    MapGame.view_map()
                    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
                    WolfPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])

                else:     # There is a path that, under the assumption that the wolf moves as I believe, leads me safely to the goal
                    print("The path that I believe the wolf will take is", wolf_path, "and if it does, I win")
                    for step, wolf_step in zip(path,wolf_path):
                        NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                        MapGame = Map(NewState)
                        moves += 1
                        if MakeVideo:
                            frame = MapGame.get_map_image()
                            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                            frames.append(frame_bgr)
                        MapGame.view_map()
                        CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
                        WolfPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])
                        ActualWolfMove = WolfPosition
                        print("The move the wolf made is", ActualWolfMove)
                        ExpectedWolfMove = wolf_step
                        print("The move I predicted is", ExpectedWolfMove)
                        if ActualWolfMove==ExpectedWolfMove:
                            # If the wolf is moving as I believe, no need to recalculate
                            print("I was right, no need to recalculate!")
                        else:
                            # If the wolf made another move, the previously calculated path is no longer valid
                            print("I was wrong, try to recalculate!")
                            break
                    