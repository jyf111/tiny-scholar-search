import urllib.request
from urllib.parse import urlencode

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

# 代理IP,由快代理提供
proxy = '183.232.56.161:8099'
proxy_values = "%(ip)s" % {'ip': proxy}
proxies = {"http": proxy_values, "https": proxy_values}
# 设置代理
handler = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(handler)
# 发送request请求
req = urllib.request.Request('http://www.google.com/', headers=headers)
res = opener.open(req)
# 打印response code
print(res.status)
# urllib字符串默认是bytes类型,需要转换到utf-8
print(res.read().decode('utf-8'))