# coding:utf-8
# by chisec
#
# fix1: 处理 json 为标准格式.
#


from demjson import decode as decodeJSON
from simplejson import dumps as encodeJSON


# 打开文件
file = open('./data/好大夫.json', 'r')
json_str = file.read()
file.close()

# 移除BOM头
if json_str.startswith(u'\ufeff'):
    json_str = json_str.encode('utf8')[3:].decode('utf8')

# 解析json
record_hdf = decodeJSON('['+json_str+']')

# 导出json
output = open('./data/好大夫_modified.json', 'w+')
output.write(encodeJSON(record_hdf))
output.close()
