# coding:utf-8
import random
import time

import simplejson as json
import requests


file = open('./data/好大夫_modified_2.json', 'r')
json_str = file.read()
file.close()

user_agent = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
    ]


def get_header():
    return {'User-Agent': random.choice(user_agent)}


def pull_data_from_haodf(link):
    print('访问：' + link)

    r = requests.get(link, headers=get_header(), timeout=30)
    r.encoding = 'gbk'
    s = r.text
    if r.status_code == 403:
        print('错误：'+str(r.status_code)+'，，重试中')
        time.sleep(4.0+random.random()*3)
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
    if sc.find('我找普通门诊大夫看过病，我来发表第一篇看病经验！') != -1:
        sc = "暂无"
    print('擅长：' + sc)

    return {'名字': name, '职称': zc, '擅长': sc}


data = json.loads(json_str)

# 创建一个没有link的dict，以及一个有多link的问题数据dict
data_without_link = []
data_without_link_to_be_solved = []
for one in data:
    line = {'名字': one['名字'], '科室': one['科室'], '医院名称': one['医院名称']}
    if line not in data_without_link:
        data_without_link.append(line)
    else:
        if line not in data_without_link_to_be_solved:
            data_without_link_to_be_solved.append(line)

# 解决问题
for one in data_without_link_to_be_solved:
    links = []
    print('处理：'+str(one))
    for line in data:
        if line['名字'] == one['名字'] and line['科室'] == one['科室'] and line['医院名称'] == one['医院名称']:
            links.append(line['link'])
    for link in links:
        pull_data_from_haodf(link)
        print()


for one in data:
    if one['名字'] == ['普通门诊']:
        print("问题数据："+str(one))
        pull_data_from_haodf(one['link'])



import re
import requests
import grequests

def get_url(html):
    m = re.findall(r'(https|http?:\/\/[^\s]+.com|cn|org)', html)
    return (m)
html= requests.get("http://www.best918.com/").text
urls = get_url(html)
gen = (grequests.get(i, timeout=3)  for i in urls)
for i in grequests.imap(gen, size=200):
    print(i.url)
    for k in get_url(i.text):
        urls.append(k)



requests.get("https://www.haodf.com/doctor/DE4r0Fy0C9Luwmy55s7SGO94z9ZEju-cx.htm", headers=get_header())

