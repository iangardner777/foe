true = True
false = False
one_hour_time = 3600
one_minute_time = 60

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toTuple(self):
        return self.x, self.y

    def toIntTuple(self):
        return int(self.x), int(self.y)

    def fromString(self, point):
        x, y = point.strip("()").split(",")
        return Point(int(x), int(y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x*other, self.y*other)

    def __truediv__(self, other):
        return Point(self.x/other, self.y/other)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def withSize(self, size):
        return Rect(self.x, self.y, size.width, size.height)

    def codeString(self):
        return f"Point{self}"


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def toTuple(self):
        return self.width, self.height

    def __eq__(self, other) -> bool:
        return self.width == other.width and self.height == other.height

    def __str__(self):
        return f"({self.width}, {self.height})"

    def codeString(self):
        return f"Size{self}"


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def toTuple(self):
        return self.x, self.y, self.width, self.height

    def toSystemTuple(self):
        return self.x, self.y, self.x + self.width, self.y + self.height

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __str__(self):
        return f"[{self.loc()}, {self.size()}]"

    def loc(self):
        return Point(self.x, self.y)

    def size(self):
        return Size(self.width, self.height)

    def withSize(self, size):
        return Rect(self.x, self.y, size.width, size.height)

    def center(self):
        return Point(self.x + self.width/2, self.y + self.height/2)

    def codeString(self):
        return f"Rect{(self.x, self.y, self.width, self.height)}"


def pointToRect(point, size=100):
    return Rect(point.x - size/2, point.y - size/2, size, size)


def pointsToRect(top_left, bottom_right):
    return Rect(top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)


def rectPlusX(rect, x):
    return Rect(rect.x + x, rect.y, rect.width, rect.height)


def rectExpand(rect, x):
    return Rect(rect.x - x, rect.y - x, rect.width + x*2, rect.height + x*2)