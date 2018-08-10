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

    # if both:
    #     collect_and_restart_production(Point(1619, 1043), spot)
    #     #collect_and_restart_production(Point(1619, 1043) - alchemist_row_offset, spot)
    # collect_and_restart_production(Point(1384, 1013) + alchemist_row_offset, spot)


def collect_and_restart_production(point, spot):
    collect_production(point)
    start_production(point, spot)


def collect_production(point):
    slowClick(pointForScroll(point))
    deadClick()


def start_production(point, spot):
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


def loop_ub_quests(n):
    click_quest(Colors.OPEN_QUEST)
    for i in range(n):
        loop_ub_quest()
    click_quest(Colors.CLOSE_QUEST)


def loop_ub_quest():
    for i in range(6):
        click_quest(Colors.ABORT_QUEST)
    click_quest(Colors.ABORT_QUEST_7)
    click_quest(Colors.UB_QUEST)
    click_quest(Colors.COLLECT_QUEST, true)
    closeBluePrintIfNecessary()


def click_quest(key, search=false):
    clickButton(key, search=search)
    setMouseLoc(Host.dead_click)
    wait(1)
