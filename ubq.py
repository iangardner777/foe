import Locs
from Core import *
from Vision import *
from foe import *


all_quests = {}


def get_quest_names():
    load_quest_names()
    open_quests()

    for i in range(8):
        find_quests()
        abort_quest()


def load_quest_names():
    file = open(f"data/markers/quest_names.txt")
    lines = file.readlines()
    for line in lines:
        num, quest_list = line.strip('\n').split(':')
        for quest in quest_list.split("#"):
            all_quests[quest] = int(num)
    file.close()


def get_other_q_type(q_type):
    if q_type == COIN:
        return SUPPLY
    if q_type == SUPPLY:
        return COIN
    Log.warning(f"Don't know how to find other for {type}.")


INVALID_QUEST = -1
UBQ = 1
COIN = 2
SUPPLY = 3
FP = 4
q1 = None
p1 = INVALID_LOC
q2 = None
p2 = INVALID_LOC
quest_num = 0
current_screen = None


def clear_current_screen():
    global current_screen
    if current_screen:
        current_screen.close()
    current_screen = None


def get_current_screen():
    global current_screen
    if current_screen is None:
        current_screen = fullScreenShot()
    return current_screen


# Why can't this be read from foe
def closeBluePrintIfNecessary():
    return clickButtonIfNecessary(Colors.BP_CLOSE)


def open_quests():
    slowClick(Point(38, 162), 1) #open quests
    slowClick(Point(656, 609), 1) #scroll
    clear_current_screen()


def loop_ub_quest(num, iteration):
    load_quest_names()

    open_quests()

    global quest_num
    quest_num = 0
    while quest_num < num:
        if not find_quests():
            saveImage(get_current_screen(), "QUEST_NOT_FOUND_LOOP_UBQ")
            Logging.warning("Didn't find quest in loop ubq!")
            return false

        if q1 == INVALID_QUEST:
            saveImage(get_current_screen(), "INVALID_QUEST_LOOP_UBQ")
            Logging.warning("Invalid quest found in loop ubq!")
            return false

        if q1 == UBQ:
            if not collect_quest(p1):
                return false
        else:
            collect_point = find_marker("collect", get_current_screen(), p1)
            if collect_point != INVALID_LOC:
                if not collect_quest(p1, q1):
                    return false
            elif q2 == UBQ:
                if not collect_quest(p2):
                    return false
            else:
                if q1 != COIN and q1 != SUPPLY and (q2 == COIN or q2 == SUPPLY):
                    abort_quest()
                else:
                    abort_quest2()

        # elif q1 == COIN or q1 == SUPPLY or q1 == FP:
        #     collect_point = find_marker("collect", get_current_screen(), p1)
        #     if collect_point != INVALID_LOC:
        #         collect_quest(p1, q1)
        #     elif q2 == UBQ:
        #         collect_quest(p2)
        #     else:
        #         if q1 == FP:
        #             abort_quest()
        #         else:
        #             abort_quest2()
        # elif q1 == UBQ:
        #     collect_quest(p1)
        # else:
        #     abort_quest()
    return true


def abort_quest():
    point = find_marker("abort", get_current_screen(), debug=false)
    slowClick(point + Point(2, 2), 2)
    clear_current_screen()


def abort_quest2():
    point = find_marker("abort2", get_current_screen())
    slowClick(point + Point(2, 2), 1.6)
    clear_current_screen()


offset2c = Point(466, 487) - Point(11, 376)
offset2s = Point(466, 556) - Point(11, 376)
def pay_ubq(point):
    collect_point = find_marker("collect", get_current_screen(), point)
    if collect_point == INVALID_LOC:
        slowClick(point + offset2s, 1.5)
        slowClick(point + offset2c, 1.5)
        clear_current_screen()


def collect_quest(point, from_quest=UBQ):
    if from_quest == UBQ:
        pay_ubq(point)

    for reward in rewards:
        if collect_reward(point, reward, from_quest):
            return true
        if q1 == INVALID_QUEST:
            return false

    #try a second time to avoid too fast errors
    wait(5)
    if from_quest == UBQ:
        pay_ubq(point)
    for reward in rewards:
        if collect_reward(point, reward, from_quest):
            return true
        if q1 == INVALID_QUEST:
            return false

    # reward = input("What is the resource?")
    # copy_marker_from(f"r_{reward}", "r_medals", point)
    # rewards.add(reward)
    # print(f"{rewards}")
    return false


# rewards = {"brass", "basalt", "medals"}
rewards = {'basalt', 'blue_print', 'brass', 'coins', 'forge_point_pack', 'gunpowder', 'medals', 'supplies', 'talc_powder', 'silk'}
collect_quest_point = INVALID_LOC


def collect_reward(point, reward, from_quest=UBQ):
    global collect_quest_point, quest_num
    collect_quest_point = point
    reward_point = find_marker(f"r_{reward}", get_current_screen(), collect_quest_point, true)
    if reward_point == INVALID_LOC:
        return false

    if reward == 'coins' and from_quest != COIN:
        if not ensure_coins(check_for_big(reward_point)):
            return false
    elif reward == 'supplies' and from_quest != SUPPLY:
        if not ensure_supplies(check_for_big(reward_point)):
            return false

    collect_point = find_marker("collect", get_current_screen(), collect_quest_point)
    Logging.print(f"Collecting: {reward}")
    slowClick(collect_point, 2)
    quest_num += 1
    clear_current_screen()
    if reward == 'blue_print':
        deadClick(1)
    return true


def check_for_big(point):
    return true


def ensure_coins(big):
    return ensure_helper(big, COIN)


def ensure_supplies(big):
    return ensure_helper(big, SUPPLY)


def ensure_helper(big, q_type):
    other_type = get_other_q_type(q_type)
    global q1, p1, q2, p2, collect_quest_point
    if q1 != q_type and q2 != q_type:
        if not big and (q1 == other_type and check_for_half(p1) or q2 == other_type and check_for_half(p2)):
            return true

        if q2 == UBQ:
            abort_quest()
        elif q1 == UBQ:
            abort_quest2()

        find_quests()
        while q2 != q_type:
            old_q2 = q2
            abort_quest2()
            find_quests()
            if old_q2 == q2:
                return false

        collect_quest_point = p1
    return true


def check_for_half(point):
    return find_marker("half", get_current_screen(), point)


def find_quest1():
    global q1, p1
    q1 = None

    p1 = find_marker_full("quest", get_current_screen())[0]
    if p1 != INVALID_LOC:
        p1.x += 2
        p1.y += 2
        # print(f"found: {point}")
        q1 = get_quest_num(p1, get_current_screen())
        return true

    return false


def find_quest2():
    global q2, p2
    q2 = None

    p2 = find_marker_full("quest2", get_current_screen())[0]
    if p2 != INVALID_LOC:
        p2.x += 4
        p2.y += 4
        # print(f"found: {point2}")
        q2 = get_quest_num(p2, get_current_screen())
        return true

    return false


def find_quests():
    if find_quest1() and find_quest2():
        return true

    #some kind of logging needed here for optimization later
    wait(2)
    clear_current_screen()
    if find_quest1() and find_quest2():
        return true

    wait(5)
    clear_current_screen()
    if find_quest1() and find_quest2():
        return true

    saveImage(get_current_screen(), "QUEST_NOT_FOUND")
    Logging.warning("Quest not found 1.")

    deadClick(10)
    open_quests()  #this resets the scroll and the screen to hopefully find on second attempt
    if find_quest1() and find_quest2() and q1 != INVALID_QUEST and q2 != INVALID_QUEST:
        return true

    saveImage(get_current_screen(), "QUEST_NOT_FOUND2")
    Logging.warning("Quest not found 2.")
    return false


    # if not find_quest1() or not find_quest2():
    #     wait(5)
    #     clear_current_screen()
    #     if not find_quest1() or not find_quest2(): #some kind of logging needed here for optimization later
    #         saveImage(get_current_screen(), "FIRST_QUEST_NOT_FOUND1")
    #         Logging.warning("First quest not found 1.")
    #
    #         deadClick(10)
    #         open_quests() #this resets the scroll and the screen to hopefully find on second attempt
    #         if not find_quest1() or :
    #             saveImage(get_current_screen(), "FIRST_QUEST_NOT_FOUND2")
    #             Logging.warning("First quest not found 2.")
    #             return false
    #
    # if not find_quest2():
    #     wait(5)
    #     clear_current_screen()
    #     if not find_quest2(): #some kind of logging needed here for optimization later
    #         saveImage(get_current_screen(), "SECOND_QUEST_NOT_FOUND1")
    #         Logging.warning("Second quest not found 1.")
    #
    #         deadClick(10)
    #         open_quests() #this resets the scroll and the screen to hopefully find on second attempt
    #         if not find_quest2():
    #             saveImage(get_current_screen(), "SECOND_QUEST_NOT_FOUND2")
    #             Logging.warning("Second quest not found 2.")
    #             return false
    #
    # return true

    # if text not in quests:
    #     print(f"adding {text}")
    #     file = open(f"data/markers/quest_names.txt", "a+")
    #     file.write(f"{text}\n")
    #     quests.add(text)
    #
    # if text2 not in quests:
    #     print(f"adding {text2}")
    #     file = open(f"data/markers/quest_names.txt", "a+")
    #     file.write(f"{text2}\n")
    #     quests.add(text2)


def get_quest_num(point, screen, read=false):
    size = Size(400, 17)

    text = read_text(point.withSize(size), screen, true)
    text2 = text.split("(", 1)[0].strip()

    try:
        q_num = all_quests[text2]
    except KeyError:
        saveImage(get_current_screen(), "QuestNotInDictionary")
        Logging.warning(f"Quest not in dictionary: {text2}")

        text = read_text(point.withSize(size), screen, true, true)

        q_num = INVALID_QUEST

    if read:
        Logging.print(text)
        Logging.print(text2)

    return q_num
