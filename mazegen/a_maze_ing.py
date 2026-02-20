from typing import Any, Tuple
import sys
import os
import random
from pydantic import Field, BaseModel, model_validator


def arg_error(arg: str, argtype: str, param: str) -> int:
    print(
        f"Argument invalid or not present: {Color.red}{arg}{Color.reset} "
        f"Expected: {param}={Color.green}{argtype}{Color.reset}"
        )
    return 1


class Parameters(BaseModel):
    """
    The class that contains all the Parameters that should be read
    with read_config
    """

    width: int = Field(default=-1)
    height: int = Field(default=-1)
    en_pos: Tuple[int, int] = Field(
            default=(-1, -1), min_length=2, max_length=2
            )
    ex_pos: Tuple[int, int] = Field(
            default=(-1, -1), min_length=2, max_length=2
            )
    output_filename: str = Field(default="")
    perfect: bool = Field(default=False)
    seed: int | None = 42
    seed_is_random: bool = True

    @model_validator(mode='before')
    @classmethod
    def format_input(cls, data: Any) -> Any:
        for field in ['en_pos', 'ex_pos']:
            if field in data and isinstance(data[field], str):
                data[field] = [int(x.strip()) for x in data[field].split(',')]
        if data.get('seed') == "":
            data['seed'] = random.randint(1, 9999)
            data['seed_is_random'] = True
        return data

    def validate_parameters(self) -> bool:
        error = 0
        if self.width < 0:
            arg_error(str(self.width), "<INT>", "WIDTH")
            error = 1
            return False
        if self.height < 0:
            arg_error(str(self.height), "<INT>", "HEIGHT")
            error = 1
            return False
        if self.en_pos[0] < 0\
                or self.en_pos[0] > self.width - 1\
                or self.en_pos[1] < 0\
                or self.en_pos[1] > self.height - 1:
            arg_error(str(self.en_pos), "<INT >= 0>,<INT >= 0>", "ENTRY")
            error = 1
            return False
        if self.ex_pos[0] < 0\
                or self.ex_pos[0] > self.width - 1\
                or self.ex_pos[1] < 0\
                or self.ex_pos[1] > self.height - 1:
            arg_error(str(self.ex_pos), "<INT >= 0>, <INT >= 0", "EXIT")
            error = 1
            return False
        if not self.output_filename or\
                self.output_filename != "maze.txt":
            arg_error(str(self.output_filename), "<maze.txt>", "OUTPUT_FILE")
            error = 1
            return False
        if self.en_pos == self.ex_pos:
            print(f"{Color.red}Error:{Color.reset} "
                  f"Entry and exit should be different.")
            error = 1
            return False
        if error == 0:
            return True

        return False

    @classmethod
    def read_config(cls, file_path: str) -> Any:
        config_data: dict[str, Any] = {}

        key_map = {
            "WIDTH": "width",
            "HEIGHT": "height",
            "ENTRY": "en_pos",
            "EXIT": "ex_pos",
            "OUTPUT_FILE": "output_filename",
            "PERFECT": "perfect",
            "SEED": "seed"
        }

        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if '=' not in line:
                        continue

                    key, value = [x.strip() for x in line.split('=', 1)]

                    if key not in key_map:
                        continue

                    target_key = key_map[key]

                    try:
                        if key in ("WIDTH", "HEIGHT", "SEED"):
                            config_data[target_key] = int(value)

                        elif key in ("ENTRY", "EXIT"):
                            x_str, y_str = value.split(',')
                            x = int(x_str.strip())
                            y = int(y_str.strip())
                            config_data[target_key] = (x, y)

                        elif key == "PERFECT":
                            config_data[target_key] = value.lower() == "true"

                        elif key == "OUTPUT_FILE":
                            config_data[target_key] = value

                    except Exception:
                        arg_error(key, "invalid value", key)
                        continue

            params = cls(**config_data)

            if not params.validate_parameters():
                return None

            return params

        except FileNotFoundError:
            print(
                    f"{Color.red}Config file not found:",
                    f"{file_path}{Color.reset}"
                )
        except Exception:
            print("Error in parsing config.txt")
            print(f"Expected format: {Color.green}PARAM=DATA{Color.reset}")

        return None


class Color:
    """
    The class containing colors to have a beautiful maze
    """
    red = "\033[31m"
    green = "\033[32m"
    blue = "\033[34m"
    gray = "\033[90m"
    white = "\u001b[37m"
    reset = "\033[0m"


class Cell:
    """
    The class that represents a cell with the following attributes:
    - visited
    - walls: set
    - position: tuple
    """
    def __init__(self, x: int, y: int) -> None:
        self.visited = False
        self.walls = {"Top", "Right", "Bottom", "Left"}
        self.position = (x, y)

    def printCell(self, fileObject: Any) -> None:
        """
        Translate cell to hex and put them into file
        """
        base = "0123456789ABCDEF"
        toPrint = 0b0
        if "Left" in self.walls:
            toPrint += 1
        toPrint <<= 1
        if "Bottom" in self.walls:
            toPrint += 1
        toPrint <<= 1
        if "Right" in self.walls:
            toPrint += 1
        toPrint <<= 1
        if "Top" in self.walls:
            toPrint += 1
        print(base[toPrint], file=fileObject, end='')


class MazeGenerator:
    """
    The class used to generate and represent a maze containing cells in an
    grid.
    """
    def __init__(self, params: Parameters):
        self.grid = []
        self.midle = (int(params.height/2), int(params.width/2))
        self.params = params

        for y in range(0, params.height):
            row = []
            for x in range(0, params.width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def print_forty_two(self) -> None:
        """
        Print the 42 logo at the center of the maze if the size of the maze
        is big enough and if the entry and/or exit positionS aren't inside
        of it
        """
        (h, w) = self.midle
        shape = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        start_y = h - (len(shape) // 2)
        start_x = w - (len(shape[0]) // 2)
        temp_watermark = []
        for y_idx, row in enumerate(shape):
            for x_idx, val in enumerate(row):
                if val == 1:
                    temp_watermark.append((start_x + x_idx, start_y + y_idx))
        self.watermark = []
        if self.params.height > 10 and self.params.width > 12:
            ent = (
                int(self.params.en_pos[0]),
                int(self.params.en_pos[1])
                )
            sal = (
                int(self.params.ex_pos[0]),
                int(self.params.ex_pos[1])
                )
            entry_exit = {ent, sal}
            intersection = entry_exit.intersection(temp_watermark)
            if not intersection:
                self.watermark = temp_watermark
                for x, y in self.watermark:
                    self.grid[y][x].visited = True
            else:
                self.watermark = []

    def createMaze(self) -> None:
        """
        Removes the walls between two adjacent cells.
        """
        def deleteWalls(currentCell: Cell, nextCell: Cell) -> None:
            (xCurrent, yCurrent) = currentCell.position
            (xNext, yNext) = nextCell.position
            if xCurrent > xNext:
                if "Left" in currentCell.walls:
                    currentCell.walls.remove("Left")
                if "Right" in nextCell.walls:
                    nextCell.walls.remove("Right")
            elif xCurrent < xNext:
                if "Right" in currentCell.walls:
                    currentCell.walls.remove("Right")
                if "Left" in nextCell.walls:
                    nextCell.walls.remove("Left")
            elif yCurrent > yNext:
                if "Bottom" in nextCell.walls:
                    nextCell.walls.remove("Bottom")
                if "Top" in currentCell.walls:
                    currentCell.walls.remove("Top")
            elif yCurrent < yNext:
                if "Top" in nextCell.walls:
                    nextCell.walls.remove("Top")
                if "Bottom" in currentCell.walls:
                    currentCell.walls.remove("Bottom")

        def canContinueMoving(cellPos: tuple[int, int]) -> list[Cell]:
            """
            Get a list of adjacent cells that have not been visited yet.

            cellPos: The position of the current cell.
            """
            (x, y) = cellPos
            possibilities = []
            if y < self.params.height - 1 and not self.grid[y+1][x].visited:
                possibilities.append(self.grid[y+1][x])
            if y > 0 and not self.grid[y-1][x].visited:
                possibilities.append(self.grid[y-1][x])
            if x < self.params.width - 1 and not self.grid[y][x+1].visited:
                possibilities.append(self.grid[y][x+1])
            if x > 0 and not self.grid[y][x-1].visited:
                possibilities.append(self.grid[y][x-1])
            return possibilities

        def deleteRandomWalls(
                grid: list[Any],
                width: int,
                height: int
                ) -> None:
            """
            Remove random additional walls from the maze, creating loops
            (When the maze is not required to be perfect)
            """
            number_of_walls_to_remove = int(width * height * 0.15)
            while number_of_walls_to_remove != 0:
                row: list[Cell] = random.choice(grid)
                cell: Cell = random.choice(row)
                if len(cell.walls) < 4 and len(cell.walls) != 0:
                    (x, y) = cell.position
                    possibilities = []
                    if y < height - 1 and len(grid[y+1][x].walls) < 4:
                        possibilities.append(grid[y+1][x])
                    if y > 0 and len(grid[y-1][x].walls) < 4:
                        possibilities.append(grid[y-1][x])
                    if x < width - 1 and len(grid[y][x+1].walls) < 4:
                        possibilities.append(grid[y][x+1])
                    if x > 0 and len(grid[y][x-1].walls) < 4:
                        possibilities.append(grid[y][x-1])
                    if len(possibilities) != 0:
                        deleteWalls(cell, random.choice(possibilities))
                        number_of_walls_to_remove -= 1

        _visitedCells = []
        _currentCell = self.grid[self.params.en_pos[1]][self.params.en_pos[0]]
        _visitedCells.append(_currentCell)
        _currentCell.visited = True
        while _visitedCells:
            possibilities = canContinueMoving(_currentCell.position)
            if len(possibilities) != 0\
                    and _currentCell.position != tuple(self.params.ex_pos):
                _nextCell = random.choice(possibilities)
                deleteWalls(_currentCell, _nextCell)
                _currentCell = _nextCell
                _currentCell.visited = True
                _visitedCells.append(_currentCell)
            else:
                _currentCell.visited = True
                _visitedCells.pop(-1)
                if _visitedCells:
                    _currentCell = _visitedCells[-1]

        if not self.params.perfect:
            deleteRandomWalls(self.grid, self.params.width, self.params.height)

    def solve(self) -> list[tuple[int, int]]:
        """
        Solve the maze with breadth-first search
        and return path from entry to exit
        """
        start = tuple(self.params.en_pos)
        goal = tuple(self.params.ex_pos)

        queue = [start]
        parent_map: dict[Any, Any] = {}
        parent_map[start] = None
        while queue:
            current = queue.pop(0)
            if current == goal:
                break
            x, y = current
            cell = self.grid[y][x]
            neighbors = [
                ((x, y - 1), "Top"),
                ((x + 1, y), "Right"),
                ((x, y + 1), "Bottom"),
                ((x - 1, y), "Left")
            ]
            for (nx, ny), wall in neighbors:
                if 0 <= nx < self.params.width\
                        and 0 <= ny < self.params.height:
                    if wall not in cell.walls and (nx, ny) not in parent_map:
                        parent_map[(nx, ny)] = current
                        queue.append((nx, ny))
        path = []
        step: Any = goal
        while step is not None:
            path.append(step)
            step = parent_map.get(step)
        self.solution: list[tuple[int, int]] = path[::-1]
        return self.solution

    def export(self, output: Any) -> None:
        """
        Exports the maze structure, entry/exit, and solution
        """
        for row in self.grid:
            for cell in row:
                cell.printCell(output)
            print(file=output)
        print(file=output)
        (x, y) = (self.params.en_pos)
        print(f"{x}, {y}", file=output)
        (x, y) = (self.params.ex_pos)
        print(f"{x}, {y}", file=output)
        solution: list[tuple[int, int]] = self.solve()
        previous: tuple[int, int] = solution[0]
        for (x, y) in solution:
            px, py = previous
            if py > y:
                print("N", end='', file=output)
            elif py < y:
                print("S", end='', file=output)
            elif px > x:
                print("W", end='', file=output)
            elif px < x:
                print("E", end='', file=output)
            previous = (x, y)

    def printMap(self, bool_solve: bool) -> None:
        """
        prints the maze in the terminal
        """
        if not hasattr(self, 'solution'):
            self.solution = []
        draw_path = self.solution if bool_solve else []

        WALL = f"{Color.gray}██{Color.reset}"
        PATH = f"{Color.green}██{Color.reset}"
        START = f"{Color.red}██{Color.reset}"
        EXIT = f"{Color.red}██{Color.reset}"
        MARK = f"{Color.blue}██{Color.reset}"
        EMPTY = "  "
        watermark_coords = getattr(self, 'watermark', [])

        for y in range(self.params.height):
            top_line = ""
            for x in range(self.params.width):
                top_line += WALL
                if "Top" not in self.grid[y][x].walls\
                        and (x, y) in draw_path\
                        and (x, y - 1) in draw_path:
                    top_line += PATH
                else:
                    if "Top" in self.grid[y][x].walls:
                        top_line += WALL
                    else:
                        top_line += EMPTY
            print(top_line + WALL)
            mid_line = ""
            for x in range(self.params.width):
                if "Left" not in self.grid[y][x].walls\
                        and (x, y) in draw_path\
                        and (x - 1, y) in draw_path:
                    mid_line += PATH
                else:
                    if "Left" in self.grid[y][x].walls:
                        mid_line += WALL
                    else:
                        mid_line += EMPTY

                pos = (x, y)
                if pos == tuple(self.params.en_pos):
                    mid_line += START
                elif pos == tuple(self.params.ex_pos):
                    mid_line += EXIT
                elif pos in watermark_coords:
                    mid_line += MARK
                elif pos in draw_path:
                    mid_line += PATH
                else:
                    mid_line += EMPTY
            print(mid_line + WALL)

        print(WALL * (self.params.width * 2 + 1))


def clear() -> None:
    os.system('clear' if os.name == 'posix' else 'cls')


def main() -> None:
    """
    Controls the number of args received and executes the program in order,
    including the reauired menu controlled by options.
    """

    if len(sys.argv) == 1:
        print(
            f"{Color.red}Error:{Color.reset} Configuration file not"
            f" specified, expected: a_maze_ing.py {Color.green} <filename>"
            f" {Color.reset}"
            )
    elif len(sys.argv) != 2:
        print(
            f"{Color.red}Error:{Color.reset} Too many arguments. "
            f"Expected: a_maze_ing.py {Color.green} <filename> {Color.reset}"
            )
    else:
        try:
            parameters = Parameters.read_config(sys.argv[1])
            if not parameters:
                return

            random.seed(parameters.seed)
            maze = MazeGenerator(parameters)
            maze.print_forty_two()
            maze.createMaze()
            with open(parameters.output_filename, mode="w+") as output:
                maze.export(output)
            bool_solve = False
            bool_color: int = 0
            color_list = ["\033[33m", "\033[35m", "\033[90m", "\u001b[37m"]
            o_solution = "Show solution"
            while True:
                clear()
                maze.printMap(bool_solve)
                print(
                    f"\n{Color.white}=== A-Maze-ing ==={Color.reset} \n"
                    f"\nSeed: {Color.green}{maze.params.seed}{Color.reset}\n"
                    f"\n{Color.green}1{Color.reset} - {o_solution}"
                    f"\n{Color.green}2{Color.reset} - Change color"
                    f"\n{Color.green}3{Color.reset} - Regenerate"
                    f"\n{Color.green}4{Color.reset} - Exit"
                )
                option = input("\nOption: ").lower()
                if option == '1':
                    if not hasattr(maze, 'solution')\
                            or len(maze.solution) == 0:
                        maze.solve()
                    if not bool_solve:
                        o_solution = "Hide solution"
                    else:
                        o_solution = "Show solution"
                    bool_solve = not bool_solve
                elif option == '2':
                    Color.gray = color_list[bool_color % len(color_list)]
                    bool_color += 1
                elif option == '3':
                    parameters.seed = random.randint(1, 9999)
                    random.seed(parameters.seed)
                    maze = MazeGenerator(parameters)
                    maze.print_forty_two()
                    maze.createMaze()
                    with open(parameters.output_filename, mode="w+") as out:
                        maze.export(out)
                    bool_solve = False
                    o_solution = "Show solution"
                elif option == "4":
                    break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
