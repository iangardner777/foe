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

def collectBlacksmith():
    slowClick(pointForScroll(Point(1384, 1013)))
    slowClick(pointForScroll(Point(1384, 1013)))
    slowClick(Point(444, 533))
