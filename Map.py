import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

class Map:
    def __init__(self, state):
        self.__state = state
        
    def get_map_image(self):
        # Rimuovi il bordo nero
        image = self.__state['pixel']

        rows = np.any(image != [0, 0, 0], axis=2).any(axis=1)
        cols = np.any(image != [0, 0, 0], axis=2).any(axis=0)

        image_without_borders = image[rows][:, cols, :]
        
        return image_without_borders

    def view_map(self):
        # Ottieni l'immagine della mappa
        image = self.get_map_image()

        # Mostra la mappa
        plt.imshow(image)
        plt.show()
    
    def get_position_symbol(self, x, y):
        return chr(self.__state["chars"][x][y])

    def get_player_location(self, symbol : str = "@") -> Tuple[int, int]:
        x, y = np.where(self.__state["chars"] == ord(symbol))
        return (x[0], y[0])

    def get_monsters_location(self, symbol : str = "d"):
        x, y = np.where(self.__state["chars"] == ord(symbol))
        arr_returned = []
        for i in range(len(x)):
            position = (x[i], y[i])
            arr_returned.append(position)
        return arr_returned