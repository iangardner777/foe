from Rect import *


class Colors:
    def nameOf(key):
        dict = vars(Colors)
        for k in dict:
            # print(k, dict[k])
            if dict[k] is key:
                return k

    TOP_LEFT = "top_left"
    TOP_LEFT_850 = "top_left_850_0"
    TOP_LEFT_900 = "top_left_900_0"
    TOP_LEFT_950 = "top_left_950_0"
    sums = {
        TOP_LEFT    :(Rect(200, 200, 20, 20), 8778),
        # TOP_LEFT : (Rect(100, 100, 20, 20), 18686),
        TOP_LEFT_850:(Rect(200, 200, 20, 20), 7732),
        # TOP_LEFT_850 : (Rect(100, 100, 20, 20), 11586),
        TOP_LEFT_900:(Rect(200, 200, 20, 20), 11158),
        # TOP_LEFT_900 : (Rect(100, 100, 20, 20), 12311),
        TOP_LEFT_950:(Rect(200, 200, 20, 20), 4741)
        # TOP_LEFT_950 : (Rect(100, 100, 20, 20), 8972)
    }

    FRIEND_ACCEPT_OKAY = "friend_accept_ok"
    loc_to_color = {
        FRIEND_ACCEPT_OKAY:(Point(721, 720), (151, 83, 34))
    }

    last_tavern_seat = (38, 38, 41)
    last_tavern_seat_2 = (37, 37, 41)

    # treasure_hunt_normal = 33865
    treasure_hunt_disabled = 14544
    treasure_hunt_ready = 4882
    treasure_hunt_normal = 7707

    treasure_x_left_middle = (68, 85, 111)
    treasure_complete_left_middle = (153, 84, 35)

    friends_tab = (114, 113, 111)
    friends_tab_highlighted = (140, 143, 144)
    friends_tab_list = [
        friends_tab,
        friends_tab_highlighted,
        (138, 141, 142),
        (113, 117, 122)
    ]

    chair_blank = 1281
    chair_wait = 10220
    chair_open = 8716

    aid_wait = (46, 24, 8)
    aid_ready = (149, 81, 33)
    aid_accept_friend = (88, 134, 31)

    incident_ok = (158, 89, 37)

    blueprint_close = (123, 38, 26)
    blueprint_close_2 = (122, 37, 25)