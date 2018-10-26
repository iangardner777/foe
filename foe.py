from Settings import *
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


TAVERN_VISITS_PATH = f"data{os_sep}tavernVisits.txt"
TAVERN_VISITS_PATH_BACKUP = f"data{os_sep}tavernVisitsBackup.txt"
MISSING_FRIENDS_PATH = f"data{os_sep}tavernVisitsMissingFriends.txt"
FRIEND_TO_VISITS = {}
def loadTavernVisits():
    file = open(TAVERN_VISITS_PATH, "r")
    lines = file.readlines()
    for line in lines:
        friend_to_visits = line.strip("\n").split(":")
        FRIEND_TO_VISITS[friend_to_visits[0]] = int(friend_to_visits[1])


def saveTavernVisits(path=TAVERN_VISITS_PATH):
    file = open(path, "w+")
    for friend, visits in FRIEND_TO_VISITS.items():
        file.write(f"{friend}:{visits}\n")


def checkAid(check_taverns=false):
    #deadClick()
    for i in range(5):
        chair_rect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)
        if not doAid(chair_rect, i):
            return false

        if check_taverns and not doTavern(chair_rect, i):
            return false

    return true


def doAid(chair_rect, i, attempts=2):
    checkStatus()
    aid_point = Point(chair_rect.x, chair_rect.y + 30)
    aid_color = getColorAt(aid_point)
    if aid_color.isClose(Colors.aid_wait): return true

    if aid_color.isClose(Colors.aid_ready):
        slowClick(aid_point)
        closeBluePrintIfNecessary()
        #DOESNT WORK-prevent popup from building under friends bar interfering
        #for i in range(5):
        #    aid_point -= Point(1, 1)
        #    setMouseLoc(aid_point)
        return true

    if aid_color == Colors.aid_accept_friend:
        #friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        #text = str('ADD friend') + '-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
        #image_text = 'addFriend-' + str(i)
        #saveScreenRect(friend_rect, 50, text, image_text, 'Friends')
        return true

    Logging.warning(f"Missed aid: {i} - {aid_color} -- attemptsLeft: {attempts - 1}")
    saveImage(fullScreenShot(), "missed_aid")

    if attempts > 1:
        closeAnythingIfNecessary("aid")
        wait(2)
        return doAid(chair_rect, i, attempts - 1)

    return false
    # friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
    # text = 'aid color-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
    # image_text = 'aid-' + str(i) + '-' + str(aid_color)
    # saveScreenRect(friend_rect, 50, text, image_text, '', true)


def doTavern(chair_rect, i, attempts=2):
    checkStatus()
    color_sum = getColorSumObsolete(chair_rect, i)
    if color_sum == Colors.chair_wait or color_sum == Colors.chair_blank:
        return true

    if color_sum == Colors.chair_open:
        slowClick(chair_rect.center())

        if not ensureFriendsTavernClose():
            Logging.error("Couldn't find friend tavern close", "friend_tavern_close")
            deadClick(1)
            return false

        friend = readText(Locs.friend_tavern_name_rect)
        if friend in FRIEND_TO_VISITS:
            FRIEND_TO_VISITS[friend] += 1
        else:
            wait(5)
            friend = readText(Locs.friend_tavern_name_rect)
            if friend in FRIEND_TO_VISITS:
                FRIEND_TO_VISITS[friend] += 1
            else:
                Logging.warning(f"Friend: {friend} was not in the visits dictionary!")
                FRIEND_TO_VISITS[friend] = 1

        saveTavernVisits()
        saveImage(fullScreenShot(), f"TavernVisits{os_sep}{clean_filename(friend)}")

        deadClick(1)
        return true

    if attempts > 1:
        Logging.warning(f"Missed tavern chair: {i} - {color_sum}")
        closeAnythingIfNecessary("tavern")
        wait(2)
        loc = getMouseLoc(false)
        for i in range(50):
            loc -= Point(1, 1)
            setMouseLoc(loc)
            wait(.01)
        deadClick(.5)
        return doAid(chair_rect, i, attempts - 1)

    Logging.warning(f"LAST -- Missed tavern chair: {i} - {color_sum}")
    saveImage(fullScreenShot(), "missed_tavern_chair")
    return false
    # friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
    # text = 'chair-' + str(i) + '-' + str(chair_rect) + '-' + str(color_sum)
    # image_text = 'chair-' + str(i) + '-' + str(color_sum)
    # saveScreenRect(friend_rect, 50, text, image_text, '', true)


def closeIncidentIfNecessary():
    if clickButtonIfNecessary(Colors.INCIDENT_OKAY):
        closeBluePrintIfNecessary()
        return true


def closeBluePrintIfNecessary():
    return clickButtonIfNecessary(Colors.BP_CLOSE)


def closeGbRewardIfNecessary():
    clicked = clickButtonIfNecessary(Colors.GB_REWARD_OKAY, picture="GB_Rewards")
    if clicked:
        Logging.log("Collected GB.")
    return clicked


def closeAnythingIfNecessary(event):
    if closeIncidentIfNecessary():
        Logging.warning(f"Incident was up during {event}.")
    if closeBluePrintIfNecessary():
        Logging.warning(f"Blueprint was up during {event}.")
    if closeGbRewardIfNecessary():
        Logging.warning(f"GB reward was up during {event}.")


##### Functions #####
def checkForLogin():
    if checkForButton(Colors.PLAY_NOW, true):
        slowClick(Locs.accept_terms, 5)
        clickButton(Colors.PLAY_NOW)
        wait(2)
    elif checkForButton(Colors.PLAY_NOW2, true):
        slowClick(Locs.accept_terms, 5)
        clickButton(Colors.PLAY_NOW2)
        wait(2)


def startGame():
    if checkForColor(Colors.DEAD_CLICK):
        Logging.warning("Game was already started.")
    else:
        verySlowClick(Locs.chrome_taskbar)
        reset_status() #this is to prevent a wait for user as the screen turns on and cursor resets to middle
        resizeChrome()
        slowClick(Locs.foe_shortcut, 5)
        checkForLogin()
        slowClick(Locs.play_game)
        slowClick(Locs.sineria_select)
        slowClick(Point(640, 934))
        slowClick(Point(346, 57))

        wait(Settings.start_wait_time)

    closeAnythingIfNecessary("start")
    checkStatus()
    deadClick()
    resizeChrome()
    deadClick(2)
    if Settings.open_ge:
        open_ge()
    else:
        closeAnythingIfNecessary("start")


def open_ge():
    if clickButton(Colors.GUILD_EXPEDITION):
        deadClick(2)
        clickButton(Colors.BACK_TO_CITY)
        wait(2)
        closeAnythingIfNecessary("open ge")
        deadClick(1)


def resizeChrome(click=true):
    checkStatus()
    if click: deadClick()
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


def setGameScroll(p=false):
    if confirmColorSum(Colors.TOP_LEFT_950, p):
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

    attempts = 2
    for i in range(attempts):
        if resetScreen() != true: continue
        dragScreenSafe(Size(-1000, 0))

        if setGameScroll(true):
            return true
        elif i < attempts - 1:
            open_ge()
        else:
            Logging.error(f"Wrong top left for tavern: {i}", "wrong_tavern_top_left")

    return false


def ensureFriendsTavernClose():
    if not ensureButton(Colors.FRIENDS_TAVERN_CLOSE, 5, false):
        Logging.warning("Couldn't find the tavern close button")
        deadClick(2)
        return false
    return true


def ensureTavernOkay():
    if not ensureButton(Colors.TAVERN_OKAY, 5, false):
        Logging.warning("Couldn't find the tavern okay button")
        deadClick(2)
        return false
    return true


def checkTavern():
    if findTavern() != true: return

    verySlowClick(pointForScroll(Locs.tavern))
    if not ensureTavernOkay():
        deadClick(2)
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


def checkFriendsAidTaverns(check_neighbors=true):
    loadTavernVisits()
    clickFriendsTab()
    for i in range(29):
        checkStatus()
        if not checkAid(true):
            return false
        clickFriendsForward()

    clickGuildTab()
    for i in range(16):
        checkStatus()
        if not checkAid():
            return false
        clickFriendsForward()

    if check_neighbors:
        clickNeighborsTab()
        for i in range(20):
            checkStatus()
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
    if getColorSumObsolete(Locs.treasure_hunt_rect) == Colors.treasure_hunt_ready:
        Logging.log("Found treasure!")
    elif getColorSumObsolete(Locs.treasure_hunt_rect_3) == Colors.treasure_hunt_ready:
        loc = Locs.treasure_hunt_rect_3.center()
        Logging.log("Found treasure!")
        Logging.warning("At 3!")
    elif getColorSumObsolete(Locs.treasure_hunt_rect_2) == Colors.treasure_hunt_ready:
        loc = Locs.treasure_hunt_rect_2.center()
        Logging.log("Found treasure!")
        Logging.warning("At 2!")
    elif getColorSumObsolete(Locs.treasure_hunt_rect_1) == Colors.treasure_hunt_ready:
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


def doStuff2():
    for i in range(1000):
        Logging.log(f"iteration: {i}")

        #checkStatus() #I don't think we need this, check status is moving to more atomic functions
        startGame()

        checkStatus()
        closeAnythingIfNecessary("start")

        if Settings.run_checks:
            runChecks(Settings.check_neighbors)

        collectB()

        if checkStatus(false) == USER_HOME:
            Logging.warning(f"User is home. Not closing.")
        elif not Settings.loop_quests and Settings.shutdown:
            slowClick(Locs.chrome_close)

        if Settings.collect_smiths and Settings.smith_production == 0:
            for i in range(12):
                wait(one_hour_time/12 - one_minute_time)
                collectB(true, true)
            wait(one_hour_time/12 - one_minute_time*3)
        elif Settings.collect_smiths and Settings.smith_production == 1:
            for i in range(4):
                wait(one_hour_time/4 - one_minute_time)
                collectB(true, true)
            wait(one_hour_time/4 - one_minute_time*3)
        elif Settings.loop_quests and i < Settings.quest_loops:
            loop_ub_quests(Settings.quests_to_loop, i)
        else:
            wait(Settings.shutdown_wait_time)


def collectB(start=false, close=false):
    if not Settings.collect_smiths:
        return

    if start:
        startGame()

    findTavern()
    collectBlacksmith(Settings.smith_production)

    if close:
        slowClick(Locs.chrome_close)


def runChecks(check_neighbors=true):
    checkStatus()
    deadClick()
    checkStatus()
    resizeChrome()
    checkStatus()
    checkTavern()
    checkFriendsAidTaverns(check_neighbors)


def startEvent():
    my_list = []
    slowClick(Locs.winter_event_start, .1)
    for i in range(100):
        #print("capturing: ", i)
        my_list.append(screenShot(Locs.winter_event_rect))
    for i in range(100):
        #print("saving: ", i)
        saveImage(my_list[i], "Event" + os_sep + str(i))


def setupTavernSeats():
    deadClick()
    ensure_dir(TAVERN_VISITS_PATH)
    loadTavernVisits()
    saveTavernVisits(TAVERN_VISITS_PATH_BACKUP)
    file = open(TAVERN_VISITS_PATH, "w+")
    clickFriendsTab()

    for i in range(29):
        for i in range(5):
            chair_rect = rectPlusX(Locs.chair_rect, i*Locs.friend_spacing)

            slowClick(chair_rect.center(), 3)
            ensureFriendsTavernClose()
            friend = readText(Locs.friend_tavern_name_rect)
            if friend in FRIEND_TO_VISITS:
                Logging.log(f"{friend} was in dict with {FRIEND_TO_VISITS[friend]} visits.")
                file.write(f"{friend}:{FRIEND_TO_VISITS[friend]}\n")
                FRIEND_TO_VISITS.pop(friend)
            else:
                Logging.log(f"{friend} was not in dict.")
                file.write(f"{friend}:0\n")

            deadClick(1)

        clickFriendsForward()
    file.close()


    file = open(MISSING_FRIENDS_PATH, "a+")
    for friend, visits in FRIEND_TO_VISITS.items():
        Logging.warning(f"{friend} was in dict with {visits} visits, but wasn't found in friend list.")
        file.write(f"{friend}:{visits}\n")

def main():
    pass

    # wait(1200)
    if Settings.do_stuff:
        doStuff2()

    #report_quest_reward(0)
    #getColorSum(Rect(515, 397, 103, 61))
    #collectAlchemist()
    #setupTavernSeats()
    #saveLocToColor(Colors.FRIENDS_TAVERN_CLOSE)
    pass


if __name__ == '__main__':
    main()


# TODO - picture of whole screen and close everything when failing aids
# TODO - single picture of everything to do all aids on screen
# TODO - read params from a file so you don't have to restart