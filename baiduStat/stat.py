import urllib2
import urllib 
import random
import math
import urlparse
import time
import cookielib
import linecache
import sys
import random

referPath="./refer"
targetPath="./target"
referUrl=""
targetUrl=""

def init():
    #get random int
    referIndex=random.randint(0,999)
    targetIndex=random.randint(0,999)

    #get url
    global referPath
    global targetPath
    global referUrl
    global targetUrl
    referUrl = linecache.getline(referPath, referIndex).replace('\n','')
    targetUrl = linecache.getline(targetPath, targetIndex).replace('\n','')

    if referUrl=="" or targetUrl=="":
        sys.exit(0)
    print referUrl
    print targetUrl




########################################################################
class Baidu:
    """"""
    Referer='http://www.lixin.me'
    TargetPage='/www.lixin.me'
    BaiduID=''
    Hjs="http://hm.baidu.com/h.js?"
    Hgif="http://hm.baidu.com/hm.gif?"
    UserAgent='Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)' #IE9
    MyData={'cc':'1','ck':'1','cl':'32-bit','ds':'1024x768','et':'0','ep':'0','fl':'11.0','ja':'1','ln':'zh-cn','lo':'0','nv':'1','st':'3','v':'1.0.17'}
    #----------------------------------------------------------------------
    def __init__(self,baiduID,targetPage=None,refererPage=None):
        """Constructor"""
        self.TargetPage=targetPage or  self.TargetPage
        self.Referer=refererPage or self.Referer
        self.BaiduID=baiduID
        self.MyData['si']=self.BaiduID
        #self.MyData['su']=urllib.quote(self.Referer)
        self.MyData['su']=self.Referer
        pass
    def run(self,timeout=5):
        cj=cookielib.CookieJar()

        #add proxy
	proxyHost = "proxy.abuyun.com"
	proxyPort = "9010"
	
	proxyUser = "HK71T41EZ21304GP"
	proxyPass = "75FE0C4E23EEA0E7"
	
	proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
	    "host" : proxyHost,
	    "port" : proxyPort,
	    "user" : proxyUser,
	    "pass" : proxyPass,
	}
	
	proxy_handler = urllib2.ProxyHandler({
	    "http"  : proxyMeta,
	    "https" : proxyMeta,
	})


        #opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        opener=urllib2.build_opener(proxy_handler)
        #urllib2.install_opener(opener)
        opener.addheaders=[("Referer",self.TargetPage),("User-Agent",self.UserAgent)]
        #opener.addheaders = [("Proxy-Switch-Ip", "no")]
        try:

            response=opener.open(self.Hjs+self.BaiduID).info()
            self.MyData['rnd']=int(random.random()*2147483647 )
            self.MyData['lt']=int(time.time())
            fullurl=self.Hgif+urllib.urlencode(self.MyData)
            response2=opener.open(fullurl,timeout=timeout).info()
            self.MyData['rnd']=int(random.random()*2147483647 )
            self.MyData['et']='3'
            self.MyData['ep']='2000,100'
            response3=opener.open(self.Hgif+urllib.urlencode(self.MyData),timeout=timeout).info()
            print response3
            pass
        except urllib2.HTTPError ,ex:
            print ex.code
            pass
        except urllib2.URLError,ex:
            print ex.reason
            pass
        pass

        opener.close()

    
    
if  __name__ =="__main__":
    init()
    while 1:
        a=Baidu('ea8a600ffb76d5930a3afa6ab812f938',targetUrl,referUrl)
        a.run(30)
        break
        time.sleep(1)
