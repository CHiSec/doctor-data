# coding:utf-8
# by chisec
#
# fix2:
# 1. 去除重复
# 2. 解决同一个医生对应多个科室的问题
# 3. 移除了名为普通门诊的医生
# 4. 移除了 名字、科室 中的list
#

import simplejson as json


# 除重函数
def remove_duplicate(s):
    new_s = []
    for x in s:
        if x not in new_s:
            new_s.append(x)
    return new_s


# ------- 开始处理 -------


# 打开文件
file = open('./data/好大夫_modified.json', 'r')
json_str = file.read()
file.close()

# 解析json
data = json.loads(json_str)

# 除重
cnt1 = len(data)
data = list(remove_duplicate(data))
cnt2 = len(data)
print('去除的重复数：'+str(cnt1 - cnt2))

# 解决同一个医生对应多个科室的问题
for line in data:
    if len(line['科室']) > 1:
        print('发现问题：' + str(line))
        office = ''
        for one in line['科室']:
            if one.find('科') is not -1:
                office = one
        line['科室'] = [office]
        print('解决后：' + str(line))

# 删除名为普通门诊的医生
cnt1 = len(data)
data = [e for e in data if e['名字'] != ['普通门诊']]
cnt2 = len(data)
print('移除了名为普通门诊的医生：'+str(cnt1-cnt2))

# 移除 名字、科室 中的list
new_data = []
for e in data:
    new_data.append({'名字': e['名字'][0], '科室': e['科室'][0], '医院名称': e['医院名称'], 'link': e['link']})
data = new_data

# 导出json
output = open('./data/好大夫_modified_2.json', 'w+')
output.write(json.dumps(data))
output.close()


# output:
#
# 去除的重复数：18
# 发现问题：{'名字': ['韩晓菲'], '科室': ['无痛治疗中心', '麻醉科'], 'link': 'https://www.haodf.com/doctor/DE4r0Fy0C9LuGXJU1pWMtgqa9sDMfNCrT.htm', '医院名称': '北京口腔医院'}
# 解决后：{'名字': ['韩晓菲'], '科室': ['麻醉科'], 'link': 'https://www.haodf.com/doctor/DE4r0Fy0C9LuGXJU1pWMtgqa9sDMfNCrT.htm', '医院名称': '北京口腔医院'}
# 发现问题：{'名字': ['扈大为'], '科室': ['无痛治疗中心', '麻醉科'], 'link': 'https://www.haodf.com/doctor/DE4r0BCkuHzdehbmkticdu-554j7S.htm', '医院名称': '北京口腔医院'}
# 解决后：{'名字': ['扈大为'], '科室': ['麻醉科'], 'link': 'https://www.haodf.com/doctor/DE4r0BCkuHzdehbmkticdu-554j7S.htm', '医院名称': '北京口腔医院'}
# 移除了名为普通门诊的医生：42
#
