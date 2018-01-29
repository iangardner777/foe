import os
import time
import win32api, win32con, win32gui
from Rect import *
from Locs import *
from Colors import *

from PIL import ImageGrab, ImageOps
from numpy import *

host_x = 0
host_y = 110
host_width_pad = 14
host_height_pad = 7

right_offset = 0
game_scroll = (0, 0)

true = True
false = False
nan = 'NaN'
os_sep = "\\"

##### OS #####
def resizeWindow(hwnd, rect):
    win32gui.MoveWindow(hwnd, rect.x - 7, rect.y,
                        rect.width + host_x + host_width_pad, rect.height + host_y + host_height_pad, true)

def wait(duration):
    time.sleep(duration)

##### Ix #####    
def leftClick(point):
    mousePos(point)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def slowClick(point, time=2):
    leftClick(point)
    wait(time)
    
def verySlowClick(point):
    slowClick(point, 5)

def deadClick(time=.01):
    leftClick(Locs.dead_click)
    wait(time)

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.01)
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.01)

def drag(pointFrom, pointTo):
    mousePos(pointFrom)
    leftDown()
    wait(.1)

    iterations = 20
    x_offset = (pointTo[0] - pointFrom[0])/iterations
    y_offset = (pointTo[1] - pointFrom[1])/iterations
    point = pointFrom;
    for i in range(iterations):
        point = (point[0] + x_offset, point[1] + y_offset)
        mousePos(point)
        wait(.1)
        
    wait(1)
    leftUp()
    wait(.1)

def dragScreen(offset):
    deadClick()
    point = (1200 if(offset[0] < 0) else 200, 1200 if(offset[1] < 0) else 200)
    finishPoint = (point[0] + offset[0], point[1] + offset[1])
    drag(point, finishPoint)
    
def mousePos(point):
    win32api.SetCursorPos((int(host_x + point[0]), int(host_y + point[1])))
    
def setMousePos(point):
    win32api.SetCursorPos((int(host_x + point[0]), int(host_y + point[1])))
    
def getLoc(p=true):
    x,y = win32api.GetCursorPos()
    x = x - host_x
    y = y - host_y
    if(p): print("(" + str(x) + ", " + str(y) + ")")
    return (x, y)

def getLocFast():
    for i in range(100):
        getLoc()
        wait(.1)

def mouseLoc():
    return getLoc(false)

def getRect(p=true):
    wait(.5)
    topLeft = getLoc()
    wait(5)
    bottomRight = getLoc()
    rect = pointsToRect(topLeft, bottomRight)
    if(p): print('(' + str(rect[0]) + ', ' + str(rect[1]) + ', ' + str(rect[2]) + ', ' + str(rect[3]))
    return rect

def pointForRightOffset(point):
    return (point[0] + right_offset, point[1])

def pointForScroll(point):
    return (point[0] - game_scroll[0], point[1] - game_scroll[1])

# def pointToRect(point, size=100):
#     return (point[0] - size/2, point[1] - size/2, size, size)
#
# def pointsToRect(topLeft, bottomRight):
#     return (topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1])

def rectToScreen(rect):
    x = rect[0] + host_x
    y = rect[1] + host_y
    return (x, y, x + rect[2], y + rect[3])

# def rectMiddle(rect):
#     return (rect[0] + rect[2]/2, rect[1] + rect[3]/2)
#
# def rectPlusX(rect, x):
#     return (rect[0] + x, rect[1], rect[2], rect[3])
#
# def rectExpand(rect, x):
#     return (rect[0] - x, rect[1] - x, rect[2] + x*2, rect[3] + x*2)

##### Computer Vision #####
def screenShot(rect):
    return ImageGrab.grab(rectToScreen(rect))

def fullScreenShot():
    return screenShot(Locs.full_screen)

def saveFullScreenShot(text):
    saveImage(fullScreenShot(), text)

def saveImage(image, text, withTime=true):
    name = os.getcwd() + os_sep + str(text)
    if(withTime): name += '__' + str(int(time.time()))
    name += '.png'
    image.save(name, 'PNG')

def saveScreenRect(rect, expand, text, imageText, folder='', miss=false):
    if(miss):
        text = 'MISS! ' + text
        imageText = 'MISS-' + imageText
    print(text)

    if(folder != ''): imageText = str(folder) + os_sep + imageText
    if(expand != -1): rect = rectExpand(rect, expand)
    saveImage(screenShot(rect), imageText)

def trackPixelHorizontal(loc, rgb, image):
    for i in range(-50, 50):
        newLoc = (loc[0] + i, loc[1])
        pixel = image.getpixel(newLoc)
        if pixel == rgb: return i
    return nan

def findPixel(loc, rgb, image):
    pixel = findPixelHelper(loc, rgb, image, 20)
    if(pixel != nan):
        print("Found pixel on first attempt: ", pixel)
        return pixel
    
    pixel = findPixelHelper(loc, rgb, image, 50)
    if(pixel != nan):
        print("Found pixel on second attempt: ", pixel)
        return pixel
    
    pixel = findPixelHelper(loc, rgb, image, 100)
    if(pixel != nan):
        print("Found pixel on third attempt: ", pixel)
        return pixel
    return nan

def findPixelHelper(loc, rgb, image, r):
    for i in range(-r, r):
        for j in range(-r, r):
            newLoc = (loc[0] + i, loc[1] + j)
            #print(newLoc)
            pixel = image.getpixel(newLoc)
            if pixel == rgb: return newLoc
    return nan

def getColorAt(loc):
    image = screenShot((loc[0], loc[1], 1, 1))
    return image.getpixel((0, 0))

def saveLocToColor(key):
    loc = mouseLoc()
    mousePos(Locs.dead_click)
    wait(3)
    #loc = Colors.loc_to_color[key][0]
    color = getColorAt(loc)
    
    keyName = Colors.nameOf(key)
    print(keyName, ":", (loc, color))

    wait(4)
    color = getColorAt(loc)
    print(keyName, ":", (loc, color))

def getColorSum(rect, i='default', debug=false, save=false):
    image = ImageGrab.grab(rectToScreen(rect))
    grayImage = ImageOps.grayscale(image)
    imageSum = array(grayImage.getcolors()).sum()
    if debug:
        saveImage(image, str(i) + '__' + str(imageSum))
        print(i, rect, imageSum)
    if save: 
        saveImage(image, "ImageSums" + os_sep + str(i) + '__' + str(imageSum), false)
    return imageSum

def saveColorSum(key):
    getColorSum(Colors.sums[key][0], key, false, true)

def confirmColorSum(key):
    rectAndSum = Colors.sums[key]
    return getColorSum(rectAndSum[0]) == rectAndSum[1]

def closeBluePrintIfNecessary():
    color = getColorAt(Locs.blueprint_close)
    if(color == Colors.blueprint_close or color == Colors.blueprint_close_2):
        slowClick(Locs.blueprint_close)
        return true

def closeIncidentIfNecessary():
    if(getColorAt(Locs.incident_ok) == Colors.incident_ok):
        slowClick(Locs.incident_ok)
        closeBluePrintIfNecessary()
        return true

def clickButton(key, attempts = 2):
    if(attempts < 1): return false
    loc = Colors.loc_to_color[key][0]
    color = Colors.loc_to_color[key][1]
    
    if(getColorAt(loc) == color):
        slowClick(loc)
        return true

    print("Missed button:", key, "-- attemptsLeft: ", attempts - 1)
    if(attempts > 1):
        wait(2)
        return clickButton(key, attempts - 1)
    return false
    
def co(i):
    chairRect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)
    aidPoint = (chairRect[0], chairRect[1] + 30)

    hitAid = true
    aidColor = getColorAt(aidPoint)

    friendRect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
    text = 'aid color-' + str(i) + '-' + str(aidPoint) + '-' + str(aidColor)
    imageText = 'aid-' + str(i) + '-' + str(aidColor)
    saveScreenRect(friendRect, 50, text, imageText, '', true)
    
    return aidColor

def checkAid(checkTaverns=false):
    #deadClick()
    for i in range(5):
        chairRect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)
        doAid(chairRect, i)
        
        if(checkTaverns):
            sum = getColorSum(chairRect, i)
            if(sum != Colors.chair_wait and sum != Colors.chair_blank):
                if(sum != Colors.chair_open):    
                    friendRect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
                    text = 'chiar-' + str(i) + '-' + str(chairRect) + '-' + str(sum)
                    imageText = 'chair-' + str(i) + '-' + str(sum)
                    saveScreenRect(friendRect, 50, text, imageText, '', true)
                slowClick(rectMiddle(chairRect), 3)
                slowClick(Locs.dead_click, 1)

def doAid(chairRect, i, attempts=2):
    aidPoint = (chairRect[0], chairRect[1] + 30)
    aidColor = getColorAt(aidPoint)
    if(aidColor == Colors.aid_wait): return
    
    if(aidColor == Colors.aid_ready):
        slowClick(aidPoint)
        closeBluePrintIfNecessary()
        return
        
    if(aidColor == Colors.aid_accept_friend):
        friendRect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        text = str('ADD friend') + '-' + str(i) + '-' + str(aidPoint) + '-' + str(aidColor)
        imageText = 'addFriend-' + str(i)
        saveScreenRect(friendRect, 50, text, imageText, 'Friends')
        return
        
    if(attempts > 1):
        print("Missed aid: " + str(i) + '-' + str(aidColor) + " -- attemptsLeft: ", attempts - 1)
        wait(2)
        if(closeIncidentIfNecessary()):
            print("Incident was up during aid.")
        if(closeBluePrintIfNecessary()):
            print("Blueprint was up during aid.")
        doAid(chairRect, i, attempts - 1)
    else:
        friendRect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        text = 'aid color-' + str(i) + '-' + str(aidPoint) + '-' + str(aidColor)
        imageText = 'aid-' + str(i) + '-' + str(aidColor)
        saveScreenRect(friendRect, 50, text, imageText, '', true)
                    


##### Functions #####
def startGame(quick=false):
    verySlowClick(Locs.chrome_taskbar)
    resizeChrome()
    slowClick(Locs.foe_shortcut, 20)
    slowClick(Locs.play_game)
    slowClick(Locs.sineria_select)
    
def resizeChrome(click=true):
    if(click):
        deadClick()
    hwnd = win32gui.GetForegroundWindow()
    # resizeWindow(hwnd, Rect.fromTuple(Locs.full_screen))
    resizeWindow(hwnd, Locs.full_screen)
    # resizeWindow(hwnd, Rect(Locs.full_screen[0], Locs.full_screen[1], Locs.full_screen[2], Locs.full_screen[3]))
    # resizeWindow(hwnd, Locs.full_screen)

def dragScreenSafe(offset):
    dragScreen(offset)
    if(closeIncidentIfNecessary()):
        dragScreen(offset)

def resetScreen():
    for i in range(4):
        if(confirmColorSum(Colors.TOP_LEFT)): return true
        dragScreenSafe((1000, 1000))
    print("Couldn't find top left of screen")
    saveImage(fullScreenShot(), "no_top_left")
    return false

def setGameScroll():
    global game_scroll
    if(confirmColorSum(Colors.TOP_LEFT_850)):
        game_scroll = (850, 0)
        return true
    elif(confirmColorSum(Colors.TOP_LEFT_900)):
        game_scroll = (900, 0)
        return true
    elif(confirmColorSum(Colors.TOP_LEFT_950)):
        game_scroll = (950, 0)
        return true
    return false
    

def findTavern():
    if(setGameScroll()): return true
    
    for i in range(2):
        if(resetScreen() != true): continue
        dragScreenSafe((-1000, 0))
        
        if(setGameScroll()): return true
        else:
            print("Wrong top left for tavern: " + str(i))
            saveImage(fullScreenShot(), "wrong_tavern_top_left")

    return false

def checkTavern():
    if(findTavern() != true): return

    verySlowClick(pointForScroll(Locs.tavern))
    color = getColorAt(Locs.last_tavern_seat)
    if(color != Colors.last_tavern_seat and color != Colors.last_tavern_seat_2):
        print("Tavern full, collecting.")
        slowClick(Locs.tavern_collect)
    slowClick(Locs.tavern_ok)

def checkEvent():
    if(getColorAt(Locs.event_ok) == Colors.event_ok):
        slowClick(Locs.event_ok)

def clickFriendsForward():
    #rect = (Locs.friends_forward_button[0] - 10, Locs.friends_forward_button[1] - 10, 21, 21)
    #getColorSum(rect, "forward", True)
    slowClick(Locs.friends_forward_button, 1.5)
    
def clickFriendsBack():
    slowClick(Locs.friends_back_button)
    
def clickNeighborsTab():
    slowClick(Locs.neighbors_tab)
    clickFriendsBack()
def clickGuildTab():
    slowClick(Locs.guild_tab)
    clickFriendsBack()
def clickFriendsTab():
    color = getColorAt(Locs.friends_tab)
    if(color in Colors.friends_tab_list):
        slowClick(Locs.friends_tab)
    else:
        print("Friends tab not expaned: ", color)
        slowClick(Locs.friends_tab_collapsed)
        
    clickFriendsBack()
    
def checkTavernSeats(checkNeighbors=true):
    clickFriendsTab()
    for i in range(29):
        checkAid(true)
        clickFriendsForward()

    clickGuildTab()
    for i in range(16):
        checkAid()
        clickFriendsForward()

    if(checkNeighbors):
        clickNeighborsTab()
        for i in range(20):
            checkAid()
            clickFriendsForward()

shouldCheckTreasure = true
def checkTreasureHunt(alwaysCheck=false):
    #close it if open
    image = fullScreenShot()
    offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    #deadClick didn't work here for Treasure Hunt
    if offset != nan:
        verySlowClick(Locs.treasure_x_left_middle)
        image = fullScreenShot()

    #check for treasure ready
    #offset = trackPixelVertical(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)

    if(getColorSum(Locs.treasure_hunt_rect) == Colors.treasure_hunt_ready):
        print("Found treasure!")
    elif(alwaysCheck == false): 
        return 
    
    verySlowClick(Locs.treasure_hunt)
    image = fullScreenShot()

    offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    if(offset == nan):
        print("Couldn't find Treasure Hunt menu!")
        saveImage(image, 'no_treasure_hunt_menu')
        return

    global right_offset
    right_offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    #print(right_offset)
    #right_offset = 0

    for i in range(6):
        point = pointForRightOffset(Locs.treasure_left_middle[i])
        #print(i, point, image.getpixel(point), Colors.treasure_complete_left_middle)
        if(image.getpixel(point) == Colors.treasure_complete_left_middle):
            print("Collecting treasure: ", i + 1)
            verySlowClick(point)
            saveAndExitTreasure(i)
            return

    if(alwaysCheck == false):
        print("Couldn't find Collect button!")
        saveImage(image, "treausre_miss")
        for i in range(6):
            point = pointForRightOffset(Locs.treasure_left_middle[i])
            rect = pointToRect(point, 100)
            saveImage(screenShot(rect), "treausre_miss__" + str(i))
    
    verySlowClick(Locs.treasure_x_left_middle)

def saveAndExitTreasure(i):
    saveImage(fullScreenShot(), "TreasureHunt" + os_sep + str(i + 1) + os_sep)
    if(closeIncidentIfNecessary() != true):
        wait(5)
        saveImage(fullScreenShot(), "TreasureHunt" + os_sep + str(i + 1) + os_sep + "2nd")
        closeIncidentIfNecessary()
        #deadClick didn't work here for Treasure Hunt
    verySlowClick(Locs.treasure_x_left_middle)
    

def doStuff():
    resizeChrome()
    for i in range(100):
        print('iteration: ', i)
        checkTreasureHunt()
        checkTavern()
        checkTavernSeats()
        checkTreasureHunt()
        wait(300)
        checkTreasureHunt()
        wait(300)

def doStuff2(alwaysCheckTreasure=false, checkNeighbors=true, start=true):
    for i in range(1000):
        print('iteration: ', i)
        if(i != 0 or start):
            startGame()
            wait(30)
            deadClick()
            resizeChrome()
            deadClick(2)


        if(i % 10 == 0 and (i != 0 or alwaysCheckTreasure)):
            runChecks(true, checkNeighbors)
        else:
            runChecks(false, checkNeighbors)

        slowClick(Locs.chrome_close)
        wait(1200)

def runChecks(alwaysCheckTreasure=false, checkNeighbors=true):
    deadClick()
    resizeChrome()
    checkTreasureHunt(alwaysCheckTreasure)
    checkTavern()
    checkTavernSeats(checkNeighbors)
    checkTreasureHunt()

def startEvent():
    myList = []
    slowClick(Locs.winter_event_start, .1)
    for i in range(100):
        #print("capturing: ", i)
        myList.append(screenShot(Locs.winter_event_rect))
    for i in range(100):
        #print("saving: ", i)
        saveImage(myList[i], "Event" + os_sep + str(i))

def main():
    pass
    resizeChrome()
    doStuff2(start=false)

if __name__ == '__main__':
    main()