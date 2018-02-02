from Vision import *

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
        doAid(chair_rect, i)

        if check_taverns:
            color_sum = getColorSum(chair_rect, i)
            if color_sum != Colors.chair_wait and color_sum != Colors.chair_blank:
                if color_sum != Colors.chair_open:
                    friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
                    text = 'chair-' + str(i) + '-' + str(chair_rect) + '-' + str(color_sum)
                    image_text = 'chair-' + str(i) + '-' + str(color_sum)
                    saveScreenRect(friend_rect, 50, text, image_text, '', true)
                slowClick(rectMiddle(chair_rect), 3)
                deadClick(1)


def doAid(chair_rect, i, attempts=2):
    aid_point = Point(chair_rect.x, chair_rect.y + 30)
    aid_color = getColorAt(aid_point)
    if aid_color == Colors.aid_wait: return

    if aid_color == Colors.aid_ready:
        slowClick(aid_point)
        closeBluePrintIfNecessary()
        return

    if aid_color == Colors.aid_accept_friend:
        friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        text = str('ADD friend') + '-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
        image_text = 'addFriend-' + str(i)
        saveScreenRect(friend_rect, 50, text, image_text, 'Friends')
        return

    if attempts > 1:
        print("Missed aid: " + str(i) + '-' + str(aid_color) + " -- attemptsLeft: ", attempts - 1)
        wait(2)
        if closeIncidentIfNecessary():
            print("Incident was up during aid.")
        if closeBluePrintIfNecessary():
            print("Blueprint was up during aid.")
        doAid(chair_rect, i, attempts - 1)
    else:
        friend_rect = rectPlusX(Locs.friend_rect, i*Locs.friend_spacing)
        text = 'aid color-' + str(i) + '-' + str(aid_point) + '-' + str(aid_color)
        image_text = 'aid-' + str(i) + '-' + str(aid_color)
        saveScreenRect(friend_rect, 50, text, image_text, '', true)


##### Functions #####
def startGame():
    verySlowClick(Locs.chrome_taskbar)
    resizeChrome()
    slowClick(Locs.foe_shortcut, 20)
    slowClick(Locs.play_game)
    slowClick(Locs.sineria_select)


def resizeChrome(click=true):
    if click: deadClick()
    hwnd = win32gui.GetForegroundWindow()
    resizeWindow(hwnd, Host.full_screen)


def dragScreenSafe(offset):
    dragScreen(offset)
    if closeIncidentIfNecessary():
        dragScreen(offset)


def resetScreen():
    for i in range(4):
        if confirmColorSum(Colors.TOP_LEFT): return true
        dragScreenSafe(Size(1000, 1000))
    print("Couldn't find top left of screen")
    saveImage(fullScreenShot(), "no_top_left")
    return false


def setGameScroll():
    if confirmColorSum(Colors.TOP_LEFT_850):
        Host.game_scroll = Point(850, 0)
        return true
    elif confirmColorSum(Colors.TOP_LEFT_900):
        Host.game_scroll = Point(900, 0)
        return true
    elif confirmColorSum(Colors.TOP_LEFT_950):
        Host.game_scroll = Point(950, 0)
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
    color = getColorAt(Locs.last_tavern_seat)
    if color != Colors.last_tavern_seat and color != Colors.last_tavern_seat_2:
        print("Tavern full, collecting.")
        slowClick(Locs.tavern_collect)
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
        print("Friends tab not expanded: ", color)
        slowClick(Locs.friends_tab_collapsed)

    clickFriendsBack()


def checkTavernSeats(check_neighbors=true):
    clickFriendsTab()
    for i in range(29):
        checkAid(true)
        clickFriendsForward()

    clickGuildTab()
    for i in range(16):
        checkAid()
        clickFriendsForward()

    if check_neighbors:
        clickNeighborsTab()
        for i in range(20):
            checkAid()
            clickFriendsForward()


def checkTreasureHunt(always_check=false):
    #close it if open
    image = fullScreenShot()
    offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    #deadClick didn't work here for Treasure Hunt
    if offset != nan:
        verySlowClick(Locs.treasure_x_left_middle)
        # image = fullScreenShot()

    #check for treasure ready
    #offset = trackPixelVertical(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)

    if getColorSum(Locs.treasure_hunt_rect) == Colors.treasure_hunt_ready:
        print("Found treasure!")
    elif always_check == false:
        return

    verySlowClick(Locs.treasure_hunt)
    image = fullScreenShot()

    offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)
    if offset == nan:
        print("Couldn't find Treasure Hunt menu!")
        saveImage(image, 'no_treasure_hunt_menu')
        return

    Host.right_offset = trackPixelHorizontal(Locs.treasure_x_left_middle, Colors.treasure_x_left_middle, image)

    for i in range(6):
        point = pointForRightOffset(Locs.treasure_left_middle[i])
        #print(i, point, image.getpixel(point), Colors.treasure_complete_left_middle)
        if getColorAt(point, image) == Colors.treasure_complete_left_middle:
            print("Collecting treasure: ", i + 1)
            verySlowClick(point)
            saveAndExitTreasure(i)
            return

    if always_check == false:
        print("Couldn't find Collect button!")
        saveImage(image, "treasure_miss")
        for i in range(6):
            point = pointForRightOffset(Locs.treasure_left_middle[i])
            rect = pointToRect(point, 100)
            saveImage(screenShot(rect), "treasure_miss__" + str(i))

    verySlowClick(Locs.treasure_x_left_middle)


def saveAndExitTreasure(i):
    saveImage(fullScreenShot(), "TreasureHunt" + os_sep + str(i + 1) + os_sep)
    if closeIncidentIfNecessary() != true:
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


def doStuff2(always_check_treasure=false, check_neighbors=true, start=true):
    for i in range(1000):
        print('iteration: ', i)
        if i != 0 or start:
            startGame()
            wait(30)
            deadClick()
            resizeChrome()
            deadClick(2)

        if i%10 == 0 and (i != 0 or always_check_treasure):
            runChecks(true, check_neighbors)
        else:
            runChecks(false, check_neighbors)

        slowClick(Locs.chrome_close)
        wait(1200)


def runChecks(always_check_treasure=false, check_neighbors=true):
    deadClick()
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
    # resizeChrome()
    # doStuff2(start=false)
    doStuff2()
    # checkTreasureHunt()


if __name__ == '__main__':
    main()