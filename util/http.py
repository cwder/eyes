import requests


class Http:

    @staticmethod
    def http_warp(url, encoding='utf8'):
        def decorated(func):
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
            response = requests.get(url, timeout=10, headers=headers)
            response.encoding = encoding
            func(response.text)
        return decorated

