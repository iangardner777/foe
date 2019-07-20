import Locs
from Core import *
from Vision import *
from foe import *


all_quests = {}


def get_quest_names():
    for i in range(8):
        find_quests()


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


UBQ = 1
COIN = 2
SUPPLY = 3
FP = 4
q1 = None
p1 = INVALID_LOC
q2 = None
p2 = INVALID_LOC
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

    while true:
        # global q1, p1, q2, p2
        find_quests()

        # if Settings.do_test:
        #     return

        if q1 == COIN:
            collect_point = find_marker("collect", get_current_screen(), p1)
            if collect_point != INVALID_LOC:
                collect_quest(p1, q1)
                # loop_ub_quest(num, iteration)
            elif q2 == UBQ:
                # print("found it")
                pay_ubq(p2)
                collect_quest(p2)
                # loop_ub_quest(num, iteration)
            else:
                abort_quest2()
                # loop_ub_quest(num, iteration)
        elif q1 == SUPPLY:
            collect_point = find_marker("collect", get_current_screen(), p1)
            if collect_point != INVALID_LOC:
                collect_quest(p1, q1)
                # loop_ub_quest(num, iteration)
            elif q2 == UBQ:
                # print("found it 2")
                pay_ubq(p2)
                collect_quest(p2)
                # loop_ub_quest(num, iteration)
            else:
                abort_quest2()
                # loop_ub_quest(num, iteration)
        elif q1 == UBQ:
            # print("found it 3")
            pay_ubq(p1)
            collect_quest(p1)
            # loop_ub_quest(num, iteration + 1)
            pass
            # pay_ubq(p2, screen)
            # collect_ubq(p2, screen)
        else:
            abort_quest()
            # loop_ub_quest(num, iteration)

    # if q1 == UBQ:
    #     print("found it")
    # else:
    #     point = find_marker("abort")
    #     slowClick(point)
    #     loop_ub_quest(num, iteration)


    # for i in range(6):
    #     click_quest(Colors.ABORT_QUEST)
    # click_quest(Colors.ABORT_QUEST_7)
    # click_quest(Colors.UB_QUEST_s)
    # click_quest(Colors.UB_QUEST_c)
    # if not ensureButton(Colors.COLLECT_QUEST, search=true):
    #     return false
    #
    # report_quest_reward(num, iteration)
    # click_quest(Colors.COLLECT_QUEST, true)
    # closeBluePrintIfNecessary()
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
    for reward in rewards:
        if collect_reward(point, reward, from_quest):
            return true

    #try a second time to avoid too fast errors
    wait(5)
    for reward in rewards:
        if collect_reward(point, reward, from_quest):
            return true


    reward = input("What is the resource?")
    copy_marker_from(f"r_{reward}", "r_medals", point)
    rewards.add(reward)
    print(f"{rewards}")
    return true


# rewards = {"brass", "basalt", "medals"}
rewards = {'basalt', 'blue_print', 'brass', 'coins', 'forge_point_pack', 'gunpowder', 'medals', 'supplies', 'talc_powder', 'silk'}
collect_quest_point = INVALID_LOC


def collect_reward(point, reward, from_quest=UBQ):
    global collect_quest_point
    collect_quest_point = point
    reward_point = find_marker(f"r_{reward}", get_current_screen(), collect_quest_point, true)
    if reward_point != INVALID_LOC:
        if reward == 'coins' and from_quest != COIN:
            ensure_coins(check_for_big(reward_point))
        elif reward == 'supplies' and from_quest != SUPPLY:
            ensure_supplies(check_for_big(reward_point))

        collect_point = find_marker("collect", get_current_screen(), collect_quest_point)
        Logging.print(f"Collecting: {reward}")
        slowClick(collect_point, 2)
        clear_current_screen()
        if reward == 'blue_print':
            deadClick(1)
        return true
    return false


def check_for_big(point):
    return true


def ensure_coins(big):
    ensure_helper(big, COIN)


def ensure_supplies(big):
    ensure_helper(big, SUPPLY)


def ensure_helper(big, q_type):
    other_type = get_other_q_type(q_type)
    global q1, p1, q2, p2, collect_quest_point
    if q1 == q_type or q2 == q_type:
        return
    else:
        if not big and (q1 == other_type and check_for_half(p1) or q2 == other_type and check_for_half(p2)):
            return

        if q2 == UBQ:
            abort_quest()
        elif q1 == UBQ:
            abort_quest2()

        find_quests()
        while q2 != q_type:
            abort_quest2()
            find_quests()

        collect_quest_point = p1


def check_for_half(point):
    return find_marker("half", get_current_screen(), point)


def find_quests():
    global q1, p1, q2, p2
    q1 = q2 = None

    p1 = find_marker_full("quest", get_current_screen())[0]
    if p1 != INVALID_LOC:
        p1.x += 2
        p1.y += 2
        # print(f"found: {point}")
        q1 = get_quest_num(p1, get_current_screen())
    else:
        Logging.warning("First quest not found.")
        open_quests() #this resets the scroll and the screen to hopefully find on second attempt
        find_quests()

    p2 = find_marker_full("quest2", get_current_screen())[0]
    if p2 != INVALID_LOC:
        p2.x += 4
        p2.y += 4
        # print(f"found: {point2}")
        q2 = get_quest_num(p2, get_current_screen())
    else:
        Logging.warning("Second quest not found.")
        open_quests() #this resets the scroll and the screen to hopefully find on second attempt
        find_quests()

    return q1, p1, q2, p2

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


def get_quest_num(point, screen):
    size = Size(400, 17)

    text = read_text(point.withSize(size), screen)
    text2 = text.split("(", 1)[0].strip()

    try:
        quest_num = all_quests[text2]
    except KeyError:
        Logging.warning(f"Quest not in dictionary: {text2}")
        quest_num = -1
    return quest_num
