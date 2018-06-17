import urllib2,time,random,os,json,math
import sys
from urlparse import urljoin
reload(sys)
sys.setdefaultencoding("utf-8")
#entype = sys.getfilesystemencoding()

class jdcrawler:
	def __init__(self,type='SP'):
		#self.state = int(file('record').readline())
		self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
						'Connection':'keep=alive',
						'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
						'Accept-Language':'zh-CN,zh;q=0.8',
						#'Accept-Charset':'gbk;q=0.7,*;q=0.3',
						'Host':'club.jd.com'}

		self.headers['Cookie']="ipLoc-djd=1-72-2799-0; ipLocation=%u5317%u4EAC; unpl=V2_ZzNtbRcEEx18CUFQck4IV2IHF1kRAxAVdQATAH5MVAxhAkYIclRCFXMUR1FnGFsUZwMZXEVcQRxFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJARdURVBLHXUORFVLKV8FVwMTbUdeRhV2AU9VeClsAlczIlpGV0EVcjhHZHopHlE7BhtYS1BDWHABQ1R4EFUEZDMTbUE%3d; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|34866991730_0_dba980658fec4545beb119de4d9870ed|1491447999567; TrackID=1H7tFb43jwyO66fneOey-3n4XhpJNO8SSCQxCvqtzbZAXyqWTM27Jcq3StiQXBfMe182qIDVJdd-7lqM7emI7RgmSltI9pK31qdd6HteSwzkU7NaUPEB_YT7-2nOxJNN4; pinId=2jCnyQn3LgvQ-ApjhgaAdQ; pin=u_6787fd299c54b; unick=Jean_%E5%8F%A3%E5%8F%AF%E5%A6%AE; _tp=ZjYrGWYio8V%2FrjhezTnxIw%3D%3D; _pst=u_6787fd299c54b; ceshi3.com=000; 3AB9D23F7A4B3C9B=7QAQF7PGJYBOAPR4YNEW4WDKMLOGZYLMYSZAL3PITTZVP7CZLT2G4C3UPC5XCQESXUNSXJJYV7U27ATKNGFYYVY24E; thor=34A952AE43BD53ED133F57A8FF413D81DEEC88BAB78ACB95C8FCC4753E2988724302344F15B858A911CE1A3878F267F5E8C71368B54428017191A834928D435B3787B21E483E19938A925B25A534050AFEDB61650D8A99FACBB48324D59D5B0A3EE8AB902829937C96AA571EB67771A321066105CAA9A7B3791F6B6ADAC18CA7164AA8A8957A941B2B623B0A58B7D6418C5463852D9354A127438BD5471BDE7B; __jda=122270672.484128802.1460696723.1492487057.1492498385.27; __jdb=122270672.2.484128802|27.1492498385; __jdc=122270672; __jdu=484128802"
		
		'''
		self.cookies = {'ipLoc-djd':'1-72-2799-0','ipLocation':'%u5317%u4EAC',\
			'unpl':'V2_ZzNtbRcEEx18CUFQck4IV2IHF1kRAxAVdQATAH5MVAxhAkYIclRCFXMUR1FnGFsUZwMZXEVcQRxFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJARdURVBLHXUORFVLKV8FVwMTbUdeRhV2AU9VeClsAlczIlpGV0EVcjhHZHopHlE7BhtYS1BDWHABQ1R4EFUEZDMTbUE%3d',\
			'__jdv':'122270672|baidu-search|t_262767352_baidusearch|cpc|34866991730_0_dba980658fec4545beb119de4d9870ed|1491447999567',\
			'TrackID':'1H7tFb43jwyO66fneOey-3n4XhpJNO8SSCQxCvqtzbZAXyqWTM27Jcq3StiQXBfMe182qIDVJdd-7lqM7emI7RgmSltI9pK31qdd6HteSwzkU7NaUPEB_YT7-2nOxJNN4',\
			'pinId':'2jCnyQn3LgvQ-ApjhgaAdQ','pin':'u_6787fd299c54b','unick':'Jean_%E5%8F%A3%E5%8F%AF%E5%A6%AE',\
			'_tp':'ZjYrGWYio8V%2FrjhezTnxIw%3D%3D','_pst':'u_6787fd299c54b',\
			'ceshi3.com':'000','3AB9D23F7A4B3C9B':'7QAQF7PGJYBOAPR4YNEW4WDKMLOGZYLMYSZAL3PITTZVP7CZLT2G4C3UPC5XCQESXUNSXJJYV7U27ATKNGFYYVY24E',\
			'thor':'34A952AE43BD53ED133F57A8FF413D81DEEC88BAB78ACB95C8FCC4753E2988724302344F15B858A911CE1A3878F267F5E8C71368B54428017191A834928D435B3787B21E483E19938A925B25A534050AFEDB61650D8A99FACBB48324D59D5B0A3EE8AB902829937C96AA571EB67771A321066105CAA9A7B3791F6B6ADAC18CA7164AA8A8957A941B2B623B0A58B7D6418C5463852D9354A127438BD5471BDE7B',\
			'__jda':'122270672.484128802.1460696723.1492487057.1492498385.27',\
			'__jdb':'122270672.2.484128802|27.149249838','__jdc':'122270672','__jdu':'484128802'}
		'''

		self.dir = '../Corups/jdata/'+type+'/'
		if os.path.exists(self.dir) is False:
			os.mkdir(self.dir)
		#print self.dir

	def shop(self):
		shopids = [sid.strip() for sid in file('jdshopids.txt')]
		for shopid in shopids:
			print shopid
			self.crawl(shopid)
			print "%s done" % shopid

	def crawl(self,shopid):
		datadir = self.dir+shopid
		if os.path.exists(datadir) is False:
			print "Make New Folder",datadir
			os.mkdir(datadir)

		url1='https://club.jd.com/comment/productPageComments.action?productId='+shopid+'&score=0&sortType=5&page='
		url2='&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv91319'

		left = 5000-len(os.listdir(datadir))+1
		if left <= 0: return

		left /= 10.0
		left = int(math.ceil(left))
		print 'left %d for shop %s' % (left,shopid)
		ran_num=random.sample(range(800), left)
		
		failure = 0
		for i in ran_num:
			if os.path.exists('%s/%d-1.txt' % (datadir,i+1)):
				continue

			#nobreakflag = True
			#print "start page %d" % (i+1)

			t = i%10
			print "wait %d seconds" % t
			time.sleep(t)

			url = url1+str(i)+url2
			print "crawling url %s" % (url)
			try:
				req = urllib2.Request(url=url,headers=self.headers)
				c = urllib2.urlopen(req,timeout=20)
				json = self.load_json(c.read().decode('gbk').encode('utf-8'))
			except:
				failure += 1
				print "Could Not Open %s" % url
				if failure == 5:
					#out = file('jdata-%s-reali.txt' % shopid, 'a')
					#out.write('%d\n' % (i))
					break
				print "Wait For Several Minutes"
				time.sleep(60*failure)
				continue

			#c = c.read()
			#print c.decode('gbk').encode('utf-8')
			#break
			failure = 0
			j = 1
			for obj in json['comments']:
				if len(obj['content']) >= 5:
					out = file('%s/%d-%d.txt' % (datadir,i+1,j),'w')
					out.write(obj['content'])
					out.close()
				if 'afterUserComment' in obj:
					if 'hAfterUserComment' in obj['afterUserComment'] and len(obj['afterUserComment']['hAfterUserComment']['content'])>=5:
						out = file('%s/%d-%d-a.txt' % (datadir,i+1,j),'w')
						out.write(obj['afterUserComment']['hAfterUserComment']['content'])
						out.close()
				j+=1

	def load_json(self,jsonp):
		jsonp_begin = 'fetchJSON_comment98vv91319('
		jsonp_end = ');'
		jsonp = jsonp.strip()
		if not jsonp.startswith(jsonp_begin) or not jsonp.endswith(jsonp_end):
			print jsonp
			raise ValueError('Invalid JSONP')
		return json.loads(jsonp[len(jsonp_begin):-len(jsonp_end)])