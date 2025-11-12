import random
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import WilsonsTheme
from terminalmaze.resources.grid import Cell, Grid


class Wilsons(Algorithm):
    def __init__(self, maze: Grid, theme: WilsonsTheme) -> None:
        super().__init__(maze, theme)
        self.theme = theme
        self.status_text["Algorithm"] = "Wilsons"
        self.status_text["Unvisited"] = 0
        self.status_text["Walked"] = 0
        self.status_text["Cell"] = ""
        self.status_text["State"] = ""
        self.skip_frames = theme.searching_frames_skipped

    def generate_maze(self) -> Generator[Grid, None, None]:
        target = self.maze.random_cell()
        ve_target = ve.ModifySingleCell(self.theme.target)

        ve_target.cell = target
        self.visual_effects["target"] = ve_target

        ve_working_cell = ve.Animation(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_working_cell

        ve_searching_walk = ve.ModifyMultipleCells(self.theme.searching_walk)
        self.visual_effects["searching_walk"] = ve_searching_walk

        ve_linking_walk = ve.ModifyMultipleCells(self.theme.linking_walk)
        self.visual_effects["linking_walk"] = ve_linking_walk

        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_last_linked

        ve_new_linked_walks = ve.Animation(self.theme.new_linked_walk)
        self.visual_effects["new_linked_walk"] = ve_new_linked_walks

        unvisited_cells = list(self.maze.each_cell())
        unvisited_cells.remove(target)
        links = 0
        while unvisited_cells:
            walk: list[Cell] = []
            ve_searching_walk.cells = walk
            walking = True
            working_cell = random.choice(unvisited_cells)
            ve_working_cell.cells.append(working_cell)
            walk.append(working_cell)
            while walking:
                self.status_text["State"] = "Searching"
                next_cell = random.choice(list(n for n in self.maze.get_neighbors(working_cell).values() if n))
                if next_cell in walk:
                    walk = walk[: walk.index(next_cell) + 1]
                    ve_searching_walk.cells = walk
                    working_cell = walk[-1]
                    ve_working_cell.cells.append(working_cell)
                elif next_cell not in unvisited_cells:
                    self.status_text["State"] = "Linking"
                    walking = False
                    ve_searching_walk.cells = []
                    ve_linking_walk.cells = [cell for cell in walk]
                    ve_linking_walk.cells.append(next_cell)
                    if "target" in self.visual_effects:
                        del self.visual_effects["target"]
                    for i, cell in enumerate(walk):
                        if cell == walk[-1]:
                            self.maze.link_cells(cell, next_cell)
                            ve_last_linked.cells.append(next_cell)
                        else:
                            self.maze.link_cells(cell, walk[i + 1])
                            ve_last_linked.cells.append(walk[i + 1])
                        unvisited_cells.remove(cell)
                        self.status_text["Unvisited"] = len(unvisited_cells)
                        self.status_text["Walked"] = len(walk)
                        self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                        yield self.maze
                    else:
                        ve_last_linked.cells.append(next_cell)
                        yield self.maze
                    ve_linking_walk.cells = []
                    ve_new_linked_walks.cells.extend(walk)
                    ve_new_linked_walks.cells.append(next_cell)
                    links += 1
                else:
                    walk.append(next_cell)
                    working_cell = next_cell
                    ve_working_cell.cells.append(working_cell)
                    self.status_text["Unvisited"] = len(unvisited_cells)
                    self.status_text["Walked"] = len(walk)
                    self.status_text["Links"] = links
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                    if links > 3:
                        self.skip_frames = 5
                    if self.frame_wanted():
                        yield self.maze
        while ve_new_linked_walks.animating:
            yield self.maze
        self.visual_effects.clear()
        yield self.maze
