# coding:utf-8
# by chisec
#
# addFields
# 从爬取到的网页中提取字段
#

import simplejson as json


def get_data_from_page(filename):
    try:
        file = open(filename, 'r')
    except Exception:
        print('not found')
        return {}
    s = file.read()
    file.close()

    print('网页中得到：')

    start = s.find('【') + 1
    end = s.find('】')
    name = s[start:end]
    # print('姓名：' + name)

    start = s.find('，') + 1
    end = s.find('，', start)
    zc = s[start:end]
    # print('职称：' + zc)

    start = s.find('<a href=\\"\\/hospital\\/')
    start = s.find('>', start) + len('>')
    end = s.find('<\\/a>', start)
    hospital = s[start:end].encode().decode('unicode_escape')
    print('hospital:', hospital)

    # \u64c5\u3000\u3000\u957f == 擅　　长
    start = s.find("\\u64c5\\u3000\\u3000\\u957f")
    start = s.find("\\n\\t\\t\\t\\t       ", start) + len("\\n\\t\\t\\t\\t       ")
    end = s.find('\\t', start)
    sc = s[start:end].encode().decode('unicode_escape')
    if sc.find('<') != -1 or sc.find('>') != -1:
        sc = "暂无"
    sc = sc.splitlines()[0]
    sc = sc.replace('\\/', '、')
    # print('擅长：' + sc)

    start = s.find('<a class=blue href="//') + len('<a class=blue href="//')
    end = s.find('/?', start)
    homepage = 'https://'+s[start:end]
    # print('HomePage: ', homepage)

    return {'hospital': hospital, 'name': name, '职称': zc, '擅长': sc, 'HomePage': homepage}


# load data
file = open('./data/好大夫_modified_2.json', 'r')
json_str = file.read()
file.close()
data = json.loads(json_str)


data_new = []
data_removed = []
for line in data:
    arr = str(line['link']).split('/')
    arr.reverse()
    filename = './data/pages/' + arr[0]
    # print(line['医院名称'])
    res = get_data_from_page(filename)
    if res == {}:
        data_removed.append(line)
    else:
        data_new.append({**line, **res})

# 导出 json
output = open('./data/好大夫_modified_3.json', 'w+')
output.write(json.dumps(data_new))
output.close()

output = open('./data/好大夫_removed_3.json', 'w+')
output.write(json.dumps(data_removed))
output.close()