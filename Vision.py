from Core import *
from Colors import *

import os
from PIL import ImageGrab, ImageOps
from numpy import *

nan = 'NaN'


##### Computer Vision #####
def screenShot(rect):
    return ImageGrab.grab(rectToScreen(rect).toTuple())


def fullScreenShot():
    return screenShot(Host.full_screen)


def saveFullScreenShot(text):
    saveImage(fullScreenShot(), text)


def saveImage(image, text, with_time=true):
    name = os.getcwd() + os_sep + str(text)
    if with_time: name += '__' + str(int(time.time()))
    name += '.png'
    image.save(name, 'PNG')


def saveScreenRect(rect, expand, text, image_text, folder='', miss=false):
    if miss:
        text = 'MISS! ' + text
        image_text = 'MISS-' + image_text
    print(text)

    if folder != '': image_text = str(folder) + os_sep + image_text
    if expand != -1: rect = rectExpand(rect, expand)
    saveImage(screenShot(rect), image_text)


def trackPixelHorizontal(loc, rgb, image):
    for i in range(-50, 50):
        new_loc = Point(loc.x + i, loc.y)
        pixel = image.getpixel(new_loc.toTuple())
        if pixel == rgb: return i
    return nan


def findPixel(loc, rgb, image):
    pixel = findPixelHelper(loc, rgb, image, 20)
    if pixel != nan:
        print("Found pixel on first attempt: ", pixel)
        return pixel

    pixel = findPixelHelper(loc, rgb, image, 50)
    if pixel != nan:
        print("Found pixel on second attempt: ", pixel)
        return pixel

    pixel = findPixelHelper(loc, rgb, image, 100)
    if pixel != nan:
        print("Found pixel on third attempt: ", pixel)
        return pixel
    return nan


def findPixelHelper(loc, rgb, image, r):
    for i in range(-r, r):
        for j in range(-r, r):
            new_loc = Point(loc.x + i, loc.y + j)
            pixel = image.getpixel(new_loc.toTuple())
            if pixel == rgb: return new_loc
    return nan


def getColorAt(loc, image=None):
    if image == None:
        image = screenShot(Rect(loc.x, loc.y, 1, 1))
        return image.getpixel((0, 0))
    return image.getpixel(loc.toTuple())


def saveLocToColor(key):
    loc = mouseLoc()
    mousePos(Host.dead_click)
    wait(3)
    # loc = Colors.loc_to_color[key][0]
    color = getColorAt(loc)

    key_name = Colors.nameOf(key)
    print(key_name, ":", (loc, color))

    wait(4)
    color = getColorAt(loc)
    print(key_name, ":", (loc, color))


def getColorSum(rect, i='default', debug=false, save=false):
    image = screenShot(rect)
    gray_image = ImageOps.grayscale(image)
    image_sum = array(gray_image.getcolors()).sum()
    if debug:
        saveImage(image, str(i) + '__' + str(image_sum))
        print(i, rect, image_sum)
    if save:
        saveImage(image, "ImageSums" + os_sep + str(i) + '__' + str(image_sum), false)
    return image_sum


def saveColorSum(key):
    getColorSum(Colors.sums[key][0], key, false, true)


def confirmColorSum(key):
    rect_and_sum = Colors.sums[key]
    return getColorSum(rect_and_sum[0]) == rect_and_sum[1]


def closeBluePrintIfNecessary():
    color = getColorAt(Locs.blueprint_close)
    if color == Colors.blueprint_close or color == Colors.blueprint_close_2:
        slowClick(Locs.blueprint_close)
        return true


def closeIncidentIfNecessary():
    if getColorAt(Locs.incident_ok) == Colors.incident_ok:
        slowClick(Locs.incident_ok)
        closeBluePrintIfNecessary()
        return true


def clickButton(key, attempts=2):
    if attempts < 1: return false
    loc = Colors.loc_to_color[key][0]
    color = Colors.loc_to_color[key][1]

    if getColorAt(loc) == color:
        slowClick(loc)
        return true

    print("Missed button:", key, "-- attemptsLeft: ", attempts - 1)
    if attempts > 1:
        wait(2)
        return clickButton(key, attempts - 1)
    return false