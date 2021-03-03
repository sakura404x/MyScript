# -*- coding:utf-8 -*-
"""
@Author: Naraku
@File: Github_CVE_Wechat.py
"""
import time
import json
import requests
from operator import itemgetter


def getNews():
    year = time.strftime("%Y", time.localtime(time.time()))
    try:
       api = f"https://api.github.com/search/repositories?q=CVE-{year}&sort=updated"
       response = requests.get(api).text
       data = json.loads(response)
       return data
    except Exception as e:
       print(e, "Github链接不通")


def parseData(index):
    item = items[index]
    cve_name = item['name']
    cve_url = item['svn_url']
    cve_des = item['description']
    if not cve_des:  # 描述为空时会返回None
        cve_des = "Null"
    content = f"{cve_name}: {cve_url}, Des: {cve_des}"
    return content


def sendMsg(content):
    send_url = f"https://sc.ftqq.com/{SCKEY}.send"
    data = {
        "text": "CVE监控提醒",
        "desp": content
    }
    r = requests.post(send_url, data=data)


if __name__ == '__main__':
    SCKEY = "SCU94821Te9d458b475dcb1ad62e72aa114847d3c5e9e6535c498f"
    total = 0  # 初始化
    while True:
        data = getNews()
        if total != data['total_count']:
            total = data['total_count']
            items = sorted(data['items'], key=itemgetter('id'), reverse=True)  # 根据items中的id进行排序
            content = parseData(0)  # 返回最新的1条
            sendMsg(content)
        time.sleep(60)