# coding:utf-8
# by chisec
#
# fix3:
# 通过爬取网页扩充字段
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


def pull_data_from_haodf(link):
    print('访问：' + link)

    try:
        r = requests.get(link, headers=get_header(), timeout=3, proxies=get_random_ip(ip_list))
        r.encoding = 'gbk'
        s = r.text
        if r.status_code != 200:
            print('错误：' + str(r.status_code) + '，，重试中')
            # time.sleep(5.0+random.random()*3)
            return pull_data_from_haodf(link)
    except Exception as e:
        print('错误：' + str(e) + '，，重试中')
        return pull_data_from_haodf(link)

    print('网页中得到：')

    start = s.find('【') + 1
    end = s.find('】')
    name = s[start:end]
    print('姓名：' + name)

    start = s.find('，') + 1
    end = s.find('，', start)
    zc = s[start:end]
    print('职称：' + zc)

    # \u64c5\u3000\u3000\u957f == 擅　　长
    start = s.find("\\u64c5\\u3000\\u3000\\u957f")
    start = s.find("\\n\\t\\t\\t\\t       ", start) + len("\\n\\t\\t\\t\\t       ")
    end = s.find('\\t', start)
    sc = s[start:end].encode().decode('unicode_escape')
    if sc.find('<') != -1 or sc.find('>') != -1:
        sc = "暂无"
    sc = sc.splitlines()[0]
    print('擅长：' + sc)

    return {'职称': zc, '擅长': sc}
    # return {'名字': name, '职称': zc, '擅长': sc}


# --------- start ------------

# init ua & proxies
ua = UserAgent()
file = open('./data/ip_list_https.json', 'r')
ip_list_json = file.read()
file.close()
ip_list = json.loads(ip_list_json)

# load data
file = open('./data/好大夫_modified_2.json', 'r')
json_str = file.read()
file.close()
data = json.loads(json_str)

def pull_data_from_haodf_gq(r):
    print(r.status_code)
    r.encoding = 'gbk'
    s = r.text
    print('网页中得到：')

    start = s.find('【') + 1
    end = s.find('】')
    name = s[start:end]
    print('姓名：' + name)

    start = s.find('，') + 1
    end = s.find('，', start)
    zc = s[start:end]
    print('职称：' + zc)

    # \u64c5\u3000\u3000\u957f == 擅　　长
    start = s.find("\\u64c5\\u3000\\u3000\\u957f")
    start = s.find("\\n\\t\\t\\t\\t       ", start) + len("\\n\\t\\t\\t\\t       ")
    end = s.find('\\t', start)
    sc = s[start:end].encode().decode('unicode_escape')
    if sc.find('<') != -1 or sc.find('>') != -1:
        sc = "暂无"
    sc = sc.splitlines()[0]
    print('擅长：' + sc)

    return {'职称': zc, '擅长': sc}

# todo 加入队列实现失败重试，加入try catch...


def add_id(data):
    i = 0
    return [{**e, 'id': i} for e in data]


def e_handler(request, exception):
    print("Request failed: ", request, ", exception: ", exception)


def pulling_task(data, count):
    data_removed = []
    tasks = []
    for i in data:
        tasks.append(grequests.get(i['link'], headers=get_header(), proxies=get_random_ip(ip_list), timeout=3))

    data_new = []
    for r in grequests.imap(tasks, size=200):
        if r is not None and (r.status_code == 200 or r.status_code == 404):
            if r.status_code == 200 or r.status_code == 404:
                for i in data:
                    if i['link'] == r.url:
                        if r.status_code == 200:
                            print('count: ', count)
                            count = count+1
                            data_new.append({**i, **pull_data_from_haodf_gq(r)})
                            data.remove(i)
                        elif r.status_code == 404:
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
    return {"new":data_new, "remain": data, "count": count, "removed": data_removed}


data_new = []
data_removed = []
step = 200
offset = 0
data_block = []
count = 0
while len(data_new) + len(data_removed) < len(data):
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
    data_removed.extend(res['removed'])
    data_new.extend(res['new'])
    data_block = res['remain']
    count = res['count']
    # 导出json
    output = open('./data/好大夫_modified_3.json', 'w+')
    output.write(json.dumps(data_new))
    output.close()
    output = open('./data/好大夫_removed_3.json', 'w+')
    output.write(json.dumps(data_removed))
    output.close()


if __name__ == '__main__':
    print('test')
