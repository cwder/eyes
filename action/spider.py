import requests
from bs4 import BeautifulSoup

url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"


class Spider:

    def __init__(self):
        pass

    def get_name(self):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Host": "quote.eastmoney.com",
            "Referer": "http://quote.eastmoney.com/center",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }

        requests.adapters.DEFAULT_RETRIES = 5
        try:
            response = requests.get(url, timeout=10, headers=headers)
            response.encoding = 'utf8'
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            games_jq_list = soup.find_all(class_='listview full')
            print(html)
        except:
            pass


if __name__ == '__main__':
    Spider().get_name()
