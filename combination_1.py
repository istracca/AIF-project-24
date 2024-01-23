from Map import *
from utils import *

def combination_1(MapGame, Joystick, Goal, SuccessorFunction):
    moves = 0

    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
    MonsterPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])
    MapGame.view_map()

    while(1):
        if CharacterPosition==Goal:
            print("Target reached in", moves, "moves!")
            return moves
        if CharacterPosition==MonsterPosition:
            print("Wolf wins")
            return False
        else:
            res = a_star_search_zero_risk(CharacterPosition,Goal,MonsterPosition,SuccessorFunction)
            if res!=False:      # Esiste un percorso a rischio zero. Seguo quello fino alla fine
                path = res
                print("I found a 100% safe path:", path)
                for step in path:
                    NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                    MapGame = Map(NewState)
                    moves += 1
                    MapGame.view_map()
                    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
            else:
                # Ipotizzando che i lupi si muovano come descritto in next_step_monster, cerco un percorso sicuro almeno sotto tale ipotesi
                path, monster_path, cost = a_star_prev_monst(CharacterPosition,Goal,MonsterPosition,SuccessorFunction)
                print(path, cost)
                if cost >= 10000:    # Tale percorso sicuro non esiste. Provo a sopravvivere aspettando che il lupo sbagli
                    print("Se il lupo gioca bene, ha vinto. Cerco di sopravvivere il più a lungo possibile sperando che sbagli")
                    step = trying_to_survive(CharacterPosition,MonsterPosition,Goal,SuccessorFunction)
                    NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                    MapGame = Map(NewState)
                    moves += 1
                    MapGame.view_map()
                    CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
                    MonsterPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])

                else:       # Esiste un percorso che, nell'ipotesi che il lupo si muove come credo, mi porta sano e salvo all'obiettivo
                    print("Il percorso che ritengo che il lupo farà è", monster_path, "e se lo farà ho vinto io")
                    for step, monster_step in zip(path,monster_path):
                        NewState = Joystick.Move(inverse_convert(CharacterPosition), inverse_convert(step))
                        MapGame = Map(NewState)
                        moves += 1
                        MapGame.view_map()
                        CharacterPosition = convert_coordinates_format(MapGame.get_player_location())
                        MonsterPosition = convert_coordinates_format(MapGame.get_monsters_location()[0])
                        ActualMonsterMove = MonsterPosition
                        print("La mossa che il lupo ha fatto è", ActualMonsterMove)
                        ExpectedMonsterMove = monster_step
                        print("La mossa che avevo previsto è", ExpectedMonsterMove)
                        if ActualMonsterMove==ExpectedMonsterMove:
                            # Se il lupo si sta muovendo come credo, non c'è bisogno di ricalcolare
                            print("Avevo ragione, non ricalcolo!")
                        else:
                            # Se il lupo ha fatto un'altra mossa, il percorso calcolato precedentemente non è più valido
                            print("Mi sono sbagliato, provo a ricalcolare!")
                            break
                    