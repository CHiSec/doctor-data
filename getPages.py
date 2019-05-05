# coding:utf-8
# by chisec
#
# getPages
# 爬取网页
#

# patch
from gevent import monkey
monkey.patch_all()

import requests
import simplejson as json
from fake_useragent import UserAgent
import random
import time
import grequests
from queue import Queue


def get_random_ip(ip_list):
    proxy_ip = random.choice(ip_list)
    proxies = {'https': 'https://'+proxy_ip}
    return proxies


def get_header():
    return {'User-Agent': ua.random}


def save_page(r):
    arr = str(r.url).split('/')
    arr.reverse()
    filename = './data/pages/'+arr[0]
    r.encoding = 'gbk'

    print('写入文件：', filename)
    file = open(filename, 'w+')
    file.write(r.text)
    file.close()
    print('写入完成')


def e_handler(request, exception):
    print("Request failed: ", request, ", exception: ", exception)


def pulling_task(data, count):
    data_removed = []
    tasks = []
    for i in data:
        tasks.append(grequests.get(i['link'], headers=get_header(), proxies=get_random_ip(ip_list), timeout=3))

    for r in grequests.imap(tasks, size=200):
        if r is not None:
            if r.status_code == 200 or r.status_code == 404:
                for i in data:
                    if i['link'] == r.url:
                        if r.status_code == 200:
                            count = count + 1
                            print('count: ', count)
                            save_page(r)
                            data.remove(i)
                        elif r.status_code == 404 or r.status_code == 301:
                            data_removed.append(i)
                            data.remove(i)
                        break
            else:
                print(r.status_code)
        # else:
        #     print('None Error')
    # retry
    # if len(data) > 0:
    #     data_new.extend(pulling_task(data, data_removed, count))
    return {"remain": data, "count": count, "removed": data_removed}

# --------- start ------------

# init ua & proxies
ua = UserAgent()
file = open('./data/ip_list_https.json', 'r')
ip_list_json = file.read()
file.close()
ip_list = json.loads(ip_list_json)

# load data
file = open('./data/好大夫_removed_3.json', 'r')
json_str = file.read()
file.close()
data = json.loads(json_str)

# processing
data_removed = []
step = 200
offset = 0
data_block = []
count = 0
while len(data) > 0:
    print('block: ', len(data_block))
    if offset + step > len(data):
        data_block.extend(data[offset:])
    elif len(data_block) == 0:
        data_block = data[offset: offset + step]
        offset = offset + step
    else:
        offset = offset + step - len(data_block)
        data_block.extend(data[offset: offset + step - len(data_block)])
    res = pulling_task(data_block, count)
    data_block = res['remain']
    count = res['count']
    data_removed.extend(res['removed'])


if __name__ == '__main__':
    print('test')
