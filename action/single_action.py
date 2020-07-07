import re

from sqlalchemy import Column, Integer

from create_db import Base
from model.shares import Shares
from util.url import Url
from bs4 import BeautifulSoup as bs

from util.util import Util


@Util.http_wrap(url=Url.get_single_url(), encoding='gbk')
def spiderSingleTable(text):
    soup = bs(text, "html.parser")
    items = soup.find_all(target="_blank")
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    for i in items:
        res = re.search(p1, i.text)
        if res is not None:
            data = res.group()
            if data.startswith("(600") or data.startswith("(601") \
                    or data.startswith("(602") or data.startswith("(000"):
                a = i.text.replace(')', '')
                res = a.split('(')
                # Shares.addShares(res[1], res[0])
                t = type(res[1], (Base,),
                         {"__tablename__": res[1], "id": Column(Integer, autoincrement=True, primary_key=True)})
