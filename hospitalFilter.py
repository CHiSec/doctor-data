import simplejson as json


def name_filter(lhs, rhs):
    if len(lhs) == 0 or len(rhs) == 0:
        return 0
    cnt = 0
    long = lhs if len(lhs)>len(rhs) else rhs
    short = rhs if len(lhs)>len(rhs) else lhs
    long_i = 0
    short_i = 0
    while long_i < len(long) and short_i < len(short):
        if long[long_i] == short[short_i]:
            cnt = cnt + 1
            long_i = long_i + 1
            short_i = short_i + 1
        else:
            long_i = long_i + 1

    return cnt / len(short)


if __name__ == '__main__':
    # test
    print('test')
    print(name_filter('首都医科大学附属北京中医医院', '医科大附属中医院'))
    print(name_filter('首都医科大学附属北京中医医院', '医科大附属中医院测试'))

    # load file
    file = open('./data/hosnotcont.json', 'r')
    s = file.read()
    file.close()

    # load data
    data = []
    for i in s.splitlines():
        data.append(json.loads(i))

    # proc
    data_new = []
    data_drop = []
    cnt_new = 0
    cnt_old = 0
    for i in data:
        line = {"name": i['name']}
        cnt_old = cnt_old + 1
        for j in i['whospital'].split(','):
            for k in i['hhospital'].split(','):
                if name_filter(j, k) > 0.9:
                    cnt_new = cnt_new + 1
                    print('cnt_new:', cnt_new, 'cnt_old', cnt_old)
                    new_line = line
                    new_line['whospital'] = j
                    new_line['hhospital'] = k
                    data_new.append(new_line)

    # output
    file = open('./data/hosnotcont_new.json', 'w+')
    file.write(json.dumps(data_new))
    file.close()


