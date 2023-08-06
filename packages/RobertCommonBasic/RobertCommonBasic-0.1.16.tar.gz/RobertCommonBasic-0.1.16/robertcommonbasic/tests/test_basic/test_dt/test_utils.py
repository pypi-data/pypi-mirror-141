from robertcommonbasic.basic.dt.utils import get_datetime, convert_time_by_timezone, get_timezone

def test_time():
    tm = get_datetime('Asia/Shanghai').astimezone(get_timezone(str('UTC'))[0])
    utc = convert_time_by_timezone(tm, 'Asia/Shanghai', 'UTC')
    print(utc)

test_time()