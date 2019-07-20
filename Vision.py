from Core import *
from Colors import *

import os
from PIL import Image
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


def getColorSumObsolete(rect, i='default', debug=false, save=false):
    image = screenShot(rect)
    gray_image = ImageOps.grayscale(image)
    colors = gray_image.getcolors()
    arr = array(colors)
    image_sum = arr.sum()
    if debug:
        saveImage(image, str(i) + '__' + str(image_sum))
        print(i, rect, image_sum)
    if save:
        saveImage(image, "ImageSums" + os_sep + str(i) + '__' + str(image_sum), false)
    return image_sum


def getColorSum(rect, i='default', debug=false, save=false):
    image = screenShot(rect)
    gray_image = ImageOps.grayscale(image)
    colors = gray_image.getcolors()
    arr = array(colors)
    image_sum = 0

    for a in arr:
        image_sum = image_sum + a[0]*a[1]

    if debug:
        saveImage(image, str(i) + '__' + str(image_sum))
        print(i, rect, image_sum)
    if save:
        saveImage(image, "ImageSums" + os_sep + str(i) + '__' + str(image_sum), false)
    return image_sum


def saveColorSum(key):
    getColorSumObsolete(Colors.sums[key][0], key, false, true)


def confirmColorSum(key, printMiss=false):
    rect_and_sums = Colors.sums[key]
    sum = getColorSumObsolete(rect_and_sums[0])

    values = ""
    for i in range(1, len(rect_and_sums)):
        if sum == rect_and_sums[i]:
            return true
        values = f"{values}{'' if i == 1 else ','}{rect_and_sums[i]}"

    if printMiss:
        Logging.warning(f"Color sum miss: {key} - {sum} - values:{values}")

    return false


def ensureButton(key, attempts=2, log=false, search=false):
    if attempts < 1: return false

    loc_and_color = Colors.loc_and_color[key]
    loc = loc_and_color[0]
    color = loc_and_color[1]
    #image = screenShot(Rect(loc.x, loc.y, 1, 1))
    image = fullScreenShot()
    screen_color = getColorAt(loc, image)
    #if screen_color.isVeryClose(color, true):
    if screen_color.isClose(color):
        return true

    if search:
        loc.y -= 20
        for i in range(40):
            screen_color = getColorAt(loc, image)
            if screen_color.isVeryClose(color, true):
                return true
            loc.y += 1

    if log:
        Logging.warning(f"Missed button: {key} -- attemptsLeft: {attempts - 1} -- {color.toString()} : {loc_and_color[1].toString()}")
    if attempts > 1:
        wait(2)
        return ensureButton(key, attempts - 1, log)
    return false


def clickButton(key, attempts=2, log=false, picture=None, search=false):
    if ensureButton(key, attempts, log, search):
        if picture is not None:
            saveFullScreenShotToFolder(picture)

        slowClick(Colors.loc_and_color[key][0])
        return true
    return false


def clickButtonIfNecessary(key, picture=None):
    return clickButton(key, 1, false, picture)


def checkForButton(key, search):
    return ensureButton(key, 1, false, search)


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


def read_text(rect, image, treated=true):
    # rect = getRect()
    # rect = Rect(13, 156, 261, 17)
    # rect = Locs.friend_tavern_name_rect

    # image = screenShot(rect)

    # saveImage(image, "test_full")
    image = image.crop(rect.toSystemTuple())
    # saveImage(image, 'test')

    img = Image.new(image.mode, image.size)
    pixelMap = image.load()
    pixelsNew = img.load()

    thresh = 150
    thresh2 = 200

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixelMap[i, j]
            # if pixel[0] > thresh and pixel[1] > thresh and pixel[2] > thresh and sum(pixel) > thresh2*3:
            if pixel[0] > thresh2 and pixel[1] > thresh2 and pixel[2] > thresh2:
                pixelsNew[i, j] = (0, 0, 0)
            elif pixel[0] > thresh and pixel[1] > thresh and pixel[2] > thresh:
                pixelsNew[i, j] = (128, 128, 128)
            else:
                pixelsNew[i, j] = (255, 255, 255)
    #img.show()

    # saveImage(img, 'test_treated')

    # text1 = image_to_string(image, config=' -psm 7 foe_quest_names.txt')
    # Log.print(text)
    text = image_to_string(img, config=' -psm 7 foe_quest_names.txt')
    # Log.print(text)

    image.close()
    img.close()
    # pixelMap.close()
    # pixelsNew.close()
    return text


def save_image_live():
    # rect = getRect()
    # image = screenShot(rect)

    image = Image.open("data/test.png")
    saveImage(image, 'test2')


pixels_large = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
                (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
                (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]

pixels_small = [(0, 0), (1, 0), (2, 0), (3, 0),
                (0, 1), (1, 1), (2, 1), (3, 1),
                (0, 2), (1, 2), (2, 2), (3, 2),
                (0, 3), (1, 3), (2, 3), (3, 3)]


def find_image(screen, image, point, large=false):
    screen_map = screen.load()
    image_map = image.load()

    pixels_to_check = pixels_large if large else pixels_small

    offset = 50
    r = (range(max(point.x - offset, 0), point.x + offset), range(max(point.y - offset, 0), point.y + offset))
    for i in r[0]:
        for j in r[1]:
            found = true

            pixels_found = 0

            for k in pixels_to_check:
                screen_pixel = Color.fromTuple(screen_map[i + k[0], j + k[1]])
                image_pixel = Color.fromTuple(image_map[k[0], k[1]])
                if not screen_pixel.isVeryClose(image_pixel):
                    found = false
                    break
                else:
                    pixels_found += 1

            # print(f"Pixels found: {pixels_found}")

            if found:
                # screen_map.close()
                # image_map.close()
                return Point(i, j)

    # screen_map.close()
    # image_map.close()
    return INVALID_LOC


def pixels_to_image():
    img = Image.new('RGB', (6, 6))

    pass


def find_image_test(screen, image, point):
    screen_map = screen.load()
    image_map = image.load()

    # pixels_to_check = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    #                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    #                    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
    #                    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
    #                    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
    #                    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]

    pixels_to_check = [(0, 0), (1, 0), (2, 0), (3, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1),
                       (0, 2), (1, 2), (2, 2), (3, 2),
                       (0, 3), (1, 3), (2, 3), (3, 3)]

    # saveImage(image, "test")

    img = Image.new('RGB', (4, 4))
    img_pixels = img.load()
    for k in pixels_to_check:
        img_pixels[k[0], k[1]] = image_map[k[0], k[1]]

    # saveImage(image, "test")
    saveImage(img, "test2")

    offset = 200
    r = (range(max(point.x - offset, 0), point.x + offset), range(max(point.y - offset, 0), point.y + offset))
    for i in r[0]:
        for j in r[1]:
            found = true

            pixels_found = 0
            screen_test_image = Image.new('RGB', (4, 4))
            screen_test_pixels = screen_test_image.load()

            for k in pixels_to_check:
                screen_test_pixels[k[0], k[1]] = screen_map[i + k[0], j + k[1]]

                screen_pixel = Color.fromTuple(screen_map[i + k[0], j + k[1]])
                image_pixel = Color.fromTuple(image_map[k[0], k[1]])
                if not screen_pixel.isClose(image_pixel):
                    found = false
                    # break
                else:
                    pixels_found += 1

            if pixels_found > 6:
                print(f"Pixels found: {pixels_found}")
                saveImage(screen_test_image, f"{i}x{j}")
                getMouseLoc()
                pass

            # print(f"Pixels found: {pixels_found}")
            # saveImage(screen_test_image, f"{i}x{j}")

            if found:
                return Point(i, j)

    return INVALID_LOC


markers_folder = "data/markers/"


def save_marker(marker, point=INVALID_LOC, ref_point=Point(0, 0), variance=Point(20, 20)):
    if point == INVALID_LOC:
        point = getMouseLoc()
    set_safe_mouse_loc()
    rect = point.withSize(Size(20, 20))
    image = screenShot(rect)
    saveImage(image, f"{markers_folder}{marker}", false)
    save_marker_info(marker, point - ref_point, ref_point, variance)


def save_marker_info(marker, point, offset, variance):
    file = open(f"{markers_folder}{marker}.txt", "w+")
    file.write(f"{marker}:{point}:{offset}:{variance}")
    Log.print(f"Saving: {marker}:{point}:{offset}:{variance}")


def save_marker_from(marker, ref_point=INVALID_LOC, ref_marker=None):
    if ref_point == INVALID_LOC and ref_marker is not None:
        ref_point = find_marker(ref_marker)

    point = getMouseLoc()
    save_marker(marker, point, ref_point)


def copy_marker(marker, ref_marker):
    point, offset, variance = load_marker_info(ref_marker)

    save_marker(marker, point, offset, variance)


def copy_marker_from(marker, ref_marker, ref_point):
    point, offset, variance = load_marker_info(ref_marker)

    save_marker(marker, point + ref_point, ref_point, variance)


def load_marker_info(marker):
    file = open(f"{markers_folder}{marker}.txt", "r")
    line = file.readline()
    marker_info = line.strip("\n").split(":")

    point = INVALID_LOC.fromString(marker_info[1])
    offset = INVALID_LOC.fromString(marker_info[2])
    variance = INVALID_LOC.fromString(marker_info[3])
    file.close()
    return point, offset, variance


def find_marker_full(marker, screen=None, ref_point=Point(0, 0), large=false, debug=false):
    if screen is None:
        screen = fullScreenShot()
    point, offset, variance = load_marker_info(marker)
    point += ref_point

    image = Image.open(f"{markers_folder}{marker}.png")

    if debug:
        real_point = find_image_test(screen, image, point)
    else:
        real_point = find_image(screen, image, point, large)

    # print(f"{point} :: {real_point}")
    image.close()
    return real_point, offset, variance


def find_marker(marker, screen=None, ref_point=Point(0, 0), large=false, debug=false):
    return find_marker_full(marker, screen, ref_point, large, debug)[0]


def click_marker(marker):
    pass