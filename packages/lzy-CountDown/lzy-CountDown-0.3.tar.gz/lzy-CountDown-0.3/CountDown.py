import time
import requests


def CountDown(*args):
    response = requests.get('http://www.baidu.com')
    gmt_ts = time.mktime(time.strptime(response.headers['date'][5:25], "%d %b %Y %H:%M:%S"))
    return int(time.mktime(time.strptime(*args, "%Y-%m-%d %H:%M:%S")))-int(gmt_ts + 8 * 3600)