import random
from typing import Generator


from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm


class Wilsons(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Wilons"

    def generate_maze(self) -> Generator[Grid, None, None]:
        walk: list[Cell] = []
        target = self.maze.random_cell()
        self.visual_effects["logic1"] = target
        unvisited_cells = list(self.maze.each_cell())
        unvisited_cells.remove(target)
        links = 0
        while unvisited_cells:
            walk = []
            self.visual_effects["logic0"] = walk
            walking = True
            working_cell = random.choice(unvisited_cells)
            self.visual_effects["working_cell"] = working_cell
            walk.append(working_cell)
            frame_delay = 10
            while walking:
                next_cell = random.choice(list(n for n in self.maze.get_neighbors(working_cell).values() if n))
                if next_cell in walk:
                    walk = walk[: walk.index(next_cell) + 1]
                    self.visual_effects["logic0"] = walk
                    working_cell = walk[-1]
                    self.visual_effects["working_cell"] = working_cell
                elif next_cell not in unvisited_cells:
                    walking = False
                    for i, cell in enumerate(walk):
                        if cell == walk[-1]:
                            self.maze.link_cells(cell, next_cell)
                        else:
                            self.maze.link_cells(cell, walk[i + 1])

                        unvisited_cells.remove(cell)
                        self.status_text["Unvisited"] = len(unvisited_cells)
                        self.status_text["Walked"] = len(walk)
                        self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                        yield self.maze
                    self.visual_effects.pop("logic1", None)
                    links += 1
                else:
                    walk.append(next_cell)
                    working_cell = next_cell
                    self.visual_effects["working_cell"] = working_cell
                    if self.showlogic:
                        self.status_text["Unvisited"] = len(unvisited_cells)
                        self.status_text["Walked"] = len(walk)
                        self.status_text["Links"] = links
                        self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                        if links < 3:
                            frame_delay -= 1
                            if frame_delay == 0:
                                frame_delay = 40
                                yield self.maze
                        else:
                            frame_delay -= 1
                            if frame_delay == 0:
                                frame_delay = 3
                                yield self.maze
