# coding:utf-8
import random
import time

import requests
import simplejson as json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
ip_list = []


def get_ip_list(url):
    try:
        # web_data = requests.get(url, headers=get_header(), proxies=get_random_ip(), timeout=10)
        web_data = requests.get(url, headers=get_header(), timeout=10)
    except Exception as e:
        print(e)
        return get_ip_list(url)
    soup = BeautifulSoup(web_data.text, 'html')
    ips = soup.find_all('tr')
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    # # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    # for ip in ip_list:
    #     try:
    #         proxy_host = "https://" + ip
    #         proxy_temp = {"https": proxy_host}
    #         res = urllib.urlopen(url, proxies=proxy_temp).read()
    #     except Exception as e:
    #         ip_list.remove(ip)
    #         continue
    # return ip_list


def get_random_ip():
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_header():
    # user_agent = [
    #     "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
    # ]
    # return {'User-Agent': random.choice(user_agent)}
    return {'User-Agent': ua.random}


# 导出
# for i in range(300):
# if i > 0:
#     url = 'http://www.xicidaili.com/nn/'+str(i)
#     time.sleep(5)
#     print(url)
#     get_ip_list(url)

# 爬取的代理质量太差，改用开源代理库
url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
raw = requests.get(url, headers=get_header()).text
for line in raw.splitlines():
    ip_list.append(json.loads(line))

print('一共获得 ip 数：', len(ip_list))

output = open('./data/ip_list.json', 'w+')
output.write(json.dumps(ip_list))
output.close()

# 过滤非 https 代理
https_ip_list = []
for ip in ip_list:
    if ip['type'] == 'https':
        https_ip_list.append(ip['host'] + ':' + str(ip['port']))

print('过滤非 https 代理后剩余 ip 数：', len(https_ip_list))

file = open('./data/ip_list_https.json', 'w+')
file.write(json.dumps(https_ip_list))
file.close()
