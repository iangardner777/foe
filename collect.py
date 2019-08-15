import Locs
from Core import *
from foe import *

alchemist_row_offset = (Locs.last_alchemist - Locs.first_alchemist)/(Locs.rows_alchemist - 1)
alchemist_column_offset = Locs.right_alchemist - Locs.first_alchemist


def collectAlchemist():
    deadClick()
    findTavern()
    for i in range(Locs.rows_alchemist):
        row_loc = Locs.first_alchemist + alchemist_row_offset*i
        slowClick(pointForScroll(row_loc))
        slowClick(pointForScroll(row_loc) + alchemist_column_offset)


def collectBlacksmith(spot, both=true):
    #point = Point(1619, 1043) - alchemist_row_offset
    point = Point(1381, 1083)
    collect_and_restart_production(point, spot)
    point += alchemist_row_offset
    collect_and_restart_production(point, spot)
    point += alchemist_row_offset
    collect_and_restart_production(point, spot)
    point += alchemist_row_offset
    collect_and_restart_production(point, spot)

    dragScreenSafe(Size(0, -100))
    Host.scroll_location = Host.scroll_location + Point(0, 90 )
    collect_and_restart_production(Point(1381, 1083) - alchemist_row_offset, spot)

    # if both:
    #     collect_and_restart_production(Point(1619, 1043), spot)
    #     #collect_and_restart_production(Point(1619, 1043) - alchemist_row_offset, spot)
    # collect_and_restart_production(Point(1384, 1013) + alchemist_row_offset, spot)


def collect_and_restart_production(point, spot):
    collect_production(point)
    start_production(point, spot)


def collect_production(point):
    checkStatus()
    slowClick(pointForScroll(point))
    deadClick()


def start_production(point, spot):
    checkStatus()
    slowClick(pointForScroll(point))
    slowClick(start_production_spot[spot])
    deadClick()


five = Point(444, 533)
fifteen = five + Point(225, 0)
one_hour = fifteen + Point(225, 0)
four_hour = five + Point(0, 200)
eight_hour = fifteen + Point(0, 200)
one_day = one_hour + Point(0, 200)

start_production_spot = [
    five,
    fifteen,
    one_hour,
    four_hour,
    eight_hour,
    one_day
]


def loop_ub_quests(num, iteration):
    # if not click_quest(Colors.OPEN_QUEST):
    #     return false
    # for i in range(num):
    if not loop_ub_quest(num, iteration):
        return false
    deadClick(1)
    return true
    #click_quest(Colors.CLOSE_QUEST)


def loop_ub_quest2(num, iteration):
    for i in range(6):
        click_quest(Colors.ABORT_QUEST)
    click_quest(Colors.ABORT_QUEST_7)
    click_quest(Colors.UB_QUEST_s)
    click_quest(Colors.UB_QUEST_c)
    if not ensureButton(Colors.COLLECT_QUEST, search=true):
        return false

    report_quest_reward(num, iteration)
    click_quest(Colors.COLLECT_QUEST, true)
    closeBluePrintIfNecessary()
    return true


def click_quest(key, search=false):
    checkStatus()
    if not clickButton(key, search=search):
        return false
    checkStatus()
    setMouseLoc(Host.dead_click)
    wait(1)
    return true


QUEST_REWARDS_PATH = f"data{os_sep}questRewards.txt"
QUEST_REWARDS_PATH_BACKUP = f"data{os_sep}questRewardsBackup.txt"
QUEST_REWARDS_KEY_PATH = f"data{os_sep}questRewardsKey.txt"
REWARD_TO_HITS = {}
SUM_TO_REWARD = {}
COIN_REWARD = "COIN"
SUPPLY_REWARD = "SUPPLY"
def load_rewards():
    file = open(QUEST_REWARDS_PATH, "r")
    lines = file.readlines()
    for line in lines:
        reward_to_hits = line.strip("\n").split(":")
        REWARD_TO_HITS[reward_to_hits[0]] = int(reward_to_hits[1])
    file.close()

    file = open(QUEST_REWARDS_KEY_PATH)
    lines = file.readlines()
    for line in lines:
        reward_to_sum = line.strip("\n").split(":")
        SUM_TO_REWARD[int(reward_to_sum[1])] = reward_to_sum[0]
    file.close()


def save_rewards(path=QUEST_REWARDS_PATH):
    file = open(path, "w+")
    for reward, hits in REWARD_TO_HITS.items():
        file.write(f"{reward}:{hits}\n")


def report_quest_reward(i, iteration):
    load_rewards()
    # rect = Rect(515, 397, 103, 61)
    rect = Rect(546, 405, 43, 33)

    # SMALL SUPPLY:177276:221122
    # LARGE SUPPLY:177276:219468
    # SMALL COIN:200832:225901
    # LARGE COIN:200832:223749
    # GOOD_BRICKS:158878
    # GOOD_GLASS:236270
    # GOOD_HERBS:84590
    # GOOD_ROPES:125418
    # GOOD_SALT:142182
    # BP:148725
    # MEDALS:128225
    # FP_PACK:134524

    color_sum = getColorSum(rect)
    if color_sum not in SUM_TO_REWARD:
        Logging.warning(f"Couldn't find reward in key for sum: {color_sum}")
        reward = str(color_sum)
    else:
        reward = SUM_TO_REWARD[color_sum]

    if reward == SUPPLY_REWARD or reward == COIN_REWARD:
        color_sum = getColorSum(Rect(515, 441, 107, 18))
        if color_sum not in SUM_TO_REWARD:
            Logging.warning(f"Couldn't find reward in key for {reward}. Sum: {color_sum}")
            reward = str(color_sum)
        else:
            reward = SUM_TO_REWARD[color_sum]

    if reward in REWARD_TO_HITS:
        REWARD_TO_HITS[reward] += 1
    else:
        Logging.warning(f"Reward: {reward} was not in the dictionary!")
        REWARD_TO_HITS[reward] = 1

    saveFullScreenShotToFolder("data", "rewards", f"{i}_{color_sum}")
    save_rewards()

    file = open(QUEST_REWARDS_PATH_BACKUP, "a+")
    file.write(f"{iteration}-{i}:{color_sum}\n")
    file.close()


