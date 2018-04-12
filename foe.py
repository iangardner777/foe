from Vision import *
from collect import *

nan = 'NaN'


def co(i):
    chair_rect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)
    aid_point = Point(chair_rect.x, chair_rect.y + 30)

    aid_color = getColorAt(aid_point)

    friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
    text = 'aid color-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
    image_text = 'aid-' + str(i) + '-' + str(aid_color)
    saveScreenRect(friend_rect, 50, text, image_text, '', true)

    return aid_color


def checkAid(check_taverns=false):
    #deadClick()
    for i in range(5):
        chair_rect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)
        if not doAid(chair_rect, i):
            return false

        if check_taverns:
            color_sum = getColorSum(chair_rect, i)
            if color_sum != Colors.chair_wait and color_sum != Colors.chair_blank:
                if color_sum != Colors.chair_open:
                    Logging.warning(f"Missed tavern chair: {i} - {color_sum}")
                    saveImage(fullScreenShot(), "missed_tavern_chair")
                    return false
                    # friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
                    # text = 'chair-' + str(i) + '-' + str(chair_rect) + '-' + str(color_sum)
                    # image_text = 'chair-' + str(i) + '-' + str(color_sum)
                    # saveScreenRect(friend_rect, 50, text, image_text, '', true)
                slowClick(chair_rect.center(), 3)
                deadClick2(1)

    return true


def doAid(chair_rect, i, attempts=2):
    aid_point = Point(chair_rect.x, chair_rect.y + 30)
    aid_color = getColorAt(aid_point)
    if aid_color.isClose(Colors.aid_wait): return true

    if aid_color.isClose(Colors.aid_ready):
        slowClick(aid_point)
        closeBluePrintIfNecessary()
        return true

    if aid_color == Colors.aid_accept_friend:
        friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        text = str('ADD friend') + '-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
        image_text = 'addFriend-' + str(i)
        saveScreenRect(friend_rect, 50, text, image_text, 'Friends')
        return true

    Logging.warning(f"Missed aid: {i} - {aid_color} -- attemptsLeft: {attempts - 1}")
    saveImage(fullScreenShot(), "missed_aid")

    if attempts > 1:
        closeAnythingIfNecessary("aid")
        wait(2)
        return doAid(chair_rect, i, attempts - 1)
    else:
        return false
        # friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        # text = 'aid color-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
        # image_text = 'aid-' + str(i) + '-' + str(aid_color)
        # saveScreenRect(friend_rect, 50, text, image_text, '', true)


def closeIncidentIfNecessary():
    if clickButtonIfNecessary(Colors.INCIDENT_OKAY):
        closeBluePrintIfNecessary()
        return true


def closeBluePrintIfNecessary():
    return clickButtonIfNecessary(Colors.BP_CLOSE)


def closeGbRewardIfNecessary():
    return clickButtonIfNecessary(Colors.GB_REWARD_OKAY, picture="GB_Rewards")


def closeAnythingIfNecessary(event):
    if closeIncidentIfNecessary():
        Logging.warning(f"Incident was up during {event}.")
    if closeBluePrintIfNecessary():
        Logging.warning(f"Blueprint was up during {event}.")
    if closeGbRewardIfNecessary():
        Logging.warning(f"GB reward was up during {event}.")


##### Functions #####
def checkForLogin():
    if(checkForButton(Colors.PLAY_NOW)):
        slowClick(Locs.accept_terms)
        clickButton(Colors.PLAY_NOW)
        wait(2)


def startGame():
    verySlowClick(Locs.chrome_taskbar)
    resizeChrome()
    slowClick(Locs.foe_shortcut, 5)
    checkForLogin()
    slowClick(Locs.play_game)
    slowClick(Locs.sineria_select)


def resizeChrome(click=true):
    if click: deadClick2()
    hwnd = win32gui.GetForegroundWindow()
    resizeWindow(hwnd, Host.full_screen)


def dragScreenSafe(offset):
    closeAnythingIfNecessary("before drag screen")
    dragScreen(offset)
    if closeAnythingIfNecessary("after drag screen"):
        dragScreen(offset)


def resetScreen():
    if confirmColorSum(Colors.TOP_LEFT): return true
    attempts = 2
    for i in range(attempts):
        dragScreenSafe(Size(1000, 1000))
        if confirmColorSum(Colors.TOP_LEFT, i == attempts - 1): return true
    # print("Couldn't find top left of screen")
    saveImage(fullScreenShot(), "no_top_left")
    return false


def setGameScroll():
    if confirmColorSum(Colors.TOP_LEFT_950):
        Host.scroll_location = Point(950, 0)
        return true
    elif confirmColorSum(Colors.TOP_LEFT_900):
        Host.scroll_location = Point(900, 0)
        return true
    elif confirmColorSum(Colors.TOP_LEFT_850):
        Host.scroll_location = Point(850, 0)
        return true
    return false


def findTavern():
    if setGameScroll(): return true

    for i in range(2):
        if resetScreen() != true: continue
        dragScreenSafe(Size(-1000, 0))

        if setGameScroll():
            return true
        else:
            print("Wrong top left for tavern: " + str(i))
            saveImage(fullScreenShot(), "wrong_tavern_top_left")

    return false


def checkTavern():
    if findTavern() != true: return

    verySlowClick(pointForScroll(Locs.tavern))
    if not ensureButton(Colors.TAVERN_OKAY, 5, true):
        Logging.warning("Couldn't find the tavern okay button")
        deadClick2(2)
        return

    color = getColorAt(Locs.last_tavern_seat)
    if not color.isVeryClose(Colors.last_tavern_seat, true):
        Logging.log("Tavern full, collecting.")
        verySlowClick(Locs.tavern_collect)

    slowClick(Locs.tavern_ok)


def checkEvent():
    if getColorAt(Locs.event_ok) == Colors.event_ok:
        slowClick(Locs.event_ok)


def clickFriendsForward():
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
    if color in Colors.friends_tab_list:
        slowClick(Locs.friends_tab)
    else:
        Logging.warning(f"Friends tab not expanded: {color}")
        slowClick(Locs.friends_tab_collapsed)

    clickFriendsBack()


def checkTavernSeats(check_neighbors=true):
    clickFriendsTab()
    for i in range(29):
        if not checkAid(true):
            return false
        clickFriendsForward()

    clickGuildTab()
    for i in range(16):
        if not checkAid():
            return false
        clickFriendsForward()

    if check_neighbors:
        clickNeighborsTab()
        for i in range(20):
            if not checkAid():
                return false
            clickFriendsForward()

    return true


def checkTreasureHunt(always_check=false):
    # #close it if open
    # image = fullScreenShot()
    # offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    # #deadClick didn't work here for Treasure Hunt
    # if offset != nan:
    #     verySlowClick(Locs.treasure_x_left_middle)
    #     # image = fullScreenShot()
    #
    # #check for treasure ready
    # #offset = trackPixelVertical(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)

    loc = Locs.treasure_hunt_rect.center()
    if getColorSum(Locs.treasure_hunt_rect) == Colors.treasure_hunt_ready:
        Logging.log("Found treasure!")
    elif getColorSum(Locs.treasure_hunt_rect_3) == Colors.treasure_hunt_ready:
        loc = Locs.treasure_hunt_rect_3.center()
        Logging.log("Found treasure!")
        Logging.warning("At 3!")
    elif getColorSum(Locs.treasure_hunt_rect_2) == Colors.treasure_hunt_ready:
        loc = Locs.treasure_hunt_rect_2.center()
        Logging.log("Found treasure!")
        Logging.warning("At 2!")
    elif getColorSum(Locs.treasure_hunt_rect_1) == Colors.treasure_hunt_ready:
        loc = Locs.treasure_hunt_rect_1.center()
        Logging.log("Found treasure!")
        Logging.warning("At 1!")
    elif not always_check:
        return

    verySlowClick(loc)
    image = fullScreenShot()

    offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    if offset == nan:
        Logging.warning("Couldn't find Treasure Hunt menu!")
        saveImage(image, 'no_treasure_hunt_menu')
        return

    Host.right_offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)

    for i in range(6):
        point = pointForRightOffset(Locs.treasure_left_middle[i])
        #print(i, point, image.getpixel(point), Colors.treasure_complete_left_middle)
        if getColorAt(point, image) == Colors.treasure_complete_left_middle:
            Logging.log(f"Collecting treasure: {i + 1}")
            verySlowClick(point)
            saveAndExitTreasure(i)
            return

    if always_check == false:
        Logging.warning("Couldn't find Collect button!")
        saveImage(image, "treasure_miss")
        for i in range(6):
            point = pointForRightOffset(Locs.treasure_left_middle[i])
            rect = pointToRect(point, 100)
            saveImage(screenShot(rect), "treasure_miss__" + str(i))

    verySlowClick(Locs.treasure_x_left_middle)


def saveAndExitTreasure(i):
    saveFullScreenShotToFolder("TreasureHunt", i + 1)
    if not closeIncidentIfNecessary():
        wait(5)
        saveFullScreenShotToFolder("TreasureHunt", i + 1, text="2nd")
        closeIncidentIfNecessary()
        #deadClick didn't work here for Treasure Hunt
    verySlowClick(Locs.treasure_x_left_middle)


def doStuff():
    resizeChrome()
    for i in range(100):
        Logging.log(f"iteration: {1}")
        checkTreasureHunt()
        checkTavern()
        checkTavernSeats()
        checkTreasureHunt()
        wait(300)
        checkTreasureHunt()
        wait(300)


def doStuff2(always_check_treasure=false, check_neighbors=true, start=true):
    for i in range(1000):
        Logging.log(f"iteration: {i}")
        if i != 0 or start:
            startGame()
            wait(30)
            deadClick2()
            resizeChrome()
            deadClick2(2)

        closeAnythingIfNecessary("start")

        if i%10 == 0 and (i != 0 or always_check_treasure):
            runChecks(true, check_neighbors)
        else:
            runChecks(false, check_neighbors)

        slowClick(Locs.chrome_close)
        wait(1200)


def runChecks(always_check_treasure=false, check_neighbors=true):
    deadClick2()
    resizeChrome()
    checkTreasureHunt(always_check_treasure)
    checkTavern()
    checkTavernSeats(check_neighbors)
    checkTreasureHunt()


def startEvent():
    my_list = []
    slowClick(Locs.winter_event_start, .1)
    for i in range(100):
        #print("capturing: ", i)
        my_list.append(screenShot(Locs.winter_event_rect))
    for i in range(100):
        #print("saving: ", i)
        saveImage(my_list[i], "Event" + os_sep + str(i))


def main():
    pass
    alway_check_treasure = false
    check_neighbors = true
    start = true
    # wait(1200)
    doStuff2(alway_check_treasure, check_neighbors, start)
    #collectAlchemist()
    #checkTreasureHunt()
    # confirmColorSum("test", true)


if __name__ == '__main__':
    main()


# TODO - conditional start
# TODO - picture of whole screen and close everything when failing aids
# TODO - single picture of everything to do all aids on screen
# TODO - Daddy's home