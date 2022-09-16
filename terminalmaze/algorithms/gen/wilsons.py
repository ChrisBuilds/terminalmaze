import random
from typing import Generator
from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve


class Wilsons(Algorithm):
    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.theme = theme["wilsons"]
        self.status_text["Algorithm"] = "Wilsons"
        self.status_text["Time Elapsed"] = ""
        self.status_text["Unvisited"] = 0
        self.status_text["Walked"] = 0
        self.status_text["Cell"] = ""
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        walk: list[Cell] = []
        target = self.maze.random_cell()
        ve_target = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=target, color=self.theme["target"]  # type: ignore [arg-type]
        )
        self.visual_effects["target"] = ve_target
        ve_walk = ve.ColorMultipleCells(
            layer=0, category=ve.LOGICSTYLE, cells=[], color=self.theme["walk"]  # type: ignore [arg-type]
        )
        self.visual_effects["walk"] = ve_walk
        ve_workingcell = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=Cell(0, 0), color=self.theme["workingcell"]  # type: ignore [arg-type]
        )
        self.visual_effects["working_cell"] = ve_workingcell
        ve_linktrail = ve.TrailingColor(
            layer=1, category=ve.STYLE, cells=[], colors=self.theme["linktrail"], traveldir=0  # type: ignore [arg-type]
        )
        self.visual_effects["linktrail"] = ve_linktrail
        unvisited_cells = list(self.maze.each_cell())
        unvisited_cells.remove(target)
        links = 0
        while unvisited_cells:
            walk = []
            ve_walk.cells = walk
            walking = True
            working_cell = random.choice(unvisited_cells)
            ve_workingcell.cell = working_cell
            walk.append(working_cell)
            frame_delay = 10
            while walking:
                self.status_text["State"] = "Searching"
                next_cell = random.choice(list(n for n in self.maze.get_neighbors(working_cell).values() if n))
                if next_cell in walk:
                    walk = walk[: walk.index(next_cell) + 1]
                    ve_walk.cells = walk
                    working_cell = walk[-1]
                    ve_workingcell.cell = working_cell
                elif next_cell not in unvisited_cells:
                    self.status_text["State"] = "Linking"
                    walking = False
                    if "target" in self.visual_effects:
                        del self.visual_effects["target"]
                    for i, cell in enumerate(walk):
                        if cell == walk[-1]:
                            self.maze.link_cells(cell, next_cell)
                            ve_linktrail.cells.insert(0, next_cell)
                        else:
                            self.maze.link_cells(cell, walk[i + 1])
                            ve_linktrail.cells.insert(0, walk[i + 1])
                        ve_linktrail.cells = ve_linktrail.cells[: len(ve_linktrail.colors)]
                        unvisited_cells.remove(cell)
                        self.status_text["Unvisited"] = len(unvisited_cells)
                        self.status_text["Walked"] = len(walk)
                        self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                        self.status_text["Time Elapsed"] = self.time_elapsed()
                        yield self.maze
                    self.visual_effects.pop("logic1", None)
                    links += 1
                else:

                    walk.append(next_cell)
                    working_cell = next_cell
                    ve_workingcell.cell = working_cell
                    self.status_text["Unvisited"] = len(unvisited_cells)
                    self.status_text["Walked"] = len(walk)
                    self.status_text["Links"] = links
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                    if links < 3:
                        frame_delay -= 1
                        if frame_delay == 0:
                            frame_delay = 40
                            self.status_text["Time Elapsed"] = self.time_elapsed()
                            if ve_linktrail.cells:
                                ve_linktrail.cells.pop()
                            yield self.maze
                    else:
                        frame_delay -= 1
                        if frame_delay == 0:
                            frame_delay = 3
                            self.status_text["Time Elapsed"] = self.time_elapsed()
                            if ve_linktrail.cells:
                                ve_linktrail.cells.pop()
                            yield self.maze
        self.visual_effects.clear()
        yield self.maze
