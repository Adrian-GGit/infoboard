import datetime
import time

def timestamp_to_datetime(timestamp, timezone):
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp)
    timezone_offset = datetime.timedelta(seconds=timezone)
    return (utc_dt + timezone_offset).strftime('%-H:%M')


def get_system_time():
    return datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y").strftime('%-H:%M')
