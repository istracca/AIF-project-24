import heapq
import random

def manhattan_distance(Position1, Position2):
    return abs(Position1[0]-Position2[0])+abs(Position1[1]-Position2[1])

def diagonal_distance(Position1, Position2):
    return max(abs(Position1[0]-Position2[0]),abs(Position1[1]-Position2[1]))

# Ritorna, se esiste, il percorso più breve a rischio nullo. Utilizza UCS con il costo di uno step sicuro=0,
# di uno step non sicuro = 1000. A parità di costo sceglie di espandere prima nodi più vicini al goal. Essendo
# che il costo è zero, di fatto l'algoritmo usato per l'espansione dei nodi è Greedy Search
def a_star_search_zero_risk(start, goal, MonsterPosition, SuccessorFunction):
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
            next_cost = 10000 if not is_safe(next_position, MonsterPosition, SuccessorFunction, len(path) + 1) else 1
            next_path = path + [next_position]
            heapq.heappush(open_set, (current_cost + next_cost + diagonal_distance(next_position,goal), current_cost + next_cost, next_position, next_path))

# Semplice A*. Viene utilizzato per calcolare il percorso più breve da un mostro all'agente
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

# Assumiamo che la strategia di movimento del lupo sia la seguente: data la mossa del giocatore, calcola con a*
# il percorso più corto da ognuna delle sue possibili mosse alla posizione del giocatore.
# Sceglie la mossa da cui il percorso per raggiungere il giocatore è più corto
# A parità di lunghezza del percorso sceglie la casella più vicina al giocatore utilizzando la Manhattan Distance
# A parità di Manhattan Distance sceglie casualmente
def next_step_monster(ActualPosition,NewAgentPosition,SuccessorFunction):
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


#   A* provando a prevedere il lupo. L'idea è: ogni volta che scelgo una mossa simulo il movimento del lupo
#   utilizzando la next_step_monster. Scelgo il percorso che mi garantisce un costo minore, dove il costo è
#   1*#steps + 10000*#steps_non_sicuri, non sicuri se il mostro usa la strategia next_step_monster
def a_star_prev_monst(start, goal, MonsterStart, SuccessorFunction):
    open_set = [(0 + diagonal_distance(start,goal), 0, start, [], MonsterStart, [])]
    closed_set = set()

    while open_set:
        _, current_cost, current_position, path, MonsterPosition, monster_path = heapq.heappop(open_set)


        if current_position == goal:
            return [path, monster_path, current_cost]  # Percorso trovato

        if (current_position, tuple(MonsterPosition)) in closed_set:
            continue  # Stato già esplorato

        closed_set.add((current_position, tuple(MonsterPosition)))

        for next_position in SuccessorFunction(current_position):
            next_monster_position = next_step_monster(MonsterPosition, next_position, SuccessorFunction)
            next_cost = 10000 if next_position==next_monster_position else 1
            next_path = path + [next_position]
            next_monster_path = monster_path + [next_monster_position]
            heapq.heappush(open_set, (current_cost + next_cost + diagonal_distance(next_position,goal), current_cost + next_cost, next_position, next_path, next_monster_position, next_monster_path))


# Given the position of monsters, returns if a position is safe or not in n_steps, i.e. if a position can be occupied by at least one of the monster in n_steps
def is_safe(Position,MonsterPosition,SuccessorFunction,n_steps):
    if a_star_search(MonsterPosition, Position, SuccessorFunction)[1] <= n_steps:
        return False
    else:
        return True
    
def convert_coordinates_format(Position):
    return (Position[1]-34,Position[0]-5)

def inverse_convert(Position):
    return(Position[1]+5,Position[0]+34)


# Data una posizione, restituisce le mosse da quella posizione tali che sia massimizzata la scelta di mosse
# allo step successivo, considerando in ciascun caso il worst-case per quanto riguarda la mossa del lupo
def max_choices_moves(Position,MonsterPosition, SuccessorFunction):
    next_positions = [x for x in SuccessorFunction(Position) if is_safe(x,MonsterPosition,SuccessorFunction,1)]
    dict_moves = dict()
    for mymove in next_positions:
        dict_moves.update({mymove:how_many_moves_worst_case(mymove,MonsterPosition,SuccessorFunction)})
    max_dict = max(dict_moves.values())
    max_choices_moves = [key for key, value in dict_moves.items() if value==max_dict]
    return max_choices_moves

#  Data una posizione p in cui l'agente si muove e la posizione del lupo prima di tale mossa, restituisce il numero
#   di mosse che sarà possibile da p dopo che il lupo avrà mosso, calcolato nel peggiore dei casi
def how_many_moves_worst_case(NewPosition, OldMonsterPosition, SuccessorFunction):
    NewMonsterPositions = SuccessorFunction(OldMonsterPosition)
    arr_possible_choices=[]
    for monster_pos in NewMonsterPositions:
        moves = [x for x in SuccessorFunction(NewPosition) if (x!=monster_pos and x not in SuccessorFunction(monster_pos))]
        arr_possible_choices.append(len(moves))
    return min(arr_possible_choices)

#   Strategia che sceglie la mossa da eseguire come quella che massimizza le mosse possibili allo step successivo,
#   considerando il caso peggiore. A parità di mosse possibili, viene scelta la mossa con una minore Manhattan Distance
#   dal goal. A ulteriore parità, viene scelta una mossa casualmente
def trying_to_survive(Position,MonsterPosition,Goal,SuccessorFunction):
    moves = max_choices_moves(Position,MonsterPosition,SuccessorFunction)
    manhattan_dist_moves = [manhattan_distance(move,Goal) for move in moves]
    min_manhattan = min(manhattan_dist_moves)
    candidates = [move for move in moves if manhattan_distance(move,Goal)==min_manhattan]
    return random.choice(candidates)
