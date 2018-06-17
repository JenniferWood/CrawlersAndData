import urllib2,time,random,os
from bs4 import BeautifulSoup
import sys
from urlparse import urljoin
reload(sys)
sys.setdefaultencoding( "utf-8" )

class crawler:
	def __init__(self):
		#self.state = int(file('record').readline())
		self.headers = {}
		self.headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		self.headers['Connection']='keep=alive'
		self.headers['Cookie']='''
		_hc.v="\\"9bf0c497-6bcd-442c-8831-11af2b3775ac.1462454285\\""; __utma=1.1396579858.1463541809.1463541809.1490843498.2; __utmz=1.1490843498.2.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dper=fb429c325dec3e190e48f269c9255d5c76616b0349544d395f1333f17c118ff8; ua=dpuser_0057853301; ll=7fd06e815b796be3df069dec7836c3df; PHOENIX_ID=0a010444-15b6ad6d295-15f2935; __mta=54809364.1492146359027.1492146681995.1492147031072.3; s_ViewType=10; JSESSIONID=D89CD5F58A5A9CC936093B4FEF5ED401; aburl=1; cy=2; cye=beijing
		'''
		print self.headers

	def shop(self,s=0,pages=50):
		crawled = [line.strip() for line in file('record')]

		i=s
		while i<pages:
			t = random.randint(1,60)
			print "wait %d seconds" % t
			time.sleep(t)

			url = "https://www.dianping.com/search/category/2/10/g110o10p%d" % (i+1)
			print "crawling url %s" % url

			try:
				req = urllib2.Request(url=url,headers=self.headers)
				c=urllib2.urlopen(req,timeout=20)
			except:
				print "Could Not Open %s" % url
				i+=1
				continue
			soup=BeautifulSoup(c.read(),'lxml')
			try:
				shops = soup.find_all(attrs={'data-hippo-type':'shop'})
				for shop in shops:
					stm = shop['href'][6:]
					if stm in crawled:
						print "%s is crawled" % stm
						continue

					shopurl = urljoin(url,shop['href'])
					if self.crawl(shopurl,200,50) is True:
						out = file('record','a')
						out.write('\n%s'%stm)
						out.close()
					else:
						print "Interpret",stm
						break
			except:
				print "Something happened"
				break
			i+=1
			


	def crawl(self,shopurl,pages=200,start = 0):
		i = start
		nobreakflag = True
		#print "start page %d" % (i+1)

		while i<pages:

			url = shopurl+"/review_more?pageno=%d" % (i+1)
			print "crawling url %s" % url
			try:
				req = urllib2.Request(url=url,headers=self.headers)
				c=urllib2.urlopen(req,timeout=20)
			except:
				print "Could Not Open %s" % url
				i+=1
				t = random.randint(0,30)
				print "wait %d seconds" % t
				time.sleep(t)
				continue

			soup=BeautifulSoup(c.read(),'lxml')
			try:
				title = soup.find("div",class_="revitew-title").h1.a.string

				if os.path.exists('data/%s/%d-1.txt' %(title,i+1)):
					print "This page is crawled"
					i+=1
					continue

				if os.path.exists('data/'+title) is False:
					os.mkdir('data/'+title)

				contents = soup.find_all(class_="J_brief-cont")
				for j in range(len(contents)):
					revfile = 'data/%s/%d-%d.txt'%(title,i+1,j+1)
					if os.path.exists(revfile): 
						continue

					out = file('data/%s/%d-%d.txt'%(title,i+1,j+1),'w')
					try:
						out.write("%s\n" % (contents[j].string.strip()))
					except:
						out.write("%s\n" % (contents[j].get_text('\n','br/').strip()))
				i+=1
				nobreakflag = True
				t = random.randint(0,30)
				print "wait %d seconds" % t
				time.sleep(t)
			except:
				print "Problem occurs"
				if nobreakflag is True:
					print "Try again after 1 minute..."
					time.sleep(60)
					nobreakflag = False
				else:
					return False
		return True

			