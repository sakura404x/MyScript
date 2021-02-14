#coding:utf-8
import requests
import re
import time
import threading
import traceback
import os
from xlwt import Workbook
from sys import argv

script, filename = argv
filenames = filename.replace(".txt","")
time1 = time.strftime("%Y-%m-%d", time.localtime())	#获取当前时间，用于生成文件名： %Y-%m-%d-%H_%M_%S
error_log_filename = "%s-%s" % (time1,filenames)
path = "%s-output-logs" % error_log_filename
os.system("mkdir " + path)

xc=int(input('线程数:'))
# xc = int(1)

headers={
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
}

results = []
file = open('%s/%s-error_log.txt' % (path,error_log_filename),'w',encoding="utf-8")
def check(urls):
	for url in urls:
		if "://" not in url:
			url = "http://" + url
			url2 = "https://" + url
		else:
			url = url
		try:
			req = requests.get(url, headers=headers, timeout=10, verify=False)	#跳过证书认证的话加：verify = False
			title = re.findall("<title>(.*?)</title>",req.text,re.S)
			#获取返回包大小
			response_size = len(req.text)
			remainder = response_size % 1024	#计算余数
			response_size //= 1024	#计算整除
			len_size = str(response_size) + "." + str(remainder) + " KB"
			#获取Server信息
			server_info = req.headers['Server']
			results.append([req.status_code,server_info,len_size,title,url])	#列表：用来写入表格
			#赋予颜色
			statusCode = "\033[0;31m{}\033[0m".format(req.status_code)
			server_info = "\033[0;32m{}\033[0m".format(server_info)
			len_size = "\033[0;33m{}\033[0m".format(len_size)
			title = "\033[0;34m{}\033[0m".format(title)
			url = "\033[1;30m{}\033[0m".format(url)
			#输出结果
			print(statusCode + " " + server_info + " " + len_size + " " + title + ' --> ' + url)
			# 写入表格
			book = Workbook()
			sheet1 = book.add_sheet("results")
			for k, j in enumerate(["order","Status_Code", "Server Info", "Size", "Title", "URL"]):
				sheet1.write(0, k, j)
			for index, info in enumerate(results):
				# print(index, info)
				for k, j in enumerate(info):
					# 添加序号 在第一列
					if k == 0:
						sheet1.write(index + 1, k, index + 1)
					sheet1.write(index + 1, k + 1, j)
			book.save('%s/%s-results.xls' % (path,error_log_filename))
		except Exception as e:
			pass
			error_type = "错误类型：",e.__class__.__name__
			error_details = "错误细节：",e
			# print(url)
			# print("错误类型：",e.__class__.__name__)
			# print("错误细节：",e)
			file.write(str(url) + '\n' + str(error_type) + '\n' + str(error_details) + "\n\n")
			# traceback.print_exc()
		

def main():
	with open("%s" % filename, 'r') as f:
		urls_list = f.read().split('\n')
	urls = []
	twoList = [[] for i in range(xc)]
	for i, e in enumerate(urls_list):
		twoList[i % xc].append(e)
	for i in twoList:
		urls.append(i)
	thread_list = [threading.Thread(target=check, args=(urls[i],)) for i in range(len(urls))]
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

if __name__ == '__main__':
    main()
	
