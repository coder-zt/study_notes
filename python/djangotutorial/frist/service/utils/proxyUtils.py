# 代理工具

import requests

proxy_server = f"http://H31335518696Z2RC:179B7DDBE85E81FD@http-cla.abuyun.com:9030"

proxies = {"http": proxy_server, "https": proxy_server}


def switchProxy():
    switchUrl = "http://proxy.abuyun.com/switch-ip"
    requests.get(switchUrl, proxies=proxies)
