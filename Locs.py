from Rect import *


class Locs:
    chrome_taskbar = Point(612, 1472)
    chrome_close = Point(1335, -97)
    foe_shortcut = Point(16, -16)

    chrome_recent = Point(412, 450)
    play_game = Point(987, 451)
    sineria_select = Point(670, 281)

    accept_terms = Point(553, 444)
    #accept_terms2 = Point(549, 442)

    winter_event_start = Point(683, 483)
    winter_event_top_left = Point(354, 573)
    winter_event_bottom_right = Point(1004, 892)
    winter_event_rect = pointsToRect(winter_event_top_left, winter_event_bottom_right)

    tavern = Point(1300, 250)
    last_tavern_seat = Point(360, 570)
    tavern_collect = Point(612, 707)
    tavern_ok = Point(640, 900)

    # treasure_hunt_rect = Rect(3, 341, 54, 54)
    treasure_hunt_rect_3 = Rect(48, 451, 5, 11)
    treasure_hunt_rect_2 = Rect(48, 361, 5, 11)
    treasure_hunt_rect_1 = Rect(48, 271, 5, 11)
    treasure_hunt_rect = treasure_hunt_rect_3
    treasure_x_left_middle = Point(1133, 858)
    treasure_x = Rect(1133, 850, 17, 17)
    treasure_ok = Point(668, 735)

    treasure_1_left_middle = Point(804, 1125)
    treasure_2_left_middle = Point(1004, 1148)
    treasure_3_left_middle = Point(919, 1082)
    treasure_4_left_middle = Point(1014, 1012)
    treasure_5_left_middle = Point(885, 973)
    treasure_6_left_middle = Point(773, 1003)
    treasure_1_success = Rect(804, 1117, 138, 18)
    treasure_3_failed = Rect(919, 1074, 138, 18)

    treasure_left_middle = [
        treasure_1_left_middle,
        treasure_2_left_middle,
        treasure_3_left_middle,
        treasure_4_left_middle,
        treasure_5_left_middle,
        treasure_6_left_middle
    ]

    neighbors_tab = Point(740, 1100)
    guild_tab = Point(805, 1100)
    friends_tab = Point(870, 1100)
    friends_tab_collapsed = Point(870, 1226)

    chair_rect = Rect(340, 1200, 21, 21)
    chair_size = Size(21, 21)
    friend_spacing = 107
    friend_rect = Rect(264, 1120, 98, 119)
    friend_name_rect = friend_rect
    friend_name_rect.height = 16
    friend_tavern_name_rect = Rect(460, 388, 442, 28)

    blueprint_close = Point(720, 832)
    incident_ok = Point(636, 732)

    friends_forward_button = Point(chair_rect.x + friend_spacing*5 + 35, chair_rect.y - 20)
    friends_back_button = Point(chair_rect.x - friend_spacing + 10, chair_rect.y + 10)

    first_alchemist = Point(1977, 1110)
    right_alchemist = Point(2072, 1065)
    last_alchemist = Point(1606, 925)
    rows_alchemist = 7