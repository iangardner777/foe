host_x = 0
host_y = 110
host_width_pad = 14
host_height_pad = 7

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if(index == 0):
            return self.x
        return self.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __getitem__(self, index):
        if(index == 0):
            return self.width
        return self.height

    def __str__(self):
        return "({0}, {1})".format(self.width, self.height)

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __getitem__(self, index):
        if(index == 0):
            return self.x
        elif(index == 0):
            return self.y
        elif(index == 0):
            return self.width
        return self.height

    def fromTuple(tuple):
        return Rect(tuple[0], tuple[1], tuple[2], tuple[3])

    def __str__(self):
        return  "[{0}, {1}]".format(self.loc(), self.size())

    def loc(self):
        return Point(self.x, self.y)

    def size(self):
        return Size(self.width, self.height)


def pointToRect(point, size=100):
    return (point[0] - size/2, point[1] - size/2, size, size)

def pointsToRect(topLeft, bottomRight):
    return (topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])

def rectToScreen(rect):
    x = rect[0] + host_x
    y = rect[1] + host_y
    return (x, y, x + rect[2], y + rect[3])

def rectMiddle(rect):
    return (rect[0] + rect[2]/2, rect[1] + rect[3]/2)

def rectPlusX(rect, x):
    return (rect[0] + x, rect[1], rect[2], rect[3])

def rectExpand(rect, x):
    return (rect[0] - x, rect[1] - x, rect[2] + x*2, rect[3] + x*2)


# box = Rect(Point(0, 0), 100, 200)
# bomb = Rect(Point(100, 80), 5, 10)    # In my video game
# print("box: ", box)
# print("bomb: ", bomb)