from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int

    def inside(self, width: int, height: int) -> bool:
        return (0 <= self.x < width) and (0 <= self.y < height)


class Direction:
    offset_x: int = 0
    offset_y: int = 0

    def __init__(self):
        raise NotImplementedError()

    def __call__(self, pos: Pos) -> Pos:
        return Pos(x=pos.x + self.offset_x, y=pos.y + self.offset_y)


@dataclass
class Left(Direction):
    offset_x = -1


@dataclass
class Right(Direction):
    offset_x = 1


@dataclass
class Up(Direction):
    offset_y = -1


@dataclass
class Down(Direction):
    offset_y = 1


@dataclass
class SimplifiedMove:
    pos: Pos
    direction: Union[Right, Down]


@dataclass
class Move:
    pos: Pos
    direction: Direction

    def valid_move(self, width: int, height: int) -> bool:
        return self.pos.inside(width=width, height=height) and self.direction(
            self.pos
        ).inside(width=width, height=height)

    def simplify(self) -> SimplifiedMove:
        if isinstance(self.direction, Left):
            return Move(pos=self.direction(self.pos), direction=Right())
        elif isinstance(self.direction, Up):
            return Move(pos=self.direction(self.pos), direction=Down())
        return self


@dataclass
class Cell:
    is_right_set: bool = False
    is_down_set: bool = False
    who_set_last: Optional[int] = None

    def set_right(self, who: int):
        self.is_right_set = True
        self.who_set_last = who

    def set_down(self, who: int):
        self.is_down_set = True
        self.who_set_last = who


@dataclass
class Board:
    width: int
    height: int
    board: List[List[Cell]]

    def __init__(self, width: int, height: int) -> "Board":
        self.width = width
        self.height = height
        self.board = [[Cell()] * width for _ in range(height)]

    def make_move(self, move: Move, who: int) -> Optional["Board"]:
        if move.valid_move(width=self.width, height=self.height):
            simple_move = move.simplify()
            x, y = simple_move.pos.x, simple_move.pos.y
            if isinstance(simple_move.direction, Right):
                self.board[y][x].set_right(who=who)
            else:
                self.board[y][x].set_down(who=who)
            return self
        else:
            return None
