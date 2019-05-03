##  部署说明

- 运行环境 python3.7.3
- 依赖包清单在 requirements.txt, 可使用以下命令一键安装：
  ```
  pip install -r requirements.txt
  ```
##  运行说明

1. 首先运行 `fix.py` 将数据格式化为标准 `json`, 导出为 `好大夫_modified.json`
2. 运行 `fix2.py` 以解决下列问题（导出为`好大夫_modified_2.json`）：
    1. 去除重复
    2. 解决同一个医生对应多个科室的问题
    3. 移除名为普通门诊的医生
    4. 移除 名字、科室 中的`list`
3. 运行 `getProxies.py` 以获得数据爬虫所需的`代理 ip`, 导出为 `ip_list.json` 及 `ip_list_https.json`
4. 运行 `fix3.py` 数据爬虫进行扩充字段以及数据校验, 导出为 `好大夫_modified_3.json`, 校验有误的会被移除并放入 `好大夫_removed_3.json`