from Locs import *
from Core import *

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def fromTuple(t):
        return Color(t[0], t[1], t[2])

    def toTuple(self):
        return self.r, self.g, self.b

    def __eq__(self, other: str) -> bool:
        return self.equals(other)

    def equals(self, other, variance=0):
        if type(other) is not Color: return false
        return abs(self.r - other.r) <= variance and abs(self.g - other.g) <= variance and abs(self.b - other.b) <= variance

    def isVeryClose(self, other, warn=false):
        eq = self.equals(other, 2)
        if eq and warn and self != other:
            Logging.warning(f"Color: {self.toString()} didn't match exactly: {other.toString()}")
        return eq

    def isClose(self, other):
        return self.equals(other, 5)

    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def toString(self):
        return f"{Colors.nameOf(self)} {self}"

    def codeString(self):
        return f"Color{self}"


class Colors:
    NOT_NAMED = "not_named"
    def nameOf(key):
        vars_dict = vars(Colors)
        for k in vars_dict:
            if vars_dict[k] == key:
                return k
        return Colors.NOT_NAMED

    TOP_LEFT = "top_left"
    TOP_LEFT2 = "top_left2"
    TOP_LEFT_850 = "top_left_850_0"
    TOP_LEFT_900 = "top_left_900_0"
    TOP_LEFT_950 = "top_left_950_0"
    sums = {
        TOP_LEFT    :(Rect(200, 200, 20, 20), 8764, 8955, 8165),
        TOP_LEFT_850:(Rect(300, 200, 20, 20), 4741, 4534, 4606),
        TOP_LEFT_900:(Rect(250, 200, 20, 20), 4741, 4534, 4606),
        TOP_LEFT_950:(Rect(200, 200, 20, 20), 4741, 4534, 4606),

        # "test":(Rect(1150, 200, 20, 20), 4606)
    }

    FRIEND_ACCEPT_OKAY = "friend_accept_ok"
    TAVERN_OKAY = "tavern_ok"
    FRIENDS_TAVERN_CLOSE = "friends_tavern_close"
    INCIDENT_OKAY = "incident_ok"
    BP_CLOSE = "bp_close"
    GB_REWARD_OKAY = "gb_reward_ok"
    PLAY_NOW = "play_now"
    loc_and_color = {
        FRIEND_ACCEPT_OKAY:(Point(721, 720), Color(151, 83, 34)),
        TAVERN_OKAY:(Locs.tavern_ok, Color(152, 83, 34)),
        FRIENDS_TAVERN_CLOSE:(Point(731, 893), Color(129, 40, 28)),
        INCIDENT_OKAY:(Locs.incident_ok, Color(158, 89, 37)),
        BP_CLOSE:(Locs.blueprint_close, Color(122, 37, 25)),
        GB_REWARD_OKAY:(Point(622, 762), Color(151, 83, 34)),
        PLAY_NOW:(Point(565, 534), Color(136, 28, 0))
    }

    last_tavern_seat = Color(37, 37, 41)
    last_tavern_seat_obsolete = Color(38, 38, 41)

    # treasure_hunt_normal = 33865
    treasure_hunt_disabled = 14544
    treasure_hunt_ready = 4882
    treasure_hunt_normal = 7707

    treasure_x_left_middle = Color(68, 85, 111)
    treasure_complete_left_middle = Color(153, 84, 35)

    friends_tab = Color(114, 113, 111)
    friends_tab_highlighted = Color(140, 143, 144)
    friends_tab_list = [
        friends_tab,
        friends_tab_highlighted,
        Color(140, 144, 144),
        Color(138, 141, 142),
        Color(113, 117, 122)
    ]

    chair_blank = 1281
    chair_wait = 10220
    chair_open = 8716

    aid_wait = Color(46, 24, 8)
    aid_ready = Color(149, 81, 33)
    aid_accept_friend = Color(88, 134, 31)