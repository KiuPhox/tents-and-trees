import pygame

from constants.GameConfig import ScreenSize

from managers.GameManager import GameManager

from objects.Node import Node

class Grid:
    def __init__(self) -> None:
        self.matrix = []
        self.grid = []
        pass

    def create(self):
        level_data = GameManager.get_current_level_data()

        self.matrix = level_data["map"]
        
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        for y in range(rows):
            row = []
            for x in range(cols):
                pos = ((x - cols / 2) * 65 + ScreenSize.WIDTH / 2, (y - rows / 2) * 65 + ScreenSize.HEIGHT / 2)
                coord = (x, y)

                node = Node(coord, pos, self.matrix[y][x])
                
                row.append(node)
            self.grid.append(row)
            

    def update(self, screen: pygame.Surface):
        for row in self.grid:
            for node in row:
                node.update(screen)
        pass

    