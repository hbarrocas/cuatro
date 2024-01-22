from random import randint
from copy import deepcopy

WELL_WIDTH = 9
WELL_DEPTH = 22

""" Event IDs """
EV_SHAPE_CHANGE = 1
EV_SHAPE_DROP = 2
EV_WELL_CHANGE = 3
EV_SCORE_CHANGE = 4
EV_STATUS_CHANGE = 5
EV_GAME_OVER = 6
EV_GAME_WON = 7
EV_GAME_ABORT = 8
EV_MENU_CHANGE = 9
EV_KEY_PRESS = 10
EV_CORE_EXIT = 11
EV_TIMER1 = 12
EV_TIMER2 = 13


class EventBus:
    _events = {}

    def subscribe(self, ev_id: int, callback):
        if ev_id not in self._events:
            self._events[ev_id] = []
        self._events[ev_id].append(callback)

    def unsubscribe(self, ev_id: int, callback):
        if ev_id not in self._events:
            return
        if callback not in self._events[ev_id]:
            return
        self._events[ev_id].remove(callback)

    def publish(self, ev_id: int, *args, **kwargs):
        if ev_id in self._events:
            return [cb(*args, **kwargs) for cb in self._events[ev_id]]
        print(f"{ev_id} event does not have any subscribers")


class Position:
    """ A position class that supports algebraic operations """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y)

    def __sub__(self, pos):
        return Position(self.x - pos.x, self.y - pos.y)

    def __mul__(self, scalar: int):
        return Position(self.x * scalar, self.y * scalar)

    def __eq__(self, pos):
        return self.x == pos.x and self.y == pos.y

    def __str__(self):
        return f"pos({self.x}, {self.y})"


class Brick:
    """ A tetris brick - binds a position to a type of brick """

    def __init__(self, pos, attr: int):
        self.pos = pos
        self.attr = attr

    def __str__(self):
        return f"brick[{self.pos}, attr={self.attr}]"


class Shape:
    """ A tetris shape class. Each instance creates a random shape """
    _attr = 0
    _dir = 0
    _map = None

    def __init__(self):
        shapes = [
            [
                [(2, 0), (2, 1), (2, 2), (2, 3)],
                [(0, 2), (1, 2), (2, 2), (3, 2)],
                [(2, 0), (2, 1), (2, 2), (2, 3)],
                [(0, 2), (1, 2), (2, 2), (3, 2)],
            ],
            [
                [(1, 0), (1, 1), (1, 2), (2, 2)],
                [(0, 2), (1, 2), (2, 2), (2, 1)],
                [(1, 1), (2, 1), (2, 2), (2, 3)],
                [(1, 1), (2, 1), (3, 1), (1, 2)]
            ],
            [
                [(2, 0), (2, 1), (2, 2), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (2, 2)],
                [(1, 1), (2, 1), (1, 2), (1, 3)],
                [(1, 1), (1, 2), (2, 2), (3, 2)]
            ],
            [
                [(1, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (0, 1), (1, 1), (1, 2)],
                [(1, 2), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (2, 1), (1, 2)]
            ],
            [
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)]
            ],
            [
                [(0, 1), (1, 1), (1, 2), (2, 2)],
                [(2, 0), (1, 1), (2, 1), (1, 2)],
                [(0, 1), (1, 1), (1, 2), (2, 2)],
                [(2, 0), (1, 1), (2, 1), (1, 2)]
            ],
            [
                [(1, 1), (2, 1), (0, 2), (1, 2)],
                [(1, 0), (1, 1), (2, 1), (2, 2)],
                [(1, 1), (2, 1), (0, 2), (1, 2)],
                [(1, 0), (1, 1), (2, 1), (2, 2)]
            ]
        ]
        shape = randint(0, len(shapes) - 1)
        self._map = deepcopy(shapes[shape])
        self._attr = shape
        self._dir = randint(0, 3)

    def rot_left(self):
        self._dir = (self._dir - 1) & 3

    def rot_right(self):
        self._dir = (self._dir + 1) & 3

    def get_map(self):
        def translate(p):
            x, y = p
            return Brick(Position(x, y), self._attr)
        return map(translate, self._map[self._dir])

    def __str__(self):
        m = [str(p) for p in self.get_map()]
        return f"shape{m}"


class Core:
    points = 0
    lines = 0
    level = 0
    _well = []
    _shape_pos = None
    _shape_current = None
    _shape_next = None
    _ev_bus = None

    def __init__(self, ev_bus):
        self._shape_next = Shape()
        self._ev_bus = ev_bus

    def step(self):
        if self._shape_current is None:
            self.fetch_shape()
            self._ev_bus.publish(EV_SHAPE_CHANGE, self._shape_next.get_map())
            if not self.shape_fits_at(self._shape_pos):
                self._ev_bus.publish(EV_GAME_OVER, [
                    self.points,
                    self.lines,
                    self.level
                ])
        next_pos = self._shape_pos + Position(0, 1)
        if self.shape_fits_at(next_pos):
            self._shape_pos = next_pos
            self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())
            return

        self._well = list(self.get_shape_at(self._shape_pos)) + self._well
        self.points += 2
        lines = self.scan_lines()
        self._ev_bus.publish(EV_SHAPE_DROP, lines)
        self.remove_lines(lines)
        self._shape_current = None
        self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())
        self.lines += len(lines)
        self.level = self.lines // 10
        if self.level == 10:
            self._ev_bus.publish(EV_GAME_WON, [
                self.points,
                self.lines,
                self.level
            ])
        self.points += 10 * (len(lines) ** 2)
        self._ev_bus.publish(EV_SCORE_CHANGE, [
            self.points,
            self.lines,
            self.level
        ])

    def rot_left(self):
        if self._shape_current is None:
            return
        self._shape_current.rot_left()
        if self.shape_fits_at(self._shape_pos):
            self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())
            return
        self._shape_current.rot_right()

    def rot_right(self):
        if self._shape_current is None:
            return
        self._shape_current.rot_right()
        if self.shape_fits_at(self._shape_pos):
            self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())
            return
        self._shape_current.rot_left()

    def left(self):
        if self._shape_current is None:
            return
        next_pos = self._shape_pos + Position(-1, 0)
        if self.shape_fits_at(next_pos):
            self._shape_pos = next_pos
            self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())

    def right(self):
        if self._shape_current is None:
            return
        next_pos = self._shape_pos + Position(1, 0)
        if self.shape_fits_at(next_pos):
            self._shape_pos = next_pos
            self._ev_bus.publish(EV_WELL_CHANGE, self.get_map())

    def fetch_shape(self):
        self._shape_current = self._shape_next
        self._shape_next = Shape()
        self._shape_pos = Position(2, -2)

    def get_shape_at(self, position):
        def translate(brick):
            return Brick(brick.pos + position, brick.attr)
        shape = self._shape_current.get_map() if self._shape_current else []
        return map(translate, shape)

    def shape_fits_at(self, position):
        def collides(shape_brick):
            x = shape_brick.pos.x
            y = shape_brick.pos.y
            boundaries = x < 0 or x >= WELL_WIDTH or y >= WELL_DEPTH
            samespace = any(
                map(lambda b: shape_brick.pos == b.pos, self._well)
            )
            return boundaries or samespace
        return not any(map(collides, self.get_shape_at(position)))

    def scan_lines(self):
        all_lines = [0 for y in range(WELL_DEPTH)]
        for b in self._well:
            all_lines[b.pos.y] += 1
        completed = []
        for ln in range(WELL_DEPTH):
            if all_lines[ln] == WELL_WIDTH:
                completed.append(ln)
        return completed

    def remove_lines(self, lines):
        def collapse(line):
            def _collapse(b):
                if b.pos.y > line:
                    return b
                return Brick(b.pos + Position(0, 1), b.attr)
            return _collapse
        for line in lines:
            well = filter(lambda b: b.pos.y != line, self._well)
            self._well = list(map(collapse(line), well))

    def get_map(self):
        return list(self.get_shape_at(self._shape_pos)) + self._well
