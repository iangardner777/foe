class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toTuple(self):
        return self.x, self.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def toTuple(self):
        return self.width, self.height

    def __str__(self):
        return "({0}, {1})".format(self.width, self.height)


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def toTuple(self):
        return self.x, self.y, self.width, self.height

    def __str__(self):
        return "[{0}, {1}]".format(self.loc(), self.size())

    def loc(self):
        return Point(self.x, self.y)

    def size(self):
        return Size(self.width, self.height)


def pointToRect(point, size=100):
    return Rect(point.x - size/2, point.y - size/2, size, size)


def pointsToRect(top_left, bottom_right):
    return Rect(top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)


def rectMiddle(rect):
    return Point(rect.x + rect.width/2, rect.y + rect.height/2)


def rectPlusX(rect, x):
    return Rect(rect.x + x, rect.y, rect.width, rect.height)


def rectExpand(rect, x):
    return Rect(rect.x - x, rect.y - x, rect.width + x*2, rect.height + x*2)