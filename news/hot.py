from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
import pytz
from math import log

naive = parse_datetime("1970-01-01 00:00:00")
epoch = pytz.timezone("Asia/Shanghai").localize(naive, is_dst=None)

def epoch_seconds(post_time):
    """Returns the number of seconds from the epoch to post_time."""
    td = post_time - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def hot(score, post_time):
    """The hot formula."""
    order = log(score+1, 10)
    seconds = epoch_seconds(post_time) - 1134028003
    return round(order + seconds / 90000, 7)
