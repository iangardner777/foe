from Core import *
from Colors import *

import os
from PIL import ImageOps
from numpy import *
from pytesseract import *

nan = 'NaN'


##### Computer Vision #####
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
        pixel = getColorAt(new_loc, image)
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
            pixel = getColorAt(new_loc, image)
            if pixel == rgb: return new_loc
    return nan


def getColorAt(loc, image=None):
    if image == None:
        image = screenShot(Rect(loc.x, loc.y, 1, 1))
        return Color.fromTuple(image.getpixel((0, 0)))
    return Color.fromTuple(image.getpixel(loc.toTuple()))


def saveLocToColor(key, loc=None):
    key_name = Colors.nameOf(key)
    if loc is None:
        loc = getMouseLoc(false)
        setMouseLoc(Host.dead_click)
        wait(3)
        color = getColorAt(loc)
        print(f"{key_name} : ({loc.codeString()}, {color.codeString()})")
        wait(4)
        color = getColorAt(loc)
        print(f"{key_name} : ({loc.codeString()}, {color.codeString()})")
    else:
        color = getColorAt(loc)
        print(f"{key_name} : ({loc.codeString()}, {color.codeString()})")


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


def confirmColorSum(key, printMiss=false):
    rect_and_sums = Colors.sums[key]
    sum = getColorSum(rect_and_sums[0])

    values = ""
    for i in range(1, len(rect_and_sums)):
        if sum == rect_and_sums[i]:
            return true
        values = f"{values}{'' if i == 1 else ','}{rect_and_sums[i]}"

    if printMiss:
        Logging.warning(f"Color sum miss: {key} - {sum} - values:{values}")

    return false


def ensureButton(key, attempts=2, log=false):
    if attempts < 1: return false

    loc_and_color = Colors.loc_and_color[key]
    color = getColorAt(loc_and_color[0])
    if color.isVeryClose(loc_and_color[1], true):
        return true

    if log:
        Logging.warning(f"Missed button: {key} -- attemptsLeft: {attempts - 1} -- {color.toString()} : {loc_and_color[1].toString()}")
    if attempts > 1:
        wait(2)
        return ensureButton(key, attempts - 1, log)
    return false


def clickButton(key, attempts=2, log=false, picture=None):
    if(ensureButton(key, attempts, log)):
        if picture is not None:
            saveFullScreenShotToFolder(picture)

        slowClick(Colors.loc_and_color[key][0])
        return true
    return false


def clickButtonIfNecessary(key, picture=None):
    return clickButton(key, 1, false, picture)


def checkForButton(key):
    return ensureButton(key, 1)


def checkForColor(key):
    return ensureButton(key, 1)


char_whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def readText(rect):
    image = screenShot(rect)

    #gray_image = ImageOps.grayscale(image)
    #sum = array(gray_image.getcolors()).sum()
    #saveImage(image, 'test')
    #print(f"{sum}: {image_to_string(gray_image)} -- {image_to_string(image)}")

    #return image_to_string(image, config='-oem 0 -psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz')
    return image_to_string(image, config=' -psm 7 foe_tavern_names')
    #return image_to_string(image, "eng", f"-psm 7 -c tessedit_char_whitelist={char_whitelist}")