import datetime
from enum import Enum, auto

import pytz

ISRAEL_TIMEZONE = pytz.timezone('Israel')

CHANNEL_ID = 1229734808507256835


class School(Enum):
    IRONIH = {
        1: (datetime.time(8, 15), datetime.time(9, 0)),
        2: (datetime.time(9, 0), datetime.time(9, 50)),
        3: (datetime.time(10, 10), datetime.time(10, 55)),
        4: (datetime.time(11, 0), datetime.time(11, 45)),
        5: (datetime.time(11, 50), datetime.time(12, 35)),
        6: (datetime.time(12, 55), datetime.time(13, 35)),
        7: (datetime.time(13, 40), datetime.time(14, 25)),
        8: (datetime.time(14, 30), datetime.time(15, 15)),
        9: (datetime.time(15, 15), datetime.time(16, 0)),
        10: (datetime.time(16, 0), datetime.time(16, 45)),
        11: (datetime.time(16, 45), datetime.time(17, 30))
    }
    REALI = {  # TODO: complete this
        1: (datetime.time(8, 15), datetime.time(9, 0)),
        2: (datetime.time(9, 0), datetime.time(9, 50)),
        3: (datetime.time(10, 10), datetime.time(10, 55)),
        4: (datetime.time(11, 0), datetime.time(11, 45)),
        5: (datetime.time(11, 50), datetime.time(12, 35)),
        6: (datetime.time(12, 55), datetime.time(13, 35)),
        7: (datetime.time(13, 40), datetime.time(14, 25)),
        8: (datetime.time(14, 30), datetime.time(15, 15)),
        9: (datetime.time(15, 15), datetime.time(16, 0)),
        10: (datetime.time(16, 0), datetime.time(16, 45)),
        11: (datetime.time(16, 45), datetime.time(17, 30)),
    }


SCHOOL_SCHEDULE = {}


def initSchedule(school_enum):
    global SCHOOL_SCHEDULE
    print("Initializing schedule for", school_enum)
    SCHOOL_SCHEDULE = school_enum.value


initSchedule(School.IRONIH) # Init the schedule by default to IroniH
