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



def get_random_ip(ip_list):
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
file = open('./data/ip_list.json', 'r')
ip_list_json = file.read()
file.close()
ip_list = json.loads(ip_list_json)

# load data
file = open('./data/好大夫_modified_2.json', 'r')
json_str = file.read()
file.close()
data = json.loads(json_str)

# # 创建一个没有link的dict，以及一个有多link的问题数据dict
# data_without_link = []
# data_without_link_to_be_solved = []
# for one in data:
#     line = {'名字': one['名字'], '科室': one['科室'], '医院名称': one['医院名称']}
#     if line not in data_without_link:
#         data_without_link.append(line)
#     else:
#         if line not in data_without_link_to_be_solved:
#             data_without_link_to_be_solved.append(line)
#
# # 解决问题
# for one in data_without_link_to_be_solved:
#     links = []
#     print('处理：'+str(one))
#     for line in data:
#         if line['名字'] == one['名字'] and line['科室'] == one['科室'] and line['医院名称'] == one['医院名称']:
#             links.append(line['link'])
#     for link in links:
#         pull_data_from_haodf(link)
#         print()

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

tasks = []
for i in range(10):
    tasks.append(grequests.get(data[i+50]['link'], timeout=3, headers=get_header(), proxies=get_random_ip(ip_list)))
    # print(data[i]['link'])

data_new = []
for r in grequests.map(tasks, size=50):
    if r is not None and r.status_code == 200:
        res = pull_data_from_haodf_gq(r)
        data_new.append(res)
    else:
        print(r.status_code)

# todo 加入队列实现失败重试，加入try catch...


def pulling_task(step, offset):
    tasks = []
    for i in range(step):
        tasks.append(
            grequests.get(data[i + offset]['link'], timeout=3, headers=get_header(), proxies=get_random_ip(ip_list)))
        # print(data[i]['link'])

    data_new = []
    for r in grequests.map(tasks, size=50):
        if r is not None and r.status_code == 200:
            res = pull_data_from_haodf_gq(r)
            data_new.append(res)
        else:
            print(r.status_code)


# 导出json
output = open('./data/好大夫_modified_3.json', 'w+')
output.write(json.dumps(data))
output.close()

if __name__ == '__main__':
    print('test')
