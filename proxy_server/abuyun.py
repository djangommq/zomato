
# 代理中间件，使用阿布云
import base64
import requests


class AbuyunProxy(object):
    """
    使用方法, 见测试
    """
    def __init__(self):
        # 代理服务器
        self.proxyHost = "http-dyn.abuyun.com"
        self.proxyPort = "9020"

        # 代理隧道验证信息
        self.proxyUser = "HU80498W9ZK49KGD"
        self.proxyPass = "60DBD202DC5E8F35"

        # for Python3 requests
        self.proxies = None

    def get_proxy(self):

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host" : self.proxyHost,
            "port" : self.proxyPort,
            "user" : self.proxyUser,
            "pass" : self.proxyPass,
            }

        self.proxies = {
            "http" : self.proxyMeta,
            "https" : self.proxyMeta,
            }
        return self.proxies
    

def get_proxies():
    abuyun = AbuyunProxy()
    proxies = abuyun.get_proxy()
    # print('阿布云代理: {}'.format(proxies))
    return proxies


if __name__ == "__main__":
    abuyun = AbuyunProxy()
    proxies = abuyun.get_proxy()
    url = 'http://test.abuyun.com'
    r = requests.get(url, proxies=proxies)
    print(r.text)

