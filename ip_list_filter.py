# coding:utf-8
#https://www.haodf.com/

from gevent import monkey
monkey.patch_all()

import simplejson as json
import grequests
import requests
from fake_useragent import UserAgent


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


# init ua & proxies
ua = UserAgent()
file = open('./data/ip_list_https.json', 'r')
ip_list_json = file.read()
file.close()
ip_list = json.loads(ip_list_json)

# tasks = []
ip_list_new = []
for i in ip_list:
    print('count: ',i,', ok: ', len(ip_list_new))
    # tasks.append(grequests.get('https://www.haodf.com/', timeout=5, headers=get_header(), proxies=i))
    try:
        r = requests.get('https://www.haodf.com/', timeout=2, headers=get_header(), proxies={'https': 'https://'+i})
        if r.status_code != 200:
            print('remove: '+ i)
        else:
            ip_list_new.append(i)
    except Exception:
        print('remove: '+ i)
file = open('./data/ip_list_https_filtered.json', 'w+')
file.write(json.dumps(ip_list_new))
file.close()
