# -*- coding: utf-8 -*-

# !/usr/bin/python
# -*- coding: utf-8 -*-
import re
import csv
import lxml.html
import time
import datetime
import codecs
import urllib.request
import urllib.parse
import random
import os
import os.path

def getAnnualReportHeaderText(blockData):
    return blockData.cssselect('div[class=data-header]')[0].text

def generateAllEm(ele):
    text=ele.cssselect('div')[0].xpath('text/descendant::text()')
    str=''
    for t in text:
        str+=t
    #for em in element.cssselect('em'):
    #    text
    return str

#公司名set
companySet=set()

#线程数
numThread=1

# 打开两个文件：error与data
def LoadFile(numFile):
    pass
def ReLoadFile(fdata,numFile):
    fdata.close()
    fdata=open('fdata'+str(numFile)+'-'+str(numFile+1000),'+wb')

def CloseFile():
    fdata.close()
    ferror.close()

#动态ip proxy
ip_proxy_list=[]
def LoadIpProxyPool():
    with open('proxyIp','r') as fin:
        for line in fin:
            ip_proxy_list.append({'http':line.strip()})
#动态header
USER_AGENTS = ["Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
#公司名称
'''
companyNameForSearch=[]
companySearched=set()
def LoadCompanyName():
    files = os.listdir('data')
    for file in files:
        print('loading companyName:'+file)
        with open('data/'+file,'rb+') as fin:
            for line in fin:
                companyNameForSearch.append(line.decode('utf8'))
                break
'''
def loadcompanyName(path):
    companyRet=[]
    f = open(path)#"companyName.txt"
    line = f.readlines()
    for l in line:
        companyRet.append(l)
    f.close()
    return companyRet

def askURL_Tree(url,repeatTime_short=5,repeatTime_long=3):
    while repeatTime_short>0:
        user_agent = random.choice(USER_AGENTS)
        user_ip_proxy=random.choice(ip_proxy_list)
        headers = [
            ('Accept', 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8'),
            ('Accept - Encoding','gzip, deflate, br'),
            ('Accept - Language', 'zh - CN, zh;q = 0.9, en;q = 0.8'),
            ('Cache - Control', 'max - age = 0'),
            ('Connection', 'keep - alive'),
            ('Cookie', 'TYCID=4e2dba60af3411e8a3d66b138e5d3242; undefined=4e2dba60af3411e8a3d66b138e5d3242; ssuid=226121489; aliyungf_tc=AQAAAISWqFN2qAcAmUzNfP6sMDRrVbJB; csrfToken=K2bSoHe-yHZnmfu0JqDHSugL; bannerFlag=true; RTYCID=c06a6e407bbc4535a76f74f4748e73e6; CT_TYCID=89f3f48ba86e431696add0278b914c44; token=a377c03ac9e048c984b7034b29c07177; _utm=68a4ccf6a7434f7d8b17c98efa7dbd8f; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1537430957,1537514651,1537625258,1537898184; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzAyMTk0MjE0NCIsImlhdCI6MTUzNzg5ODMyNiwiZXhwIjoxNTUzNDUwMzI2fQ.e_0Np8SWJxO8dw4LlefFeaPpG1luyrO6-efnFe85eqUnkTj3_5rO719tZxRMkl9py1vUFCTQ3zGX-g6RpR34ew%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213021942144%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzAyMTk0MjE0NCIsImlhdCI6MTUzNzg5ODMyNiwiZXhwIjoxNTUzNDUwMzI2fQ.e_0Np8SWJxO8dw4LlefFeaPpG1luyrO6-efnFe85eqUnkTj3_5rO719tZxRMkl9py1vUFCTQ3zGX-g6RpR34ew; cloud_token=4b065ea55706424c93322519cb24713c; cloud_utm=1eb5287796014e47a1c3ec9f2f1871d5; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1537898338'),
            ('Host', 'www.tianyancha.com'),
            ('Referer','https: // www.tianyancha.com / company / 22822'),
            ('Upgrade - Insecure - Requests', '1'),
            ('User-Agent', user_agent)
        ]
        request = urllib.request.Request(url)
        proxy = urllib.request.ProxyHandler(user_ip_proxy)
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        #opener.addheaders = [headers]
        opener.addheaders=headers
        urllib.request.install_opener(opener)
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8','ignore')
            #time.sleep(2)
        except urllib.request.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            print('repeat')
            repeatTime-=1
            continue
        tree = lxml.html.fromstring(html)
        break
    return tree



#options = webdriver.ChromeOptions()
#options.add_argument("headless")
#options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
#options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

#browser  = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
 #                           ,chrome_options=options
 #                           )

#def crawlCompanyData(oriData,url,index):

if __name__=='__main__':
    LoadIpProxyPool()
    LoadCompanyName()
    fdata = open('fdata0-1000.txt', '+wb')
    ferror = open('ferror', '+wb')
    total=1
    for name in companyNameForSearch:
        for i in range(1,6):
            #url='https://www.tianyancha.com/search/p'+str(i)+'?key='+urllib.parse.quote(name)
            url='https://www.tianyancha.com/search/p'+str(i)+'?key='+urllib.parse.quote("百度")
            mainHtmlTree = askURL_Tree(url)
            eles = mainHtmlTree.cssselect('div[class="search-result-single "]')
            for ele in eles:
                data = {}
                data['地点']=ele.cssselect('span[class="site"]')[0].text
                data['法定代表人']=ele.cssselect('a[class="legalPersonName hover_underline"]')[0].text
                data['注册资本']=ele.cssselect('div[class="info"]>div[class="title  text-ellipsis"]')[0].cssselect('span')[0].text
                data['注册时间']=ele.cssselect('div[class="info"]>div[class="title  text-ellipsis"]')[1].cssselect('span')[0].text
                companyUrl=ele.cssselect('div[class="header"]>a')[0].get('href')
                result=crawlCompanyData(data,companyUrl,total)
                if result==1:
                    total+=1
                if total%1000==0:
                    ReLoadFile(fdata,total/1000)
        break
    CloseFile()