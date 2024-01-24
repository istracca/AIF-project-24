import heapq
import random

def manhattan_distance(Position1, Position2):
    return abs(Position1[0]-Position2[0])+abs(Position1[1]-Position2[1])

def diagonal_distance(Position1, Position2):
    return max(abs(Position1[0]-Position2[0]),abs(Position1[1]-Position2[1]))

# Returns, if exists, the shortest risk-zero path. Uses A* with the cost of a safe step = 1,
# and the cost of an unsafe step = 10000. The h(n) is the diagonal_distance
def a_star_search_zero_risk(start, goal, WolfPosition, SuccessorFunction):
    open_set = [(0 + manhattan_distance(start,goal), 0, start, [])]
    closed_set = set()

    while open_set:
        _, current_cost, current_position, path = heapq.heappop(open_set)

        if current_cost >= 10000:
            return False

        if current_position == goal:
            return path

        if (current_position) in closed_set:
            continue

        closed_set.add(current_position)

        for next_position in SuccessorFunction(current_position):
            next_cost = 10000 if not is_safe(next_position, WolfPosition, SuccessorFunction, len(path) + 1) else 1
            next_path = path + [next_position]
            heapq.heappush(open_set, (current_cost + next_cost + diagonal_distance(next_position,goal), current_cost + next_cost, next_position, next_path))

# Simple A*. Used to calculate the shortest path from a monster to the agent. Cost of each step
# is always 1, h(n) = diagonal_distance(n, goal).
def a_star_search(start, goal, SuccessorFunction):
    open_set = [(0 + manhattan_distance(start, goal), 0, start, [])]
    closed_set = set()

    while open_set:
        _, current_cost, current_position, path = heapq.heappop(open_set)

        if current_position == goal:
            return path, current_cost  # Percorso trovato

        if current_position in closed_set:
            continue  # Stato già esplorato

        closed_set.add(current_position)

        for next_position in SuccessorFunction(current_position):
            next_cost = 1
            next_path = path + [next_position]
            heapq.heappush(open_set, (current_cost + next_cost + diagonal_distance(next_position, goal), current_cost + next_cost, next_position, next_path))

    return None, float('inf')  # Nessun percorso trovato

# Assuming that the wolf's movement strategy is as follows: given the player's move, calculate with A*
# the shortest path from each of its possible moves to the player's position.
# Choose the move from which the path to reach the player is shorter.
# In case of equal path lengths, choose the cell closest to the player using Manhattan Distance.
# In case of equal Manhattan Distance, choose randomly.
def next_step_wolf(ActualPosition,NewAgentPosition,SuccessorFunction):
    if ActualPosition==NewAgentPosition:
        return ActualPosition
    dict_moves = dict()
    for nearpoint in SuccessorFunction(ActualPosition):
        dict_moves.update({nearpoint: a_star_search(nearpoint, NewAgentPosition, SuccessorFunction)[1]})
    min_value = min(dict_moves.values())
    min_moves = [key for key, value in dict_moves.items() if value==min_value]
    dict_manhattan = {key:manhattan_distance(key,NewAgentPosition) for key in min_moves}
    min_manhattan = min(dict_manhattan.values())
    min_manhattan_moves = [key for key, value in dict_manhattan.items() if value==min_manhattan]
    return random.choice(min_manhattan_moves)


# A* trying to predict the wolf's movements. The idea is: every time I choose a move,
# I simulate the wolf's movement using the next_step_wolf strategy.
# I choose the path that guarantees me a lower cost, where the cost is
# 1 * #steps + 10000 * #unsafe_steps, unsafe if the monster uses the next_step_wolf strategy.
def a_star_prev_monst(start, goal, WolfStart, SuccessorFunction):
    open_set = [(0 + diagonal_distance(start,goal), 0, start, [], WolfStart, [])]
    closed_set = set()

    while open_set:
        _, current_cost, current_position, path, WolfPosition, wolf_path = heapq.heappop(open_set)


        if current_position == goal:
            return [path, wolf_path, current_cost]  # Percorso trovato

        if (current_position, tuple(WolfPosition)) in closed_set:
            continue  # Stato già esplorato

        closed_set.add((current_position, tuple(WolfPosition)))

        for next_position in SuccessorFunction(current_position):
            next_wolf_position = next_step_wolf(WolfPosition, next_position, SuccessorFunction)
            next_cost = 10000 if next_position==next_wolf_position else 1
            next_path = path + [next_position]
            next_wolf_path = wolf_path + [next_wolf_position]
            heapq.heappush(open_set, (current_cost + next_cost + diagonal_distance(next_position,goal), current_cost + next_cost, next_position, next_path, next_wolf_position, next_wolf_path))


# Given the position of wolf, returns if a position is safe or not in n_steps, 
# i.e. if a position can be occupied by at least one of the wolf in n_steps
def is_safe(Position,WolfPosition,SuccessorFunction,n_steps):
    if a_star_search(WolfPosition, Position, SuccessorFunction)[1] <= n_steps:
        return False
    else:
        return True
    
def convert_coordinates_format(Position):
    return (Position[1]-34,Position[0]-5)

def inverse_convert(Position):
    return(Position[1]+5,Position[0]+34)


# Given a position, returns the moves from that position such that the choice of moves is maximized
# in the next step, considering in each case the worst-case for the wolf's move
def max_choices_moves(Position,WolfPosition, SuccessorFunction):
    next_positions = [x for x in SuccessorFunction(Position) if is_safe(x,WolfPosition,SuccessorFunction,1)]
    dict_moves = dict()
    for mymove in next_positions:
        dict_moves.update({mymove:how_many_moves_worst_case(mymove,WolfPosition,SuccessorFunction)})
    max_dict = max(dict_moves.values())
    max_choices_moves = [key for key, value in dict_moves.items() if value==max_dict]
    return max_choices_moves

# Given a position p where the agent moves and the position of the wolf before that move, 
# returns the number of moves that will be possible from p after the wolf has moved, calculated in the worst case
def how_many_moves_worst_case(NewPosition, OldWolfPosition, SuccessorFunction):
    NewWolfPositions = SuccessorFunction(OldWolfPosition)
    arr_possible_choices=[]
    for wolf_pos in NewWolfPositions:
        moves = [x for x in SuccessorFunction(NewPosition) if (x!=wolf_pos and x not in SuccessorFunction(wolf_pos))]
        arr_possible_choices.append(len(moves))
    return min(arr_possible_choices)


# Strategy that chooses the move to execute as the one that maximizes the possible moves in the next step,
# considering the worst-case scenario. In case of equal possible moves, the move with the shorter Manhattan Distance
# from the goal is chosen. In case of further tie, a move is randomly chosen.
def trying_to_survive(Position,WolfPosition,Goal,SuccessorFunction):
    moves = max_choices_moves(Position,WolfPosition,SuccessorFunction)
    manhattan_dist_moves = [manhattan_distance(move,Goal) for move in moves]
    min_manhattan = min(manhattan_dist_moves)
    candidates = [move for move in moves if manhattan_distance(move,Goal)==min_manhattan]
    return random.choice(candidates)
