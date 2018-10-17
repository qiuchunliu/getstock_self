# 爬取 百度股票 页面信息
# 有时候用浏览器刷新页面都丢失，
# 爬虫经常报错
from bs4 import BeautifulSoup
import requests
import re
# 导入需要的库

'''
在东方财富网上获取深圳股票的代码
用于后续构造每个股票信息的网址
'''
ht = requests.get('http://quote.eastmoney.com/stocklist.html')
ht.encoding = ht.apparent_encoding
hts = BeautifulSoup(ht.text, 'html.parser')
aa = hts.find(id='quotesearch').contents
for i in aa:
	if i == '\n':
		# 有很多换行在列表里
		aa.pop(aa.index(i))
		# 将换行符去掉

lis = aa[4].find_all('li')
dic = {}
for st in lis:
	cw = str(st.string).split('(')[0]
	stri = 'sz' + re.search(r'(\d{6})', str(st.string)).group()
	dic[cw] = stri
	# 构造键值对：{股票名称：代码}
print(len(dic))

'''
根据用户输入的股票名称，获取代码，进而获取网址进行爬取信息
'''
name = input('股票名称：')
stnum = dic[name]
# print(stnum)
url = 'https://gupiao.baidu.com/stock/{}.html'.format(stnum)

# url = 'https://gupiao.baidu.com/stock/sz000067.html'

'''
获取股票页面
'''
head = {
	'Connection': 'keep-alive',
	'Host': 'gupiao.baidu.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64;rv:62.0) Gecko/20100101 Firefox/62.0'
}
htm = requests.get(url, headers=head)
htm.encoding = htm.apparent_encoding
htss = BeautifulSoup(htm.text, 'lxml')
print(htss)
line1 = htss.find_all('div', class_='line1')
# print(line1[0].find_all('dl'))
cjl_name = line1[0].find_all('dl')[1].dt.text
# 获取“成交量”
cjl_data = line1[0].find_all('dl')[1].dd.text
# 获取“成交量”数据
print(cjl_name, '--', cjl_data)
line2 = htss.find_all('div', class_='line2')
# print(line2[0].find_all('dl'))
zsz_name = line2[0].find_all('dl')[7].dt.text
# 获取“总市值”
zsz_data = line2[0].find_all('dl')[7].dd.text
# 获取“总市值”数据
print(zsz_name, '--', zsz_data)

