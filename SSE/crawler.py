# -*- coding: utf-8-*

import urllib,urllib2,os,sys,time,random,json,threading
from bs4 import *
from threadpool import *
from Queue import Queue

pool_size = 8

crawlUrl = 'http://query.sse.com.cn/security/stock/queryCompanyStatementNew.do'
pdfUrlPre = 'http://static.sse.com.cn'

sysPath = os.path.dirname(os.path.realpath(sys.argv[0]))
codeFile = '%s/codes.txt' % sysPath

resultDir = "%s/result" % sysPath
pdfDir = '%s/result/PDF/'%sysPath
faultListDir = '%s/result/fault.txt'%sysPath
finishDir = '%s/result/finish.txt'%sysPath

fault_queue = Queue()
finish_queue = Queue()

_jsonp_begin = r'jsonpCallback57459('
_jsonp_end = r')'

class Crawler:
	def __init__(self):
		if os.path.exists(codeFile) is False:
			print "codes.txt not found!"
			sys.exit(1)

		kw = '章程'
		#kw = keyword.decode('utf8').encode('gb2312')

		self.headers = {
						'Accept':'*/*',
						'Accept-Language':'zh-CN,zh;q=0.8',
						'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
						'Connection':'keep=alive',
						#'Accept-Encoding':'gzip, deflate',
						#'Accept-Charset':'gb2312,utf-8;q=0.7,*;q=0.3',
						'Content-Type':'application/x-www-form-urlencoded',
						'Host':'query.sse.com.cn',
						'Referer':'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
						"Cookie":"yfx_c_g_u_id_10000042=_ck17073014071517777735903783667; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042=; yfx_f_l_v_t_10000042=f_t_1501394835769__r_t_1502027269743__v_t_1502027928444__r_c_1; VISITED_MENU=%5B%228349%22%5D; VISITED_STOCK_CODE=%5B%22600000%22%2C%22600085%22%5D; VISITED_COMPANY_CODE=%5B%22600000%22%2C%22600085%22%5D; seecookie=%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C%2C%5B600085%5D%3A%u540C%u4EC1%u5802"}

		self.values = {
		'jsonCallBack':'jsonpCallback57459',
		'isPagination':'true',
		'productId':'0',
		'keyWord':kw,
		'isNew':1,
		'reportType2':'',
		'reportType':'ALL',
		'beginDate':'2015-01-01',
		'endDate':'2017-07-01',
		'pageHelp.pageSize':25,
		'pageHelp.pageCount':50,
		'pageHelp.pageNo':1,
		'pageHelp.beginPage':1,
		'pageHelp.cacheSize':1,
		'pageHelp.endPage':5,
		'_':'1502027928988'
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

	def crawl(self,code,usePorxy = True):
		self.values['productId']=code
		queryData = urllib.urlencode(self.values)
		url = '%s?%s'%(crawlUrl,queryData)

		req = urllib2.Request(url=url,headers=self.headers)

		try:

			if usePorxy is True:
				proxies = self.getRandomIp()

				print 'crawling [%s] with %s ...' % (code, proxies['http'])
				proxy_s=urllib2.ProxyHandler(proxies)     
				opener=urllib2.build_opener(proxy_s)
				c = opener.open(req,timeout=20)
			else:
				print 'crawling [%s] with local IP ...' % code
				c = urllib2.urlopen(req,timeout=20)

			resultWeb = c.read()
			res = self.parseJsonp(resultWeb)

			if res is False:
				fault_queue.put("[WARNING] %s has no pdf found." % code)
			else:
				print "*********************\n* %s - succeed! *\n*********************" % code
				finish_queue.put("%s"%code)

		except Exception,e:
			# Another chance
			if usePorxy is True:
				self.crawl(code,False)
			else:
				print "Failed crawling %s: %s" % (code,e.message)
				time.sleep(1)
				fault_queue.put("[ERROR] Failed crawling %s"%code)
			return

	def parseJsonp(self,jsonpStr):
		jsonpStr = jsonpStr.strip()
		if not jsonpStr.startswith(_jsonp_begin) or not jsonpStr.endswith(_jsonp_end):
			raise ValueError("Invalid json str: %s" % jsonpStr)

		returnDict = json.loads(jsonpStr[len(_jsonp_begin):-len(_jsonp_end)])
		datas = returnDict["result"]

		if len(datas) == 0:
			return False

		for data in datas:
			date = data["SSEDate"]
			year = date[0:4]
			dateStr = date.replace('-','')

			pdfLocal = pdfDir+year+'/'+data["title"]+"("+dateStr+")"+".pdf"
			pdfUrl = pdfUrlPre+data["URL"]
			urllib.urlretrieve(pdfUrl,pdfLocal)


	def writeLog(self,i):
		if i == 0:
			logFile = file(faultListDir,'w')
			queue = fault_queue
		else:
			logFile = file(finishDir,'a')
			queue = finish_queue

		while True:
			if queue.empty(): continue
			text = queue.get()
			logFile.write("%s\n" % text)
			queue.task_done()
			logFile.flush()
		

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
		pool = ThreadPool(pool_size)
		requests = makeRequests(self.crawl,codes)
		[pool.putRequest(req) for req in requests]
		pool.wait()

		print "***********Done************"

cr=Crawler()
cr.setup()