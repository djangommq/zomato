import requests

class jgProxy():
    def __init__(self):
        self.headers={
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6",
          "Cache-Control": "max-age=0",
          "Host": "d.jghttp.golangapi.com",
          "Proxy-Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        self.url="http://d.jghttp.golangapi.com/getip?num=1&type=1&pro=0&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=110000,130000,140000,150000,210000,310000,320000,330000,340000,350000,360000,370000,410000,420000,430000,440000,500000,510000,530000,610000,620000"

    def get_proxy(self):
        response=requests.get(self.url,headers=self.headers)
        proxy=response.text.replace('\r','').replace('\n','')
        proxies = {
          'http': 'http://{}'.format(proxy),
          'https': 'https://{}'.format(proxy)
        }
        print(proxies)
        return proxies


def get_proxies(proxies):
    jiguang = jgProxy()
    # proxies = jiguang.get_proxy()

    # 测试代理
    # url='https://www.baidu.com/'
    url='http://httpbin.org/get'
    headers={
      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    }

    if proxies != None:
        try:
          response=requests.get(url,headers=headers,proxies=proxies)
          if response.status_code==200:
              return proxies
          else:
            print('换取代理')
            proxies = jiguang.get_proxy()
            return proxies
        except Exception as e:
            print(e.args)
            print('换取代理')
            proxies = jiguang.get_proxy()
            return proxies
    else:
      proxies = jiguang.get_proxy()
      return proxies


if __name__ == '__main__':
    # jiguang=jgProxy()
    # proxy=jiguang.get_proxy()
    proxies=None
    proxies=get_proxies(proxies)
    get_proxies(proxies)
