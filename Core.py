import time
import win32api
import win32con
import win32gui

from datetime import datetime
from Locs import *

nan = 'NaN'
os_sep = "\\"


class Host:
    x = 0
    y = 110
    loc = Point(x, y)
    width_pad = 14
    height_pad = 7

    right_offset = 0
    scroll_location = Point(0, 0)

    # full_screen = Rect(0, 0, 1364, 1245)
    full_screen = Rect(0, 0, 1375 - width_pad, 1254 - height_pad)
    dead_click = Point(466, 13)
    dead_click2 = Point(Locs.friends_forward_button.x + 30, full_screen.height - 10)


def rectToScreen(rect):
    x = rect.x + Host.x
    y = rect.y + Host.y
    return Rect(x, y, x + rect.width, y + rect.height)


##### OS #####
def resizeWindow(hwnd, rect):
    win32gui.MoveWindow(hwnd, rect.x - 7, rect.y,
                        rect.width + Host.x + Host.width_pad, rect.height + Host.y + Host.height_pad, true)


def wait(duration):
    time.sleep(duration)


##### Ix #####
def click(point):
    setMouseLoc(point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    wait(.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    wait(.1)


def slowClick(point, sec=2):
    click(point)
    wait(sec)


def verySlowClick(point):
    slowClick(point, 5)


def deadClick(sec=.1):
    click(Host.dead_click)
    wait(sec)


def deadClick2(sec=.1):
    click(Host.dead_click2)
    wait(sec)


def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    wait(.01)


def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    wait(.01)


def drag(point_from, point_to):
    setMouseLoc(point_from)
    leftDown()
    wait(.1)

    iterations = 20
    x_offset = (point_to.x - point_from.x)/iterations
    y_offset = (point_to.y - point_from.y)/iterations
    point = point_from
    for i in range(iterations):
        point = Point(point.x + x_offset, point.y + y_offset)
        setMouseLoc(point)
        wait(.1)

    wait(1)
    leftUp()
    wait(.1)


def dragScreen(offset):
    deadClick2()
    point = Point(1200 if (offset.width < 0) else 200, 1200 if (offset.height < 0) else 200)
    finish_point = Point(point.x + offset.width, point.y + offset.height)
    drag(point, finish_point)


def setMouseLoc(point):
    win32api.SetCursorPos((int(Host.x + point.x), int(Host.y + point.y)))


def getMouseLoc(p=true, include_scroll=false):
    x, y = win32api.GetCursorPos()
    # x = x - Host.x
    # y = y - Host.y

    point = Point(x, y) - Host.loc
    if(include_scroll): point += Host.scroll_location

    if p: print(point.codeString())
    return point


def getMouseLocFast():
    for i in range(100):
        getMouseLoc()
        wait(.1)


def getRect(p=true):
    wait(.5)
    top_left = getMouseLoc()
    wait(5)
    bottom_right = getMouseLoc()
    rect = pointsToRect(top_left, bottom_right)
    if p: print('(' + str(rect.x) + ', ' + str(rect.y) + ', ' + str(rect.width) + ', ' + str(rect.height))
    return rect


def pointForRightOffset(point):
    return Point(point.x + Host.right_offset, point.y)


def pointForScroll(point):
    return point - Host.scroll_location


##### Logging #####
class Logging:
    def log(text: str) -> None:
        print(f"{Logging.time(true)}: {text}")

    def warning(text: str) -> None:
        print(f"---- {text}")

    def time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
