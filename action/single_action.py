from util.http import Http
from util.url import Url


@Http.http_warp(url=Url.get_single_url(), encoding='gbk')
def process(text):
    print(text)
    pass
