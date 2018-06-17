# -*- coding: utf-8-*

import urllib,urllib2
import os,sys,time,random
import threading
from threadpool import *
from bs4 import *
from Queue import Queue

reload(sys)
#entype = sys.getfilesystemencoding()

pool_size = 5

crawlUrl = 'http://disclosure.szse.cn/m/search0425.jsp'
pdfUrlPre = 'http://disclosure.szse.cn/'

sysPath = sys.path[0][:-8]
codeFile = '%s/codes.conf' % sysPath

resultDir = "%s/result" % sysPath
pdfDir = '%s/result/PDF/'%sysPath
faultListDir = '%s/result/fault.txt'%sysPath
finishDir = '%s/result/finish.txt'%sysPath

fault_queue = Queue()
finish_queue = Queue()

class Crawler:
	def __init__(self):
		#self.state = int(file('record').readline())
		keyword = '章程'
		kw = keyword.decode('utf8').encode('gb2312')

		self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
						'Connection':'keep=alive',
						'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						#'Accept-Encoding':'gzip, deflate',
						'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.3',
						'Accept-Language':'zh-CN,zh;q=0.8',
						'Content-Type':'application/x-www-form-urlencoded',
						'Host':'disclosure.szse.cn',
						'Origin':'http://disclosure.szse.cn',
						'Referer':'http://disclosure.szse.cn/m/search0425.jsp',
						'Cookie':'JSESSIONID=4A6A85855AB29DA949B0EC0DCD673196'}

		self.values = {
		'leftid':1,
		'lmid':'drgg',
		'stockCode':'0',
		'pageNo':1,
		'keyword':kw,
		'noticeType':'0131',
		'startTime':'2015-01-01',
		'endTime':'2017-07-01',
		'imageField.x':40,
		'imageField.y':13,
		'tyz':''
		}

		if os.path.exists(resultDir) is False:
			os.mkdir(resultDir)

		if os.path.exists(pdfDir) is False:
			os.mkdir(pdfDir)
			os.mkdir(pdfDir+"2015/")
			os.mkdir(pdfDir+"2016/")
			os.mkdir(pdfDir+"2017/")

		if os.path.exists(finishDir) is False:
			temp = file(finishDir,'w')
			temp.close()

		self.ipList = []

	def getIpList(self):
		url = 'http://www.xicidaili.com/nn/'
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
		req = urllib2.Request(url, headers=headers)
		res = urllib2.urlopen(req, timeout=20)
		soup = BeautifulSoup(res.read(), 'lxml')
		ips = soup.find_all('tr')
		for i in range(1, len(ips)):
			ip_info = ips[i]
			tds = ip_info.find_all('td')
			self.ipList.append(tds[1].text + ':' + tds[2].text)

	def getRandomIp(self):
		proxy_ip = 'http://' + random.choice(self.ipList)
		proxies = {'http': proxy_ip}
		return proxies

	def crawl(self,code,useproxy=False):
		self.values['stockCode']=code
		postData = urllib.urlencode(self.values)
		print 'crawling %s ...' % code
		try:
			req = urllib2.Request(url=crawlUrl,headers=self.headers,data=postData)
			if useproxy is True:
				proxies = self.getRandomIp()
				print "Transfering to proxcy http://%s"%proxies["http"]
				proxy_s=urllib2.ProxyHandler(proxies)     
				opener=urllib2.build_opener(proxy_s)
				c = opener.open(req,timeout=20)
			else:
				c = urllib2.urlopen(req,timeout=20)
		except:
			print "Failed crawling %s" % code
			time.sleep(random.randint(5,10))

			if useproxy is False:
				print "try crawling %s again..." % code
				self.crawl(code,True)
			else:
				fault_queue.put("Failed crawling %s"%code)

			return

		resultWeb = c.read()
		#result = resultWeb.decode('gb2312').encode('utf8')

		soup=BeautifulSoup(resultWeb,'lxml')
		td2 = soup.findAll('td',{'class':'td2'})

		if len(td2) == 0:
			print "No pdf found in %s's page" % code
			fault_queue.put("No pdf found in %s's page" % code)
			time.sleep(random.randint(1,3))
			return

		for td2 in td2:
			timeSpan = td2.span.string
			pdfLocal = pdfDir+timeSpan[1:5]+'/'+td2.a.string+".pdf"
			pdfUrl = pdfUrlPre+td2.a.get('href')
			urllib.urlretrieve(pdfUrl, pdfLocal)

		print "%s - succeed!" % code
		finish_queue.put("%s"%code)
		time.sleep(random.randint(1,3))

	def writeLog(self,i):
		if i == 0:
			faultList = file(faultListDir,'w')
			while True:
				if fault_queue.empty(): continue
				text = fault_queue.get()
				faultList.write("%s\n" % text)
				fault_queue.task_done()
				faultList.flush()
		else:
			finishList = file(finishDir,'a')
			while True:
				if finish_queue.empty(): continue
				text = finish_queue.get()
				finishList.write("%s\n" % text)
				finish_queue.task_done()
				finishList.flush()
		

	def setup(self):
		self.getIpList()

		for i in range(2):
			writerFault = threading.Thread(target=self.writeLog,args=(i,))
			writerFault.setDaemon(True)
			writerFault.start()

		fault_queue.join()
		finish_queue.join()

		finishedCode = [code.strip() for code in file(finishDir)]
		codes = [code.strip() for code in file(codeFile) if code.strip() not in finishedCode]
		random.shuffle(codes)

		pool = ThreadPool(pool_size)
		requests = makeRequests(self.crawl,codes)
		[pool.putRequest(req) for req in requests]
		pool.wait()

		print "***********Done************"

cr=Crawler()
cr.setup()